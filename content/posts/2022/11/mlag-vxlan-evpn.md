---
title: "Using EVPN/VXLAN with MLAG Clusters"
date: 2022-11-09 07:34:00
tags: [ evpn,vxlan ]
series: mlag
mlag_tag: deepdive
---
There's no better way to start this blog post than with a widespread myth: we don't need MLAG now that most vendors have implemented EVPN multihoming.

**TL&DR**: This myth is close to the [not even wrong](https://en.wikipedia.org/wiki/Not_even_wrong) category.

As we discussed in the [MLAG System Overview](/2022/06/mlag-deep-dive-overview.html) blog post, every MLAG implementation needs at least three functional components:
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

{{<note info>}}For more details, watch the [EVPN Multihoming Deep Dive](/2022/11/video-evpn-multihoming-deep-dive.html) video by Lukas Krattiger.{{</note>}}

### EVPN MAC-Based Load Balancing

Let's use the same data center fabric we discussed in the [Combining MLAG Clusters with VXLAN Fabric](/2022/09/mlag-deep-dive-vxlan-fabric.html) blog post:

{{<figure src="/2022/09/MLAG-VXLAN-topology.jpg" caption="MLAG cluster connected to a VXLAN fabric">}}

Now assume that S1 and S2 use different VTEP IP addresses (please note that the details are way more convoluted than the following simplified explanation):

* S1 and S2 advertise an ESI based on the LACP System ID of host A (ESI-A). 
* S1 advertises MAC-A with ESI-A and VTEP-A as the VXLAN next hop.
* S2 doesn't have to advertise MAC-A (although it could do so) -- every other PE device knows that S1 and S2 serve the same Ethernet segment and that they could use either to reach MAC-A.

So far, so good. Now for the wrench in the works: while almost all IP forwarding tables support multiple entries for the same IP prefix, it's rare to find forwarding hardware that supports more than one next-hop entry for the same MAC address. Using more than one entry for the same MAC address in the MAC forwarding table also doesn't work -- that's how the forwarding hardware implements flooding.

**Long story short**: EVPN provides all the functionality one needs to identify MLAG member links and quickly failover to a subset of links on a link or node failure. However, the forwarding hardware limitations require anycast VTEP IP addresses described in the [Combining MLAG Clusters with VXLAN Fabric](/2022/09/mlag-deep-dive-vxlan-fabric.html) blog post. We're (almost) back to square one -- or you could give up and forward all traffic for a single MAC address toward one of the egress VTEPs.

Using EVPN as the control plane protocol instead of dynamic MAC learning does provide a significant benefit: the egress PE devices can advertise whatever next hop they wish in the MAC+IP update messages. Many vendors use this functionality to differentiate between multihomed and orphan nodes:

* MAC addresses of orphan nodes are advertised with unicast VTEP IP address
* Members of an MLAG cluster advertise the MAC addresses of multihomed nodes with the shared anycast VTEP IP address.

While the above solution works great in a steady state, any single link failure might turn a multihomed node into an orphan node, triggering an interesting sequence of update messages (the details are left as an exercise for the reader).

Some vendors try to go a step further: they advertise MAC+IP information with anycast VTEP IP address and add an IP prefix (EVPN RT5) for the node IP address (a /32 or /128 prefix) with the unicast VTEP IP address. IP traffic is thus load-balanced between unicast VTEP IP addresses[^PARP], while MAC-based forwarding uses the anycast VTEP IP address.

[^PARP]: Usually requiring proxy ARP configuration on ingress PE devices.

Coming back to the "*EVPN multihoming makes MLAG obsolete*" myth: for every complex problem, there's a solution that is simple, neat, and wrong (and works best in PowerPoint). MLAG is no exception.

### More Information

* Data Center Network Reference Architecture part of [Data Center Networking](https://my.ipspace.net/bin/list?id=DC30#NETWORKING) section of [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers) webinar describes MLAG details and typical MLAG implementations.
* Watch [VXLAN Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive) webinar to learn more about VXLAN.
* [EVPN Multihoming](https://my.ipspace.net/bin/list?id=EVPN#MH) section of [EVPN Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar explains most of the EVPN-related intricate details.

All three webinars are available with [Standard ipSpace.net Subscription](https://www.ipspace.net/Subscription/).


