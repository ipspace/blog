---
title: "MLAG Deep Dive: Layer-3 Forwarding"
date: 2022-06-22 06:55:00
tags: [ switching ]
series: mlag
mlag_tag: deepdive
series_title: Layer-3 Forwarding
---
The [layer-2 forwarding](/2022/06/mlag-deep-dive-mac-learning.html) and [flooding](/2022/06/mlag-deep-dive-flooding.html) in an MLAG cluster are intricate but still reasonably easy to understand. Layer-3 is different -- as I was writing this blog post, I was constantly asking myself, "_why did they ever implement something like that?_" Please consider this a work-in-progress; I would appreciate any comments, feedback, or [pull requests](https://blog.ipspace.net/2022/05/ipspace-blog-github.html) you might provide.

We'll have to expand by-now familiar network topology to cover layer-3 edge cases. We'll still work with two switches in an MLAG cluster, but we'll have an external router attached to both of them. The hosts connected to the switches belong to two subnets (red and blue).
<!--more-->
{{<figure src="/2022/06/MLAG-L3-topology.jpg" caption="Layer-3 MLAG topology">}}

### Forwarding Requirements

Before going into the details, let's figure out what we should expect in a well-designed MLAG cluster providing layer-3 forwarding:

* One of the primary reasons to deal with MLAG complexity is _redundancy_ -- the traffic should keep flowing even when one of the MLAG cluster members crashes. That's easy to do within a layer-2 segment; to keep inter-subnet traffic flowing, the MLAG cluster members have to share the IP and MAC address of the first-hop gateway.
* We want [active/active layer-3 forwarding across the MLAG cluster](https://blog.ipspace.net/2012/05/does-optimal-l3-forwarding-matter-in.html). For example, when A sends an IP packet to B, it might use the A-S1 or the A-S2 link. It would make no sense to send that packet over the S1-S2 peer link just to be routed by the other switch. The first-hop IP and MAC address must therefore be active on all MLAG cluster members.
* MLAG cluster members must deal with misdirected traffic. In most designs, S1 and S2 advertise whole subnets (_red_ and _blue_) to the external router. While it doesn't matter whether the external router sends traffic for A or B to S1 or S2, S1 and S2 have to deal with traffic for X or Y arriving at the wrong switch.

### First-Hop IP and MAC Address


I'm positive the "_shared first-hop IP- and MAC address_" requirement immediately triggered the "_first-hop redundancy protocols (FHRP)_" knee-jerk reaction, but that doesn't have to be the case. [Arista's Virtual ARP (VARP)](https://blog.ipspace.net/2013/06/arista-eos-virtual-arp-varp-behind.html) – statically configured shared IP- and MAC address – is more than good enough, and it's pretty resilient against configuration mistakes. Yet, every other vendor insisted on running HSRP or VRRP between MLAG cluster members. 

### Active/Active Forwarding

Even worse, many vendors took ancient FHRP implementations that supported a single active forwarder and made them part of their MLAG solutions. It took years before they realized it's [perfectly fine to have all switches listen to the same MAC address](https://blog.ipspace.net/2013/05/optimal-l3-forwarding-with-varp-and.html). After all, if the MAC table on the ingress switch forwards a layer-2 packet with the FHRP destination MAC address to the layer-3 forwarding table, that same packet is not flooded to any other host (or the peer link), and there's no danger of traffic duplication.

{{<note warn>}}If you want to use active-active forwarding, [turn off ICMP redirects](https://blog.ipspace.net/2022/02/nexus-icmp-redirects.html) on routed VLANs in an MLAG cluster. More details coming in another blog post.{{</note>}}

Fortunately, most everyone got the memo -- active/active forwarding is now a table-stakes MLAG feature, and many switches support anycast gateway that extends the shared IP- and MAC addresses across the whole VLAN. Isn't it ironic that it took so long for everyone to eventually converge toward the most straightforward solution that has been known for ages?

### ARP Handling

I already mentioned misdirected traffic: an external source might send an IP packet to a switch that is not yet ready to forward it to a directly-connected host due to a missing ARP entry. 

Many MLAG implementations use a control-plane protocol that synchronizes the ARP tables between MLAG cluster members to deal with that challenge, but I can't figure out what they gain from the added complexity. After all, the worst that can happen is another ARP request and a dropped packet (or few).

It also doesn't matter if the target host sends the ARP reply through the other uplink. ARP reply is a unicast layer-2 frame, and we solved the unicast layer-2 forwarding, so we can be sure the ARP reply will arrive at the final destination.

What am I missing?

### Gateway Source MAC Address

MLAG implementations must deal with another glitch. Some devices (most notably storage devices, supposedly also some load balancers) build forwarding cache entries from the source IP- and MAC addresses of the incoming IP packets -- a clear layering violation, probably also an RFC violation.

Let's assume B is such a device. When A sends a packet to B over the A-S1 link, S1 routes the packet and forwards it to B with the S1 source MAC address. A sane IP host would ignore the source MAC address and send the return packet to the default gateway MAC address (after all, A is in a different subnet). B -- an aggressively over-optimizing device -- would build a forwarding entry from that packet saying "_to send packets to A, use S1 MAC address_", and we've lost the active-active forwarding.

There are two ways to solve this conundrum:

* A sane way: send all traffic from S1 and S2 with the shared source MAC address. Whatever the crazy hosts decide to do cannot break active-active forwarding.
* A commonly-used way: both switches process traffic sent to the shared MAC address and the local MAC addresses _of both switches_. This approach ensures no control-plane protocol (including ARP) will ever work correctly; the proof is left as an exercise for the reader.

Is there a hardware limitation I'm unaware of? If it's possible to send traffic from MAC addresses unique to each switch and receive traffic for multiple MAC addresses, why can't the switches send the traffic from the shared MAC address and receive traffic for the shared- and local MAC address? What am I missing?

{{<next-in-series page="/posts/mlag-peer-link-fabric.md">}}
### What's Next?

We covered the basics of layer-2 and layer-3 forwarding in an MLAG cluster. Time for more interesting topics, starting with "_can we get rid of the peer link?_" – the topic of the next blog post in the [MLAG Deep Dive series](/series/mlag.html#technology-deep-dive).{{</next-in-series>}}
