---
title: "Is BGP PIC Edge an Oxymoron?"
date: 2024-12-04 09:09:00+0100
tags: [ IP routing, MPLS ]
---
_This blog post discusses an old arcane question that has been nagging me from the bottom of my Inbox for almost exactly four years. Please skip it if it sounds like Latin to you, but if you happen to be one of those readers who know what I'm talking about, I'd appreciate your comments._

Terminology first:

* *Prefix Independent Convergence* allows entries in the forwarding table to point to shared next hops (or next-hop groups), reducing the FIB update bottleneck when changing the next hop for a large number of prefixes (for example, when dealing with a core link failure). More details in the [initial blog post](https://blog.ipspace.net/2012/01/prefix-independent-convergence-pic/) and [PIC applicability to fast reroute](/2020/11/fast-failover-implementation/).
* *PIC Edge* (as defined by vendor marketing) is the ability to switch to a backup CE route advertised to a backup PE router before the network convergence is complete.

Here's (in a nutshell) how PIC Edge is supposed to work:
<!--more-->
* Backup PE router receives a route from a CE router *that it does not use* (because it has a better route from the primary PE router).
* The backup PE router nonetheless advertises the CE route (*BGP Best External* functionality I [described in this video](https://my.ipspace.net/bin/get/MPLS101/BGP%20Best%20External.mp4?doccode=MPLS101)
* The primary PE router eventually receives the backup CE route and stores it (yet again, without using it). Obviously, if our network uses route reflectors, we need a bit of extra magic (BGP Add Path) to make this work.
* The backup CE route (as advertised through the MPLS/VPN core) carries a label that *points straight to the PE-CE interface*. This allows the primary PE router to *send traffic straight to the backup PE-CE interface* before the backup PE router knows it should use the backup PE-CE interface to reach the CE router.

Now for the *PIC Edge* trick: when the primary PE-CE link fails, the primary PE router rewrites its LFIB entry to send the traffic for the now-unreachable destinations to the backup PE router *and straight through the PE-CE interface* to the CE router. That roundabout forwarding path works *immediately*, even before the primary PE router sends a BGP update saying, "*I  lost the CE prefixes.*" Once the BGP updates are propagated, everyone installs new forwarding entries and stops sending the traffic to the (previous) primary PE router. Eventually, the (former) primary PE router cleans up its LFIB table.

At this point, we're ready for the crux of the blog post: *PIC Edge* needs [per-prefix (or per-CE) VPN labels](/2024/10/mpls-vpn-prefix-vrf-labels/). With the per-VRF labels, we'd get a temporary micro-loop between the primary and the backup PE routers (the details are left as an exercise for the reader). That's why we can't get PIC Edge in most EVPN implementations.

However, using per-prefix VPN labels (the default on Cisco IOS, where we first encountered the *PIC Edge* idea) effectively blocks the Prefix *Independent* Convergence part of the *PIC Edge* as each prefix uses a different VPN MPLS label. The only way to reduce the number of FIB updates seems to be the per-CE label allocation mode. That's the default setting on Junos and available on IOS XR and FRRouting, but (according to what I was able to find in Cisco documentation) not on IOS XE or Nexus OS. Thus, **PIC** Edge on IOS XE sounds like an oxymoron to me. What am I missing?

