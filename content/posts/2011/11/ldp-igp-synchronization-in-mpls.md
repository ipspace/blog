---
date: 2011-11-14 06:28:00+01:00
lastmod: 2020-12-26 08:49:00
ospf_tag: mp
tags:
- MPLS
- IS-IS
- OSPF
- LDP
- segment routing
title: LDP-IGP Synchronization in MPLS Networks
url: /2011/11/ldp-igp-synchronization-in-mpls.html
---
A reader of my blog planning to migrate his network from a traditional BGP-everywhere design to a BGP-over-MPLS one wondered about potential unexpected consequences. The [MTU implications of introducing MPLS in a running network](https://blog.ipspace.net/2011/07/mpls-mtu-challenges.html) are usually well understood (even though you [could get some very interesting behavior](https://blog.ipspace.net/2011/07/asymmetric-mpls-mtu-problem.html)); if you can, increase the MTU size by at least 16 bytes (4 labels) and [check whether MTU includes L2 header](https://blog.ipspace.net/2011/07/all-mtus-are-not-same.html). Another somewhat more mysterious beast is the interaction between IGP and LDP that can cause traffic disruptions *after the physical connectivity has been reestablished*.
<!--more-->
Here's a typical BGP-over-MPLS design (applies equally well to MPLS/VPN, 6PE, 6VPE, VPLS or pseudowires):

-   Edge routers (PE-routers) run BGP between themselves to exchange external (customer) prefixes;
-   Edge and core (P) routers run IGP (usually OSPF or IS-IS) to find optimum path toward BGP next hops;
-   P- and PE-routers use LDP to exchange labels for known IP prefixes (including BGP next hops). LDP indirectly builds end-to-end LSPs across the network core.

{{<figure src="s1600-LDPIGP_BasicSetup.png" caption="Typical IGP+LDP setup">}}

IP packets can be forwarded across BGP-free core even though the core routers don't know how to forward them. Ingress PE-router labels incoming IP packets with MPLS labels for BGP next hops, labeled packets are sent across the core (core routers don't perform IP lookup), last P-router pops the top label ([penultimate hop popping](https://blog.ipspace.net/2011/07/penultimate-hop-popping-php-demystified.html)) and the egress PE-router performs IP lookup and sends the datagram toward an external destination (the process is slightly different when you use technologies like MPLS/VPN that need a two-label stack).

{{<figure src="s1600-LDPIGP_FWD.png" caption="Packet forwarding in MPLS networks">}}

{{<note info>}}For more details watch the [LDP, FEC and BGP video ](https://my.ipspace.net/bin/get/MPLS101/4%20-%20LDP%2C%20FEC%20and%20BGP.mp4?doccode=MPLS101)from the [MPLS Essentials](https://www.ipspace.net/MPLS_Essentials) webinar.{{</note>}}

If a core link fails, IGP quickly finds an alternate path. LDP does not need to converge; when using *independent label distribution* and *liberal label retention mode* (default settings on most modern routers), every LSR saves labels advertised by all its neighbors. In our network, when A discovers that it can use B to reach the egress router, it already has the label B assigned to EG prefix in its Label Information Base (LIB). LDP thus causes no interruption in traffic flow.

{{<figure src="s1600-LDPIGP_Backup.png" caption="Packet forwarding across a backup path">}}

The situation is completely different after the physical link is restored. IGP quickly discovers new neighbors and reconverges; LDP is slower. In the short interval between IGP convergence and LDP synchronization router A sends IP packets through the new shortest path toward the egress router *with no label* (it hasn't received a label from D yet and thus has no outgoing label to use). Router D, not running BGP, has no idea what to do with those packets and thus drops them.

{{<figure src="s1600-LDPIGP_Restore.png" caption="Labeled packets are dropped on link restoration">}}

{{<note>}}The same problem can occur if you clear an LDP session or disable MPLS on an interface with **no mpls ip**.{{</note>}}

There are three solutions to this problem:

**Segment routing**: MPLS-based segment routing uses IGP to propagate globally unique labels. There's no need for LDP in an SR-MPLS environment. For more details watch the *[Segment Routing with MPLS](https://my.ipspace.net/bin/list?id=MPLS101#SR)* part of [MPLS Essentials](https://www.ipspace.net/MPLS_Essentials) webinar. I would use this one in new network designs.

**LDP-IGP synchronization**: Link cost of a newly established adjacency is set to the maximum value until LDP tells IGP it's OK to use the link. You can configure the LDP-IGP synchronization in OSPF or IS-IS, either with the **mpls ldp sync** command in the routing protocol configuration or with the **mpls ldp igp sync** interface configuration command where you can also specify an additional delay (to ensure both IGP and LDP are completely stable before you start using the new link for packet forwarding).

{{<note warn>}}The details of LDP-IGP synchronization are a bit tricky. [Read the corresponding documentation](http://www.cisco.com/en/US/docs/ios/mpls/configuration/guide/mp_ldp_igp_synch_ps10592_TSD_Products_Configuration_Guide_Chapter.html) before enabling this feature in your network.{{</note>}}

**LDP session protection**: A router tries to retain LDP sessions with all its neighbors even if they are currently not directly connected (A and D in our link failure scenario). Since the router no longer receives multicast LDP hellos from such neighbors, it uses *targeted LDP hellos* (unicast UDP packets sent to neighbor's LDP transport address) to prevent session timeouts.

{{<figure src="s1600-LDPIGP_Targeted.png" caption="Targeted LDP hellos can preserve an LDP session">}}

Targeted LDP sessions allow the routers to retain LIB information that can be used immediately after IGP convergence. There's also no need to reestablish LDP sessions with the newly-adjacent neighbors as they were never disconnected.

To configure this feature, use the **mpls ldp session protection** global configuration command. You can use an ACL to specify the neighbors you're interested in (it makes more sense to use this feature on core links than on non-redundant access links) and the duration of the session protection (default: 24 hours).

## More background information

[Enterprise MPLS/VPN Deployment](http://www.ipspace.net/Enterprise_MPLS_VPN_Deployment) webinar describes the basics of LDP, LSP establishment and packet forwarding across MPLS networks (including label stack used by MPLS/VPN and penultimate hop popping).

If you need a bit more in-depth details, [buy one of the MPLS books](https://blog.ipspace.net/2007/06/using-mpls-vpn-books-to-study-for-ccip.html) (unfortunately none of my books covers the new features like LDP session protection).

## Revision history

2020-12-26
: Added information about SR-MPLS making LDP (and LDP/IGP synchronization) obsolete.
