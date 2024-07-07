---
date: 2011-08-12 07:48:00.001000+02:00
dmvpn_tag: routing
ospf_tag: dmvpn
tags:
- DMVPN
- OSPF
title: More OSPF-over-DMVPN Questions
url: /2011/08/more-ospf-over-dmvpn-questions/
---
After weeks of waiting, perfect summer weather finally arrived ... and it’s awfully hard to write blog posts that make marginal sense when being dead-tired from day-long mountain biking, so I’ll just recap the conversation I had with Brian a few days ago. He asked:

> How would I set up a (dual) hub running OSPF with phase 1 spokes and prevent all spoke routes from being seen at other spokes? Think service provider environment.

If you want to have a scalable DMVPN environment, you have to put numerous spokes connected to the same hub in a single IP subnet (otherwise, you’ll end with point-to-point tunnels), which also means they have to be in a single OSPF area and would thus see each other’s LSAs.
<!--more-->
The only mechanism to stop the LSA propagation through the hub router is [OSPF database filter configured on the hub router](/kb/tag/OSPF/OSPF_Flood_Reduction_Hub_Spoke/), but then the spokes would receive no routes from the hub at all – you would have to configure static routes on them.

Static default routes on spokes are easy to implement if you have a single hub. In a dual-hub environment, you can use either *reliable static routing* (static routes based on IP SLA results, see my [Small Site Multihoming](/2009/05/small-site-multihoming-tutorial/) articles for more details) or tunnel health monitoring feature introduced in IOS release 15.0M. This feature would bring down a DMVPN tunnel (and make all the static routes using that tunnel disappear from the IP routing table) if the spoke cannot reach the hub through NHRP, so it’s safe to use simple static default routes pointing to both hubs.

However, OSPF is the least scalable protocol for the DMVPN environment due to its router adjacency handling. If you plan to have more than a few hundred spokes, you should consider EIGRP, passive RIP, or BGP (see my [DMVPN scalability](/2010/10/dmvpn-scalability/) post for more details).
