---
date: 2010-07-21 06:49:00.003000+02:00
tags:
- bridging
- data center
- workshop
- TRILL
title: Why Is TRILL Not Routing at Layer-2
url: /2010/07/why-is-trill-not-routing-at-layer-2/
---
Peter John Hill made an interesting observation in a comment to one of my blog posts; he wrote "*TRILL really is routing at layer 2.*"

He's partially right -- TRILL uses a routing protocol (IS-IS) and the TRILL protocol used to forward Ethernet frames (TRILL data frames) definitely has all the attributes of a layer-3 protocol:

-   TRILL data frames have layer-3 addresses (RBridge nickname);
-   They have a hop count;
-   Layer-2 next-hop is always the MAC address of the next-hop RBridge;
-   As the TRILL data frames are propagated between RBridges, the outer MAC header changes.
<!--more-->
However, once the TRILL infrastructure is set up and the best paths are computed, bridging forwarding paradigms are used to forward host-to-host data traffic, including building MAC address table by listening to data traffic and flooding of packets sent to unknown MAC destination. TRILL therefore retains most of the non-scalable properties of transparent bridging with these exceptions:

-   Convergence is faster and more predictable;
-   Data forwarding can use all the available links;
-   Core RBridges (those that have no non-TRILL links) do not need to know the end-station MAC addresses;
-   Edge RBridges need to know end-station MAC addresses only for the VLANs in which they participate (but that's also true in existing well-designed bridged networks).

For an in-depth overview of TRILL, start with the [*Setting the stage for TRILL, rethinking data center switching*](http://bradhedlund.com/2010/05/07/setting-the-stage-for-trill/) article by Brad Hedlund and continue with [RFC 5556](http://tools.ietf.org/html/rfc5556) (TRILL: Problem and Applicability Statement); you\'ll find a big-picture perspective in my [Data Center 3.0 for Networking Engineers](https://www.ipspace.net/DC30) webinar ([buy a recording](https://www.ipspace.net/SingleRecording?code=DC30) or [yearly subscription](https://www.ipspace.net/Subscription)).
