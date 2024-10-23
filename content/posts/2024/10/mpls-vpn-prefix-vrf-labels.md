---
title: "Per-Prefix and Per-VRF MPLS/VPN and EVPN Labels/VNIs"
date: 2024-10-23 08:38:00+0200
tags: [ MPLS VPN, EVPN ]
evpn_tag: mpls
---
Long long time ago[^LLTA], in an ancient town far far away[^ROME], an old-school networking Jeddi[^TT] was driving us toward a convent[^TS] where we had an SDN workshop[^SDN]. While we were stuck in the morning traffic jam, an enthusiastic engineer sitting beside me wanted to know my opinion about per-prefix and per-VRF MPLS/VPN label allocation.

At that time, I had lived in a comfortable Cisco IOS bubble for way too long, so my answer was along the lines of "Say what???" Nicola Modena[^NM] quickly expanded my horizons, and I said, "Gee, I have to write a blog post about that!" As you can see, it took me over a decade.
<!--more-->
[^LLTA]: At least a decade
[^ROME]: Rome
[^TT]: Known to the outside world as Tiziano Tofoni
[^TS]: This sounds like a mix of Star Wars and Dune, but it's true. Nuns in Rome run a conference center as a side business.
[^SDN]: Those were the days when people still believed the SDN/OpenFlow religion would save the world. Looking back, running that workshop in a convent was a nice touch.
[^NM]: The fantastic engineer sitting next to me (and a great friend)

**TL&DR**: You don't have to care unless you love living on the bleeding edge of technology.
 
### The Basics

As you probably know, MPLS/VPN uses VPNv4/VPNv6 address families to advertise VPN prefixes. An MPLS label must be attached to every prefix an egress PE-router advertises to enable the ingress PE-router to build an MPLS label stack that the egress router will understand. However, the MPLS/VPN labels have local significance, and as long as there's a label attached to every prefix, nobody cares what they are.

That gives the egress PE router the freedom to allocate labels to prefixes in any way it wishes. It could allocate a separate label for every prefix (per-prefix allocation) or a single label for the whole VRF (per-VRF allocation). Some implementations also have a third option: use the same label for all prefixes with the same next hop.

EVPN with the MPLS data plane is no different, and while I haven't looked around (yet), there must be at least some nerd knobs you can tweak; please leave a comment if you know of a vendor having those nerd knobs.

EVPN with the VXLAN data plane is usually more limited. VXLAN VNI is a VLAN in disguise and usually has to be attached to an L2 or L3 forwarding table, making EVPN transit VNI an equivalent of a per-VRF label[^VNT].

[^VNT]: The last time we met, Nicola mentioned a new trick one might use in the EVPN/VXLAN world; you'll have to wait for another blog post to learn more about that. I just hope it won't take me another decade to write it.

### Does It Matter?

Rarely. In most scenarios, the default label allocation policy works quite well unless you want to have [the full Internet routing table in a VRF](/2012/07/is-it-safe-to-run-internet-in-vrf/), in which case [per-VRF label might not be a bad idea](https://blog.ipspace.net/2013/02/internet-in-vrf-and-lfib-explosion/).

Another exception is a [one-arm hub-and-spoke VPN](/2024/09/hub-spoke-one-arm/) that [does not work with the per-VRF labels](/2024/09/hub-spoke-one-arm/#per-prefix-or-per-vrf-labels). PIC Edge, [EIBGP load balancing](/2013/06/eibgp-load-balancing/), and [Egress Peer Engineering](/2024/10/worth-reading-egress-peer-engineering/) also require per-prefix or per-next-hop labels (PIC Edge details coming in another blog post). Finally, Carrier's Carrier architecture (is anyone using that?) has to preserve end-to-end LSPs, so it needs per-prefix labels. Have I missed anything else? Please leave a comment.

Anyway, why do we have so many options? As is often the case, vendor are solving their hardware challenges with software.

In the early days of MPLS, the labels were cheap (MPLS LFIB is a simple lookup table), but it was challenging (or time-consuming) to do multiple lookups on a single packet. MPLS labels pointing to a next-hop entry that contains an outgoing interface and a layer-2 header were a perfect solution.

A few years later, hardware could do two lookups without a significant performance penalty, and per-VRF labels became a viable alternative. They are particularly popular with vendors that have to deal with hardware with limited LFIB size. Some had to get creative[^TCAM], and some probably just wanted to save a few cents[^L3FIB].

[^TCAM]: According to rumors, you had to burn expensive TCAM usually used for ACLs to implement MPLS in some data center switching ASICs.

[^L3FIB]: Considering the relative complexity of longest-prefix matches and label lookups, it's a bit hard to understand why someone would design a switching ASIC with a layer-3 forwarding table significantly larger than the LFIB. In the worst case, you could combine the LFIB and MAC address tables.

Finally, you could argue (in an angels-dancing-on-a-pin fashion) about the impact of label allocation policy on route churn[^RC]. It seems that those arguments could stay in the realm of academics and vendor marketing departments[^LCD]; the real-life impact is probably negligible unless you have tons of routes and a very peculiar network design.

[^RC]: Hint: what happens if you have multiple CE-routers advertising the same prefix and one of the links (or CE-routers) fails? Sometimes, you can pretend nothing happened; in others, you must advertise a different prefix because the label has changed.

[^LCD]: Do leave a comment if you disagree
