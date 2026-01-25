---
title: "Lab: VXLAN Bridging with EVPN Control Plane"
series_title: "VXLAN Bridging with EVPN Control Plane"
date: 2026-01-27 07:59:00+0100
tags: [ EVPN, VXLAN ]
evpn_tag: labs
---
In the previous [VXLAN labs](https://evpn.bgplabs.net/#vxlan), we covered the [basics of Ethernet bridging over VXLAN](https://evpn.bgplabs.net/vxlan/1-single/) and a [more complex scenario with multiple VLANs](https://evpn.bgplabs.net/vxlan/2-complex/). 

Now let's [add the EVPN control plane into the mix](https://evpn.bgplabs.net/evpn/1-bridging/). The data plane (VLANs mapped into VXLAN-over-IPv4) will remain unchanged, but we'll use EVPN (a BGP address family) to build the ingress replication lists and MAC-to-VTEP mappings.
<!--more-->
We'll use the same lab topology as in the [Extend a Single VLAN Segment with VXLAN](https://evpn.bgplabs.net/vxlan/1-single/) exercise (with the IBGP session between the switches), enable the EVPN address family on the IBGP session, and configure an EVPN MAC-VRF.

{{<figure src="https://evpn.bgplabs.net/evpn/topology-bridging.png">}}

{{<jump>}}[Explore the lab exercise](https://evpn.bgplabs.net/evpn/1-bridging/){{</jump>}}

You can run the lab on your own _netlab_-enabled infrastructure ([more details](https://evpn.bgplabs.net/1-setup/)), but also within a [free GitHub Codespace](https://evpn.bgplabs.net/4-codespaces/) or even on your Apple-silicon Mac ([installation](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/), [using Arista cEOS container](https://blog.ipspace.net/2025/02/arista-ceos-arm-apple-silicon/), [using VXLAN/EVPN labs](https://evpn.bgplabs.net/1-setup/#defaults)).
