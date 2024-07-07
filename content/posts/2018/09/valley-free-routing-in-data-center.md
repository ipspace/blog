---
date: 2018-09-17 07:48:00+02:00
dcbgp_tag: abstract
series:
- valley-free
- dcbgp
tags:
- design
- data center
- BGP
title: Valley-Free Routing in Data Center Fabrics
url: /2018/09/valley-free-routing-in-data-center/
---
You might have noticed that almost every *[BGP as Data Center IGP](https://www.ipspace.net/Data_Center_BGP)* design uses [the same AS number on all spine switches](https://www.ipspace.net/Data_Center_BGP/Autonomous_Systems_and_AS_Numbers) (there are exceptions coming from people who use BGP as RIP with AS-path length serving as hop count… but let’s not go there).

There are two reasons for that design choice:
<!--more-->
-   Default BGP AS-path filters immediately stop path hunting after a link failure;
-   The same default filters give you [valley-free](/2018/09/valley-free-routing/) (or [non-zigzag](/2018/09/repost-tony-przygienda-on-valley-free/)) routing – traffic between two leaf switches never traverses another leaf switch, making traffic flows and link utilization way more predictable.

We covered the drawbacks of path hunting in the [Layer-3 fabrics section](https://my.ipspace.net/bin/list?id=Clos#L3_SINGLE) of [Leaf-and-Spine Fabrics](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar… but what about the benefits or drawbacks of valley-free traffic flow?

Imagine a simple leaf-and-spine fabric that experienced a link failure.

{{<figure src="/2018/09/s400-VF_DC_LinkFailure.png" caption="Link failure in a leaf-and-spine fabric">}}

If the fabric routing protocol design isn’t valley-free, C1 finds numerous alternate paths to L1: (L2 =&gt; C2, L3 =&gt; C2, L4 =&gt; C2), resulting in an explosion of forwarding table on C1, and plenty of routing protocol noise… but there’s no change in end-to-end forwarding – the path through the valley is longer than the direct path through C2. So far so good.

What about two link failures:

{{<figure src="/2018/09/s400-VF_DC_LinkFailure_2.png" caption="Double link failure">}}

In this case, a path through a valley is the only way to get from L1 to L4, so it seems like valley-free routing is not a good idea.

As always, there’s a tradeoff, and if you haven’t identified it, you haven’t looked hard enough. If you have a fabric with two spines, valley-free routing breaks connectivity after two failures… but then you might be [better off using OSPF anyway](/2018/05/is-ospf-or-is-is-good-enough-for-my/). As an alternative, you could [use a spine-to-spine link](/2018/06/avoid-summarization-in-leaf-and-spine/) to increase failure resilience, but that increases routing complexity.

It’s really hard to implement valley-free routing with OSPF anyway. More about that in another blog post.

In larger fabrics you’d probably want to use four spine switches, and you need four strategically-placed failures to break connectivity with valley-free routing, so it’s much better to focus on routing protocol convergence than on fabric partitioning.

**Takeaway [recipe](/2011/08/road-to-complex-designs-is-paved-with/):** If you have two spine switches, use OSPF or IS-IS (instead of turning BGP into RIP). If you have more than two spine switches and you think you need BGP as the underlay routing protocol, use the same AS number on all spines to get valley-free routing.

ipSpace.net subscribers can find way more details in [Leaf-and-Spine Fabrics webinar](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures); if you want to add interactive discussions and mentoring to your learning process, go for the [Building Next-Generation Data Centers](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
