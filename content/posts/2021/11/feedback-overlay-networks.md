---
title: "Overlay Virtual Networking Examples"
date: 2021-11-15 09:21:00
tags: [ overlay networks, VXLAN, NSX ]
---
One of ipSpace.net subscribers wanted to see a real-life examples in the Overlay Virtual Networking webinar:

> I would be nice to have real world examples. The webinar lacks of contents about how to obtain a fully working L3 fabric overlay network, including gateways, vrfs, security zones, etc... I know there is not only one "design for all" but a few complete architectures from L2 to L7 will be appreciated over deep-dives about specific protocols or technologies.

Most ipSpace.net webinars are bits of a larger puzzle. In this particular case:
<!--more-->
* The _[Overlay Virtual Networking](https://www.ipspace.net/Overlay_Virtual_Networking)_ webinar addresses the principles of overlay networking, including packet flows and gateways with the outside world.
* The implementation details are by definition product-specific, and depend on whether you’re implementing overlay virtual networks in software (hypervisors or containers) or in hardware (ToR switches). The fundamental differences between a sample software and a sample hardware approach are described in _[VMware NSX, Cisco ACI or Standard-Based EVPN - www.ipSpace.net](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN)_
* You’ll find product-specific details in _[Cisco ACI Deep Dive](https://www.ipspace.net/Cisco_ACI_Deep_Dive)_ and _[VMware NSX Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)_ webinars..
* For more information on VXLAN/EVPN-based approaches to overlay virtual networking, watch _[VXLAN Technical Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive)_ and _[EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)_. The EVPN webinar includes topics like [EVPN multihoming](https://my.ipspace.net/bin/list?id=EVPN#MH) and [service insertion](https://my.ipspace.net/bin/list?id=EVPN#L47SVC).

so it's always worth exploring the whole roadmap. Admittedly, the Cloud Infrastructure roadmap is not exactly helpful