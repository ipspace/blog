---
title: "OSPF External Routes (Type-5 LSA) Mysteries"
date: 2022-10-12 07:04:00
tags:
- OSPF
ospf_tag: details
---
Daniel Dib [posted a number of excellent questions on Twitter](https://twitter.com/danieldibswe/status/1579674196833366017), including:

> While forwarding a received Type-5 LSA to other areas, why does the ABR not change the Advertising Router ID to it's own IP address? If ABR were able to change the Advertising Router ID in the Type-5 LSA, then there would be no need for Type-4 LSA which meant less OSPF overhead on the network.

**TL&DR:** The current implementation of external routes in OSPF minimizes topology database size (memory utilization)

Before going to the details, try to imagine the environment in which OSPF was designed, and the problems it was solving.
<!--more-->
In the early days of TCP/IP, IP was the Internetworking Protocol riding on top of another WAN protocol. Early implementations had IP running on top of [Protocol 1822](https://en.wikipedia.org/wiki/Interface_Message_Processor#BBN_Report_1822), later we ran IP on top of Frame Relay or ATM virtual circuits.

As local area networks and point-to-point links became prevalent, the IP community needed an *Interior[^INT] Gateway[^GW] Protocol* that would be robust enough to support large networks, including the backbones of early Internet Service Providers (ISPs).

Like everyone else, ISPs started building IP networks on top of some other switched WAN infrastructure, and it was very common to have routers at the edge of the WAN network (we would call them PE-devices today) and some other WAN switches (P-devices[^ATM]) in the WAN core. The WAN edge devices would exchange routes with the external world using [Exterior Gateway Protocol](https://www.rfc-editor.org/rfc/rfc904.html) which was later replaced by Border Gateway Protocol[^BGP].

[^ATM]: An interesting aside: the first MPLS P-devices were ATM switches -- MPLS was trying to merge IP control plane with ATM forwarding hardware.

It was well understood[^LAB] that if you want to replace WAN switches with a pure IP network, all P-devices have to have routes to all external destinations, and instead of saying _let's run BGP everywhere_, the solution was _let's redistribute BGP into OSPF_ because an IP prefix in OSPF topology database takes less memory than a full-blown BGP prefix[^RRR], and needs fewer CPU cycles to process because OSPF considers external routes after the hard work (SPF algorithm) has already been done.

{{<note warn>}}Please note that the global BGP table [had a few thousand entries](https://bgp.potaroo.net/as2.0/bgp-active.html) at that time -- OSPFv1 was published in 1991. [Redistributing today's BGP table into OSPF](https://blog.ipspace.net/2020/10/redistributing-bgp-into-ospf.html) is not a good idea.{{</note>}}

So here's your challenge: design a protocol that will compute optimal end-to-end paths toward 10-20K external routes while running on a 4 MHz 16-bit CPU with 2MB of memory (including the software image).

[^INT]: Interior: within a network

[^GW]: Gateway: an early name for a device that commonly served as a gateway between LAN and WAN. Depending on your persuasion, in the days when terminology no longer matters you might call that device a router, a switch, or a modem.

[^BGP]: Also know as [Bridging the Gap Protocol by Sky News subscribers](https://www.youtube.com/watch?v=Y-YCYXGF_UY).

[^LAB]: Or you could spend 30 seconds in a lab to prove it, something that a lot of modern networking engineer wannabes try to replace with asking questions on social media.

[^RRR]: Let alone two of them if you want to have route reflector redundancy

Now imagine that you decide to split the network into smaller chunks (because your dismal CPU can't run SPF on a 200-node network) and figure out how that protocol would have to work to find optimal paths in the following network:

{{<ascii>}}
     ┌──────┐           ┌───┐
  ┌──┤ ABR1 ├───────────┤ C │
  │  └──────┘           └─┬─┘
  │                       │
┌─┴─┐            ┌──────┐ │
│ X ├────────────┤ ABR2 ├─┘
└───┘            └──────┘
{{</ascii>}}

**Notes:**
* Line length is proportional to link cost (let's say the cost ABR1-X is 1, and the of C-ABR1 is 2).
* ABR1 and ABR2 are Area Border Routers
* ABR1, ABR2 and C are in the backbone area, ABR1, ABR2 and X are in another area
* X is redistributing an external route into the IGP
* We have to find optimal path from C to X

If we're dealing with a small number of routes (where memory consumption doesn't matter too much), we could advertise prefixes on ABRs with cost from ABR to the final destination:

* ABR1 advertises an internal prefix on X into the backbone area with cost 1
* ABR2 advertises that same prefix with cost 2
* C figures out that both paths have the same total cost (the cost of C-ABR1-X or C-ABR2-X is 3) and uses both paths.

In this scenario, every ABR has to advertise every prefix in another area. This was deemed prohibitively expensive (in terms of memory consumption) when dumping the whole BGP table into OSPF, so they went for another approach:

* X advertises 10.000 external routes (type-5 LSA)
* ABR1 and ABR2 advertise their cost to X (type-4 LSA)
* C combines the cost from C to ABR, from ABR to X, and the external cost advertised by X to get the total cost to an external destination.

**Savings:** 10.002 LSAs instead of 20.000 LSAs.

**Next question:** why does OSPF do domain-wide flooding of type-5 LSAs instead of re-originating them like ABRs do when serving not-so-stubby-areas (NSSA)?

Yet again, it's CPU cycles and memory consumption. In an NSSA area, every ABR has two copies of every external route in its topology database: a type-7 LSA in the NSSA area, and a translated type-5 LSA in the backbone area. Furthermore, the dedicated translator (the ABR with the highest router ID) has to waste CPU cycles translating (and re-originating) type-7 LSA into type-5 LSA for absolutely no gain in functionality (apart from other type-5 LSAs not getting into the NSSA area).

**To recap**: OSPF external routes were designed the way they were because OSPF had to minimize memory utilization while supporting a large number of external routes.

Loved this detour into ancient history? You'll find more of them in _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar (approximately half of it is available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free)).
