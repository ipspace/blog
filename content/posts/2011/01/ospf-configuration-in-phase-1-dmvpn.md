---
date: 2011-01-17 06:56:00.003000+01:00
dmvpn_tag: routing
tags:
- DMVPN
- OSPF
- workshop
title: OSPF Configuration in Phase 1 DMVPN Network
url: /2011/01/ospf-configuration-in-phase-1-dmvpn.html
---
[This is how you configure OSPF in a Phase 1 DMVPN network](https://my.ipspace.net/bin/get/DMVPN/D3%20-%20OSPF%20routing%20in%20Phase%201%20DMVPN.mp4?doccode=DMVPN) (read the [introductory post](https://blog.ipspace.net/2011/01/sometimes-you-need-to-step-back-and.html) and [Phase 1 DMVPN fundamentals](https://blog.ipspace.net/2011/01/dmvpn-phase-1-fundamentals.html) first):

Remember:

-   Use **point-to-multipoint** network type on the hub router to ensure the hub router is always the IP next hop for the DMVPN routes.
-   Use **point-to-multipoint** network type on the spoke routers to ensure the OSPF timers match with the hub router.
-   The DMVPN part of your network should be a separate OSPF area; if at all possible, make it a stub or NSSA area.
-   If absolutely needed, use [OSPF LSA flood filter](/kb/tag/OSPF/OSPF_Flood_Reduction_Hub_Spoke.html) on the hub router and a static default route on the spokes.

For more information, watch the *[DMVPN Technology and Configuration](http://ipspace.net/DMVPN)* webinar.
