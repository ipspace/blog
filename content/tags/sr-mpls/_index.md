---
title: SR-MPLS
page_title: Segment Routing with MPLS Labels (SR-MPLS)
minimal_sidebar: true
layout: custom
---
Segment Routing with MPLS Labels (SR-MPLS) is a major improvement over the traditional MPLS control plane (LDP or RSVP-TE). Instead of running two protocols (a routing protocol and a signaling protocol), SR-MPLS adds segment information to the IS-IS or OSPF topology database, avoiding the pesky IGP/LDP synchronization issues we've been fighting for decades.

The MPLS labels (Segment Identifiers) assigned to nodes, adjacencies, or prefixes can be used to transport data across the network (similar to traditional MPLS core), to establish traffic engineering tunnels, or to implement topology-independent loop-free alternate paths for [fast failover](/series/fast-failover/).

### {{<plushy confused>}}What Is SR-MPLS?

{{<series-listing tag="intro" weight="yes">}}

Interested in what others are saying about SR-MPLS?

{{<series-listing tag="read">}}

### {{<plushy master>}}SR-MPLS Details

As always, the devil is in the details. Here are a few SR-MPLS details you might want to know about:

{{<series-listing tag="details" weight="yes">}}

Also, you might want to explore why I claim SR-MPLS is better than LDP:

{{<series-listing tag="ldp">}}

### {{<plushy magic>}}Try It Out

{{<series-listing tag="lab">}}

### More Information

* We [implemented SR-MPLS in _netlab_](https://netlab.tools/module/sr-mpls/). You can try it out on Arista EOS, Cisco IOS XE, Cisco IOS XR, FRRouting, Junos, Nokia SR OS, and Nokia SR Linux.
* Browse [SR-MPLS workshop](https://github.com/ipspace/SR-workshop) for sample lab topologies.
* Tiziano Tofoni covered SRv6 basics in his [ITNOG10 workshop](https://www.itnog.it/itnog10/files/TRaining_Segment%20Routing%20ITNOG%202026%20april%2020_signed.pdf)

{{<series-listing title="Blog Posts I Forgot to Categorize" notag="yes">}}
