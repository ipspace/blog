---
date: 2022-12-06 07:06:00+00:00
mlag_tag: deepdive
series:
- mlag
series_weight: 500
tags:
- IP routing
- switching
title: Running Routing Protocols over MLAG Links
---
It took vendors like Cisco years to start supporting routing protocols between MLAG-attached routers and a pair of switches in the MLAG cluster. That seems like a no-brainer scenario, so there must be some hidden complexities. Let's figure out what they are.

We'll use the familiar MLAG diagram, replacing one of the attached hosts with a router running a routing protocol with both members of the MLAG cluster (for example, R, S1, and S2 are OSPF neighbors).

{{<figure src="/2022/12/mlag-routing.png">}}
<!--more-->
Now imagine both switches advertise the path to blue and orange subnets to the attached router. Each of them would advertise the prefix with their own IP address as the next hop, but from the router's perspective, both next hops would be reachable over the same link (the LAG link). The router would send packets toward A or C with the destination MAC address of S1 or S2 due to layer-3 ECMP. The router would use both members of the link aggregation group (R-S1 and R-S2) links when sending those packets due to layer-2 ECMP.

According to the rules I explained in _[Layer-2 Flooding](/2022/06/mlag-deep-dive-flooding.html)_ and _[Layer-3 Forwarding](/2022/06/mlag-active-active-layer3.html)_ blog posts, a packet arriving over the peer link can never be forwarded to a dual-attached neighbor. Suppose the router decides to send a packet toward A through S1 (using the S1 MAC address) but sends the resulting Ethernet frame through the R-S2 link. In that case, S2 forwards the packet toward S1 over the peer link (due to the destination MAC address), but S1 cannot forward it to A (because it arrived over the peer link).

Regardless of the technology limitations, users love trying to implement impossible things, and the vendors usually implement all sorts of kludges to accommodate them. Can we fix the current conundrum? Of course!

While members of an MLAG cluster have independent IP addresses, most layer-3 forwarding implementations use a shared IP/MAC address as the first-hop gateway. Announcing that IP address as the third-party next hop in routing protocol updates fixes the problem for good. That's easy to do with BGP. EIGRP and OSPF have similar functionality for external routers, but what could we do with internal routes where the routing protocol packet format does not include the next hop?

Time to get creative[^WW]. We're facing packet drops because:

* The directly attached router selects an IP address of one of the MLAG members as the next hop.
* It rewrites the Ethernet header using the MAC address of that member as the destination MAC address.
* It sends the resulting Ethernet frame to the other MLAG member.

What if we had both MLAG members listening to both MAC addresses? That would remove the extra forwarding step over the peer link, and layer-3 forwarding would work. Unfortunately, that would also break the routing protocols -- we still have to deliver unicast packets sent to the MLAG member IP address to the correct device.

Here's a possible implementation of that final kludge[^IMP]:

* Receive packets for S1 MAC, S2 MAC, and shared MAC on both MLAG members.
* Route packets for third-party destinations on the ingress MLAG member, ensuring they won't be sent over the peer link unless necessary.
* Use policy-based routing matching on the remote MLAG member IP and MAC address to push the unicast packets for that node to the peer link without doing the L2/L3 lookup or decrementing TTL[^APG].

[^APG]: Assuming you have good-enough ASIC and engineers programming it

Does that work? Of course. It's also unnecessarily complex.

**Long story short**: Don't run routing protocols over MLAG links. Use two independent links and two routing adjacencies.

[^WW]: Also known as "Where there's a will, there's a way."

[^IMP]: I'm not saying vendors are doing exactly what I'm describing. It's just that there's not much else they can do, and I'm pretty sure someone will quickly set me straight in the comments if I got too far into the weeds.

### More Information

The Data Center Network Reference Architecture part of [Data Center Networking](https://my.ipspace.net/bin/list?id=DC30#NETWORKING) section of [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers) webinar describes MLAG details and typical MLAG implementations. The webinar is part of [Standard ipSpace.net Subscription](https://www.ipspace.net/Subscription/).
