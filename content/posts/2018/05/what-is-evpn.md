---
date: 2018-05-14 10:50:00+02:00
evpn_tag: intro
tags:
- EVPN
title: What Is EVPN?
series_weight: 2000
---
EVPN might be the next big thing in networking... or at least all the major networking vendors think so. It's also a pretty complex technology that still faces some interoperability challenges (I love to call it SIP of networking).

To make matters worse, EVPN can easily become even more confusing if you follow some convoluted designs propagated on the 'net. The best antidote to that is to invest time into understanding the fundamentals and slowly work through more complex scenarios after mastering the basics.
<!--more-->
We did precisely that in the [EVPN Technical Deep Dive](http://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar (after laying the data center groundwork in the [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar); here's a summary of the *What Is EVPN* part of [EVPN Fundamentals](http://my.ipspace.net/bin/list?id=EVPN#FUNDAMENTALS) section:

-   EVPN is a multi-tenant BGP-based control plane for layer-2 (bridging) and layer-3 (routing) VPNs. It's the unifying L2+L3 equivalent of the traditional L3-only MPLS/VPN control plane.
-   EVPN was designed to be used with an MPLS data plane to replace VPLS in service provider networks. It was adopted (with VXLAN encapsulation) as the control plane used by the Network Virtualization Overlays (NVO) IETF workgroup.
-   In theory, EVPN could be used with almost any data-plane encapsulation (RFCs define extended BGP community values for MPLS, VXLAN, MPLS-over-GRE, MPLS-over-UDP, NVGRE...). In practice, it's used with either MPLS in Service Provider networks or VXLAN in IP-based Service Provider networks or data center fabrics.
-   Like MPLS/VPN, EVPN uses Route Distinguishers to make locally significant identifiers globally unique and Route Targets to indicate VPN membership. Route Distinguishers usually use an IP-address-based format, and Route Targets usually use an ASN-based format.
-   EVPN defines a mechanism to automatically generate RD and RT values from VLAN or VXLAN identifiers.
-   EVPN replaces the flood-and-learn behavior of traditional Ethernet bridges (or VPLS or simpler VXLAN implementations) with a BGP control plane. MAC addresses are propagated as BGP prefixes within the EVPN address family.
-   EVPN implementations could use dynamic IP address discovery using DHCP reply snooping, ARP request snooping, or IP packet header gleaning and advertise IP-to-MAC bindings in EVPN BGP updates.
-   EVPN can be used to implement end-to-end bridging, integrated-bridging-and-routing (IRB), or routing-only fabrics.
-   EVPN supports MAC and IP address mobility (available in most implementations) and a standard-based MLAG functionality (available in Junos and recent NX-OS).
-   Decent EVPN implementations can reduce flooding by turning off unknown unicast flooding and eliminating ARP flooding with local ARP proxy.

Want to know more? [Start here](http://my.ipspace.net/bin/list?id=EVPN#FUNDAMENTALS).
