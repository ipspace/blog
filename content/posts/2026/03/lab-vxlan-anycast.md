---
title: "Lab: Anycast Gateways on VXLAN Segments"
series_title: "Anycast Gateways on VXLAN Segments"
date: 2026-03-20 08:09:00+0100
tags: [ EVPN, VXLAN ]
evpn_tag: labs
---
Most vendors "discovered" anycast gateways when they tried implementing routing between MAC-VRFs in an EVPN environment and hit all the usual tripwires (more about that later). A few exceptions (like [Arista](/2013/06/arista-eos-virtual-arp-varp-behind/)) supported them on VLAN segments for over a decade, and it was a no-brainer to extend that support to VXLAN segments.

Want to try out how that works? The [Anycast Gateways on VXLAN Segments](https://evpn.bgplabs.net/vxlan/4-anycast/) lab exercise is just what you need.

{{<figure src="https://evpn.bgplabs.net/vxlan/topology-anycast.png">}}

You can run the lab on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).

{{<jump>}}[Explore the lab exercise](https://evpn.bgplabs.net/vxlan/4-anycast/){{</jump>}}
