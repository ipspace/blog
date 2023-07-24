---
date: 2011-01-14 07:38:00+01:00
dmvpn_tag: basics
series_weight: 400
tags:
- DMVPN
title: DMVPN Phase 1 Fundamentals
url: /2011/01/dmvpn-phase-1-fundamentals.html
---
Phase 1 DMVPN in a nutshell:

-   Point-to-point GRE tunnel on spoke routers
-   Multipoint GRE tunnel on the hub router.
-   All the DMVPN traffic (including the traffic between the spokes) flows through the hub router.
-   On the spoke routers, the hub router must be the IP next-hop for all destinations reachable through the DMVPN subnet (including other spokes).
-   Multicast packets (including routing protocol hello packets and routing updates) are exchanged only between the hub and the spoke routers.
<!--more-->
For more details watch the [DMVPN webinar](http://www.ipspace.net/DMVPN) webinar which also includes the following topics:

-   Basic hub router configuration;
-   Explanation of *GRE tunnel key* concept and its potential performance implications;
-   NHRP configuration of the hub and spoke routers;
-   Non-unique NHRP registrations;
-   Multicast over mGRE principles;
-   DMVPN redundancy;
-   IPSec configuration with shared keys and certificates;
-   Monitoring and troubleshooting guidelines.
