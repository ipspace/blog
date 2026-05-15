---
title: "Lab: EVPN Asymmetric IRB with Anycast Gateways"
series_title: "EVPN Asymmetric IRB with Anycast Gateways"
date: 2026-05-15 07:52:00+0200
tags: [ EVPN, VXLAN ]
evpn_tag: labs
---
I postponed the discussion of ARP issues with EVPN anycast gateways to keep [yesterday's blog post](/2026/05/arp-issues-evpn-asymmetric-irb/) reasonably short. If you're impatient and want to try that out, I have [just the right lab exercise](https://evpn.bgplabs.net/evpn/4-asym-irb/) for you; you'll have to extend VLANs into end-to-end MAC-VRF instances and add IRB and anycast gateways:

{{<figure src="https://evpn.bgplabs.net/evpn/topology-asymmetric-irb.png" width="400">}}

{{<jump>}}[Explore the lab exercise](https://evpn.bgplabs.net/evpn/4-asym-irb/){{</jump>}}

You can run the lab on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).
