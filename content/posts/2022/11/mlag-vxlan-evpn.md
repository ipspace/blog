---
anycast_tag: fabric
date: 2022-11-09 07:34:00+00:00
evpn_tag: details
lastmod: 2022-11-10 07:58:00
mlag_tag: evpn
series:
- mlag
- anycast
tags:
- EVPN
- VXLAN
title: Using EVPN/VXLAN with MLAG Clusters
---
There's no better way to start this blog post than with a widespread myth: we don't need MLAG now that most vendors have implemented EVPN multihoming.

**TL&DR**: This myth is close to the [not even wrong](https://en.wikipedia.org/wiki/Not_even_wrong) category.

As we discussed in the [MLAG System Overview](/2022/06/mlag-deep-dive-overview/) blog post, every MLAG implementation needs at least three functional components:
<!--more-->
* Forwarding table synchronization -- members of an MLAG cluster have to synchronize MAC and ARP tables.
* Synchronized control plane protocols -- members of an MLAG cluster must use the same system ID for LACP and should synchronize STP state (often implemented with running STP on a single member of the MLAG cluster)
* Configuration synchronization -- having different access lists configured on individual members of a link aggregation group is a fabulous recipe for lengthy troubleshooting sessions.

EVPN multihoming solves the forwarding table synchronization. An MLAG implementation could use ICCP (RFC 7275) to synchronize LAG membership and LACP (but not STP). I'm unaware of any standard technology that would address configuration synchronization.

EVPN multihoming is thus an excellent building block of an MLAG implementation, but you still need other bits, some of which are not standardized. Multi-vendor MLAG or MLAG cluster across numerous nodes (beyond the usual two) thus remains firmly in the PowerPoint domain.

That must be sad news for the true believers in the powers of EVPN, but at least EVPN provides everything you need to synchronize the forwarding tables, right? After all:

* MLAG cluster members use Ethernet Segment Identifiers (ESI) to identify links connected to the same CE device or CE network.
* PE devices use the ESI information to identify other members in an MLAG cluster and elect a dedicated forwarder (in active/standby deployments).
* MLAG cluster members use ESI information from MAC+IP updates to synchronize the MAC and ARP tables.
* Ingress PE devices can use ESI membership to implement optimal load balancing toward all MLAG cluster members, making the anycast gateway kludges irrelevant.

That is almost correct, apart from the last bit. 

{{<note info>}}For more details, watch the [EVPN Multihoming Deep Dive](/2022/11/video-evpn-multihoming-deep-dive/) video by Lukas Krattiger.{{</note>}}

### EVPN MAC-Based Load Balancing

Let's use the same data center fabric we discussed in the [Combining MLAG Clusters with VXLAN Fabric](/2022/09/mlag-deep-dive-vxlan-fabric/) blog post:

{{<figure src="/2022/09/MLAG-VXLAN-topology.jpg" caption="MLAG cluster connected to a VXLAN fabric">}}

Now assume that S1 and S2 use different VTEP IP addresses (please note that the details are way more convoluted than the following simplified explanation):

* S1 and S2 advertise an ESI based on the LACP System ID of host A (ESI-A). 
* S1 advertises MAC-A with ESI-A and VTEP-A as the VXLAN next hop.
* S2 doesn't have to advertise MAC-A (although it could do so) -- every other PE device knows that S1 and S2 serve the same Ethernet segment and that they could use either to reach MAC-A.

So far, so good. Now for the wrench in the works: while almost all IP forwarding tables support multiple entries for the same IP prefix, the same trick cannot be used in MAC forwarding table. Using more than one entry for the same MAC address in the MAC forwarding table results in (multicast) flooding across specified outgoing interfaces.

{{<note update>}}The rest of the blog post was rewritten based on readers' comments.{{</note>}}

Software-based forwarding is relatively easy to fix: FRR uses _nexthop_ objects to implement ECMP across multiple VTEPs (see [comment by _TA_](#1496)). _TA_ claims a similar forwarding structure is used by Mellanox ASICs, and [according to _DM_](#1497), "_all vendors have some working implementation of this_."

According to Junos [Dynamic Load Balancing in an EVPN-VXLAN Network](https://www.juniper.net/documentation/us/en/software/junos/evpn-vxlan/topics/concept/evpn-vxlan-dynamic-load-balancing.html), Juniper implemented *nexthop* objects for VTEP load balancing in all QFX switches, including the old QFX5100 that uses Broadcom Trident II chipset. OTOH, there's a blog post from a non-Juniper JNCIE [describing the EVPN/ESI limitations of QFX-series switches](https://danhearty.wordpress.com/2020/04/25/evpn-vxlan-virtual-gateway-qfx5k-forwarding/) and claiming that "_This behavior is well documented and there are some talks about Broadcom working with the vendors to improve gateway load-balancing with ESI functionality._" (HT: _[Daniel](#1502)_)

Does that mean that VXLAN-enabled ASICs always supported this functionality but it took Broadcom and networking vendors years to implement it? I guess we'll never know due to the wonderful [Broadcom documentation policy](/2016/05/what-are-problems-with-broadcom/), but if you have lab results proving that traffic from a single ingress switch toward a single MLAG-connected MAC address gets distributed across a pair of egress switches I'd be glad to know about them.

In the meantime, some vendors (example: Cisco) keep using anycast VTEP IP addresses described in the [Combining MLAG Clusters with VXLAN Fabric](/2022/09/mlag-deep-dive-vxlan-fabric/) blog post with EVPN control plane. Yet again, I can't comment whether that's due to hardware limitations, code reuse, or backward compatibility.

Anyway, even when using anycast IP address, using EVPN as the control plane protocol instead of dynamic MAC learning does provide a significant benefit -- the egress PE devices can advertise whatever next hop they wish in the MAC+IP update messages. An EVPN/VXLAN MLAG implementation could use this functionality to differentiate between multihomed and orphan nodes:

* MAC addresses of orphan nodes are advertised with unicast VTEP IP address
* Members of an MLAG cluster advertise the MAC addresses of multihomed nodes with the shared anycast VTEP IP address.

While the above solution works great in a steady state, any single link failure might turn a multihomed node into an orphan node, triggering an interesting sequence of update messages (the details are left as an exercise for the reader).

Once you implement proxy ARP and anycast gateway, you can go one step further: advertise MAC+IP information with anycast VTEP IP address and add an IP prefix (EVPN RT5) for the node IP address (a /32 or /128 prefix) with the unicast VTEP IP address. IP traffic is thus load-balanced between unicast VTEP IP addresses while MAC-based forwarding uses the anycast VTEP IP address.

Coming back to the "*EVPN multihoming makes MLAG obsolete*" myth: for every complex problem, there's a solution that is simple, neat, and wrong (and works best in PowerPoint). MLAG is no exception.

### More Information

* Data Center Network Reference Architecture part of [Data Center Networking](https://my.ipspace.net/bin/list?id=DC30#NETWORKING) section of [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers) webinar describes MLAG details and typical MLAG implementations.
* Watch [VXLAN Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive) webinar to learn more about VXLAN.
* [EVPN Multihoming](https://my.ipspace.net/bin/list?id=EVPN#MH) section of [EVPN Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar explains most of the EVPN-related intricate details.

All three webinars are available with [Standard ipSpace.net Subscription](https://www.ipspace.net/Subscription/).

### Revision History

2022-11-10
: Rewritten the "MAC load balancing" section based on readers' comments.