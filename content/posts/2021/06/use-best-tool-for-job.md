---
date: 2021-06-03 07:00:00+00:00
networking-fundamentals_tag: deep
tags:
- IP routing
- networking fundamentals
title: 'Routing Protocols: Use the Best Tool for the Job'
---
When I wrote about my sample OSPF+BGP hands-on lab on LinkedIn, someone couldn't resist asking:

> I’m still wondering why people use two routing protocols and do not have clean redistribution points or tunnels.

Ignoring for the moment the fact that he missed the point of the blog post (completely), the idea of "*using tunnels or redistribution points instead of two routing protocols*" hints at the potential applicability of RFC 1925 rule 4.
<!--more-->
As anyone who ever had to configure two-way route redistribution knows, it's one of the hardest things to get right and one of the most "exciting" things to troubleshoot on Sunday at 2 AM. It's so bad that I recommended [running BGP in parallel with OSPF](https://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN) to anyone who had to deal with MPLS Service Providers offering BGP as the only PE-CE routing protocol.

Coming back to the original question: does it make sense to run BGP on top of OSPF instead of just using one or the other? As always, the correct answer is "it depends," this time on (A) what problem you're trying to solve and (B) what the best tools are to solve that problem.

The "[two napkins](https://computerhistory.org/blog/the-two-napkin-protocol/)" team designed BGP to be a global endpoint reachability protocol. It does that job wonderfully and scales to millions of routes exchanged between tens of thousands of autonomous systems. It was, however, never designed to be fast or to be focused on topology discovery.

OSPF is just the opposite. It auto-discovers network topology, reacts (relatively) quickly to changes in network topology, and does its best to propagate the news as soon as possible. Compare that to the conservative approach taken by BGP:

* Receive the changes
* Recalculate the local routing table
* Compose the outbound update based on the changes in the local routing table
* Inform the upstream neighbors.

Why don't we use OSPF everywhere? It can't carry too many routes ([redistributing the BGP table into OSPF is great fun](/2020/10/redistributing-bgp-into-ospf/)), and you cannot use it to implement a hop-by-hop policy -- all routers in the same area unconditionally share the same information.

But didn't the hyperscalers prove that you can build [BGP-only data center fabrics](https://www.ipspace.net/Data_Center_BGP/)? Sure they did, and Petr Lapukhov [had good reasons](https://datatracker.ietf.org/doc/html/rfc7938#section-2.5) to build a BGP-only data center fabric at Microsoft. You can do the same, but it's not trivial unless you're using an operating system designed for that particular use case (Cumulus Linux with FRR). Does it make sense? Maybe not -- [you're not Microsoft or Facebook](/2018/05/is-ospf-or-is-is-good-enough-for-my/), and [your network might not have the same scaling problems](/2021/05/worth-reading-rethinking-bgp-data-center/), regardless of [what the vendors would like you to believe](/2017/11/bgp-as-better-igp-when-and-where/).

Add "minor" details like vendors that love running EVPN over IBGP, and all of a sudden, you're in the [twisted IBGP-over-EBGP territory](/2020/02/the-evpnbgp-saga-continues/) just because someone insisted on not using two routing protocols where they should have.

There's a reason every craftsmaster has a toolbox full of various weird (sometimes even homemade) tools -- there's the best tool for every job. The difference between a craftsmaster and an amateur wannabe trying to solve everything with hammer (or a Swiss Army Knife) is that one of them thinks about the tool to use for every job they face[^1]. It's only in networking that some people think using a single protocol to solve every challenge they face makes them heroes.

[^1]: They both know what the best tool for the job is though. One of them would always pick a hammer.

### More to Explore

I did a series of podcasts with routing protocol gurus trying to figure out whether or not BGP is the best answer when looking for a data center routing protocol:

* [Data Center Routing with RIFT](/2018/03/data-center-routing-with-rift-on/) with Dr. Tony Przygienda;
* [OpenFabric](/2018/04/openfabric-with-russ-white-on-software/) with Russ White;
* [Is BGP Good Enough](/2018/08/is-bgp-good-enough-with-dinesh-dutt-on/) with Dinesh Dutt

Prefer webinars over podcasts? Start with *[Routing Protocols](https://my.ipspace.net/bin/list?id=Net101#ROUTING)* part of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)*, and explore the best ways to [use BGP and OSPF](https://my.ipspace.net/bin/list?id=Clos#L3_SINGLE) in [leaf-and-spine fabrics](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) and in [EVPN networks](https://www.ipspace.net/EVPN_Technical_Deep_Dive).

Need even more information? Explore our extensive [BGP in Data Center Fabrics](/series/dcbgp/) series.

