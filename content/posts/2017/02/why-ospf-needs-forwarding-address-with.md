---
date: 2017-02-02 08:24:00+01:00
ospf_tag: fa
tags:
- OSPF
title: Why OSPF Needs Forwarding Address With NSSA Areas
url: /2017/02/why-ospf-needs-forwarding-address-with.html
---
In the previous blog posts I described how [OSPF tries to solve some broken designs](https://blog.ipspace.net/2017/01/ospf-forwarding-address-yet-another.html) with Forwarding Address field in Type-5 LSA -- a [kludge that unnecessarily increases the already too-high complexity of OSPF](http://blog.ipspace.net/2017/01/ospf-forwarding-address-yak-take-2.html).

NSSA areas make the whole thing worse: OSPF needs a Forwarding Address in Type-5 LSAs generated from Type-7 LSAs to ensure optimal packet forwarding. Here's why:
<!--more-->
Let's start with a small (slightly) broken network:

-   Core router (C1) is in area 0;
-   Edge router (E1) is in NSSA area 1;
-   ABRs A1 and A2 connect the edge network with the core network.

{{<figure src="/2017/02/s500-OSPF_NSSA_1.png">}}

Whenever you have multiple ABRs connected to the same set of OSPF areas, you SHOULD have a link between them within each area **and** within the backbone area. The proof is left as an exercise for the reader. Note: you can implement the backbone link as a virtual link if the non-backbone area is not a stub/NSSA area.

Due to the way the OSPF NSSA feature is designed:

-   Edge router (E1) redistributes an external subnet (192.168.1.0/24) into OSPF NSSA area as Type-7 LSA;
-   ABRs translate Type-7 LSAs into Type-5 LSAs;
-   Only one of the ABRs advertises Type-5 LSA into the backbone area (because whatever -- details in [RFC 3101](https://tools.ietf.org/html/rfc3101)).

{{<cc>}}Backbone Type-5 LSA generated from Type-7 LSA{{</cc>}}
``` code
A1#show ip ospf data external

            OSPF Router with ID (192.168.0.1) (Process ID 1)

Type-5 AS External Link States

  LS age: 113
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.4
  LS Seq Number: 80000001
  Checksum: 0x530A
  Length: 36
  Network Mask: /24
Metric Type: 2 (Larger than any link state path)
MTID: 0
Metric: 20
Forward Address: 192.168.0.2
External Route Tag: 0
```

Without the forwarding address in Type-5 LSA originated by A2 (in our sample network), C1 couldn't use both equal-cost paths toward E1 (C1-A1-E1 and C1-A2-E1); all the traffic would go through the ABR originating the Type-5 LSA.

How does the ABR figure out what forwarding address to use in Type-5 LSA translated from Type-7 LSA? It has no idea and shifts the problem to someone else (see also [RFC 1925](https://tools.ietf.org/html/rfc1925) rule 6) -- it uses whatever forwarding address is specified in Type-7 LSA.

**Corollary:** Type-7 LSA MUST have a Forwarding Address.

{{<cc>}}Type-7 LSA originated by E1{{</cc>}}
``` code
A1#show ip ospf data nssa-external

            OSPF Router with ID (192.168.0.1) (Process ID 1)

Type-7 AS External Link States (Area 1)

  LS age: 90
  Options: (No TOS-capability, Type 7/5 translation, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.2
  LS Seq Number: 80000001
  Checksum: 0xCA8A
  Length: 36
  Network Mask: /24
Metric Type: 2 (Larger than any link state path)
MTID: 0
Metric: 20
Forward Address: 192.168.0.2
External Route Tag: 0
```

When an NSSA ASBR cannot use the real external next hop as the forwarding address, it usually uses the loopback address (that's why the forwarding address in the previous printout is set to 192.168.0.2), resulting in perfect ECMP behavior on C1:

{{<cc>}}C1 has two equal-cost paths to external destinations behind E1{{</cc>}}
``` code
C1#show ip route 192.168.1.0
Routing entry for 192.168.1.0/24
  Known via "ospf 1", distance 110, metric 20, type extern 2, forward metric 3
  Last update from 10.0.0.13 on GigabitEthernet0/2, 00:23:35 ago
  Routing Descriptor Blocks:
    10.0.0.13, from 192.168.0.4, 00:23:35 ago, via GigabitEthernet0/2
      Route metric is 20, traffic share count is 1
  * 10.0.0.9, from 192.168.0.4, 00:23:35 ago, via GigabitEthernet0/1
      Route metric is 20, traffic share count is 1
```

Now let's see what happens if we shut down the loopback interface on E1 (or remove it from the OSPF process), placing E1 under considerable stress:

-   It cannot use the real external next hop (because the next hop subnet is not advertised into OSPF);
-   It doesn't have a usable loopback address advertised as an internal OSPF route.

E1 consequently takes one of its other IP addresses (I'm positive RFC 3101 goes into great detail about which one to use, but I couldn't be bothered with those details) and uses it as the forwarding address. In our case, E1 chose the IP address on the E1-A2 link.

{{<cc>}}E1 uses the internal OSPF subnet as a forwarding address{{</cc>}}
``` code
A1#show ip ospf data external

            OSPF Router with ID (192.168.0.1) (Process ID 1)

    Type-5 AS External Link States

  LS age: 25
  Options: (No TOS-capability, DC, Upward)
  LS Type: AS External Link
  Link State ID: 192.168.1.0 (External Network Number )
  Advertising Router: 192.168.0.4
  LS Seq Number: 80000002
  Checksum: 0x703B
  Length: 36
  Network Mask: /24
  Metric Type: 2 (Larger than any link state path)
  MTID: 0
  Metric: 20
  Forward Address: 10.0.0.18
  External Route Tag: 0
```

The change of forwarding address breaks load sharing on C1 as the subnet specified in the forwarding address is no longer reachable over two equal-cost paths. C1 sends all the traffic toward E1 over A2.

{{<cc>}}C1 has a single path toward the external destination behind E1{{</cc>}}
``` code
C1#show ip route 192.168.1.0
Routing entry for 192.168.1.0/24
  Known via "ospf 1", distance 110, metric 20, type extern 2, forward metric 2
  Last update from 10.0.0.13 on GigabitEthernet0/2, 00:29:09 ago
  Routing Descriptor Blocks:
  * 10.0.0.13, from 192.168.0.4, 00:29:09 ago, via GigabitEthernet0/2
      Route metric is 20, traffic share count is 1
```

Hooray, we broke OSPF (again).

### But Wait, It Gets Worse...

Igor Osadchuk sent me this tidbit:

> The interesting thing about FA is that since it is used in a recursive lookup and OSPF effectively acts as a distance vector protocol in this case, FA address has to be present in a RIB (and ultimately in a FIB) or an external prefix won\'t be resolved. Fun to troubleshoot!

### Even More Nerd Knobs

Angelos Vassiliou sent me an email pointing out that we could use **area 1 nssa translate type7 always** to force both ABRs to originate type-5 LSAs. This would solve some edge cases resulting from discontiguous NSSA areas, but would not solve our problem.

There's another nerd knob (that, in my understanding, violates the NSSA RFC): **area nssa translate type7 supress-fa** would suppress FA information in type-5 LSA originating into the backbone, potentially resulting in ECMP within the backbone, but not in correct end-to-end ECMP in scenarios with unequal-cost links.

### Do We Really Have to Deal with All This Complexity?

Probably not. After all, my calendar claims it's 2017, and most routers ship with reasonably fast CPUs and gigabytes of memory these days. Here's what you could do to make your life simpler:

-   If you have low hundreds of routers and don't care too much about the impact of convergence/SPF events, use a single OSPF area;
-   If you're wondering whether OSPF can survive a few hundred routers in the same area, use IS-IS for your next design;
-   If your network is larger than that (or you don't feel comfortable pushing OSPF to its limits), use BGP at the edges and OSPF in the core;
-   If your vendor tries to charge you extra for the privilege of using BGP tell them it's 2017 and vote with your wallet (aka *Change the Vendor*).

### Revision History

2017-02-06
: Added a few more nerd knobs suggested by Angelos Vassiliou.
