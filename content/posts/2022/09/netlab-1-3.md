---
date: 2022-09-05 07:05:00+00:00
netlab_tag: release
series_title: VXLAN and EVPN (Release 1.3)
tags:
- netlab
title: 'netlab Release 1.3: VXLAN and EVPN'
---
*netlab* release 1.3 contains two major additions:

* [VXLAN transport](https://netlab.tools/module/vxlan/) using static ingress replication or EVPN control plane -- implemented on Arista EOS, Cisco Nexus OS, Dell OS10, Nokia SR Linux and VyOS.
* [EVPN control plane](https://netlab.tools/module/evpn/) supporting VXLAN transport, VLAN bridging, VLAN-aware bundles, and symmetric IRB -- implemented on Arista EOS, Dell OS10, Nokia SR Linux, Nokia SR OS (control plane), VyOS, and FRR (control plane).

Here are some of the other goodies included in this release:
<!--more-->
* [MPLS 6PE](https://netlab.tools/module/mpls/) implemented on Arista EOS, Cisco IOS, and Cisco IOS XE
* [Default route origination on EBGP sessions](https://netlab.tools/plugins/ebgp.utils/)
* [gRPC client installation script](https://netlab.tools/netlab/install/)
* VLANs and VRFs on Cisco Nexus OS
* VRFs on Nokia SR Linux
* Complete implementation of VLAN interfaces on Nokia SR Linux
* Statically configured IPv6 hosts on Cisco IOS and Arista EOS

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).