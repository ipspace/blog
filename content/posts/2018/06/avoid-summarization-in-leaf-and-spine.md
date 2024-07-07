---
date: 2018-06-11 08:39:00+02:00
dcbgp_tag: design
series:
- dcbgp
series_weight: 650
tags:
- design
- data center
- fabric
- BGP
title: Avoid Summarization in Leaf-and-Spine Fabrics
url: /2018/06/avoid-summarization-in-leaf-and-spine/
---
I got this design improvement suggestion after publishing [*When Is BGP No Better than OSPF*](/2018/06/is-ebgp-really-better-than-ospf-in-leaf/) blog post:

> Putting all the leafs in the same ASN and filtering routes sent down to the leafs (sending just a default) are potential enhancements that make BGP a nice option.

[Tony Przygienda](https://www.linkedin.com/in/dr-tony-przygienda-018501/) quickly wrote a one-line rebuttal: "*unless links break ;-)"*
<!--more-->
{{<note warn>}}This is a generic blog post written for data center engineers building fabrics with less than few hundred switches. If you're building a larger fabric, don't look for recipes on the Internet. Your fabric will be grateful.{{</note>}}

We covered the drawbacks of summarization in leaf-and-spine fabrics in great details in the [*Layer-3 Fabrics with Non-Redundant Server Connectivity*](https://my.ipspace.net/bin/list?id=Clos#L3_SINGLE) part of [*Leaf-and-Spine Fabrics Architectures*](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar and [*Designing and Building Leaf-and-Spine Fabrics*](http://www.ipspace.net/Designing_and_Building_Data_Center_Fabrics) online course. Here's a short summary of that discussion.

### The Problem

Imagine the design proposed by my reader:

{{<figure src="/2018/06/s1600-Default-Route-Setup.png" caption="Using a default route in a data center fabric">}}

Spines announce a default route (or some other summary route) to the leaves, and the prefixes announced by leaves are not propagated to other leaves.

Now image the L1-S1 link fails. No routing update is sent to other leaves, and they continue sending the traffic as they did before. For example, L4 will (on average) send 50% of its traffic for L1 toward S1... where the traffic will be dropped because S1 has no route for prefixes advertised by L1.

{{<figure src="/2018/06/s1600-Default-Route-Failure.png" caption="A link failure creates a black hole">}}

The scenario (although in a slightly different format) should be familiar to anyone who had to deal with inter-area summarization in redundantly-built OSPF networks.

### Can We Fix It?

Sure. You can add links between spine switches, add a superspine layer, or use RIFT (not available for production deployment at the time this blog post was written) that does selective deaggregation following a link failure -- more details in Software Gone Wild [Episode 88](/2018/03/data-center-routing-with-rift-on/).

Let's focus on the challenges of the inter-spine links. Life is simple if we have just two spines: we add a link between them and run IBGP session across that link.

{{<figure src="/2018/06/s1600-Default-Route-Packet-Flow.png" caption="Adding inter-spine links">}}

That link (as [Oliver Herms](https://www.linkedin.com/in/oliver-herms-7974b091/) pointed out in a LinkedIn discussion) also increases the fabric resiliency. Without it, two link failures (example: Spine1-to-Leaf1 and Spine2-to-Leaf2) could partition the fabric.

What about larger fabrics with more than two spines. The design quickly gets trickier:

**Topology**: Will you create a full mesh between spines, or a ring between them? What will you do when you go from two spines to four or eight spines? Also, you no longer need the inter-spine link for resiliency.

**Routing**: Spines have to exchange routes across inter-spine links. Will you use IBGP or will you go for some crazy schizophrenic idea of running EBGP between routers in the same autonomous system by faking AS numbers on both ends of the session? If you go for IBGP, will you add IGP to the mix, or will you tweak next hops on IBGP sessions? Will some spines become route reflectors or will you have a full-mesh of IBGP sessions?

Think again. Is the extra complexity really worth it? Or as Russ White would say "*if you haven't identified the tradeoffs, you haven't looked hard enough*".

### Is It Worth the Effort?

Control-plane traffic (BGP updates) is negligible compared to the usual leaf-to-spine bandwidth. Control-plane CPU in data center switches is usually not involved in packet forwarding, so the CPU has all the time in the world to process BGP updates. The number of prefixes advertised in a data center fabric is typically low.

So what exactly are we trying to optimize? The only reason I could see for summarization between spines and leaves is forwarding table size on leaves. Modern data center switches shouldn't have that problem in most deployments -- for more details on unified forwarding tables (UFT) and typical table sizes in data center switches see [Data Center Fabric Architectures](http://www.ipspace.net/Data_Center_Fabrics) webinar, in particular the [UFT Technology Overview](https://my.ipspace.net/bin/list?id=DCFabric#TECHNOLOGY) video.

There might be an interesting edge case where you'd need lots of MAC and ARP entries on leaf switches, so you'd go for small IPv4 forwarding table... but even the host-focused UFT profile on Broadcom's Trident-2 has 16.000 IPv4 prefixes (and 288.000 MAC/ARP entries). Apart from that, I'd stick with the simplest possible design without any form of route summarization.
