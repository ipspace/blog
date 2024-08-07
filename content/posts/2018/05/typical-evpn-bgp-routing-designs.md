---
date: 2018-05-30 09:06:00+02:00
dcbgp_tag: design
evpn_tag: design
series:
- dcbgp
series_weight: 800
tags:
- design
- BGP
- EVPN
title: Scaling EVPN BGP Routing Designs
url: /2018/05/typical-evpn-bgp-routing-designs/
---
As discussed in a [previous blog post](/2018/05/what-is-evpn/), IETF designed EVPN to be next-generation BGP-based VPN technology providing scalable layer-2 and layer-3 VPN functionality. EVPN was initially designed to be used with MPLS data plane and was later extended to use numerous data plane encapsulations, VXLAN being the most common one.

### Design Requirements

Like any other BGP-based solution, EVPN uses BGP to transport endpoint reachability information (customer MAC and IP addresses and prefixes, flooding trees, and multi-attached segments), and relies on an underlying routing protocol to provide BGP next-hop reachability information.
<!--more-->
The most obvious approach would thus be to use BGP-based control plane with an underlying IGP (or even Fast Reroute) providing fast-converging paths to BGP next hops. You can use the same design with EVPN regardless of whether you use MPLS or VXLAN data plane:

-   Use [any IGP suitable for the size of your network](/2018/05/is-ospf-or-is-is-good-enough-for-my/). Some service providers have over a thousand routers in a single OSPF or IS-IS area. Even in highly-meshed environments (leaf-and-spine fabrics), OSPF or IS-IS easily scale to over a hundred switches.
-   Use IBGP to transport EVPN BGP updates, and BGP route reflectors for scalability.

In data centers using EBGP as an IGP replacement, you could use the existing EBGP sessions to carry IPv4 (underlay) and EVPN (overlay) address families. For more information on this approach and some alternative designs read the [BGP in EVPN-Based Data Center Fabrics](http://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics) part of [Using BGP in Data Center Leaf-and-Spine Fabrics](http://www.ipspace.net/Data_Center_BGP) document.

### Beyond a Single Autonomous System or Fabric

Like with MPLS/VPN, EVPN EBGP designs are a bit more convoluted than IBGP designs.

When using MPLS data plane, there's almost no difference between MPLS/VPN and EVPN designs:

-   Inter-AS Option B: change BGP next hop on AS boundary, and stitch EVPN MPLS labels at AS boundary. Like with MPLS/VPN, AS boundary routers would have to contain forwarding information for all VPNs (VLANs and VRFs) stretching across the AS boundary.
-   Inter-AS Option C: retain the original BGP next hop, and stitch MPLS labels for BGP next hops at AS boundary. Network operators using BGP autonomous systems in the way they were designed to be used (*collection of connected prefixes under control of a single administrative entity*) rarely use Inter-AS Option C because it requires unlimited MPLS connectivity between PE-routers in different autonomous systems.

Situation is a bit different when using EVPN with VXLAN encapsulation. There's no need for a hop-by-hop LSP between ingress and egress device -- all they need is IP transport provided by the network core. It's therefore best to leave BGP next hop (egress VXLAN Tunnel Endpoint -- VTEP) unchanged unless you're hitting the scalability limits of ASIC forwarding tables -- an equivalent to Inter-AS Option&nbsp;C.

{{<figure src="/2018/05/s1600-Multi-Pod+Overlay+Control+Plane.png" caption="Multi-pod EBGP - next hop is unchanged (diagram by Lukas Krattiger)">}}

{{<note>}}The diagrams were taken from [Using VXLAN and EVPN in Multi-Pod and Multi-Site Fabric](https://my.ipspace.net/bin/get?doc=73f25e70-31cd-11e8-b156-005056880254) presentation by Lukas Krattiger -- part of [Multi-Pod and Multi-Site Fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) section of [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.{{</note>}}

A VXLAN equivalent to MPLS Inter-AS Option B is harder to implement. In this scenario, the AS boundary device changes BGP next hop, becoming an endpoint of VXLAN tunnels.

{{<figure src="/2018/05/s1600-Multi-Site+Hierarchical+Control+Plane.png" caption="BGP next hop is changed on fabric boundary (diagram by Lukas Krattiger)">}}

The border gateway (device changing BGP next hop on fabric boundary) has to be able to:

-   Receive VXLAN-encapsulated packet;
-   Perform forwarding based on MAC address toward the next-hop VTEP, including split-horizon flooding;
-   Re-encapsulate the forwarded Ethernet frame into another VXLAN packet.

{{<figure src="/2018/05/s1600-Multi-Site+Border+Gateway.png" caption="Border gateways perform VXLAN-to-VXLAN forwarding (diagram by Lukas Krattiger)">}}

While recent merchant silicon ASICs implement RIOT (Routing In-and-Out of VXLAN Tunnels), [very few of them can do bridging In-and-Out of VXLAN Tunnels](/2022/06/vxlan-bridging-dci/) -- the mandatory prerequisite for Inter-AS Option&nbsp;B.

{{<note info>}}For more details watch [Implementing true multi-site layer-2 fabrics with Cisco's ASICs](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) in [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar -- Lukas Krattiger did a great job explaining the intricacies of multi-site fabrics with VXLAN-to-VXLAN bridging at the fabric edge.{{</note>}}

### More EVPN information

-   An [overview of using BGP in data center fabrics](http://www.ipspace.net/Data_Center_BGP) including [EVPN considerations](http://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics).
-   [EVPN Deep Dive](http://www.ipspace.net/EVPN_Technical_Deep_Dive) (focused on data center fabrics using VXLAN).

### Revision History

2023-03-01
: Added a link to a blog post describing VXLAN-to-VXLAN bridging ASIC implementations.
