---
title: "netlab 1.9.3: MLAG, Static Routes, Node Cloning"
series_title: "MLAG, Static Routes, Node Cloning"
date: 2025-01-10 08:15:00+01:00
tags: [ netlab ]
netlab_tag: release
---
[_netlab_ release 1.9.3](https://netlab.tools/release/1.9/#release-1-9-3) brings these new features:

* [Multi-chassis Link Aggregation (MLAG)](https://netlab.tools/module/lag/) on Arista EOS, Aruba CX, Cumulus NVUE, and Dell OS10
* [VRF and VLAN groups](https://netlab.tools/groups/)
* Additional [OSPF interface parameters](https://netlab.tools/module/ospf/#ospf-interface-support) (hello and dead timers, cleartext passwords, and DR priority) implemented on Arista EOS, Aruba CX, Cisco IOS/IOS-XE, Cisco Nexus OS, Cumulus Linux, Dell OS10, and FRRouting
* [Static routes](https://netlab.tools/module/routing/#generic-routing-static) with direct or indirect next hops implemented on Arista EOS, Cisco IOS/IOS-XE, FRRouting, and Linux
* [Node cloning plugin](https://netlab.tools/plugins/node.clone/) for users who want to build detailed digital twins of their networks.
* [Consistent selection of default address pools](https://netlab.tools/links/#links-default-pools) based on the number of nodes attached to a link (this could [change addressing in multi-provider topologies](https://netlab.tools/release/1.9/#release-1-9-3-breaking))
* Support for [vjunos-router](https://netlab.tools/platforms/#platform-devices) and [Cisco NSO tool](https://netlab.tools/extool/nso/).

Other new features include:
<!--more-->

* FRR VM uses Debian/Bookworm
* Bird container uses Ubuntu 24.04
* Containerlab stub links use **dummy** interfaces, removing the need for extra Linux bridges
* FRRouting supports RFC 8950-style IPv4 next hops over regular IPv6 EBGP sessions
* You can use `--feature` flag with the **netlab show modules** command to display support for a single optional feature
* STP is disabled on libvirt-created bridges to avoid interference with the STP Configuration Module
* Per-node device features allow you to tweak which features individual lab nodes support
* Most OSPF parameters can be set on the topology- or node level, including the default **passive** state
* **netlab validate** prints time spent in every successful validation test.

### Upgrading or Starting from Scratch?

* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
