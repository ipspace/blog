---
date: 2020-04-21 06:45:00+00:00
dcbgp_tag: abstract
series:
- bgp_nh
- dcbgp
tags:
- BGP
- IP routing
title: Can We Trust BGP Next Hops (Part 2)?
---
Two weeks ago I started with a seemingly simple question:

> If a BGP speaker R is advertising a prefix A with next hop N, how does the network know that N is actually alive and can be used to reach A?

... and [answered it for the case of directly-connected BGP neighbors](https://blog.ipspace.net/2020/04/can-we-trust-bgp-next-hops-part-1.html) (TL&DR: Hope for the best).

Jeff Tantsura [provided an EVPN perspective](https://blog.ipspace.net/2020/04/next-hop-vtep-reachability-evpn.html), starting with "_the common non-arguable logic is reachability != functionality_".

Now let's see what happens when we add route reflectors to the mix. Here's a simple scenario:
<!--more-->
{{<figure src="/2020/04/IBGP-RR.jpg" caption="BGP next hops when using an IBGP route reflector" >}}

Assuming we're running IBGP sessions between loopback interfaces, and all AS edge routers use **next-hop-self** so all the BGP next hops within the AS are the loopback interfaces, can we can trust that the advertised next hops are safe for packet forwarding? **TL&DR: Heck NO.**

### In Trust We Trust

In our scenario R1 advertises subnet A with next hop L1, the update is sent to R2 and reflected to R3. Here's the chain of implicit trust that leads to R3 selecting L1 as the next hop for A:

* R2 has to trust that R1 did the right thing, can reach A, and can forward packets to A (we discussed this part in the [last blog post](https://blog.ipspace.net/2020/04/can-we-trust-bgp-next-hops-part-1.html)).
* R3 has to trust that R2 (the route reflector) did its job correctly;
* R3 has to have L1 in its routing table;
* R3 has to trust that the intra-AS routing protocol did its job and calculated the correct next hop to reach L1;
* R3 has to trust that all the intermediate nodes on the IGP-computed path between itself and R1 know how to forward the traffic toward A (not just toward L1).

In the _[BGP over MPLS core](https://my.ipspace.net/bin/get/MPLS101/SR1%20-%20MPLS-Based%20Transport%20Core.mp4?doccode=MPLS101)_ design the situation is slightly different. After verifying that L1 is in R3's routing table, R3 has to:

* Hope that it has an LSP toward L1 in its LFIB, or that everyone in the forwarding path knows how to reach A.
* Having an LSP toward L1, trust that the LSP is not broken, and that everyone on the LSP does proper label swapping.

### What could possibly go wrong?

In the [last blog post](https://blog.ipspace.net/2020/04/can-we-trust-bgp-next-hops-part-1.html) I mentioned two things that can go wrong in a directly-connected BGP scenario:

* Access control lists that would drop traffic toward A;
* [RIB-to-FIB](https://blog.ipspace.net/2010/09/ribs-and-fibs.html) mismatch (lovingly called ASIC wedgie). Obviously that's not just a myth, managing that mismatch was presented as one of the first use cases for [Cisco's Network Assurance Engine](https://techfieldday.com/appearance/cisco-network-assurance-engine-presents-at-tech-field-day-extra-at-cisco-live-europe/).

Let's add a few other minor details to the mix:

* [Best path selection on BGP route reflectors could generate a persistent loop](https://blog.ipspace.net/2013/10/can-bgp-route-reflectors-really.html).
* Ever heard of BGP Wedgies? There's a [whole RFC on the topic](https://tools.ietf.org/html/rfc4264).
* Then there's [BGP-to-IGP synchronization](https://blog.ipspace.net/2017/08/synchronizing-bgp-and-ospf-or-ospf-and.html) and [IGP-to-LDP synchronization](https://blog.ipspace.net/2011/11/ldp-igp-synchronization-in-mpls.html).
* Finally, you could get corrupted LFIB anywhere on the path.

For even more BGP fun, read [Considerations in Validating the Path in BGP](https://tools.ietf.org/html/rfc5123) (RFC 5123).

After considering all that, do you really care whether R1 advertises a prefix with the next hop equal to the source IP address of its IBGP session, or with a third-party next hop that it believes works?

### Back to EVPN

I'm guessing that the [original question](https://blog.ipspace.net/2020/02/the-evpnbgp-saga-continues.html#3256817850847857930) that triggered this series of blog posts had a hidden assumption (and I apologize in advance if I got it wrong):

> In the EBGP-only data centers, it's better to run IBGP between loopback interfaces of leaf- and spine switches than to advertise loopback VTEPs over EBGP sessions on leaf-to-spine links, because we can rely on direct next hop (loopback VTEP advertised over IGBP between loopbacks) more than on third-party next hop (loopback VTEP advertised as third-party next hop over EBGP session).

Considering everything I wrote above, _reachability != functionality_, and the myriad things that can go wrong, I would consider this a minor detail, and the least of your worries. Also, remember the conclusion of my previous blog post on this topic: "_You might as well stop bothering and get a life, networks usually work reasonably well._"

{{<note info>}}If this section sounds like Latin (and I agree it's convoluted), [start with this article](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics), and explore my [previous EVPN blog posts](https://blog.ipspace.net/tag/evpn.html). I'm getting tired of repeating myself and walking in circles.{{</note>}}

### More to Explore

I'll slowly get to the routing protocols in the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar (parts of it are available with [free ipSpace.net subscription](https://www.ipspace.net/Subscription/Free)), and we have tons of content on [leaf-and-spine fabric designs](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) (including routing protocol selection) and [EVPN](https://www.ipspace.net/EVPN_Technical_Deep_Dive). 

You might also want to explore [other BGP resources](/kb/tag/BGP) we've created in the last decade and a half.
