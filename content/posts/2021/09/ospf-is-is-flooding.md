---
date: 2021-09-16 07:17:00+00:00
ospf_tag: details
tags:
- OSPF
- IS-IS
title: LSA/LSP Flooding in OSPF and IS-IS
---
[Peter Paluch](https://twitter.com/Peter_Paluch) loves blogging in microchunks on Twitter ;) This time, he [described the differences between OSPF and IS-IS](https://twitter.com/Peter_Paluch/status/1426926700294819845), and gracefully allowed me to repost the explanation in a more traditional format.

---

My friends, I happen to have a different opinion. It will take a while to explain it and I will have to seemingly go off on a tangent. Please have patience. As a teaser, though: The 2Way state between DRothers does not improve flooding efficiency -- in fact, it worsens it.
<!--more-->
On multi-access segments, OSPF introduces the role of DR (and BDR) for two independent reasons:

- The origination of type-2 LSA (LSA2) on behalf of the multi-access segment

- A tight control over LSA flooding to ensure LSDB consistency of all routers on the multi-access segment

These two purposes of DR/BDR are often confused and not treated separately. However, the origination of per-segment LSA2 is a task that exists on its own, and is independent of the task of flooding any LSAs, regardless of who originated them, to the on-segment routers.

It's true that the routers' "mental model" of how exactly the network topology inside an area looks like can get simpler if all multi-access segments with 4 or more routers are represented using LSA2. That is because instead of each of the routers pointing to each other in their LSA1 (resulting in n*(n-1) links for any single segment with n routers), all routers on the segment just point to the network's LSA2 from their LSA1, and the network points back (resulting in 2*n links). This reduces the model's link density and speeds up SPF.

This is the calculation simplification alluded to, and it positively impacts all routers in an area because they have identical LSDB contents. Originating LSA2 on behalf of a multi-access network is one of the DR's tasks in OSPF, also shared by DIS in IS-IS.

In OSPF, however, DR has one more task: It becomes the focal point of disseminating updates (one or more LSAs packaged into one or more LSUs) reliably across multi-access networks. Here, we are not talking about LSA2 originated by the DR but rather about any valid LSA originated by any router in the OSPF domain that has so far been flooded all the way to one of the routers connected to a multi-access network, and needs to be propagated across the multi-access network to the neighbors so that they can flood it further as necessary.

OSPF adopts a control freak approach here: Any update must go through DR. DR must know about the update as soon as possible, and only (B)DR is allowed to tell other neighbors on the multi-access network. DR is also responsible for collecting acks and doing retransmissions.

Also, the OSPF machinery for the initial sync of two newly discovered neighbors is complex (overly so, considering that for a pair of routers, it's used only once before they become Full) -- 3 dedicated states (ExStart, Exchange, Loading) and 2 dedicated packets (DBD, LSR).

Considering this, only neighbors of DR/BDR bother to become Full with them because they are not allowed to exchange updates directly but only with DR/BDR. This way, OSPF enforces that non-(B)DR routers won't accept updates from each other, only from the (B)DR on the segment.

That is why DRother routers stay in 2Way state with each other. Progressing further would force them to do the complex sync and become Full, and then they would be allowed to exchange updates directly, breaking the mandated rule that every update goes through (B)DR.

This way, all updates across a multi-access segment go through the (B)DR, and DR is one of the very first routers there to know, to tell others, and to make sure that others know (through LSAcks, and if needed, doing unicast retransmissions) -- all this for LSDB consistency.

This comes at an expense: If the update arrives to a multi-access segment through a DRother router, it first needs to go to DR/BDR, and DR then sends it back to the same segment to DRothers. The flooding isn't reduced -- it's doubled, and DR is the single point of failure.

In terms of flooding, OSPF's rigid approach complicates matters and the flooding is, in fact, higher than what it would be if all routers were Full with each other. IS-IS chooses a different approach that is much more relaxed, considerably simpler and works just as well.

I'll be happy to elaborate on IS-IS details if there's interest, but for now, let me just summarize: 2Way is a "parking state" for neighbors that by OSPF rules mustn't exchange updates directly. As far as flooding is concerned, DR/BDR concept in fact increases it.
