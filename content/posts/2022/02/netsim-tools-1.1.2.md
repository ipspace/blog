---
date: 2022-02-02 07:23:00+00:00
netlab_tag: archive
tags:
- netlab
title: netsim-tools Release 1.1.2
---
Every time I'm writing *netsim-tools* release notes I'm amazed at the number of features we managed to put together in just a few weeks.

{{<figure src="/2022/02/netsim-1.1.2-insights.png">}}

{{<note info>}}Starting with release 1.3, we [renamed *netsim-tools* to *netlab*](/2022/08/netsim-netlab.html).{{</note>}}

Here are the goodies from *netsim-tools* releases 1.1.1 and 1.1.2:
<!--more-->
**New devices**:

- [Cumulus Linux 5.0](https://netlab.tools/platforms/) with NVUE-based configuration
- [Hosts and default gateways](https://netlab.tools/links/#hosts-and-default-gateways)

**New features**:
- [Unnumbered EBGP sessions](https://netlab.tools/module/bgp/#notes-on-unnumbered-ebgp-sessions) on Cumulus VX
- [Open vSwitch support in containerlab](https://netlab.tools/labs/clab/#lan-bridges)
- Proof-of-concept [EVPN](https://netlab.tools/module/evpn/) and [SRv6](https://netlab.tools/module/srv6/) modules
<!--more-->
**Configurable parameters**:

- [System and interface MTU](https://netlab.tools/links/#changing-mtu)
- [VM memory and CPU settings](https://netlab.tools/nodes/#node-attributes)
- [Router ID calculations](https://netlab.tools/example/addressing-tutorial/#using-built-in-address-pools) for IPv6-only devices and [configurable router ID](https://netlab.tools/module/ospf/#node-parameters)
- [Configurable BGP cluster ID](https://netlab.tools/module/bgp/#node-configuration-parameters)
- [Static loopback addresses](https://netlab.tools/nodes/#node-attributes)

**Installation improvements**:

- Building [vEOS](https://netlab.tools/labs/eos/) and [Nexus 9300v](https://netlab.tools/labs/nxos/) libvirt boxes has been significantly simplified with **netlab libvirt package** command
- [Containerlab installation script](https://netlab.tools/netlab/install/)

**Other goodies:**

-   BGP graphs can [show RR-client sessions as directed arrows](https://netlab.tools/outputs/graph/)
