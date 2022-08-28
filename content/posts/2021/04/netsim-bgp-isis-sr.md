---
title: "netsim-tools Release 0.6: BGP, IS-IS, SR-MPLS, FRR"
series_title: "BGP, IS-IS, SR-MPLS, FRR"
date: 2021-04-28 06:25:00
tags: [ automation, BGP, IS-IS, segment routing ]
series: netlab
netlab_tag: archive
---
**TL&DR**: If you want to test BGP, OSPF, IS-IS, or SR-MPLS in a virtual lab, you might build the lab faster with netsim-tools release 0.6.

In the netsim-tools release 0.6 I focused on adding routing protocol functionality:

* [IS-IS](https://netsim-tools.readthedocs.io/en/latest/module/isis.html) on Cisco IOS/IOS XE, Cisco NX-OS, Arista EOS, FRR, and Junos.
* [BGP](https://netsim-tools.readthedocs.io/en/latest/module/bgp.html) on the same set of platforms, including support for multiple autonomous systems, EBGP, IBGP full mesh, IBGP with route reflectors, next-hop-self control, and BGP/IGP interaction.
* [Segment Routing with MPLS](https://netsim-tools.readthedocs.io/en/latest/module/sr-mpls.html) on Cisco IOS XE and Arista EOS.

You'll also get:
<!--more-->
* Support for FRR running in Docker containers under **containerlab** (release 0.6.1).
* [Passive and external interfaces in OSPF](https://netsim-tools.readthedocs.io/en/latest/module/ospf.html#using-link-roles);
* Strict checking of configuration module parameters (so you won't chase invisible typos);
* An Ansible playbook that creates configuration snippets in a local directory instead of deploying them to lab devices.

### Links

* [Github repository](https://github.com/ipspace/netlab)
* [Documentation](https://netsim-tools.readthedocs.io/)
* [Installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html)
* [Platform support](https://netsim-tools.readthedocs.io/en/latest/platforms.html)
