---
title: "Worth Reading: Ephemeral BGP Leaks"
date: 2026-05-28 07:22:00+0200
tags: [ worth reading, BGP, security ]
---
Doug Madory wrote an interesting article (published on APNIC blog) arguing that [we shouldn't worry about ephemeral BGP leaks](https://blog.apnic.net/2026/05/25/ephemeral-leaks-and-automated-bgp-route-leak-detection/) that can be observed only during the [BGP path hunting process](https://lostintransit.se/2023/10/09/path-hunting-in-bgp/) that follows a route withdrawal.

I have to disagree with that. It's never a good idea to ignore a [dead canary in the coal mine](https://en.wikipedia.org/wiki/Sentinel_species).

While the ephemeral leaks do not impact the end result (after all, the route is gone), they are an important indicator of the lack of BGP route policy enforcement in the autonomous systems that propagate them. If an autonomous system is propagating a bogus route when no better routes are available, it's equally likely to propagate a bogus route when an intruder manages to inject it.
