---
date: 2018-09-27 09:05:00+02:00
dcbgp_tag: abstract
evpn_tag: design
series:
- valley-free
- dcbgp
tags:
- design
- data center
- fabric
- BGP
- EVPN
title: Implications of Valley-Free Routing in Data Center Fabrics
url: /2018/09/implications-of-valley-free-routing-in/
---
As I explained in a [previous blog post](/2018/09/valley-free-routing-in-data-center/), most leaf-and-spine best-practices (as in: what to do if you have no clue) use [BGP as the IGP routing protocol](https://www.ipspace.net/Data_Center_BGP/BGP_Fabric_Routing_Protocol) ([regardless of whether it’s needed](/2018/05/is-ospf-or-is-is-good-enough-for-my/)) with the [same AS number shared across all spine switches](https://www.ipspace.net/Data_Center_BGP/Autonomous_Systems_and_AS_Numbers) to implement valley-free routing.

This design has an interesting consequence: when a link between a leaf and a spine switch fails, they can no longer communicate.
<!--more-->
For example, when the link between L1 and C1 in the following diagram fails, there’s no connectivity between L1 and C1 as there’s no valley-free path between them.

{{<figure src="/2018/09/s550-VF_DC_LinkFailure.png" caption="Link failure results in connectivity loss due to lack of valley-free path">}}

No big deal, right? After all, we built the data center fabric to exchange traffic between external devices attached to leaf nodes. Well, I hope you haven’t connected a firewall or load balancer straight to the spine switches using MLAG or a similar trick.

**Lesson learned**: connect all external devices (including network services devices) to leaf switches. Spine switches should provide nothing more than intra-fabric connectivity.

{{<note info>}}[ipSpace.net subscribers](https://www.ipspace.net/Subscription) can find more details in [leaf-and-spine fabrics](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.{{</note>}}

There’s another interesting consequence. As you might know, some vendors love [designs that use IBGP or EBGP EVPN sessions between loopback interfaces of leaf and spine switches on top of EBGP underlay](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics).

Guess what happens after the L1-C1 link failure: the EVPN session between loopback interfaces (regardless of whether it’s an IBGP or EBGP session) is lost no matter what because L1 cannot reach C1 (and vice versa) anyway.

{{<figure src="/2018/09/s550-VF_EVPN_Failure.png" caption="EVPN session failure following a link loss">}}

**Inevitable conclusion**: all the [grand posturing](/2020/02/the-evpnbgp-saga-continues/) explaining how EVPN sessions between loopback interfaces running on top of underlay EBGP are so much better than EVPN running as an additional address family on the directly-connected EBGP session *in a typical data center leaf-and-spine fabric* is plain *merde* (pardon my French).

Even worse, I’ve seen a vendor-produced design that used:

-   EBGP in a small fabric that would work well enough with OSPF for the foreseeable future;
-   IBGP EVPN sessions between loopback interfaces of leaf and spine switches;
-   Different AS numbers on spine switches to make it all work, turning underlay EBGP into a TCP version of RIPv2 using AS path length as the hop count.

As I said years ago: [the road to broken design is paved with great recipes](/2011/08/road-to-complex-designs-is-paved-with/).

**Lesson learned**: whenever evaluating a design, consider all possible failure scenarios.

Don’t get me wrong. There might be valid reasons to use IBGP EVPN sessions on top of EBGP underlay. There are valid reasons to use IBGP route reflectors implemented as VNF appliances for scalability… but the designs promoted by most networking vendors these days make little sense once you figure out how routing really works.

### For the Few People Interested in the Red Pill

If you want to know more about leaf-and-spine fabrics (and be able to figure out where exactly the vendor marketers cross the line between unicorn-colored reality and plain bullshit), start with the [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) and [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinars (both are part of [Standard ipSpace.net subscription](https://www.ipspace.net/Subscription)).

Finally, when you want to be able to design more than just the data center fabrics, check out the [Building Next-Generation Data Center online course](https://www.ipspace.net/Building_Next-Generation_Data_Center).
