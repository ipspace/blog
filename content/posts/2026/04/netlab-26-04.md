---
title: "netlab 26.04: EXOS, BGP Prefix Origination, More Static Routes"
series_title: "EXOS, BGP Prefix Origination, More Static Routes (Release 26.04)"
date: 2026-04-13 07:28:00+02:00
tags: [ netlab ]
netlab_tag: release
---
_netlab_ release 26.04 is out. Here are the highlights:

- **Extreme Networks EXOS** is supported as a Vagrant box or containerlab node with OSPF, VLAN, and VRRP configuration (by [Seb d’Argoeuves](https://github.com/sdargoeuves)).
- The new [**bgp.advertise**](https://netlab.tools/module/bgp/#bgp-advertise-prefix) node attribute allows you to advertise networks in the IP routing table into BGP. It’s supported on most platforms.
- The **bgp.originate** attribute is now [dual-stack and VRF-aware](https://netlab.tools/module/bgp/#bgp-advertise-prefix), allowing you to originate IPv4 and IPv6 prefixes into per-VRF BGP instances.
- New platforms with static route support: **FortiOS** (by [Aleksey Popov](https://github.com/a-v-popov)), **Nexus OS**, **Nokia SR OS**, **Nokia SR Linux**. **OpenBSD** got *discard* static routes.

<!--more-->

Want more? How about:

- **EVPN/VXLAN-over-IPv6** is now supported on **FRRouting** ([interoperability with EOS](/2026/04/frr-evpn-ipv6-pmsi/) coming with the next FRR release).
- You can use [OSPF area parameters](https://netlab.tools/plugins/ospf.areas/#plugin-ospf-areas) with **BIRD** and BGP confederations with **Junos**.
- You can use **bgp.import** parameter on **Junos** to [import routes](https://netlab.tools/module/routing_protocols/#routing-import) into global and VRF BGP instances. Other routing protocols are planned for the next release (once we figure out the optimal [Junos routing policy chains](https://github.com/ipspace/netlab/issues/3285))

For even more details, check the [release notes](https://netlab.tools/release/26.04/).

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
