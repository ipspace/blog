---
date: 2016-04-18 09:58:00.002000+02:00
tags:
- MPLS
- SDN
- traffic engineering
- segment routing
title: Zero Bandwidth Traffic Engineering
url: /2016/04/zero-bandwidth-traffic-engineering/
---
Oliver Steudler from Juniper sent me a link to an interesting Juniper blog post describing [zero-bandwidth traffic engineering](http://forums.juniper.net/t5/SDN-and-NFV-Era/Using-Zero-Bandwidth-BW-LSPs-for-Optimal-Network-Utilization-in/ba-p/289472).

Read the blog post first and then come back for some opinionated rambling ;)

**Is the problem real?** Yes.
<!--more-->
Make-before-break inevitably results in temporary double bandwidth booking. While RSVP-TE solves double-counting on shared legs of the path, it cannot do the same when the old and the new paths diverge.

**Is this a problem worth solving?** It depends on the percentage of the network bandwidth reserved for traffic engineering tunnels. You don't have the problem if you use MPLS-TE solely for fast reroute, or if you don't use most of the reservable bandwidth.

**Will this work without a controller?** No. Someone has to keep track of how much bandwidth is actually reserved, and in this case the information resides only within the controller. If you allow the MPLS routers to establish additional (non-PCE-controlled) tunnels, you'll get a nice mess.

**Isn't this functionally equivalent to TE for Segment Routing** **(aka SPRING)?** Yes. In both cases the network devices don't track bandwidth reservations and thus cannot make reliable autonomous decisions.

**So why exactly do we need two equivalent solutions?** Most routers deployed today don't support SPRING, and some may not support (at least some variants of) segment routing without a hardware upgrade. Zero-bandwidth trick works with every router running PCE client.
