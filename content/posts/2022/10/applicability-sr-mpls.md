---
title: "On Applicability of MPLS Segment Routing (SR-MPLS)"
date: 2022-10-18 06:28:00
tags: [ segment routing, MPLS ]
lastmod: 2022-10-20 13:54:00
---
Whenever I compare MPLS-based Segment Routing (SR-MPLS) with it's distant IPv6-based cousin (SRv6), someone invariably mentions the specter of large label stacks that some hardware cannot handle, for example:

> Do you think vendors current supported label max stack might be an issue when trying to route a packet from source using Adj-SIDs on relatively big sized (and meshed) cores? Many seem to be proposing to use SRv6 to overcome this.

I'd dare to guess that more hardware supports MPLS with decent label stacks than SRv6, and if I've learned anything from my [chats with Laurent Vanbever](/2015/11/fibbing-ospf-based-traffic-engineering/), it's that it sometimes takes surprisingly little to push the traffic into the right direction. You do need a controller that can figure out what that little push is and where to apply it though.
<!--more-->
But wait, it gets better. How about:

> The problem with SR-MPLS is that it does not play well with commodity hardware and ECMP. The label stack depth renders many commodity ASIC's unable to make a ECMP decision to send the flow on [...] SRv6 offsets this via the entropy field. Allowing the ingress point to set an entropy value which mid-points in the network can hash on.

Let me rephrase this one: existing cheap hardware cannot solve a (perceived?) problem caused by overly large MPLS label stack, and the solution is to buy new expensive hardware (that supports SRv6)? There's something wrong with this picture ;)

Fortunately, while vendors keep solving imaginary problems in PowerPoint, there are still networking engineers who use novel technologies to build better and more stable networks. Here's what [Antti Ristimäki had to say about SR-MPLS](/2022/09/greenfield-sr-mpls-srv6/#1391):

> The thing with SR-MPLS is that most of the presentations and slideshows available tend to emphasize how SR-MPLS is based on a lot of stacked MPLS labels or "instructions", with which to steer the traffic throughout the network via desired path. But at least in our case the main driver for migrating from LDP and RSVP-TE to SR-MPLS was to simplify the network and as such most of our traffic is essentially forwarded with only one transport label, or temporarily with a few if TI-LFA is doing a local repair. It is beautifully simple, easy to understand and debug.
>
> The traffic-engineering capabilities of SR-MPLS are great but I'd hope that people would also value much higher the simplicity that one can achieve with SR-MPLS. This also somehow relates to what Sander wrote above that it is so much fun when the label remains unchanged when the packet traverses through the network.

As I said a long time ago, SR-MPLS control plane is [the best thing that happened to the MPLS world in a long while](/2019/04/why-is-mpls-segment-routing-better-than/) and [using it to build a BGP-free core](/2021/05/segment-routing-mpls-bgp-free-core/) couldn't be simpler (as long as you stay within one IGP area). It's so nice to see someone came to the same conclusions and implemented the results in a production network.

### But Wait, There's More

Speaking of *solving imaginary problems in PowerPoint*, here's a wonderful comment someone[^WKH] working for a major networking vendor left on LinkedIn:

> Hmm.. you have 300,000 routers with RFC3107 and tiers of IGP's. Each router in your network potentially supports a different maximum label stack, some 3, some 8...
>
> You have 4 different vendors telling you that SR path engineering is the solution to all your problems.
>
> You have 10's of NOS versions each with unique compliance to the ever evolving SR based standard
>
> What you don't have is an audit of why your label traffic is being incorrectly forwarded or dropped half way through the network......
>
> You can either dig a bigger hole... or just accept that SRv6 and appropriate management tools are the most expedient manner to scale a network and stop building work arounds.

He forgot to mention that:

* You would probably have to upgrade 290,000 of your routers before you could run SRv6 everywhere in your network, and have interesting interoperability nightmares in the meantime.
* You will either be totally dependent on a single vendor, or still deal with 10s of NOS versions with various levels of support for SRv6.
* Finally, which exact variant of SRv6 are we talking about? SRv6 or SRv6+? People finally realized how bloated SRv6 is and started talking about shorter SIDs, compressed SRH, variable-length SID... Yeah, I'm positive all that will end really well for people who care about interoperability.

[^WKH]: No, I will not tell you who it was.

### Revision History

2022-10-20
: Added a wonderful LinkedIn comment