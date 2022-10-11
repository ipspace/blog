---
title: "On Applicability of MPLS Segment Routing (SR-MPLS)"
date: 2022-10-18 06:28:00
tags: [ segment routing, MPLS ]
---
Whenever I compare MPLS-based Segment Routing (SR-MPLS) with it's distant IPv6-based cousin (SRv6), someone invariably mentions the specter of large label stacks that some hardware cannot handle, for example:

> Do you think vendors current supported label max stack might be an issue when trying to route a packet from source using Adj-SIDs on relatively big sized (and meshed) cores? Many seem to be proposing to use SRv6 to overcome this.

I'd dare to guess that more hardware supports MPLS with decent label stacks than SRv6, and if I've learned anything from my [chats with Laurent Vanbever](https://blog.ipspace.net/2015/11/fibbing-ospf-based-traffic-engineering.html), it's that it sometimes takes surprisingly little to push the traffic into the right direction. You do need a controller that can figure out what that little push is and where to apply it though.
<!--more-->
But wait, it gets better. How about:

> The problem with SR-MPLS is that it does not play well with commodity hardware and ECMP. The label stack depth renders many commodity ASIC's unable to make a ECMP decision to send the flow on [...] SRv6 offsets this via the entropy field. Allowing the ingress point to set an entropy value which mid-points in the network can hash on.

Let me rephrase this one: existing cheap hardware cannot solve a (perceived?) problem caused by overly large MPLS label stack, and the solution is to buy new expensive hardware (that supports SRv6)? There's something wrong with this picture ;)

Fortunately, while vendors keep solving imaginary problems in PowerPoint, there are still networking engineers who use novel technologies to build better and more stable networks. Here's what [Antti Ristimäki had to say about SR-MPLS](https://blog.ipspace.net/2022/09/greenfield-sr-mpls-srv6.html#1391):

> The thing with SR-MPLS is that most of the presentations and slideshows available tend to emphasize how SR-MPLS is based on a lot of stacked MPLS labels or "instructions", with which to steer the traffic throughout the network via desired path. But at least in our case the main driver for migrating from LDP and RSVP-TE to SR-MPLS was to simplify the network and as such most of our traffic is essentially forwarded with only one transport label, or temporarily with a few if TI-LFA is doing a local repair. It is beautifully simple, easy to understand and debug.
>
> The traffic-engineering capabilities of SR-MPLS are great but I'd hope that people would also value much higher the simplicity that one can achieve with SR-MPLS. This also somehow relates to what Sander wrote above that it is so much fun when the label remains unchanged when the packet traverses through the network.

As I said a long time ago, SR-MPLS control plane is [the best thing that happened to the MPLS world in a long while](https://blog.ipspace.net/2019/04/why-is-mpls-segment-routing-better-than.html) and [using it to build a BGP-free core](https://blog.ipspace.net/2021/05/segment-routing-mpls-bgp-free-core.html) couldn't be simpler (as long as you stay within one IGP area). It's so nice to see someone came to the same conclusions and implemented the results in a production network.
