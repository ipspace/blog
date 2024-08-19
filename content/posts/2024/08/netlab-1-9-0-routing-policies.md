---
title: "netlab 1.9.0: Routing Policies, Default Routes, Route Redistribution"
series_title: "Routing Policies, Default Routes, Route Redistribution (Release 1.9.0)"
date: 2024-08-20 07:27:00+02:00
tags: [ netlab ]
netlab_tag: release
---
[_netlab_ release 1.9.0](https://netlab.tools/release/1.9/) brings tons of new routing features:

* [Generic Routing Configuration Module](https://netlab.tools/module/routing/#generic-routing) implements routing policies (route maps), prefix filters, AS-path filters, and BGP community filters.
* [Default route origination](https://netlab.tools/module/ospf/#ospf-default) in OSPFv2 and OSPFv3
* [Route import](https://netlab.tools/module/routing_protocols/#routing-import) (redistribution) into OSPFv2, OSPFv3, and BGP.
* [Named prefixes](https://netlab.tools/prefix/#named-prefixes)

Other new goodies include:
<!--more-->
* [Change device configurations during validation tests](https://netlab.tools/topology/validate/#validate-config)
* [Use SuzieQ in validation tests](https://netlab.tools/topology/validate/#validate-suzieq)
* [VRF multihop EBGP sessions](https://netlab.tools/plugins/ebgp.multihop/#plugin-ebgp-multihop)
* Automatic loading of Linux kernel drivers (VXLAN, MPLS) required by device containers (FRR, VyOS)
* Display markdown reports as [ASCII text rendered with rich.markdown](https://netlab.tools/netlab/report/)
* Support for MPLS data plane in cEOS containers
* Support for vJunos-switch running in vrnetlab containers

This release is also the most-tested _netlab_ release ever. From the ~100 integration tests in release 1.8.4, we got to [almost 150 integration tests](https://github.com/ipspace/netlab/tree/dev/tests/integration) covering [most _netlab_-supported technologies](https://netlab.tools/module-reference/), and we [ran those tests on 15 different platforms](https://release.netlab.tools/) (the testing process took over 36 hours). Want to know how many bugs we fixed based on the test results? Check the [release notes](https://netlab.tools/release/1.9/#release-1-9-0) ;)

### Upgrading or Starting from Scratch

* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
