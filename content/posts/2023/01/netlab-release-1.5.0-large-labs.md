---
date: 2023-01-30 07:24:00+00:00
netlab_tag: archive
series_title: Larger Lab Topologies (Release 1.5.0)
tags:
- netlab
title: 'netlab Release 1.5.0: Larger Lab Topologies'
---
_netlab_ release 1.5.0 includes features that will help you start very large lab topologies (someone managed to run over 90 Mikrotik routers on a 24-core server):

* You can [start *libvirt* virtual machines in batches](https://netlab.tools/labs/libvirt/#starting-virtual-machines-in-batches) to reduce the CPU overload that causes startup failures on large topologies.
* You can [combine virtual machines and containers in the same lab](https://netlab.tools/providers/#combining-virtualization-providers), further reducing the memory footprint for devices available as true containers (Linux hosts, Cumulus/FRR routers, Arista cEOS)
* Use [custom management network IP subnet](https://netlab.tools/labs/libvirt/#libvirt-management-network) if you're running out of management IP addresses

To get more details and learn about additional features included in release 1.5.0, [read the release notes](https://netlab.tools/release/1.5/#release-1-5-0). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
