---
title: "netlab 25.12: Cisco IOS/XR Configuration Modules, More VXLAN Goodies"
series_title: "Cisco IOS/XR Configuration Modules, More VXLAN Goodies (Release 25.12)"
date: 2025-12-08 07:16:00+01:00
tags: [ netlab ]
netlab_tag: release
---
[*netlab* release 25.12](https://netlab.tools/release/25.12/) (25.12.02 to be exact -- I had a few [PEBCAK](https://en.wiktionary.org/wiki/PEBCAK) moments) was published last Friday. Here are the highlights:

- Significantly improved Cisco IOS/XR support. With the _netlab_ release 25.12, you can configure VLANs, VRFs, static routes, route redistribution, OSPF default routes, BGP confederations, and BGP local-as
- VXLAN-over-IPv6 on Arista EOS
- VXLAN with ingress replication on Cisco Catalyst 8000v
- The **shutdown** [link/interface attribute](https://netlab.tools/links/#link-attributes) can be used to start labs with interfaces turned off
- Large BGP community lists, implemented on Arista EOS, FRR, and Junos. You can use standard- or large community lists in [routing policies](https://netlab.tools/module/routing/#generic-routing-policies)
- The **[netlab validate](https://netlab.tools/netlab/validate/#netlab-validate)** command will [reread validation tests](https://netlab.tools/netlab/validate/#netlab-validate-dev) from a modified lab topology file every time you run it. It can also read validation tests from a separate file.
<!--more--> 
We also had to make a few [potentially-breaking changes](https://netlab.tools/release/25.12/#breaking-changes), fixed a [bunch of bugs](https://netlab.tools/release/25.12/#bug-fixes-25-12), and added [over a dozen](https://netlab.tools/release/25.12/#new-functionality) small improvements.

You'll find all the details in the [release notes](https://netlab.tools/release/25.12/).

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
