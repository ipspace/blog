---
date: 2022-06-16 06:55:00+00:00
lastmod: 2022-06-19 16:02:00
mlag_tag: deepdive
series:
- mlag
series_title: Layer-2 Flooding
series_weight: 800
tags:
- switching
title: 'MLAG Deep Dive: Layer-2 Flooding'
---
In the [previous blog post](/2022/06/mlag-deep-dive-mac-learning.html) of the [*MLAG Technology Deep Dive* series](/series/mlag.html#technology-deep-dive), we explored the intricacies of layer-2 unicast forwarding. Now let's focus on layer-2 BUM[^BUM] flooding functionality of an MLAG system. 

Our network topology will have two switches and five hosts, some connected to a single switch. That's not a good idea in an MLAG environment, but even if you have a picture-perfect design with everything redundantly connected, you will have to deal with it after a single link failure.
<!--more-->
{{<figure src="/2022/06/MLAG-topology.jpg" caption="Simple MLAG topology">}}

[^BUM]: BUM: Broadcasts, Unknown Unicast, Multicasts.

Imagine host A sending a broadcast (or any other frame that needs to be flooded). It could use the A-S1 or the A-S2 link to do so. Let's assume it uses the A-S1 link. The broadcast has to be received by every other host connected to the same broadcast domain. Getting it to X and B is simple – S1 sends it over a directly connected link.

What about C and Y? Only S2 can deliver the broadcast to them – S1 has to send all flooded frames to S2 over the peer link. So far, so good, but now we're hitting a snag: a packet S2 receives over the peer link should not be flooded to hosts with active connections to both switches[^M1]. S2 should forward the broadcast to C and Y, but not to A or B. In other words: S2 must implement a split horizon between single-attached and dual-attached hosts.

[^M1]: Things get interestingly complex if we have more than two switches in an MLAG cluster. I'll leave the gory details as an exercise for the reader.

Let's assume our switches use a MAC forwarding table with an extra _default_ entry that contains the list of all ports to which they should flood a BUM frame.[^DF] That works great for standalone switches, but we need two _default_ entries for switches operating in an MLAG cluster:

[^DF]: In theory, a single _default_ entry is good enough to implement BUM flooding unless you want to implement IGMP snooping.

* A _default_ entry for packets received from connected network devices. S1 would forward such packets to X, A, B, and S2[^IEEESH]; S2 would deliver them to A, B, C, Y, and S1.
* Another _default_ entry for packets received over the peer link. S1 would forward them to X but not to A or B. Likewise, S2 would send them to C and Y, but not A or B.

[^IEEESH]: Following the usual IEEE 802.1 split-horizon rule: never forward a frame to the port from which it has been received.

These requirements are not too different from what we need to implement stackable switches, so we can expect some forwarding ASICs to contain mechanisms to deal with them. The ASIC could select one or the other _default_ entry based on the input port, or use metadata attached to the incoming frame[^PF] if the MLAG implementation is using additional (proprietary) encapsulation on the peer link[^PE].

[^PF]: A flag saying, "_this frame is coming from a peer link, please flood it to everyone that's not connected to me_."

[^PE]: According to Dinesh Dutt, most modern MLAG implementations use standard Ethernet encapsulation on the peer link.

The real fun starts when we try to replace the peer link with fabric connection using MPLS or VXLAN encapsulation. MPLS label stack is an obvious solution[^ML]: RFC 7432 contains a [lengthy convoluted section](https://datatracker.ietf.org/doc/html/rfc7432#section-8.3) explaining how to advertise and use an additional MPLS label to implement split horizon switching. 

There's no _extra label_ in VXLAN, and the only solution ([detailed in RFC 8365](https://datatracker.ietf.org/doc/html/rfc8365#section-8.3.1)) is to use the source IP address of the VXLAN packets to figure out whether the packet is coming from the virtual peer link. That must be tremendous fun to program in forwarding hardware judging from the catastrophic bugs that riddled early EVPN-only MLAG implementations.

Back to those two _default_ entries. The switch ASIC could support them, our you could use two MAC tables (one for regular ports, one for peer link) with a lot of VLAN magic, but there's a much more creative solution: use ACL on outgoing port. All you need is a high-priority entry on all LAG ports saying "_if the packet came from the peer link, drop it_."

In our example, the switch software would configure an entry saying "_drop a packet if it came over the S1-S2 link_" on links to A and B, but not on links to X, Y, and C -- all those switches are connected to a single MLAG member, and have to receive flooded packets arriving through the peer link.

[^ML]: All problems in networking that are worth solving can be solved with one or more additional MPLS labels 😜

{{<next-in-series page="/posts/2022/06/mlag-active-active-layer3.md">}}
### What's Next?

We're only three blog posts into this series and we already got layer-2 forwarding sorted out. It's time to move to layer-3 challenges, starting with active/active layer-3 forwarding – the topic of the next blog post in the [MLAG Deep Dive series](/series/mlag.html#technology-deep-dive).{{</next-in-series>}}

### Revision History

2022-06-19
: Added the _outgoing ACL_ solution based on lengthy chat with Dinesh Dutt. Dinesh, thanks a million!
