---
title: "netlab 25.07: Summaries and Confederations"
series_title: "Summarization and Confederations (Release 25.07)"
date: 2025-07-15 08:27:00+01:00
tags: [ netlab ]
netlab_tag: release
---
[*netlab* release 25.07](https://netlab.tools/release/25.07/) was published yesterday. The major new features include:

* The [ospf.areas plugin](https://netlab.tools/plugins/ospf.areas/) supports OSPFv2 and OSPFv3 stub areas, NSSA areas, and area ranges.
* The [BGP routing policies](https://netlab.tools/plugins/bgp.policy/) plugin supports aggregate BGP routes
* The [BGP configuration module](https://netlab.tools/module/bgp/) supports BGP confederations

But wait, there's much more:
<!--more-->
* [Stefano Sasso](https://www.linkedin.com/in/ssasso/) added the [evpn.multihoming](https://netlab.tools/plugins/evpn.multihoming/#plugin-evpn-multihoming) plugin that implements EVPN Ethernet Segment Identifiers and EVPN-based MLAG/multihoming
* [Remi Locherer](https://www.linkedin.com/in/remilocherer/) persuaded me to add OpenBSD support. He also implemented the final touches of the *initial configuration* support, such as the IPv6 router advertisement messages.
* [Urs Baumann](https://www.linkedin.com/in/ubaumannch/) integrated his [Network Unit Testing System (NUTS)](https://github.com/network-unit-testing-system/nuts) with netlab.
* We finally cleaned up the [installation process](https://netlab.tools/netlab/install/#netlab-install). It has a more consistent user interface, checks the Linux distribution you're using, and sorts the installation scripts in dependency order.

New device features include STP and LAG on Cisco IOS, traditional VLAN interfaces on Dell OS10, multi-VDOM mode on Fortinet, and LAG on VyOS.

Finally, we decided to document the [*support level* of various platforms](https://netlab.tools/platforms/#supported-virtual-network-devices)[^SPR] (you can also see them in the **netlab show devices** printout), and included the major caveats (like "don't use Cumulus containers" and "the vagrant account on Cumulus Vagrant boxes has an expired password") in the **netlab show images** printout.

[^SPR]: You don't like seeing your favorite platform has a *minimal* level of support? Become a contributor!

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
