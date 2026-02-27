---
title: "Lab: More Complex EVPN/VXLAN Bridging Scenario"
series_title: "More Complex EVPN/VXLAN Bridging Scenario"
date: 2026-02-27 09:13:00+0100
tags: [ EVPN, VXLAN ]
evpn_tag: labs
---
In the first EVPN/VXLAN lab, we [added the EVPN control plane to bridging over VXLAN](https://evpn.bgplabs.net/evpn/1-bridging/).  Now, let's try out a more complex scenario: several EVPN MAC-VRFs mapped to different VLAN segments on individual PE-devices.

{{<figure src="https://evpn.bgplabs.net/evpn/topology-complex.png" width="400">}}

{{<jump>}}[Explore the lab exercise](https://evpn.bgplabs.net/evpn/2-complex/){{</jump>}}

You can run the lab on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).
