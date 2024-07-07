---
date: 2011-01-18 06:35:00+01:00
dmvpn_tag: basics
series_weight: 300
tags:
- DMVPN
title: DMVPN Phase 2 Fundamentals
url: /2011/01/dmvpn-phase-2-fundamentals/
---
Phase 2 DMVPN in a nutshell:

-   Multipoint GRE tunnels on all routers.
-   NHRP is used for dynamic spoke registrations (like with Phase 1 DMVPN), but also for on-demand resolution of spoke transport addresses.
-   Traffic between the spokes initially flows through the hub router until NHRP resolves the remote spoke transport IP address and IKE establishes the IPSec session with it.
-   The IP next-hop address for any prefix reachable over DMVPN must be the egress router (hub or spoke). From the routing perspective, Phase 2 DMVPN subnet should behave like a LAN.
-   Multicast packets (including routing protocol hello packets and routing updates) are exchanged only between the hub and the spoke routers.
-   Routing adjacencies are established only between the hub and the spoke routers unless you use statically configured neighbors.

For more details watch the [DMVPN webinar](http://www.ipspace.net/DMVPN) webinar.