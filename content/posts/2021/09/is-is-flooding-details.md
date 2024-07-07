---
title: IS-IS Flooding Details
date: 2021-09-22 07:24:00
tags: [ IS-IS ]
---
Last week I published an [unrolled version of Peter Paluch's explanation of flooding differences between OSPF and IS-IS](/2021/09/ospf-is-is-flooding/). Here's the second part of the saga: [IS-IS flooding details](https://twitter.com/Peter_Paluch/status/1430270978207145991) (yet again, reposted in a more traditional format with Peter's permission).

---
In IS-IS, DIS[^1] is best described as a "baseline benchmark" -- a reference point that other routers compare themselves to, but it does not sit in the middle of the flow of updates (Link State PDUs, LSPs).

[^1]: Designated Intermediate System (= Router)

A quick and simplified refresher on packet types in IS-IS: A LSP carries topological information about its originating router -- its System ID, its links to other routers and its attached prefixes. It is similar to an OSPF LSU containing one or more LSAs of different types.
<!--more-->
A Complete Sequence Number PDU (CSNP) contains the inventory of all LSPs known to the router that originated the CSNP. It is similar to the OSPF DBD packet. Finally, a Partial Sequence Number PDU (PSNP) is similar to OSPF LSR and LSAck, and is used both to request and to acknowledge the reception of an LSP.

In IS-IS, on a multi-access network, all routers are fully adjacent. The DIS periodically originates a CSNP packet and floods it on the segment, thereby telling other routers: "Hey, this is my link-state database inventory."

If a router needs to flood a new LSP, it just does it right away, and every other router on the segment receives it. None of them sends any PSNP (ack)! Instead, the routers that received the LSP expect to see it listed in the upcoming periodic CSNP from the DIS.

If the LSP is listed in the CSNP, it means that the DIS received it and all is good -- no further action taken. If the LSP is missing from the CSNP, the routers on the segment that have the LSP simply schedule the LSP for reflooding. Since the timers are jittered, one of the routers will be the first one to reflood the LSP on the segment, upon which the other routers won't bother anymore. The whole process with expecting the LSP in the upcoming CSNP repeats, possibly with yet another reflooding till the DIS finally gets it.

If the flooded LSP was missed by another router that is not the DIS, that router will eventually receive the periodic CSNP from the DIS and see an LSP listed there that the router does not know about or that is newer than the router's copy. In this case, the router will flood a PSNP requesting the missing LSP, and the DIS -- upon receiving the PSNP -- will flood the LSP to the segment. The DIS never stands in the middle of the flow of LSPs between senders and receivers. Routers on the multi-access segment update each other directly.

The sync model in IS-IS is strikingly simple: Every router floods the updates to everyone but compares itself to the DIS. If the DIS is missing an LSP, let's flood it on the segment and update everyone, including the DIS. If I am missing an LSP that the DIS knows about, let me ask for it and the DIS will flood it on the segment, updating everyone including myself.

The DIS is the box that every other router compares itself to and decides who needs to be updated: DIS (and others along with DIS), or me (and others along with me).

This mechanism in IS-IS is simple, straightforward, nowhere the level of overengineering we see in OSPF's ExStart/Exchange/Loading/Full progression, dedicated DBD/LSR packets, and the obnoxious intrusivity of DR into all LSA flooding.
