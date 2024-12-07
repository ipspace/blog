---
kb_section: OSPF_DV
minimal_sidebar: true
title: When OSPF Becomes a Distance Vector Protocol
toc_title: Introduction
url: /kb/Internet/OSPF_DV/
tags: [ OSPF ]
ospf_tag: areas
date: 2024-12-11 08:05:00+0100
alt_section: posts
index: true
---
We were always told that Open Shortest Path First (OSPF) is a fast converging link-state routing protocol that always results in a loop-free and blackhole-free network topology. In reality, it’s a link-state protocol within an area and almost a distance-vector protocol between areas.

In this article, I’ll illustrate how this unexpected behavior can affect the convergence of your network and how you can use proprietary extensions of Cisco IOS to alleviate the undesired side effects of OSPF.
<!--more-->

{{<note migrated>}}This article was written in 2007, and has been updated and republished on ipSpace.net in 2023.{{</note>}}

## The Scenario

Let’s start with a very simple network topology displayed in Figure 1: four routers in a meshed OSPF area, with two of them (A1 and A2) also participating in area 0 (thus becoming Area Border Routers – ABR).

{{<figure src="/kb/Internet/OSPF_DV/NetDiagram.jpg" caption="Sample network topology">}}

This topology is very common in hierarchical networks (A1 and A2 would be the core or aggregation routers, and S1 and S2 would be two sites with a backdoor link between them).

{{<note>}}
The backdoor link between S1 and S2 was inserted solely to better illustrate the side effects of OSPF. The same behavior is observed (although in a slightly less pronounced way) in a pure hub-and-spoke scenario.
{{</note>}}

When a subnet is lost on the S1 router (subnet loss can be easily emulated by disabling a loopback interface), the corresponding route is lost on S2 when it runs the Shortest Path First (SPF) algorithm (the IP routing debugging printouts are included in Listing 1). However, the route mysteriously reappears in a few milliseconds, now pointing to both ABRs (obviously a black hole). After another five seconds, the spurious routes disappear, resulting in completed network convergence.

{{<note>}}
**Technical details**

The initial SPF delay and the inter-SPF interval can be configured with the [**timers throttle spf** router configuration command](http://www.cisco.com/en/US/products/ps6350/products_configuration_guide_chapter09186a00804556e3.html).
{{</note>}}

{{<cc>}}Area Border Routers blackhole a lost subnet{{</cc>}}
```
S2#show debug

IP routing:

  IP routing debugging is on for access list 98

S2#show access-list

Standard IP access list 98

    10 permit 10.0.0.11

S2#
04:44.047: RT: del 10.0.0.11/32 via 10.0.2.17, ospf metric [110/65]
04:44.051: RT: delete subnet route to 10.0.0.11/32
04:44.051: RT: NET-RED 10.0.0.11/32
04:44.087: RT: add 10.0.0.11/32 via 10.0.2.13, ospf metric [110/139]
04:44.091: RT: NET-RED 10.0.0.11/32
04:44.119: RT: add 10.0.0.11/32 via 10.0.2.5, ospf metric [110/139]
04:44.123: RT: NET-RED 10.0.0.11/32
04:49.139: RT: del 10.0.0.11/32 via 10.0.2.13, ospf metric [110/139]
04:49.143: RT: NET-RED 10.0.0.11/32
04:49.175: RT: del 10.0.0.11/32 via 10.0.2.5, ospf metric [110/139]
04:49.179: RT: delete subnet route to 10.0.0.11/32
04:49.183: RT: NET-RED 10.0.0.11/32
```

This behavior might seem purely academic at first, but if the backup solution on S2 uses another routing protocol or floating static routes, the backup route will not be applied until the spurious routes received from ABRs are removed.
