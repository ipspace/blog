---
title: "New Project: Open-Source VXLAN/EVPN Labs"
series_title: "Extend a Single VLAN Segment with VXLAN"
date: 2025-10-30 08:11:00+0100
tags: [ EVPN, VXLAN ]
evpn_tag: labs
---
After launching the [BGP labs](https://bgplabs.net/) in 2023 and [IS-IS labs](https://isis.bgplabs.net/) in 2024, it was time to start another project that was quietly sitting on the back burner for ages: open-source (and free) [VXLAN/EVPN labs](https://evpn.bgplabs.net/).

The first lab exercise is already online and expects you to [extend a single VLAN segment](https://evpn.bgplabs.net/vxlan/1-single/) across an IP underlay network using VXLAN encapsulation with static ingress replication.
<!--more-->
{{<figure src="https://evpn.bgplabs.net/vxlan/topology-single.png">}}

You can use the labs on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).

I also collected [a long list of ideas](https://evpn.bgplabs.net/3-upcoming/) for future lab exercises. Further suggestions are most welcome; leave them in comments or send me an email.
 