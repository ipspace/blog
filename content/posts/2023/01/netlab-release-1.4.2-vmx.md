---
date: 2023-01-09 07:20:00+00:00
netlab_tag: archive
series_title: Juniper vMX and Junos/CSR1000v Features (Release 1.4.2)
tags:
- netlab
title: 'netlab Release 1.4.2: Juniper vMX and Junos Features'
---
One of the last things I did before going on the Christmas break was to push out [netlab release 1.4.2](https://netlab.tools/release/1.4/#release-1-4-2). Its highlights include:

- [Juniper vMX](https://netlab.tools/platforms/) by [Stefano Sasso](https://www.linkedin.com/in/ssasso)
- BFD, VRF, MPLS, SR-MPLS, and MPLS/VPN on Junos (also by Stefano)
- Full VLAN support on vMX and routed VLAN interfaces on vSRX (yet again, Stefano's contribution)
- VyOS containerlab support by [Oleg A. Arkhangelsky](https://github.com/sysoleg)
- CSR 1000v VLAN and VXLAN support

Upgrading is as easy as ever: execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
