---
date: 2010-09-02 07:14:00.002000+02:00
tags:
- switching
- IP routing
title: RIBs and FIBs (aka IP Routing Table and CEF Table)
url: /2010/09/ribs-and-fibs.html
lastmod: 2020-12-26 13:51:00
---
Every now and then, I'm asked about the difference between *Routing Information Base* (RIB), also known as IP Routing Table and *Forwarding Information Base* (FIB), also known as CEF table  (on Cisco's devices) or IP forwarding table.

Let's start with an overview picture (which does tell you more than the next thousand words I'll write):
<!--more-->
{{<figure src="/2010/09/s1600-RibFib.png" caption="Interaction between routing protocols, routing table, and forwarding table">}}

A router has numerous ways of learning the best paths toward individual IP prefixes: they might be directly connected, configured as static routes or learned through dynamic routing protocols.

Each dynamic routing protocol ([including RIP](/2008/08/rip-route-database.html)) has its own set of internal data structures, known as OSPF/IS-IS database, EIGRP topology table or BGP table. The routing protocol updates its data structures based on routing protocol updates exchanged with its neighbors, eventually collecting all the relevant information. Throughout this article we'll work with 10.0.1.1/32 learned through OSPF and 10.0.11.11/32 learned through BGP, so let's inspect the relevant OSPF/BGP data structures.

``` {.code}
RR#show ip bgp | begin Network
   Network          Next Hop            Metric LocPrf Weight Path
r>i10.0.1.1/32      10.0.1.1                 0    100      0 i
r>i10.0.1.2/32      10.0.1.2                 0    100      0 i
*>i10.0.11.11/32    10.0.1.1                 0    100      0 i

RR#show ip ospf database router 10.0.1.1

            OSPF Router with ID (10.0.1.5) (Process ID 1)

                Router Link States (Area 0)

  LS age: 1612
  Options: (No TOS-capability, DC)
  LS Type: Router Links
  Link State ID: 10.0.1.1
  Advertising Router: 10.0.1.1
  LS Seq Number: 80000003
  Checksum: 0xC764
  Length: 60
  Number of Links: 3

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.1.1
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.1.6
     (Link Data) Router Interface address: 10.0.7.9
      Number of MTID metrics: 0
       TOS 0 Metrics: 64

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.7.8
     (Link Data) Network Mask: 255.255.255.252
      Number of MTID metrics: 0
       TOS 0 Metrics: 64
```

Each routing protocol runs its own route selection algorithm (SPF algorithm in case of OSPF or IS-IS or [pretty complex set of rules in case of BGP](http://www.cisco.com/en/US/tech/tk365/technologies_tech_note09186a0080094431.shtml)), deriving a set of IP prefixes reachable through that routing protocol, and IP next hops that should be used to reach them. 

You can view the results of these route selection algorithms with protocol-specific **show** commands (for example, **show ip bgp _prefix_** for BGP and **show ip ospf rib _prefix_** for OSPF).

``` {.code}
RR#show ip bgp 10.0.11.11
BGP routing table entry for 10.0.11.11/32, version 6
Paths: (1 available, best #1, table default)
  Not advertised to any peer
  Local
    10.0.1.1 (metric 66) from 10.0.1.1 (10.0.1.1)
      Origin IGP, metric 0, localpref 100, valid, internal, best
RR#show ip ospf rib 10.0.1.1

            OSPF Router with ID (10.0.1.5) (Process ID 1)

OSPF local RIB
Codes: * - Best, > - Installed in global RIB

*>  10.0.1.1/32, Intra, cost 66, area 0
     SPF Instance 2, age 00:48:15
     Flags: RIB, HiPrio
      via 10.0.2.1, FastEthernet0/0, flags: RIB
       LSA: 1/10.0.1.1/10.0.1.1
```

Both BGP and OSPF associate IP next hops with IP prefixes, but BGP simply uses the value of the next-hop attribute attached to the BGP route, whereas OSPF computes the IP address of the next-hop OSPF router with the SPF algorithm.

The results of intra-routing-protocol route selection are inserted in the IP routing table (RIB) based on *administrative distance* (and there are interesting consequences if two routing protocols have the same AD). Most routing protocols don't complain when their routes are not used in the IP routing table; [BGP has a special show command that can display RIB failures](/2007/12/what-is-bgp-rib-failure.html). In our scenario, the 10.0.1.1/32 prefix is received via OSPF and BGP and the OSPF route wins as OSPF has lower AD than internal BGP route.

``` {.code}
RR#show ip bgp rib-failure
Network      Next Hop    RIB-failure            RIB-NH Matches
10.0.1.1/32  10.0.1.1    Higher admin distance  n/a
10.0.1.2/32  10.0.1.2    Higher admin distance  n/a
```

Ideally, we would use RIB to forward IP packets, but we can't as some entries in it (static routes and BGP routes) could have next hops that are not directly connected.

Compare an IBGP route in the IP routing table (RIB) with an OSPF route:

``` {.code}
RR#show ip route 10.0.11.11
Routing entry for 10.0.11.11/32
  Known via "bgp 65000", distance 200, metric 0, type internal
  Last update from 10.0.1.1 00:00:55 ago
  Routing Descriptor Blocks:
  * 10.0.1.1, from 10.0.1.1, 00:00:55 ago
      Route metric is 0, traffic share count is 1
      AS Hops 0
      MPLS label: none

RR#show ip route 10.0.1.1
Routing entry for 10.0.1.1/32
  Known via "ospf 1", distance 110, metric 66, type intra area
  Last update from 10.0.2.1 on FastEthernet0/0, 00:33:47 ago
  Routing Descriptor Blocks:
  * 10.0.2.1, from 10.0.1.1, 00:33:47 ago, via FastEthernet0/0
      Route metric is 66, traffic share count is 1
```

OSPF route has an outgoing interface; it's computed by the SPF algorithm and transferred in the IP routing table. BGP route has no outgoing interface and its next hop is not directly connected; the router has to perform *recursive lookups* to find the outgoing interface (recursive lookups are also used to implement EBGP load balancing with loopback interfaces).

Early Cisco IOS releases performed a recursive lookup on the first packet sent to a new destination (*process switching*) and cached the result for subsequent packets (*fast switching*). Fast switching worked well in early Internet (with few global IP prefixes), but as the Internet grew and address-spraying DoS attacks became common, core routers frequently experienced *cache* [*trashing*](http://en.wikipedia.org/wiki/Thrashing_(computer_science)). Large number of packets were being process switched, resulting in very high CPU utilization and occasional router meltdown. It was time to move from cache-assisted forwarding to deterministic forwarding.

Forwarding Information Base (FIB) and Cisco Express Forwarding (CEF) were introduced to make layer-3 switching performance consistent. When IP routes are copied from RIB to FIB, their next hops are resolved, outgoing interfaces are computed and multiple entries are created when the next-hop resolution results in multiple paths to the same destination.

For example, when the BGP route from the previous printout is inserted into FIB, its next-hop is changed to point to the actual next-hop router. The information about the recursive next-hop is retained, as it allows the router to update the FIB (CEF table) without rescanning and recomputing the whole RIB if the path toward the BGP next-hop changes.

``` {.code}
RR#show ip cef 10.0.11.11 detail
10.0.11.11/32, epoch 0, flags rib only nolabel, rib defined all labels
  recursive via 10.0.1.1
    nexthop 10.0.2.1 FastEthernet0/0 label 19
```

Fully evaluated FIB (CEF table) can then be used directly for layer-3 switching.

For more details watch the *[Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH)* part of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.
