---
date: 2007-09-08 06:55:00+02:00
tags:
- IP routing
- LAN
title: 'Static routing with Catalyst 3750: and the winner is …'
url: /2007/09/static-routing-with-catalyst-3750-and.html
---
The [Static routing with Catalyst 3750](/2007/09/get-creative-static-routing-with.html) post has generated a lot of good, creative ideas. Some of the proposed solutions were better than the others and some were simply not implementable (but nonetheless, had great creative potential :). Here is my list of the favorites:

**A routing protocol:** as a few of you have rightly pointed out, this is the best choice.

**Aggressive Unidirectional Link Detection (UDLD)**: this is my second favorite, as it\'s a reliable link-level mechanism that will detect a break in the fiber cable ... exactly the right tool for the job.
<!--more-->
**Object tracking and reliable static routes** would also work. This was my initial solution, and it works at least from IOS release 12.2(37)SE.
<!--more-->
**GRE tunneling with GRE keepalives** probably has performance issues (I am not sure GRE is ASIC-switched on Catalyst 3750). The idea is to create a GRE tunnel between IP addresses on the primary fiber link. If the connectivity breaks, but the subnet remains available, the GRE keepalives will detect the failure.

**Spanning tree** will not work. It does not test the two-way connectivity and might actually create a loop (if I stop receiving spanning tree hellos, I might assume the link is connected to a workstation and OK to use).

**Etherchannel and LACP** would most likely fail. If the radio adapters work as switches, so you cannot establish an Etherchannel across the two links. I am also not sure that the PAgP or LACP would detect a unidirectional link when the carrier is present on both ends. Any experience?

**Bidirectional Forwarding Detection (BFD)** is not available on Catalyst 3750 at all (the ISR routers got it as late as IOS release 12.4(15)T). Furthermore, BFD (as implemented in IOS today) detects a *routing protocol neighbor* failure, not an *IP next-hop* failure, so you need to run a routing protocol first (in which case we wouldn\'t be discussing this scenario, as we would have changed the boss, as someone has suggested).
