---
title: "Lab: Implementing VRF-Lite with VXLAN"
series_title: "Implementing VRF-Lite with VXLAN"
date: 2026-06-05 08:21:00+0100
tags: [ EVPN, VXLAN ]
evpn_tag: labs
---
Did you know that you can implement a VRF-Lite design with VXLAN? All you need are devices that can run VRF routing protocols over VXLAN-backed VLAN segments.

Compared to the "traditional" VRF-Lite design, in which you need a set of VLANs on every link and every device running the routing protocol for every VRF, the VXLAN-based design needs just IP routing on the core switches, resulting in a design that's pretty close to what we were building with DMVPN (without IPsec and NHRP complications).
<!--more-->
Intrigued? You can try it out in the [Implement VRF-Lite with VXLAN](https://evpn.bgplabs.net/vxlan/5-vrf-lite/) lab exercise.

{{<figure src="https://evpn.bgplabs.net/vxlan/topology-vrf-lite.png">}}

You can run the lab on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).

{{<jump>}}[Explore the lab exercise](https://evpn.bgplabs.net/vxlan/5-vrf-lite/){{</jump>}}
