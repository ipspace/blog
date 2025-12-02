---
title: "Lab: More Complex VXLAN Deployment Scenario"
series_title: "More Complex VXLAN Deployment Scenario"
date: 2025-12-05 07:22:00+0100
tags: [ EVPN, VXLAN ]
evpn_tag: labs
---
In the [first VXLAN lab](https://evpn.bgplabs.net/vxlan/1-single/), we covered the very basics. Now it's time for a few essential concepts (before introducing the EVPN control plane or integrated routing and bridging):

* Each VXLAN segment could have a different set of VTEPs (used to build the BUM flooding list)
* While the VXLAN Network Identifier (VNI) must be unique across the participating VTEPs, you could map different VLAN IDs into a single VNI (allowing you to merge two VLAN segments over VXLAN)
* Neither VXLAN VNI nor VLAN ID has to be globally unique (but it helps to make them unique to remain sane)
<!--more-->
You can practice these topics in the [More Complex VXLAN Deployment Scenario](https://evpn.bgplabs.net/vxlan/2-complex/) lab exercise.

{{<figure src="https://evpn.bgplabs.net/vxlan/topology-complex.png">}}

You can run the lab on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).
