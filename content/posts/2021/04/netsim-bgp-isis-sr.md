---
date: 2021-04-28 06:25:00+00:00
netlab_tag: archive
series_title: BGP, IS-IS, SR-MPLS, FRR
tags:
- netlab
title: 'netsim-tools Release 0.6: BGP, IS-IS, SR-MPLS, FRR'
---
**TL&DR**: If you want to test BGP, OSPF, IS-IS, or SR-MPLS in a virtual lab, you might build the lab faster with netsim-tools release 0.6.

In the netsim-tools release 0.6 I focused on adding routing protocol functionality:

* [IS-IS](https://netlab.tools/module/isis/) on Cisco IOS/IOS XE, Cisco NX-OS, Arista EOS, FRR, and Junos.
* [BGP](https://netlab.tools/module/bgp/) on the same set of platforms, including support for multiple autonomous systems, EBGP, IBGP full mesh, IBGP with route reflectors, next-hop-self control, and BGP/IGP interaction.
* [Segment Routing with MPLS](https://netlab.tools/module/sr-mpls/) on Cisco IOS XE and Arista EOS.

You'll also get:
<!--more-->
* Support for FRR running in Docker containers under **containerlab** (release 0.6.1).
* [Passive and external interfaces in OSPF](https://netlab.tools/module/ospf/#using-link-roles);
* Strict checking of configuration module parameters (so you won't chase invisible typos);
* An Ansible playbook that creates configuration snippets in a local directory instead of deploying them to lab devices.

### Links

* [Github repository](https://github.com/ipspace/netlab)
* [Documentation](https://netlab.tools/)
* [Installation guide](https://netlab.tools/install/)
* [Platform support](https://netlab.tools/platforms/)
