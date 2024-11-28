---
title: "Lab: Dual-Stack IS-IS Routing"
series_title: "Dual-Stack IS-IS Routing"
date: 2024-11-29 07:47:00+01:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/basic/5-ipv6/
---
Contrary to the OSPF world, where we have to use two completely different routing protocols to route IPv4 and IPv6 (unless you believe in the IPv4 address family in OSPFv3), IS-IS provided multi-protocol support from the very early days of its embracement by IETF. Adding IPv6 support was only a matter of a few extra TLVs, but even there, IETF gave us two incompatible ways of making IPv6 work with IS-IS.

Want to know more? You'll find the details in the [Dual-Stack (IPv4+IPv6) IS-IS Routing](https://isis.bgplabs.net/basic/5-ipv6/) lab exercise.

{{<figure src="https://isis.bgplabs.net/basic/topology-ipv6.png">}}
