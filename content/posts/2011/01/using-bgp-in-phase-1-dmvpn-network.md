---
date: 2011-01-07 06:55:00.001000+01:00
dmvpn_tag: routing
tags:
- DMVPN
- BGP
title: Using BGP in Phase 1 DMVPN network
url: /2011/01/using-bgp-in-phase-1-dmvpn-network.html
---
If you're building a DMVPN network with large spoke-to-hub ratio, BGP is one of the better options -- it has no scalability limitations associated with multicast flooding; the only parameter you have to consider is the number of BGP sessions the hub router can handle (and [according to this presentation](http://www.cisco.com/web/strategy/docs/gov/IntegNet_Feb17_915_Lynn.pdf), ASR can handle 2000+ spokes).
<!--more-->
Here's a brief summary; to learn more, watch a (free) [step-by-step explanation of BGP-over-Phase 1 DMVPN configuration guidelines](https://my.ipspace.net/bin/get/DMVPN/2.2%20-%20Routing%20Protocols%20in%20DMVPN%20Phase%201.mp4?doccode=DMVPN) video:

-   Use EBGP between the hub and the spoke routers to eliminate potential IBGP next-hop issues (unless your hub router can [change BGP next hops on reflected routes](/2014/04/changes-in-ibgp-next-hop-processing.html))
-   You should filter outbound routing updates on the hub router to minimize the amount of routing information and the load placed on the hub router;
-   When using an outbound filter in the hub router, advertise the default route to the spokes;
-   Use BGP session templates and policy templates to minimize the hub router's BGP configuration.
