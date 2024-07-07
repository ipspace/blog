---
date: 2013-10-09 07:37:00+02:00
dcbgp_tag: sdn
series:
- dcbgp
tags:
- MPLS
- SDN
- data center
- BGP
title: 'Exception Routing with BGP: SDN Done Right'
url: /2013/10/exception-routing-with-bgp-sdn-done/
---
One of the holy grails of data center SDN evangelists is controller-driven traffic engineering (throwing more leaf-and-spine bandwidth at the problem might be cheaper, but definitely not sexier). Obviously they don't call it traffic engineering as they don't want to scare their audience with MPLS TE nightmares, but the idea is the same.

Interestingly, you [don't need new technologies](/2013/04/the-many-paths-to-sdn/) to get as close to that holy grail as you wish; Petr Lapukhov got there with a 20 year old technology -- BGP.
<!--more-->
### The Problem

I'll use a well-known suboptimal network to illustrate the problem: a ring of four nodes (it could be anything, from a [monkey-designed fabric](/2012/04/monkey-design-still-doesnt-work-well/), to a [stack of switches](/2012/11/stackable-data-center-switches-do-math/)) with heavy traffic between nodes A and D.

{{<figure src="/2013/10/s400-BGP_SDN_Topology.png" caption="A suboptimal data center fabric">}}

In a shortest-path forwarding environment you cannot spread the traffic between A and D across all links (although you might get close with a large bag of tricks).

Can we do any better with a controller-based forwarding? We definitely should. Let's see how we can tweak BGP to serve our SDN purposes.

### Infrastructure: Using BGP as IGP

If you want to use BGP as the information delivery vehicle for your SDN needs, you MUST ensure it's the highest priority routing protocol in your network. The easiest design you can use is a BGP-only network using BGP as a more scalable (albeit a bit slower) IGP. [EBGP is better than IBGP](/2011/08/ibgp-or-ebgp-in-enterprise-network/) as it doesn\'t need an underlying IGP to get reachability to BGP next hops.

{{<figure src="/2013/10/s400-BGP_SDN_EBGP.png" caption="Build EBGP sessions between data center switches">}}

### BGP-Based SDN Controller

After building a BGP-only data center, you can start to insert controller-generated routes into it: establish an IBGP session from the controller (cluster) to every BGP router and use higher local preference to override the EBGP-learned routes. You might also want to [set **no-export** community on those routes](/2012/10/setting-no-export-bgp-community/) to ensure they aren't leaked across multiple routers.

{{<figure src="/2013/10/s520-BGP_SDN_Controller.png" caption="Add a BGP controller to the mix">}}

Obviously I'm handwaving over lots of moving parts -- you need topology discovery, reliable next hops, and a few other things. If you really want to know all those details, listen to the [Packet Pushers podcast](http://packetpushers.net/show-164-cool-or-hot-lapukhov-nkposongs-bgp-sdn/) where we deep dive around them.

### Results: Unequal-Cost Multipath

The SDN controller in our network could decide to split the traffic between A and D across multiple paths. All it has to do to make it work is to send the following IBGP routing updates for prefix D:

-   Two identical BGP paths (with next hops B and D) to A (to ensure the BGP route selection process in A uses BGP multipathing);
-   A BGP path with next hop C to B (B might otherwise send some of the traffic for D to A, resulting in a forwarding loop between B and A).

{{<figure src="/2013/10/s520-BGP_SDN_Flow.png" caption="Controller-driven unequal-cost multipath">}}

You can get even fancier results if you run MPLS in your network (hint: read the [IETF draft on remote LFA](http://tools.ietf.org/html/draft-ietf-rtgwg-remote-lfa-02) to get a few crazy ideas).

#### More information

-   [Routing Design for Large-Scale Data Centers](http://www.nanog.org/meetings/nanog55/presentations/Monday/Lapukhov.pdf) (Petr's presentation @ NANOG 55)
-   [Use of BGP for Routing in Large-Scale Data Centers](http://tools.ietf.org/html/draft-lapukhov-bgp-routing-large-dc-06) (IETF draft)
-   [Centralized Routing Control in BGP Networks](http://tools.ietf.org/html/draft-lapukhov-bgp-sdn-00) (IETF draft)
-   [Cool or Hot? Lapukhov + Nkposong's BGP SDN](http://packetpushers.net/show-164-cool-or-hot-lapukhov-nkposongs-bgp-sdn/) (Packet Pushers Podcast)
