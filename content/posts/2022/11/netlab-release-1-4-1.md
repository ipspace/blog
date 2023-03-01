---
date: 2022-11-28 07:12:00+00:00
netlab_tag: release
series_title: Cisco ASAv (Release 1.4.1)
tags:
- netlab
title: 'netlab Release 1.4.1: Cisco ASAv'
---
The star of the [*netlab* release 1.4.1](https://netsim-tools.readthedocs.io/en/latest/release/1.4.html) is [Cisco ASAv support](https://netsim-tools.readthedocs.io/en/latest/platforms.html): IPv4 and IPv6 addressing, IS-IS and BGP, and libvirt box building instructions.

Other new features include:

* [VRRP](https://netsim-tools.readthedocs.io/en/latest/module/gateway.html) on VyOS
* [Anycast gateway and VRRP](https://netsim-tools.readthedocs.io/en/latest/module/gateway.html) on Dell OS10 (with a [bunch of caveats](https://netsim-tools.readthedocs.io/en/latest/caveats.html#dell-os10))
* Unnumbered OSPF interfaces on VyOS
* Support for all [EVPN bundle services](https://netsim-tools.readthedocs.io/en/latest/module/evpn.html#evpn-bundle-services)
* FRR version 8.4.0

Upgrading is as easy as ever: execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netsim-tools.readthedocs.io/en/latest/tutorials.html) and the [installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html).
