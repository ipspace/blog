---
date: 2017-02-09 10:39:00+01:00
ospf_tag: fa
tags:
- design
- OSPF
title: The Unintended Consequences of NSSA Kludges
url: /2017/02/the-unintended-consequences-of-nssa.html
---
Remember the [kludges needed to make OSPF NSSA areas work correctly](/2017/02/why-ospf-needs-forwarding-address-with.html)? We concluded that saga by showing how the rules of RFC 3101 force a poor ASBR to choose an IP address on one of its OSPF-enabled interfaces as a forwarding address to be used in Type-7 LSA.

What could possibly go wrong with such a "simple" concept?
<!--more-->
Let's start with the network we used in the [previous blog post](/2017/02/why-ospf-needs-forwarding-address-with.html). At the end of that blog post, we shut down the loopback interface on E1 to force it to select something else as the Type-7 LSA forwarding address. While that resulted in suboptimal traffic flow, we could still ping 192.168.1.1 (IP address on a non-OSPF loopback interface on E1) from C1.

{{<figure src="/2017/02/s550-OSPF_NSSA_2.png">}}

Now let's pretend the interface E1 chose is a Metro Ethernet link, and it just failed in one of those mysterious ways where everything seems OK, but no packets make it across the link. We'll emulate this too-well-known behavior (never a Service Provider fault if you ask them) with an incoming **deny ip any any** access list.

{{<note>}}Service Providers are more thorough -- they'd also drop ARP packets and everything else, but this ACL will do for our purposes.{{</note>}}

To make the fault look even more like a Metro Ethernet network, we'll install the ACL only on E1 side of A2E1 link, resulting in a unidirectional link. As expected, the OSPF adjacency between A2 and E1 goes down. Totally unexpected, C1 can no longer ping external subnets on E1 *even though there's a perfectly good path from C1 to E1.*

C1 has the destination in its routing table:

``` code
C1#show ip route 192.168.1.0
Routing entry for 192.168.1.0/24
  Known via "ospf 1", distance 110, metric 20, type extern 2, forward metric 2
  Last update from 10.0.0.13 on GigabitEthernet0/2, 00:29:09 ago
  Routing Descriptor Blocks:
  * 10.0.0.13, from 192.168.0.4, 00:29:09 ago, via GigabitEthernet0/2
      Route metric is 20, traffic share count is 1
```

Pings return *destination unreachable* ICMP replies

``` code
C1>ping 192.168.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:
U.U.U
Success rate is 0 percent (0/5)
```


### Wait, What?

Let's trace the path from C1 to E1. The routing entry for 192.168.1.0/24 on C1 points to A2, and A2 claims it doesn't know anything about 192.168.1.0/24. Confusing, right?

A2 doesn't know anything about 192.168.1.0

``` code
A2#show ip route 192.168.1.0
% Network not in table
```

Well, it turns out the broken link between A2 and E1 also broke the NSSA area in two parts, and A2 wouldn't consider the Type-7 LSA from E1 when running SPF as it has no intra-area connectivity to E1.

{{<figure src="/2017/02/s550-OSPF_NSSA_3.png">}}

Type-7 LSA refers to an unreachable router ID and is thus ignored:

``` code
A2#show ip ospf data nssa-external

            OSPF Router with ID (192.168.0.4) (Process ID 1)

    Type-7 AS External Link States (Area 1)

  LS age: 1284
  Options: (No TOS-capability, Type 7/5 translation, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.2
  LS Seq Number: 8000000C
  Checksum: 0xD3C5
  Length: 36
  Network Mask: /24
  Metric Type: 2 (Larger than any link state path)
  MTID: 0
  Metric: 20
  Forward Address: 10.0.0.18
  External Route Tag: 0
```

The packet from C1 arrives at A2, and A2 simply drops it (resulting in ICMP unreachables observed on C1).

Will the situation get any better when Type-7 LSA ages out on A2? Let's reset the OSPF process on A2 with the **clear ip ospf process** command. Type-7 LSA is gone, and A2 sees only the backbone Type-5 LSA but still refuses to install 192.168.1.0/24 into the forwarding table:

Type-5 LSA looks good but is still not used:

``` code
A2#show ip ospf data external

            OSPF Router with ID (192.168.0.4) (Process ID 1)

    Type-5 AS External Link States

  LS age: 893
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.1
  LS Seq Number: 80000001
  Checksum: 0x842B
  Length: 36
  Network Mask: /24
  Metric Type: 2 (Larger than any link state path)
  MTID: 0
  Metric: 20
  Forward Address: 10.0.0.18
  External Route Tag: 0
```

It seems this behavior is a consequence of Rule #4 of Section 16.4 in [RFC 2328](https://tools.ietf.org/html/rfc2328) (OSPF v2):

> If the forwarding address is non-zero, look up the forwarding address in the routing table. The matching routing table entry must specify an intra-area or inter-area path.

Looks like a stub interface (OSPF-enabled interface with no neighbors on it) doesn't satisfy the *intra-area or inter-area path* criteria. A2 thus ignores the Type-5 LSA pointing to its directly connected interface.

### Nerd Knobs to Rescue

The **area nssa translate type7 always suppress-fa** nerd knob suggested by Angelos Vassiliou would solve this problem (because there would be no recursive lookup for the forwarding address) while at the same time violating paragraph (2) of [section 3.2 in RFC 3101](#section-3.2).

You could argue that the ABR behaves like every type-7 LSA would be aggregated into a separate address range, as described in paragraph (3) of the same section. I still have to check how Cisco IOS handles the costs of such type-5 LSA.

### The Really Sad Part

I created at least one OSPF deep-dive course and taught it at least a dozen times (quite often having Cisco's TAC engineers in the audience), and I was still surprised to see this behavior.

### Summary

OSPF is way too complex for its own good. If you must use OSPF, get rid of as much of its complexity as you can-- use a single area if at all possible, and stay away from NSSA areas.
