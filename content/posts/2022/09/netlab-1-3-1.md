---
date: 2022-09-19 07:08:00+00:00
netlab_tag: release
series_title: BGP local-as, FRR and Cumulus Data Plane Enhancements (Release 1.3.1)
tags:
- netlab
title: 'netlab Release 1.3.1: BGP local-as, FRR and Cumulus Data Plane Enhancements'
---
*netlab* release 1.3.1 contains major additions to FRR and Cumulus Linux, and new BGP features:

* VXLAN, VLANs, VRFs, and EVPN [implemented on](https://netlab.tools/platforms/#platform-dataplane-support) FRR and Cumulus Linux
* [BGP local-as](https://netlab.tools/module/bgp/#node-configuration-parameters) implemented in the BGP configuration module and supported on Arista EOS, Cisco IOS, Dell OS10, FRR, and Nokia SR Linux.
* Configurable [BGP transport sessions](https://netlab.tools/module/bgp/#node-configuration-parameters)
* Configurable [default BGP address families](https://netlab.tools/module/bgp/#node-configuration-parameters) supported on Arista EOS, Cisco IOS, Cumulus Linux, FRR, and Nokia SR Linux.

Here are some of the other goodies included in this release:
<!--more-->

* FRR support for IPv6 LLA (unnumbered) BGP sessions
* New default container and VM versions: FRR 8.3.1, Cumulus Linux 4.4.0 (container), Cumulus Linux with NVUE 5.2.0 (VM)
* Per-VRF BGP router ID implemented on Cisco IOS and Arista EOS
* [Select address pools](https://netlab.tools/links/#selecting-custom-address-pools) with **pool** VLAN or link attribute (using **role** attribute to select an addressing pool is deprecated)
* Add **message** attribute to lab topology to display a ‘this is how you use this lab’ help message after the lab is started and configured
* Implement ‘startup configuration’ parameter for containerlab
* Device configuration files can be created from *netlab* templates and mapped into containers. Currently used to start FRR daemons in FRR 8.3.1 container.
* Add multiple debugging flags to debug just parts of the data transformation code

Finally, in the *I shouldn't be mentioning it, but here we go* department:

* BGP local-as can be used on some platforms to turn an EBGP session into an IBGP session.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
