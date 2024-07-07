---
date: 2012-11-23 07:06:00+01:00
eigrp_tag: basic
tags:
- EIGRP
title: EIGRP Loop Prevention Logic
url: /2012/11/eigrp-loop-prevention-logic/
---
Hamid sent me the following question:

> I have already memorized (bad idea, BTW) that a loop can occur if FD < RD. Could you please tell me how a loop could occur assuming FD < RD and we ignore the feasibility condition.

I'll use a simple three-router network (see the following diagram) to illustrate why EIGRP cannot figure out whether an alternate more expensive path could lead to a loop or not.
<!--more-->
{{<figure src="/2012/11/s400-EIGRP_baseline.png">}}

Based on the link costs (I'm using scalar metrics for simplicity), C advertises the LAN IP prefix with cost=5. B adds its own incoming link cost (12), reporting the total cost of 17 to A (RD = 17).

A receives a similar update from C and adds its incoming cost (10). The total cost of getting from A to LAN prefix behind C is 15 (FD = 15).

{{<figure src="/2012/11/s400-EIGRP_update.png">}}

However, A does not know whether B has an alternate path to C or whether it reports the path through A back to A.

Assuming EIGRP split horizon is disabled on B (which might be required for NBMA networks like DMVPN), B could increase the total cost to C and report the increased cost back to A.

{{<figure src="/2012/11/s400-EIGRP_loop.png">}}

We know that's not the case because we can see the whole topology of the network. A doesn't have that much visibility (that's the main difference between EIGRP and OSPF); the only safe course of action it can take is not to use alternate paths with RD > FD.
