---
date: 2022-10-10 06:22:00+00:00
netlab_tag: archive
series_title: Mikrotik RouterOS 7, Additional EVPN Platforms (Release 1.3.2)
tags:
- netlab
title: 'netlab Release 1.3.2: Mikrotik RouterOS 7, Additional EVPN Platforms'
---
The star of the [*netlab* release 1.3.2](https://netlab.tools/release/1.3/) is [Mikrotik RouterOS version 7](https://netlab.tools/platforms/). Stefano Sasso did a fantastic job adding support for VLANs, VRFs, OSPFv2, OSPFv3, BGP, MPLS, and MPLS/VPN, plus the libvirt [box-building recipe](https://netlab.tools/labs/routeros7/).

Jeroen van Bemmel contributed another major PR[^PR] adding VLANs, VRFs, VXLAN, EVPN, and OSPFv3 to Nokia SR OS.

Other platform improvements include:
<!--more-->
* OSPFv3 on Cumulus Linux and Cisco Nexus OS
* EVPN on Cisco Nexus OS
* EVPN VLAN bundle service on Nokia SR Linux
* EVPN over IPv6 LLA sessions on Cumulus Linux and FRR
* BGP local-as on EBGP VRF sessions on Cumulus Linux
* Configurable BGP address families on VyOS and Dell OS10

[^PR]: Pull Request, not press release ;)

We also added new functionality, including:

* Static IPv4/IPv6 addresses on containerlab management network
* EVPN transit VNI [shared between VRFs](https://netlab.tools/module/evpn/#integrated-routing-and-bridging)
* [Define VLAN and VRF parameters in groups](https://netlab.tools/groups/#using-group-node-data-with-vrfs-and-vlans)
* [Disable OSPF, EIGRP, or IS-IS on a link or an interface](https://netlab.tools/module/routing/#routing-disable)
* [Disable EBGP sessions on a link or an interface](https://netlab.tools/module/routing/#routing-disable)

Upgrading is as easy as ever: execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
