---
title: "netsim-tools Release 1.2.1: More MPLS and VRFs, Dell OS10, Cumulus 5.0 on Containerlab"
date: 2022-04-21 07:41:00
tags: [ automation ]
series: netsim
netsim_tag: release
---
I already mentioned the [netsim-tools Easter Egg](/2022/04/netsim-tools-better-with-gui.html), here are the other cool features shipping in release 1.2.1:

- [Dell OS10 on *libvirt*](https://netsim-tools.readthedocs.io/en/latest/labs/dellos10.html) (including BGP, OSPFv2, OSPFv3 and VRF Lite) by Stefano Sasso
- [VRFs, MPLS, and MPLS/VPN support](https://netsim-tools.readthedocs.io/en/latest/platforms.html#platform-module-support) on Mikrotik RouterOS and VyOS by Stefano Sasso
- [Containerlab support for Cumulus 5.0 with NVUE](https://netsim-tools.readthedocs.io/en/latest/platforms.html#platform-provider-support) including [Simple VRF-Lite](https://netsim-tools.readthedocs.io/en/latest/module/vrf.html#module-vrf-platform-support) by Julien Dhaille

To upgrade *netsim-tools*, use `pip3 install --upgrade netsim-tools`; if you're starting from scratch, read the [installation instructions](https://netsim-tools.readthedocs.io/en/latest/install.html).
