---
date: 2011-03-24 07:17:00.004000+01:00
tags:
- bridging
- data center
- TRILL
title: TRILL/Fabric Path – STP Integration
url: /2011/03/trillfabric-path-stp-integration/
---
Every [Data Center fabric technology](/2011/03/data-center-fabric-architectures/) has to integrate seamlessly with legacy equipment running the venerable Spanning Tree Protocol (STP) or one of its facelifted incarnations (for example, RSTP or MST). The alternative, called *rip-and-replace* when talking about other vendors' boxes or *synchronized upgrade* when promoting your wares (no, I haven't heard it yet, but I'm sure it's coming), is simply indigestible to most data center architects.

TRILL and Cisco's proprietary Fabric Path take a very definitive stance: the new fabric is the backbone of the network routing TRILL-encapsulated layer-2 frames across bridged segments (TRILL) or contiguous backbone (Fabric Path). Both architectures segment the original STP domain into small chunks at the edges of the network as shown in the following figure:
<!--more-->
{{<figure src="/2011/03/s1600-TrillSTPIntegration.png">}}

{{<note>}}Did you notice I used the *routing at layer-2* oxymoron? Packet forwarding within the TRILL backbone is true routing; unfortunately [TRILL also retains all the drawbacks of bridging](/2010/07/why-is-trill-not-routing-at-layer-2/).{{</note>}}

The devices running TRILL could participate in the small STP domains, but that participation has nothing to do with TRILL (the [TRILL draft is adamant](https://tools.ietf.org/html/draft-ietf-trill-rbridge-protocol-16#section-2.6): *RBridges do not use spanning tree*). In that case, some edge ports might become blocked by STP (the left-hand case in the figure).

Whether they run STP or not, the RBridges have to ensure there's a single point of contact between a VLAN in the STP domain and the backbone, otherwise all the flooded packets would enter the backbone through multiple entry points, resulting in duplicate packets received by the remote hosts (which might break some odd fainthearted protocols running directly on top of L2). One of the RBridges therefore becomes an *appointed forwarder* for an edge VLAN.

The right-hand part of the figure illustrates the appointed forwarder concept: the RBridges don't participate in the STP, none of their edge ports are blocked, but only one of the RBridges acts as a forwarder between the edge STP domain and the TRILL backbone (marked with A), all other RBridges ignore packets received through that VLAN (marked with B).

{{<note info>}}Assuming the RBridges perform TRILL-based bridging between its edge ports, each access switch on the right-hand side belongs to an independent STP domain and becomes the root of a very small spanning tree.{{</note>}}

As the forwarders are appointed on per-VLAN basis (if you want to know the details, the allocation is done by the Designated RBridge -- DRB), it's quite easy to achieve per-VLAN load balancing by adjusting the allocation algorithm used by the DRB.

{{<note info>}}A bit off-topic: a pair of Nexus 7000 switches connected with a VPC+ link can perform active-active forwarding into the Fabric Path backbone.{{</note>}}
