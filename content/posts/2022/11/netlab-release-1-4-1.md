---
date: 2022-11-28 07:12:00+00:00
netlab_tag: release
series_title: Cisco ASAv (Release 1.4.1)
tags:
- netlab
title: 'netlab Release 1.4.1: Cisco ASAv'
---
The star of the [*netlab* release 1.4.1](https://netlab.tools/release/1.4/) is [Cisco ASAv support](https://netlab.tools/platforms/): IPv4 and IPv6 addressing, IS-IS and BGP, and libvirt box building instructions.

Other new features include:

* [VRRP](https://netlab.tools/module/gateway/) on VyOS
* [Anycast gateway and VRRP](https://netlab.tools/module/gateway/) on Dell OS10 (with a [bunch of caveats](https://netlab.tools/caveats/#dell-os10))
* Unnumbered OSPF interfaces on VyOS
* Support for all [EVPN bundle services](https://netlab.tools/module/evpn/#evpn-bundle-services)
* FRR version 8.4.0

Upgrading is as easy as ever: execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
