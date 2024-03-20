---
date: 2019-12-10 08:33:00+01:00
evpn_tag: details
tags:
- VXLAN
- BGP
- EVPN
title: EVPN Route Targets, Route Distinguishers, and VXLAN Network IDs
url: /2019/12/evpn-route-targets-route-distinguishers.html
---
Got this interesting question from one of my readers:

> BGP EVPN message carries both VNI and RT. In importing the route, is it enough either to have VNI ID or RT to import to the respective VRF?. When importing routes in a VRF, which is considered first, RT or the VNI ID?

A bit of terminology first (which you'd be very familiar with if you ever had to study how MPLS/VPN works):
<!--more-->
-   **RT = Route Target** - a VPN-identifying extended BGP community used to tag BGP routes. You might need more than one route target per VPN in complex scenarios.
-   **RD = Route Distinguisher** - a prefix prepended to tenant prefixes to make them globally unique, otherwise we couldn't use BGP to carry them around.
-   **VNI = VXLAN Network Identifier** - a 24-bit layer-2 segment ID used in VXLAN headers the same way VLAN ID is used in 802.1q headers. VNI is carried in EVPN routes in *MPLS label* field together with *BGP Encapsulation* extended community saying "*MPLS label is really a VNI*"

RT and RD are control-plane constructs used to make BGP prefixes unique (RD) and to control route import from global BGP table into per-tenant forwarding table (RT).

{{<note>}}
Various implementations might have several intermediate steps where the tenant routes would be collected in BGP table before being copied into per-tenant routing table and finally into per-tenant forwarding table (see also: [RIB and FIB](https://blog.ipspace.net/2010/09/ribs-and-fibs.html)).
{{</note>}}

VNI is data-plane construct used to select local MAC address table or IP forwarding table.

Now it should be really easy to answer the original question:

-   Like with MPLS/VPN, Route Target is used when importing EVPN routes into local routing/forwarding tables;
-   Like MPLS labels are not used to import MPLS/VPN or MPLS-based EVPN routes, VNI is not used during the route import process;
-   VNI is used when processing incoming VXLAN packets to select the tenant forwarding table.

### An Interesting Aside

In theory, VNI (like MPLS labels) has local significance, which means that different remote VTEPs **within the same MAC address table** could use different VNI values. In practice, I don't know if any ASIC supports that... and meanwhile (trying to address both) RFC 8365 talks about globally-significant and locally-significant VNI.

Do you need locally-significant VNI to implement PVLAN-like hub-and-spoke VPN, or could you do it with a globally-significant VNI? Let's leave that as an exercise for the reader ;)

### More information

You could get tons of relevant EVPN details from our [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar or go straight to the source:

-   [A Network Virtualization Overlay Solution Using Ethernet VPN (EVPN)](https://tools.ietf.org/html/rfc8365) (RFC 8365)
-   [BGP MPLS-Based Ethernet VPN](https://tools.ietf.org/html/rfc7432) (RFC 7432)
-   [The BGP Encapsulation Subsequent Address Family Identifier (SAFI) and the BGP Tunnel Encapsulation Attribute](https://tools.ietf.org/html/rfc5512) (RFC 5512)

---

Many thanks to [Dinesh Dutt](https://www.ipspace.net/Author:Dinesh_Dutt), [Nicola Modena](https://www.ipspace.net/Expert:Nicola_Modena) and [Lukas Krattiger](https://www.ipspace.net/Author:Lukas_Krattiger) for fact-checking and improving the blog post.
