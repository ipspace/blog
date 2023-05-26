---
date: 2009-07-29 07:05:00+02:00
tags:
- BGP
title: Aggressive BGP Fall-Over Behavior
url: /2009/07/aggressive-bgp-fall-over-behavior.html
---
Soon after I wrote the *Designing Fast Converging BGP Networks* article (you'll find it somewhere in [this list](/kb/Internet/), one of my regular readers sent me an interesting problem: BGP sessions would be lost in his (IS-IS based) core network if he would use **fall-over** on IBGP neighbors and the BGP router would have a primary and a backup path to the IBGP neighbor.

It turned out to be an interesting side effect of aggressive route table purge following a link failure: the route to BGP neighbor was removed from the routing table before IS-IS ran SPF and installed an alternate route, and BGP decided it's time to give up and terminate the session.

For more details, read the *[What Exactly Happens after a Link Failure](https://blog.ipspace.net/2020/12/what-happens-after-link-failure.html)* blog post.