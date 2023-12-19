---
date: 2011-01-19 06:43:00+01:00
dmvpn_tag: routing
ospf_tag: dmvpn
tags:
- DMVPN
- OSPF
title: Configuring OSPF in a Phase 2 DMVPN network
url: /2011/01/configuring-ospf-in-phase-2-dmvpn.html
---
Cliffs Notes version (details in the [DMVPN webinar](https://www.ipspace.net/DMVPN_Technology_and_Configuration)):

-   Configure **ip nhrp multicast-map** for the hub on the spoke routers. Otherwise, the spokes will not send OSPF hellos to the hub.
-   Use dynamic NHRP multicast maps on the hub router, or the spokes will not receive its OSPF hellos.
-   Use **broadcast** network type on all routers.

{{<note warn>}}You could use the **non-broadcast** network type and configure the neighbors manually, but that would just destroy the scalability of the solution. If you use **point-to-multipoint** network type, all the traffic will flow through the hub router.{{</note>}}
<!--more-->
-   Only the NHRP next-hop servers (usually the hub router(s)) can send OSPF hellos to everyone. If any other router becomes DR or BDR, you'll get hard-to-explain partial connectivity.
-   Set OSPF DR priority to a high value on the hub router (so even if an under-configured spoke joins the network, it won't preempt the hub).
-   Set OSPF DR priority to zero on the spoke routers (this ensures they can never become a DR or BDR).
-   The DMVPN part of your network should be a separate OSPF area; if at all possible, make it a stub or NSSA area.