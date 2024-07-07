---
date: 2011-05-02 06:33:00.002000+02:00
dmvpn_tag: quirk
tags:
- DMVPN
- workshop
title: NHRP Convergence Issues in Multi-Hub DMVPN Networks
url: /2011/05/nhrp-convergence-issues-in-multi-hub/
---
**Summary for differently attentive**: A hub router failure in multi-hub DMVPN networks can cause spoke-to-spoke traffic disruptions that last up to three minutes.

Almost every DMVPN design I've seen has multiple hubs for redundancy purposes. I've always preached the "one hub per DMVPN tunnel" mantra (see the diagram below) to those who were willing to listen citing "NHRP issues after hub failure" as one of the main reasons you should not have two or more hubs per DMVPN tunnel.

{{<figure src="/2011/05/s1600-DMVPN_2H2T.png" caption="Each hub router controls an independent DMVPN tunnel">}}
<!--more-->
The one-hub-per-tunnel rule works well in small and medium-sized DMVPN deployments, but you can't use it in large-scale (Phase 3) deployments with hierarchical hub structure as NHRP shortcuts between subnets never got properly implemented in the DMVPN code. In these cases, you're forced to have multiple hubs in the same DMVPN subnet.

{{<figure src="/2011/05/s1600-DMVPN_2H1T.png" caption="Multiple hubs in a single DMVPN network">}}

While developing the material for the [DMVPN New Features](http://www.ipSpace.net/DMVPN150) webinar, I tested the convergence of both designs and found out significant differences in a hub failure scenario (convergence after a spoke failure depends purely on the routing protocol settings).

### Why Does It Matter?

A hub router has three important roles in a Phase 2/3 DMVPN network:

-   It's a routing protocol neighbor for all the spokes (spokes can't exchange routing protocol messages directly due to lack of NHRP multicast maps);
-   Spokes use it for NHRP resolution while trying to establish spoke-to-spoke tunnels;
-   Spokes send all the inter-spoke traffic through the hub until they manage to establish direct IPsec session.

A hub failure can thus directly impact spoke-to-spoke connectivity in those DMVPN networks where spokes can't establish direct IPsec sessions (due to NAT or other limitations).

### Convergence of One-Hub-per-Tunnel DMVPN Designs

When you lose a hub router in one-hub-per-tunnel DMVPN design, NHRP registrations on the tunnel fail completely and the routing across the affected tunnel stops after the spoke routers figure out their routing protocol neighbor is gone.

If you use short NHRP registration timer (configured with **ip nhrp registration timeout**), NHRP detects the hub failure pretty quickly (spoke routers need at most NHRP registration timer + 10 seconds to detect the failure; details are described in my [DMVPN New Features](http://www.ipSpace.net/DMVPN150) webinar).

If you combine 10 second NHRP timers with interface state tracking (configured with **if-state nhrp**), the spokes stop using the failed tunnel in less than 20 seconds.

### Convergence of Multi-Hub DMVPN Designs

Losing a hub in multi-hub DMVPN design will not affect the routing across the DMVPN tunnel. Spokes will eventually detect one of their routing protocol neighbors is gone, but the change will not affect their routing tables.

NHRP spokes usually use a single hub router for NHRP resolution and interim inter-spoke traffic (until a spoke-to-spoke session is established); the spoke-to-spoke traffic could also flow over the hub router indefinitely if you have the spoke routers behind a too-restrictive NAT device (yet again, you'll find all the details in my [DMVPN New Features](http://www.ipSpace.net/DMVPN150) webinar). Failure of the "selected" hub router could thus also disrupt the spoke-to-spoke traffic. The disruption period depends on IOS release.

**IOS releases prior to NAT enhancements**. The spokes detect hub router failure through NHRP registration timeouts (see above). Spoke-to-spoke traffic flows through the hub only if the NRHP entry for the other spoke is *incomplete* or otherwise faulty (for example, IPsec session is not operational, resulting in *no socket* state) and is *not tied to any individual hub*. As soon as the spoke detects the failure of its currently selected hub router, it switches to another hub router, resulting in short disruption of inter-spoke traffic.

**IOS releases after NAT enhancements (12.4T and 15.x)**. Spoke routers create [fake NHRP entries for other spokes](/2011/04/dmvpn-spoke-nhrp-behavior-changed-in/) using the hub's router NBMA address. The fake entry disappears as soon as the spoke router receives a NHRP reply from the other spoke, but could stay in the NHRP cache indefinitely if the spoke-to-spoke IPsec session cannot be established.

These entries are tied to *specific NBMA address* (of the selected hub router), not to the hub router and do not disappear when the spoke router discovers hub router failure (via NHRP registration failure). To make matters worse, the fake entries use a 3-minute expiration timer that cannot be adjusted with any publicly available DMVPN configuration command that I could find. A hub router failure can thus disrupt the spoke-to-spoke traffic for up to three minutes (until the fake NHRP entry expires).

### More information

You'll find tons of details in our [DMVPN webinars](https://www.ipspace.net/Roadmap/VPN_webinars).