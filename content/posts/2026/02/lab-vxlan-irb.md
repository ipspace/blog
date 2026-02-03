---
title: "Lab: Routing Between VXLAN Segments"
series_title: "Routing Between VXLAN Segments"
date: 2026-02-06 07:59:00+0100
tags: [ EVPN, VXLAN ]
evpn_tag: labs
redirect: https://evpn.bgplabs.net/vxlan/3-irb/
---
In the previous [EVPN/VXLAN lab exercises](https://evpn.bgplabs.net/), we covered the [basics of Ethernet bridging over VXLAN](https://evpn.bgplabs.net/vxlan/1-single/) and the [use of the EVPN control plane](https://evpn.bgplabs.net/evpn/1-bridging/) to build layer-2 segments.

It's time to move up the protocol stack. Let's see how you can route between VXLAN segments, this time using unique unicast IP addresses on the layer-3 switches.

{{<figure src="https://evpn.bgplabs.net/vxlan/topology-irb.png">}}

{{<jump>}}[Explore the lab exercise](https://evpn.bgplabs.net/vxlan/3-irb/){{</jump>}}

You can run the lab on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).
