---
title: "netsim-tools Release 1.1.2"
date: 2022-02-02 07:23:00
tags: [ automation ]
series: netsim
netsim_tag: release
---
Every time I'm writing *netsim-tools* release notes I'm amazed at the number of features we managed to put together in just a few weeks.

{{<figure src="/2022/02/netsim-1.1.2-insights.png">}}

Here are the goodies from *netsim-tools* releases 1.1.1 and 1.1.2:
<!--more-->
**New devices**:

- [Cumulus Linux 5.0](https://netsim-tools.readthedocs.io/en/latest/platforms.html) with NVUE-based configuration
- [Hosts and default gateways](https://netsim-tools.readthedocs.io/en/latest/links.html#hosts-and-default-gateways)

**New features**:
- [Unnumbered EBGP sessions](https://netsim-tools.readthedocs.io/en/latest/module/bgp.html#notes-on-unnumbered-ebgp-sessions) on Cumulus VX
- [Open vSwitch support in containerlab](https://netsim-tools.readthedocs.io/en/latest/labs/clab.html#lan-bridges)
- Proof-of-concept [EVPN](https://netsim-tools.readthedocs.io/en/latest/module/evpn.html) and [SRv6](https://netsim-tools.readthedocs.io/en/latest/module/srv6.html) modules
<!--more-->
**Configurable parameters**:

- [System and interface MTU](https://netsim-tools.readthedocs.io/en/latest/links.html#changing-mtu)
- [VM memory and CPU settings](https://netsim-tools.readthedocs.io/en/latest/nodes.html#node-attributes)
- [Router ID calculations](https://netsim-tools.readthedocs.io/en/latest/example/addressing-tutorial.html#using-built-in-address-pools) for IPv6-only devices and [configurable router ID](https://netsim-tools.readthedocs.io/en/latest/module/ospf.html#node-parameters)
- [Configurable BGP cluster ID](https://netsim-tools.readthedocs.io/en/latest/module/bgp.html#node-configuration-parameters)
- [Static loopback addresses](https://netsim-tools.readthedocs.io/en/latest/nodes.html#node-attributes)

**Installation improvements**:

- Building [vEOS](https://netsim-tools.readthedocs.io/en/latest/labs/eos.html) and [Nexus 9300v](https://netsim-tools.readthedocs.io/en/latest/labs/nxos.html) libvirt boxes has been significantly simplified with **netlab libvirt package** command
- [Containerlab installation script](https://netsim-tools.readthedocs.io/en/latest/netlab/install.html)

**Other goodies:**

-   BGP graphs can [show RR-client sessions as directed arrows](https://netsim-tools.readthedocs.io/en/latest/outputs/graph.html)
