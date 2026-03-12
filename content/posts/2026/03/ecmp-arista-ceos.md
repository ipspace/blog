---
title: "IPv4 ECMP Works on Arista cEOS Release 4.35.2F"
date: 2026-03-12 10:09:00+0100
tags: [ switching ]
---
When I wrote about the [anycast-ECMP-in-MPLS behavior](/2021/11/anycast-mpls/) in 2011, I had to use Cisco IOS to prove that ECMP worked, since Arista cEOS (running the Linux kernel for IP forwarding) didn't install more than one equal-cost path into the Linux forwarding table.

Arista cEOS got better in the meantime; IPv4 ECMP works like a charm on cEOS release 4.35.02F. With the [same lab topology](https://github.com/ipspace/netlab-examples/blob/master/routing/anycast-mpls-ospf/topology.yml) I'd [used in 2021](/2021/11/anycast-mpls/), I was able to see the traffic spread across multiple nodes:
<!--more-->
{{<figure src="/2021/11/MPLS-anycast-ospf-topo.png" caption="Lab topology">}}

{{<cc>}}Traceroute toward the anycast IPv4 address on L1 running Arista EOS{{</cc>}}
```
$ netlab connect l1 traceroute 10.0.0.42
Connecting to 192.168.121.101 using SSH port 22, executing traceroute 10.0.0.42
traceroute to 10.0.0.42 (10.0.0.42), 30 hops max, 60 byte packets
 1  s1 (10.1.0.2)  0.070 ms  0.007 ms  0.007 ms
 2  l2 (10.1.0.5)  2.326 ms  2.392 ms l3 (10.1.0.9)  2.861 ms
 3  10.0.0.42 (10.0.0.42)  4.089 ms  4.180 ms  4.826 ms
```

**Notes:**

* Arista EOS uses UDP-based traceroute, sending UDP packets to port 33434
* Arista EOS devices reply to UDP probes with ICMP *port unreachable* messages sent *from the destination IP address*, making it impossible to figure out which anycast node the traffic hit.

However, when I dug a bit deeper, I stumbled upon some truly mysterious behavior:

* The EOS IP routing table on S1 has two entries for 10.0.0.42/32 (pointing to L2 and L3)

{{<cc>}}EOS IP routing table entry for IPv4 prefix 10.0.0.42/32 on S1 running Arista cEOS{{</cc>}}
```
s1#show ip route 10.0.0.42/32 detail
...
 O        10.0.0.42/32 [110/30] PM
           via 10.1.0.5, Ethernet2 s1 -> l2
           via 10.1.0.9, Ethernet3 s1 -> l3
```

* The underlying Linux IP routing table has a single entry

{{<cc>}}Linux IP routing table entry for IPv4 prefix 10.0.0.42/32 on S1 running Arista cEOS{{</cc>}}
```
s1#bash ip route show 10.0.0.42/32
10.0.0.42 via 10.1.0.5 dev et2 proto gated metric 30
```

* Based on that, one would expect that the *traceroute* from S1 to the anycast IP address wouldn't use all paths, **and that's exactly what happens**:

{{<cc>}}Traceroute toward the anycast IPv4 address on S1 running Arista EOS{{</cc>}}
```
s1#traceroute 10.0.0.42
traceroute to 10.0.0.42 (10.0.0.42), 30 hops max, 60 byte packets
 1  l2 (10.1.0.5)  0.067 ms  0.008 ms  0.018 ms
 2  10.0.0.42 (10.0.0.42)  1.183 ms  1.191 ms  1.447 ms
```

Somehow, Arista cEOS makes ECMP work for *forwarded* traffic, but not for the *locally originated* traffic. I have no idea what they do behind the scenes 🤷‍♂️, but it's nice to see at least some ECMP behavior in the virtual data-plane implementation.
