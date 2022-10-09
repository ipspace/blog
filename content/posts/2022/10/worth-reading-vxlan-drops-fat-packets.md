---
title: "Worth Reading: VXLAN Drops Large Packets"
date: 2022-10-09 07:41:00
tags: [ VXLAN ]
---
Ian Nightingale published an [interesting story of connectivity problems he had in a VXLAN-based campus network](https://constantpinger.home.blog/2022/09/27/selective-packet-loss-over-vxlan-fat-packets-dropped/). **TL&DR**: it's always the MTU (unless it's DNS or BGP).

The really fun part: even though large L2 segments might have magical properties (according to vendor fluff), there's no host-to-network communication in transparent bridging, so there's absolutely no way that the ingress VTEP could tell the host that the packet is too big. In a layer-3 network you have at least a fighting chance...

For more details, watch the *[Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH)* part of _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar (most of it available with [Free Subscription](https://www.ipspace.net/Subscription/Free)).
