---
date: 2021-06-17 06:04:00+00:00
dcbgp_tag: newrp
series:
- dcbgp
tags:
- data center
- BGP
- design
title: Questions about BGP in the Data Center (with a Whiff of SRv6)
---
Henk Smit left numerous questions in a comment referring to the [Rethinking BGP in the Data Center](/2021/05/worth-reading-rethinking-bgp-data-center/) presentation by Russ White:

> In Russ White's presentation, he listed a few requirements to compare BGP, IS-IS and OSPF. Prefix distribution, filtering, TE, tagging, vendor-support, autoconfig and topology visibility. The one thing I was missing was: scalability.

I noticed the same thing. We kept hearing how BGP scales better than link-state protocols (no doubt about that) and how you couldn't possibly build a large data center fabric with a link-state protocol... and yet this aspect wasn't even mentioned.
<!--more-->
> When I read about BGP-in-DC for the first time, a few years ago, I remember people claiming that IS-IS couldn't handle the flooding, when you have so many routers in your network. And the duplicate flooding was unsustainable when you have lots of neighbors (>=64?). But Russ didn't mention scalability at all. On the other hand, we have 4 current drafts to improve IS-IS flooding (dynamic flooding, congestion control, proxy-area and 8-level-hierarchy).

> So my question is: do people still think IS-IS doesn't scale for large DCs? And if so, can anyone give me rough numbers where things go wrong? How many routers ? How many neighbors per router? Are we talking 10k routers in an area/domain? 100k? Why are areas not feasible? Anyone who has ever done any real performance measurements? (Not easy, I think). I'd love to hear what people think (less what rumors people heard from others). I understand that these number vary largely per implementation, but I'm still interested.

I tried to get answers to very similar questions three years back and did a series of podcasts on the topic including:

* [Data Center Routing with RIFT](/2018/03/data-center-routing-with-rift-on/) with Dr. Tony Przygienda
* [OpenFabric](/2018/04/openfabric-with-russ-white-on-software/) with Russ White
* [Is BGP Good Enough](/2018/08/is-bgp-good-enough-with-dinesh-dutt-on/) with Dinesh Dutt.

What I got were vague statements from Tony and Russ effectively saying "_you shouldn't have a problem until you get to an area with hundreds of switches_" and Dinesh saying "_very large fabrics running OSPF work just fine if you do your homework_". 

I might have a cynical conclusion or two, but I'll try to stay diplomatic.

> I would imagine my personal favorite DC design would be: 1) IS-IS for the underlay. Easy configuration. 2) EVPN/BGP for the overlay. Scales very well. 3) segment-routing in the data-plane. You can replace VXLAN, you can do TE if you want, etc.

That's more-or-less what I've been saying for years (excluding segment routing ;)... and of course nobody listens, least of all vendors on a lemming run toward ever-more-convoluted BGP-over-BGP designs.

> Or is segment-routing hardware still considered too expensive for large-scale DCs?

SR-MPLS is implementable on any decent merchant silicon ASIC -- just take a look at Arista EOS. Most merchant silicon supported MPLS (with some limitations) a decade ago, and as hyperscalers moved WAN forwarding decisions to edge web proxies instead of WAN routers, I'm positive at least some of them use MPLS forwarding at the WAN edge.

SRv6 is a different story. Very few merchant ASICs support it (apart from _anything can be done with programmable silicon_ fairy tales). Jericho2c+ seems to be one of the exceptions... but it started _sampling_ last September, and we have no idea what its SRv6 limitations might be. Has anyone seen it in a shipping product? Are you aware of any other merchant silicon SRv6 implementation and their limitations (segment stack depth comes to mind)? Comments are most welcome!
