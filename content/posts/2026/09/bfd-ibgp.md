---
title: "BFD on IBGP Sessions? Why Exactly?"
date: 2026-09-30 07:14:00+0200
tags: [ BGP ]
---
A friend of mine sent me an email with a weird observation:

> In the last year, I've seen a number of networks configure BFD on their iBGP sessions with very aggressive timers, including a network with 300 msec BFD timers (900 msec holddown).

There might be (marginally sane) reasons to run BFD on iBGP sessions instead of relying on other failure detection mechanisms, but using such short timers seems like a Really Bad Idea&trade;
<!--more-->
Let's start with what anyone touching BGP should always keep in mind: IBGP is an endpoint reachability propagation mechanism[^DKVS], not a routing protocol for figuring out the next hop toward a destination. It SHOULD[^CVI] always be used together with an IGP that calculates the best path to internal (intra-AS) IP prefixes, which IBGP can then use for next hops.

[^DKVS]: You can also call it *distributed key-value store* if you want to sound really cool.

[^CVI]: Don't get me started on crazy vendor ideas, sometimes even documented in their _validated designs_. I ranted about them in the past; if you haven't read those blog posts, grab a bag of popcorn and start searching ;)

However, an IBGP peer advertising the best BGP route could go down due to a router reload or any other node failure. BGP convergence relying solely on BGP timers could take a while, and BFD might seem like a great answer.

Some vendors[^SV] realized this decades ago and implemented fast *next-hop tracking* -- when a BGP next hop disappears from the routing table[^NHTD], all BGP routes using it are revoked from the BGP table, allowing the BGP routing process to select alternate routes (either those already in the BGP table or advertised by its neighbors during the BGP convergence process). 

[^SV]: I'm really sorry if your box doesn't implement that functionality; someone was obviously sloppy when buying your network equipment. Maybe it's time to switch vendors?

[^NHTD]: Some implementations include a configurable delay to prevent route flushing during IGP convergence.

A failed IBGP neighbor should thus be detected via a change in the IP routing table caused by IGP convergence. Using BFD as a workaround is like applying a thick layer of lipstick to an ugly pig (= a broken IGP or a bad BGP implementation). Also, don't even try to argue that you have to use BFD to detect forwarding-path failures between IBGP peers; that just proves your network is broken beyond hope.

Finally, a word about BFD timers. If you're so far from a sane network design or implementation that BFD between IBGP peers is your only hope, PRETTY PLEASE don't use aggressive timers, or you might lose IBGP sessions (and IBGP routes) during a normal IGP convergence event. Also, multihop BFD (which is what we need for IBGP sessions) might not be implemented in hardware, which makes it even more vulnerable to CPU overloads. See also [How Fast Can We Detect a Network Failure?](/2020/11/detecting-network-failure/), [To BFD or Not to BFD?](/2017/10/to-bfd-or-not-to-bfd/), and [Know Thy Environment Before Redesigning It](/2019/06/know-thy-environment-before-redesigning/).
