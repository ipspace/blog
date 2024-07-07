---
title: "Using Unequal-Cost Multipath to Cope with Leaf-and-Spine  Fabric Failures"
date: 2021-04-20 07:15:00
tags: [ fabric, design ]
series: [ UCMP, dcbgp ]
dcbgp_tag: interesting
---
Scott submitted an interesting the comment to my *[Does Unequal-Cost Multipath (UCMP) Make Sense](/2021/02/does-ucmp-make-sense/)* blog post:

> How about even Large CLOS networks with the same interface capacity, but accounting for things to fail; fabric cards, links or nodes in disaggregated units. You can either UCMP or drain large parts of your network to get the most out of ECMP.

Before I managed to write a reply (sometimes it takes months while an idea is simmering somewhere in my subconscious) [Jeff Tantsura](https://www.linkedin.com/in/jeff-tantsura/) pointed me to an [excellent article by Erico Vanini](https://www.usenix.org/conference/nsdi17/technical-sessions/presentation/vanini) that describes the types of asymmetries you might encounter in a leaf-and-spine fabric: an ideal starting point for this discussion.
<!--more-->
## Defining the Problem

Leaf-and-spine fabrics are usually *symmetrical* -- there's an equal number of paths (and equal number of hops) to get from any edge to any other edge. 

{{<figure src="/2021/04/ucmp-symmetry.png" caption="Looks symmetrical, right?">}}

Due to that property, it's mostly OK to use simple equal-cost multipath (ECMP) on leaf switches to get decent traffic distribution (ignoring for the moment the challenges of long-lived elephant flows).

Traditional routing protocols + ECMP can adjust to many failures in well-designed leaf-and-spine fabrics, and I haven't found a scenario in a simple leaf-and-spine fabric where a node failure would result in asymmetry. Answering the same question for multi-stage fabrics is left as an exercise for the reader.

There are, however, two link failure scenarios that require special attention:

* Failure of one link in a leaf-to-spine bundle
* Impact of link failures on third-party traffic.

## Link-in-a-Bundle Failure

Imagine the following fabric with two parallel links connecting leafs and spines:

{{<figure src="/2021/04/ucmp-bundle.png" caption="Link-in-a-bundle failure">}}

When the L2-S2 link fails, we could get into one of the following scenarios (for more details, watch the *[Route Summarization and Link Aggregation](https://my.ipspace.net/bin/get/Clos/7.13%20-%20Route%20Summarization%20and%20Link%20Aggregation.mp4?doccode=Clos)* video from [*Leaf-and-Spine Fabric Architectures*](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures):

**LAG between L2 and S2** with **bandwidth and routing cost adjustment** based on the number of links in the bundle. The moment a bundle member fails, the cost of the LAG link goes up, and nobody is using it anymore. UCMP would be a solution for this scenario.

**LAG between L2 and S2** without bandwidth or routing cost adjustment based on the number of links in the bundle. UCMP is of no use, as a member link failure doesn't change a thing from the routing protocol perspective.

**Multiple routing adjacencies between L2 and S2.** The cost between L2 and S2 stays the same no matter how many routing adjacencies you have between the two nodes. UCMP cannot help you.

In theory, you could adjust link state routing protocols to compute end-to-end cost differently when there's more than one routing adjacency between two routers, or adjusts distance vector routing protocols to report lower cost when the next hop is reachable over multiple links, but no-one seems to be "brave" enough to do anything along these lines. Well, almost no-one (see below).

In practice, I don't think that handling this particular failure scenario is worth the extra complexity. You might disagree and deeply care about this problem -- put your money where your mouth is and buy two more spine switches instead of burdening everyone else with more complex (and buggy) routing code. Problem solved.

## When There's a Problem, There's a BGP Solution

Of course we can solve the above problem with BGP. What else did you expect? 

Imagine you're [(mis)using EBGP as your IGP](https://www.ipspace.net/Data_Center_BGP/), and your vendor:

* Tweaked their BGP implementation to propagate [DMZ Link Bandwidth extended community](https://tools.ietf.org/html/draft-ietf-idr-link-bandwidth-07) across EBGP sessions (described in an [informational draft](https://tools.ietf.org/html/draft-mohanty-bess-ebgp-dmz-00))
* Tweaked their handling of DMZ Link Bandwidth to advertise cumulative downstream bandwidth
* Tweaked their handling of EBGP ECMP to implement UCMP based on DMZ Link Bandwidth attribute received from downstream EBGP neighbors belonging to different autonomous systems (requiring as-path-relax feature, but almost everyone is doing that anyway).

Such an implementation would neatly solve the above problem. I described Arista EOS implementation years ago somewhere in the [*Data Center Fabric Architectures*](https://www.ipspace.net/Data_Center_Fabrics) webinar. I have no idea whether they're still doing that... but then no network OS feature ever disappears[^1]. Pointers to other implementations are highly welcome.

{{<figure src="/2021/04/ucmp-arista-dmz-bandwidth.png" caption="Arista's aggregation of DMZ Link Bandwidth (June 2016)">}}

## Third-Party Link Failure

Now let's consider a more interesting scenario -- simple leaf-and-spine fabric with a single link failure:

{{<figure src="/2021/04/ucmp-third-party-failure.png" caption="Third-party link failure">}}

Because there's a single path between L1 and L3, the link between S1 and L3 becomes more congested than the link between S2 and L3. If L2 uses ECMP between S1 and S2, half of its traffic encounters a more-congested link.

There's nothing any routing protocol I'm aware of can do in this scenario, and UCMP is of no help either. Routing protocols are concerned with *downstream* paths, and the problem is caused by an independent *upstream* path.

## Long Story Short

I don't think asymmetries in leaf-and-spine fabrics are worth spending any sleepless nights on... unless of course you have frequent failures that take weeks to fix, but then you have a bigger problem than lack of UCMP.

Also note that all of the problems described in this blog post diminish if you use four or eight spine switches instead of two (plus you increase the resiliency of your fabric). The proof is left as an exercise for the reader.

For more details, watch the [*Leaf-and-Spine Fabric Architectures*](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures), now with brand-new *[Using OSPF in Leaf-and-Spine Fabrics](https://my.ipspace.net/bin/list?id=Clos#L3_SINGLE)* section.

[^1]: OK, AppleTalk did disappear from Cisco IOS decades after I've last seen it in the wild. X.25 is probably still there.
