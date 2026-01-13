---
title: "Do You Need IS-IS Areas?"
date: 2026-01-14 08:45:00+0100
tags: [ IS-IS ]
---
**TL&DR**: Most probably not, but if you do, you'd better not rely on random blogs for professional advice #justSaying 😜

Here's an interesting question I got from a reader in the midst of an OSPF-to-IS-IS migration:

> Why should one bother with different [IS-IS] areas when the routing hierarchy is induced by the two levels and the appropriate IS-IS circuit types on the links between the routers?

Well, if you think you need a routing hierarchy, you're bound to use IS-IS areas because that's how the routing hierarchy is implemented in IS-IS. However...
<!--more-->
* People were building networks with hundreds of routers in a single IS-IS area in the 90s.
* Because of that, the IS-IS code in major network operating systems tends to be pretty decent.
* As a consequence, unless you have a ginormous network, you'll probably be just fine with a single IS-IS area. Just make sure all your routers are either L1-only or L2-only intermediate systems, or you'll get an explosion in the LSP database size ([more details](https://isis.bgplabs.net/basic/6-level-2/)).

On the other hand, you might be unfortunate enough to own inferior hardware that cannot cope with too many changes or large routing tables. In that case, the IS-IS routing hierarchy may still be useful for fault isolation[^FI] and route summarization.

[^FI]: Like in OSPF, a topology change in an IS-IS level is confined to that level and gets propagated to the other IS-IS level only as a change in prefix cost/reachability. Summarizing routes between hierarchy levels further reduces the amount of that change.

However, keep in mind that IS-IS wasn't designed to route IP[^DRIP]. For example, by default, level-1 routers in an IS-IS area know only that there's another router in their area attached to the level-2 backbone, and use that information to generate a default route. While you can inject level-2 routes into a level-1 area (and summarize prefixes in the process), this process must be configured and may not be supported on all platforms.

[^DRIP]: Using it for IPv4 (and later IPv6) routing was a side effect of having a decent IGP.

Speaking of platform support: there are IS-IS implementations out there (for example, FRRouting) that do not implement inter-level prefix propagation[^NUI]. Checking the capabilities of your network devices before designing your IS-IS network is, unfortunately, still a thing in 2026.

[^NUI]: That might be a pretty good indication that nobody running FRRouting is using multi-level IS-IS.

Want to know more about how IS-IS areas really work? Dan Partelly created a beautiful set of (free) IS-IS lab exercises that walk you through the details:

* [Multilevel IS-IS Deployments](https://isis.bgplabs.net/advanced/1-multilevel/)
* [Distributing Level-2 IS-IS Routes into Level-1 Areas](https://isis.bgplabs.net/advanced/2-route-leak/)
* [Summarizing Level-1 Routes into Level-2 Backbone](https://isis.bgplabs.net/advanced/3-summarization/)

Even running these exercises is free: all you have to do is [create a GitHub Codespaces instance](https://isis.bgplabs.net/4-codespaces/), [install the Arista cEOS container](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) in it (or use SR Linux), and start kicking the tires.
