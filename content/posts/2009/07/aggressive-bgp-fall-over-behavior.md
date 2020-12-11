---
date: 2009-07-29 07:05:00+02:00
tags:
- BGP
title: Aggressive BGP Fall-Over Behavior
url: /2009/07/aggressive-bgp-fall-over-behavior.html
needs_fix: true
---
Soon after I wrote the *Designing Fast Converging BGP Networks* article (you'll find it somewhere in [this list](https://www.ipspace.net/kb/Internet/), one of my regular readers sent me an interesting problem: BGP sessions would be lost in his (IS-IS based) core network if he would use **fall-over** on IBGP neighbors and the BGP router would have a primary and a backup path to the IBGP neighbor.

We've identified the source of the problem (delayed SPF run) and I decided to document it. It took "a while" (and a kind nudge from Mateusz following a discussion on Cisco-NSP mailing list) to find time to set up the test lab and document the behavior. You can find the (undesired) results in the [Aggressive BGP fall-over behavior](http://wiki.nil.com/Aggressive_BGP_fall-over_behavior) in the [CT3 wiki](http://wiki.nil.com/).

Just in case someone from Cisco wants to put this on a wish list: please add a configurable delay to the **neighbor fall-over** command like you did with the **bgp nexthop trigger delay** command.

