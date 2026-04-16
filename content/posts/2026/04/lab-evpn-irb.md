---
title: "Lab: Integrated Routing and Bridging (IRB) with EVPN MAC-VRF Instances"
series_title: "Integrated Routing and Bridging (IRB) with EVPN MAC-VRF Instances"
date: 2026-04-17 08:13:00+0200
tags: [ EVPN, VXLAN ]
evpn_tag: labs
---
Most EVPN documentation rushes into the complexities of symmetric IRB, type-5 EVPN routes, and EVPN IP-VRFs, but if you want to master a technology, it's better to take it slow and proceed with small steps. In [today's lab exercise](https://evpn.bgplabs.net/evpn/3-irb/), we'll do just that: explore what happens when you add IP addresses (we'll use anycast gateways) to VLAN interfaces tied to EVPN MAC-VRF instances.

{{<figure src="https://evpn.bgplabs.net/evpn/topology-irb.png" width="400">}}

{{<jump>}}[Explore the lab exercise](https://evpn.bgplabs.net/evpn/3-irb/){{</jump>}}

You can run the lab on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).
