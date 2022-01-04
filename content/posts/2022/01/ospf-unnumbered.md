---
title: "Running OSPF over Unnumbered Ethernet Interfaces"
date: 2022-01-10 07:04:00
tags: [ OSPF ]
series: unnumbered-interfaces
---
Remember the *unnumbered IP interfaces* saga? Let's conclude it with the final challenge: can we run link-state routing protocols (OSPF or IS-IS) over unnumbered interfaces?

**Quick answer**: Sure, just use IPv6.

Cheater! IPv6 doesn't count. There are no unnumbered interfaces in IPv6 -- every interface has at least a link-local address (LLA). Even more, routing protocols are designed to run over LLA addresses, including some EBGP implementations, allowing you to build an LLA-only network (see [RFC 7404](https://datatracker.ietf.org/doc/html/rfc7404) for details).

OK, what about IPv4?

**TL&DR**: It works, but...
<!--more-->

As always, let's start with the fundamentals. Every router running a routing protocol needs to:

* Advertise itself (unless you're using static neighbor configuration)
* Find its neighbors
* Build some sort of relationship with the neighbors (adjacency)
* Encode its local topology in some data structure
* Exchange data with its neighbors
* Select best routes according to its view of the world

Can OSPF do all that over unnumbered interfaces? We'll use the following lab topology to test it out (all interfaces are unnumbered):

{{<figure src="/2022/01/unnumbered-ospf-topology.png" caption="Lab topology">}}

**Hello messages**: no problem. Use the IP address assigned to the interface (usually the loopback address) as the source IP. Destination IP is a multicast address anyway.

**Finding the neighbors and building adjacency**: getting trickier. While the standard never spells it out (or I couldn't find it), I have an impression that the underlying assumption is that all OSPF interfaces apart from P2P links have an IP subnet associated with them. I found one of the closest matches in Section 8.2 (receiving protocol packets): 

> If the receiving interface connects to a broadcast network, Point-to-MultiPoint network or NBMA network the sender is identified by the IP source address found in the packet's IP header. If the receiving interface connects to a point-to-point network or a virtual link, the sender is identified by the Router ID (source router) found in the packet's OSPF header.

Next, there's the check of the network mask advertised in the OSPF Hello packet. The network mask might match (loopback interfaces usually use /32 prefixes), but we have another get-out-of-jail card on P2P links. Section 10.5 of RFC 2328 says

> However, there is one exception to the above rule: on point-to-point networks and on virtual links, the Network Mask in the received Hello Packet should be ignored.

To recap: while the OSPF adjacency works perfectly fine on unnumbered point-to-point links, it would be an exercise in futility to try to make it work on point-to-multipoint unnumbered interfaces. Cisco IOS XE neatly solves the conundrum by not sending Hello packets out of unnumbered interfaces that are not configured as point-to-point OSPF networks.

**Encoding local topology**: trivial. Add a *router link* to type-1 LSA without a corresponding *stub* link you'd get on a numbered link. Here's a type-1 LSA from a router with an unnumbered interface:

```
r1#show ip ospf data router 10.0.0.1

            OSPF Router with ID (10.0.0.1) (Process ID 1)

		Router Link States (Area 0.0.0.0)

  LS age: 420
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.0.1
  Advertising Router: 10.0.0.1
  LS Seq Number: 8000000A
  Checksum: 0x6E6D
  Length: 48
  Number of Links: 2

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.0.1
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.0.2
     (Link Data) Router Interface address: 0.0.0.8
      Number of MTID metrics: 0
       TOS 0 Metrics: 10
```

**Selecting the best routes**: needs a bit of extra effort. Consider the following route pointing to an unnumbered Ethernet interface:

```
r1#show ip route 10.0.0.3
Routing entry for 10.0.0.3/32
  Known via "ospf 1", distance 110, metric 21, type intra area
  Last update from 10.0.0.2 on GigabitEthernet2, 01:14:44 ago
  Routing Descriptor Blocks:
  * 10.0.0.2, from 10.0.0.3, 01:14:44 ago, via GigabitEthernet2
      Route metric is 21, traffic share count is 1
```

Next hop of the route is 10.0.0.2... but how do we know where that is? Well, we have an entry for 10.0.0.2, but it's not exactly useful -- it says *to get there, go there*.

```
r1#show ip route 10.0.0.2
Routing entry for 10.0.0.2/32
  Known via "ospf 1", distance 110, metric 11, type intra area
  Last update from 10.0.0.2 on GigabitEthernet2, 01:16:05 ago
  Routing Descriptor Blocks:
  * 10.0.0.2, from 10.0.0.2, 01:16:05 ago, via GigabitEthernet2
      Route metric is 11, traffic share count is 1
```

I explained the necessary glue in the [Unnumbered Ethernet Interfaces](https://blog.ipspace.net/2021/06/unnumbered-ethernet-interfaces.html) blog post, here's the TL&DF[^TLDF] summary:

* OSPF next hops are supposed to be directly connected.
* What we need is a glue ARP entry for 10.0.0.2 on outgoing internet (GigabitEthernet2)

{{<cc>}}Glue ARP entry on GigabitEthernet2{{</cc>}}
```
r1#show arp gigabitEthernet2
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.0.0.1                -   5254.0091.b284  ARPA   GigabitEthernet2
Internet  10.0.0.2               91   5254.00e1.4213  ARPA   GigabitEthernet2
```


[^TLDF]: Too Lazy, Didn't Follow
