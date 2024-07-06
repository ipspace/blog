---
date: 2022-03-07 09:53:00+00:00
netlab_tag: archive
tags:
- netlab
title: netsim-tools Release 1.1.3
---
*netsim-tools* release 1.1.3 brings a number of goodies, including:

* [OSPFv3 support](https://netlab.tools/module/ospf/) on a few platforms (we're still [looking for contributors to implement OSPFv3 on other platforms](/2022/03/contribute-netsim-ospf.html))
* EIGRP implementation of [common routing protocol features](https://netlab.tools/module/routing/) (router ID, passive and external interfaces)
* [Configurable address family support](https://netlab.tools/module/routing/#af) for IS-IS, OSPF and EIGRP
* Support for /31 IPv4 P2P links
* Configurable MTU for VyOS and RouterOS

{{<note info>}}Starting with release 1.3, we [renamed *netsim-tools* to *netlab*](/2022/08/netsim-netlab.html).{{</note>}}
<!--more-->
If you're building your own *libvirt* boxes, you might also appreciate:

* **[netlab show](https://netlab.tools/netlab/show/)** command displays system settings (including image names) in tabular format
* [Restructured installation documentation](https://netlab.tools/install/)
* Box creating scripts for [Cisco CSR 1000v](https://netlab.tools/labs/csr/) and [Juniper vSRX 3.0](https://netlab.tools/labs/vsrx/)

The final tidbits:

* **[netlab up](https://netlab.tools/netlab/up/)** has new flags: `--no-config` and `--fast-config`
* **[netlab install](https://netlab.tools/netlab/install/)** installs Vagrant from Hashicorp repository

To upgrade *netsim-tools*, use `pip3 install --upgrade netsim-tools`; if you're starting from scratch, read the [installation instructions](https://netlab.tools/install/).
