---
date: 2018-12-10 09:17:00+01:00
tags:
- MPLS
- IPv6
- segment routing
title: Segment Routing Anyone?
url: /2018/12/segment-routing-anyone/
---
One of my readers listened to a podcast where a \$vendor described how they found another use case for ~~source routing~~ IPv6 segment routing (SR): 5G networks... and wondered whether SR made a comeback or is about to.

I don't know nearly enough about mobile networks to have an opinion, however...
<!--more-->
Considering that mobile network backhauls use tunnels of some sort anyway, using source routing (which is what segment routing really is) instead of tunnels might make sense, although it still sounds pretty academic to me.

### Quick Diversion Into SR 101...

Keep in mind the networking vendors managed to squeeze two completely different technologies under the Segment Routing umbrella:

-   MPLS labels stacks,
-   IPv6 extension headers.

You can use segment routing with MPLS label stacks on existing hardware (the only limit is the stack size on ingress node), while IPv6 SR needs either new hardware or [NPUs](https://en.wikipedia.org/wiki/Network_processor).

At least the MPLS version of Segment Routing uses new control-plane extensions to existing routing protocols (IS-IS, OSPF, BGP) to distribute labels for prefixes (including nodes when prefix = loopback interface), or adjacencies (read: interfaces unless you're using shared LANs).

### And We're Back...

MPLS version of segment routing seems to be popular in large data centers, particularly at WAN edge of large content providers. It's also a relatively small evolutionary step - data plane is the same, control plane is replaced with something that makes way more sense than current hodgepodge of LDP, RSVP...

Even outside of that particular use case, using segment routing functionality to allocate MPLS labels to BGP next hops makes perfect sense and eventually simplifies your network.

IPv6 Segment Routing is another story. It replaced the abhorred (and now [deprecated](https://tools.ietf.org/html/rfc5095)... because nothing ever dies in IETF) RH0 with something else, but it's still source routing using extension headers... and [very few hardware platforms](https://tools.ietf.org/id/draft-filsfils-spring-srv6-interop-00.html) support it (all of them with special engineering code).

The whole IPv6 SR saga seems like another [LISP exercise](/2017/09/why-is-cisco-pushing-lisp-in-enterprise/) to me - we have a technology we invested a lot of money in, let's find a problem it could solve. Look, here's another one...

Am I wrong? Is someone using IPv6 SR in (anywhere close to) production?
