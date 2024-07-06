---
title: "Segment Routing vs LDP in Hub-and-Spoke Networks"
date: 2022-03-09 07:32:00
tags: [ MPLS, segment routing ]
---
I got an interesting question that nicely illustrates why Segment Routing (the MPLS variant) is so much better than LDP. Imagine a redundant hub-and-spoke network with hundreds of spokes. Let's settle on 500 spokes -- IS-IS supposedly has no problem dealing with a link-state topology of that size.

{{<figure src="/2022/03/LDP-Hub-Spoke.jpg">}}

Let's further assume that all routers advertise only their loopbacks[^SVC] and that we're using unnumbered hub-to-spoke links to minimize the routing table size. The global routing table thus contains ~500 entries. MPLS forwarding tables (LFIB) contain approximately as many entries as each router assigns a label to every prefix in the routing table[^DUS]. What about the LDP table (LIB -- Label Information Base)?
<!--more-->
The LIB tables on spokes contain ~1000 entries -- each hub router is advertising it label bindings for all entries in its forwarding table. So far so good. What about the LIB tables on the hub routers? They contain 250.000 entries -- each spoke router is advertising its 500 label bindings to both hubs even though we never want to use spokes as transit routers between hubs.

[^SVC]: We'll run MPLS-based services on top of that network, using loopbacks as BGP next hops.

[^DUS]: Assuming unsolicited downstream label allocation.

Now let's assume we use numbered hub-to-spoke links. The routing table size increases to 1500 entries (peanuts), the hub LIB size increases to 750.000 entries.

A knee-jerk reaction could be to "fix" the LDP behavior with downstream-on-demand allocation, but keep in mind there's a reason for the default behavior: after a topology change, all routers already have the labels from the new downstream neighbors because everyone assigns and advertises a label to everything just in case it might be needed. After a careful consideration, you might decide to use unsolicited downstream allocation on hub routers and downstream-on-demand on spokes[^SUP], and reduce the LIB size by orders of magnitude.

[^SUP]: Assuming your vendor supports the whole range of LDP options

You might also fine-tune the LDP label allocation on the spoke routers (don't assign labels to other spokes) or LDP label advertisement (don't advertise labels for other spokes to the hub routers), but you just piled layers of kludges on top of a suboptimal[^KL] network design. Segment routing is ridiculously simple compared to all that:

[^KL]: Because you have to fix it with kludges ;)

* No need for LDP -- labels are advertised in IGP together with IP prefixes
* No [LDP-to-IGP synchronization headaches](/2011/11/ldp-igp-synchronization-in-mpls.html).
* No [black holes or broken LSPs after link reestablishement](/2017/08/synchronizing-bgp-and-ospf-or-ospf-and.html)
* No LIB scaling issues
* Single label per device (unless you configure adjacency SIDs)

There's just a tiny little detail: you have to configure segment identifiers on all devices, but then you have to configure loopbacks as well, and you wanted to automate device configuration builds and deployments anyway, right?

Or maybe I'm just overreacting and solving imaginary scaling problems at scale? Leave a comment!

### More Information

You probably know there are tons of good MPLS books out there; you might also want to watch these webinars:

* [MPLS Essentials](https://www.ipspace.net/MPLS_Essentials) (free)
* [Segment Routing Introduction](https://www.ipspace.net/Segment_Routing_Introduction)
* [Enterprise MPLS VPN Deployment](https://www.ipspace.net/Enterprise_MPLS_VPN_Deployment)
