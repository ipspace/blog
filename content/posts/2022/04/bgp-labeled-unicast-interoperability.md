---
title: "BGP Labeled Unicast Interoperability Challenges"
date: 2022-04-05 07:11:00
tags: [ BGP, MPLS ]
---
Jeff Tantsura left me tantalizing hint after reading the _[BGP Labeled Unicast on Cisco IOS](/2022/03/bgp-labeled-unicast-cisco-ios.html)_ blog post:

> Read carefully “[Relationship between SAFI-4 and SAFI-1 Routes](https://datatracker.ietf.org/doc/html/rfc8277#section-5)” section in RFC 8277

The start of that section doesn't look promising (and it gets worse):

> It is possible that a BGP speaker will receive both a SAFI-1[^SF1] route for prefix P and a SAFI-4[^SF4] route for prefix P.  Different implementations treat this situation in different ways.

Now for the details:
<!--more-->

[^SF1]: Unlabeled IPv4 or IPv6 prefix. See _[Three Dimensions of BGP Address Family Nerd Knobs](/2022/01/bgp-af-nerd-knobs.html)_ for more details.

[^SF4]: IPv4 or IPv6 prefix with one or more MPLS labels attached to it.

> For example, some implementations may regard SAFI-1 routes and SAFI-4 routes as completely independent and may treat them in a "ships in the night" fashion.

That's how Arista EOS treats them.

> Other implementations may treat the SAFI-1 and SAFI-4 routes for a given prefix as comparable, such that the best route to prefix P is either a SAFI-1 route or a SAFI-4 route but not both.

That would be Cisco IOS.

> Some implementations may allow a single BGP session to carry UPDATEs of both SAFI-1 and SAFI-4; other implementations may disallow this.

Both Cisco IOS and Arista EOS can carry SAFI-1 and SAFI-4 updates over the same BGP session. IOS XR is a bit different -- see the [comment by Fred Cuiller](/2022/03/bgp-labeled-unicast-cisco-ios.html#1105) for more details.

> A BGP speaker may receive a SAFI-4 route over a given BGP session but may have other BGP sessions for which SAFI-4 is not enabled.  In this case, the BGP speaker MAY convert the SAFI-4 route to a SAFI-1 route and then propagate the result over the session on which SAFI-4 is not enabled.  Whether this is done is a matter of local policy.

Cisco IOS automatically converts SAFI-1 route into SAFI-4 route and vice versa. I couldn't find a nerd knob that would configure similar behavior on Arista EOS.

Considering all the implementation differences and potential local policies, how can we ever build a multi-vendor environment using BGP Labeled Unicast? The last paragraph of [Section 5 of RFC 8277](https://datatracker.ietf.org/doc/html/rfc8277#section-5) gives a depressing answer:

> These differences in the behavior of different implementations may result in unexpected behavior or lack of interoperability.  In some cases, it may be difficult or impossible to achieve the desired policies with certain implementations or combinations of implementations.

In other words, _it's broken beyond repair_. I thought we reached the low point of interoperability with SIP or (early) EVPN, but the networking industry never ceases to amaze me.
