---
date: 2016-02-10 08:32:00+01:00
dcbgp_tag: newrp
series:
- dcbgp
tags:
- design
- OSPF
- data center
- BGP
title: BGP or OSPF? Does Topology Visibility Matter?
url: /2016/02/bgp-or-ospf-does-topology-visibility.html
---
[One of the comments](https://blog.ipspace.net/2016/02/using-bgp-in-data-center-fabrics.html?showComment=1455038894509#c7711023460231292939) added to my [*Using BGP in Data Centers*](http://blog.ipspace.net/2016/02/using-bgp-in-data-center-fabrics.html) blog post said:

> With symmetric fabric... does it make sense for a node to know every bit of fabric info or is reachability information sufficient?

Let's ignore for the moment that large non-redundant layer-3 fabrics where BGP-in-Data-Center movement started don't need more than endpoint reachability information, and focus on a bigger issue: is knowledge of network topology (as provided by OSPF and not by BGP) beneficial?
<!--more-->

### Before We Start

A few weeks after I published this blog post I received an email that indicated at least some readers understood the question I was trying to address in this blog post as "*Do we need to know the state of the topology of our network?*"

That was never the intended scope of this blog post, and anyone who thinks the answer is not a resounding YES is a clear victim of section 2.4 of RFC 1925.

However, as some people advertise using OSPF as the underlying protocol in large data center networks instead of now more hip BGP-only approach "*because it gives you visibility into network topology*", this blog post addresses the routing protocol side of things, specifically: *does visibility of network topology enable a router in a distributed system to construct better forwarding table?*

Also, keep in mind that there are many ways one can discover the current state of network topology, starting with reading tables of LLDP neighbors, BGP neighbors, or OSPF neighbors using ancient methods like SNMP. BGP-LS or other methods of data extraction from OSPF or IS-IS topology databases are not the only answer.

### The History

Link-state protocols (OSPF and IS-IS) were created as a reaction to extremely slow convergence speeds of early versions of RIP that propagated reachability information with periodic updates.

EIGRP (which is just an [optimized distance vector protocol](https://blog.ipspace.net/2010/08/eigrp-myths-debunked.html)) was created as a reaction to complexities of OSPF.

It looks like another case of a technology pendulum being swung back and forth between two extremes. Does one of them work better than the other?

### The Results Are the Same

With link costs being equal, OSPF, IS-IS and EIGRP produce the same forwarding topology (so would RIP if it had link costs, or BGP is you'd encode link costs in AS-path length).

No surprise there. As long as we stick with the [hop-by-hop destination-only](https://blog.ipspace.net/2015/11/packet-and-flow-based-forwarding.html) forwarding paradigm, there's nothing that a router could do based on knowledge of wider network topology, because it cannot influence the forwarding decisions made by the downstream next-hop router.

{{<note>}}That's why [EIGRP needs *feasible successor*](https://blog.ipspace.net/2012/08/eigrp-mba-like-perspective.html) and why [LFA](http://blog.ipspace.net/2012/01/loop-free-alternate-ospf-meets-eigrp.html) is so limited in what it can do. The proof is left as an exercise for the readers. However, if you need more information search for excellent LFA-related articles by [Russ White](http://packetpushers.net/author/russ-white/).{{</note>}}

The only difference between link state and distance vector protocols used in traditional IP routing is the method of information dissemination: flooding-and-computing (link-state) or computing-and-propagating (distance vector).

### Are Convergence Speeds Different?

Short answer: No.

Early implementations of distance vector protocols were excruciatingly slow. Modern implementations using flash updates and reverse poisoning are approximately as fast as link-state protocols.

In any case, you don't want the network overreacting to every change, so every routing protocol includes all sorts of dampening knobs (LSA origination timer, flooding timer, SPF interval...), making link-state and distance-vector protocols even more similar in performance.

Finally, in large networks the routing protocol convergence time becomes insignificant compared to the [time needed to install the changes in the forwarding hardware](https://blog.ipspace.net/2012/01/prefix-independent-convergence-pic.html).

### Is There Any Use for Network Topology?

Is there something that a link-state protocol can do that a distance-vector one cannot? As long as we're using hop-by-hop forwarding paradigm the answer is NO.

The topology information becomes important when the forwarding technology used in the network supports paths (virtual circuits) between network devices, the typical examples being MPLS Traffic Engineering and Segment Routing. In these cases the nodes can use the knowledge of wider network topology to build alternate paths (MPLS Fast Reroute) or redirect traffic away from the failure point ([Remote LFA](http://packetpushers.net/remote-lfa-2/)).

### Back to the Data Center

Is there any use for detailed knowledge of network topology in a data center switch? Not for IP routing... unless you're deploying MPLS-TE in your data center, in which case I would like to remind you that additional bandwidth might be cheaper than the engineers needed to operate such a network.

Could the data center switches use network topology for other purposes? For example, a leaf switch might decide to change its load balancing algorithm on leaf-to-spine links based on utilization of downstream spine-to-leaf links.

While some proprietary fabrics do that, no traditional routing protocol propagates such information for good reasons -- it might quickly lead to widespread instabilities.

The final answer is thus NO. From the packet forwarding perspective it doesn't matter whether you use OSPF or BGP in your data center fabric. For other relevant aspects, watch the   [Leaf-and-Spine Fabric Designs](http://www.ipspace.net/Leaf-and-Spine_Fabric_Designs) webinar.
