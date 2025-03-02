---
date: 2010-06-11 07:15:00+02:00
tags:
- IPv6
- service providers
- IS-IS
title: Multi-Topology IS-IS
url: /2010/06/multi-topology-is-is/
---
IS-IS has "forever" (at least since [RFC 1195](http://datatracker.ietf.org/doc/rfc1195/)) supported multiple layer-3 protocols, but always with a nasty side-effect: if a link in your network did not support one of them, you could get hard-to-diagnose black holes.

The problem is illustrated in the left-hand column of the following diagram. Due to a single IS-IS topology, the shortest path between A and B is the direct link, and since IPv6 is not enabled on that link (click on the diagram to get an enlarged version where you\'ll be able to see the link colors), A and B cannot exchange IPv6 traffic even though there's an alternate path between them.
<!--more-->
{{<figure src="/2010/06/s400-ISIS+Multi-Topology.png">}}

When you enable multi-topology IS-IS (right-hand column in the diagram), the routers build two topologies, one for each L3 protocol (usually IPv4 and IPv6), and can find the optimum path for each L3 protocol even when some links in the network support only one of them.

You'll find more details in the [Dual-Stack (IPv4+IPv6) IS-IS Routing](https://isis.bgplabs.net/basic/5-ipv6/) lab exercise (part of [open-source multi-vendor IS-IS labs](https://isis.bgplabs.net/)).