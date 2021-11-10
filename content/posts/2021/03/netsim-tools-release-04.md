---
title: "netsim-tools: Unnumbered Interfaces, Configuration Modules, OSPF"
date: 2021-03-29 07:12:00
tags: [ automation ]
series: netsim-tools
lastmod: 2021-07-12 18:00:03
series_tag: release
---
**TL&DR**: The [new release of netsim-tools](https://netsim-tools.readthedocs.io/en/latest/release/0.4.html) includes unnumbered interfaces, configuration modules, and OSPF configuration.

In mid-March, we enjoyed another excellent presentation by [Dinesh Dutt](https://www.ipspace.net/Author:Dinesh_Dutt), this time focused on [running OSPF in leaf-and-spine fabrics](https://my.ipspace.net/bin/list?id=Clos#L3_SINGLE). He astonished me when he mentioned unnumbered Ethernet interfaces being available on all major network operating systems. It was time to test things out, and I wanted to use my networking simulation builder to build the test lab.
<!--more-->
**Job#1**: add [unnumbered interface support](https://netsim-tools.readthedocs.io/en/latest/addressing.html#unnumbered-interface-support) to [netsim-tools](https://github.com/ipspace/netsim-tools).

I also wanted to have OSPF configured on all devices without logging into them and typing like a mad monkey. I was thinking about adding configuration modules (OSPF, BGP, EVPN...) to network topologies for a long while. This was a perfect opportunity to put the framework in place.

**Job#2**: add support for [extensible and configurable configuration modules](https://netsim-tools.readthedocs.io/en/latest/modules.html).

Finally, after implementing the unnumbered interfaces and configuration module framework, it was time to develop a basic OSPF configuration module. 

**Job#3**: add support for [OSPF routing configuration](https://netsim-tools.readthedocs.io/en/latest/module/ospf.html). It allows you to configure OSPF process ID, node-level and per-link areas, and link costs.

Building a full-blown OSPF test network became a simple process (details coming in another blog post):

* Describe desired network topology in YAML file.
* Run **netlab create** script to create Ansible inventory and Vagrantfile.
* Start the lab with **vagrant up**. Wait... Wait some more...
* [Deploy device configurations](https://netsim-tools.readthedocs.io/en/latest/configs.html) with **netlab initial** command. The playbook deploys initial device configurations as well as any configuration modules (OSPF in my example).
* Start doing the real testing instead of wasting time building and configuring a lab.

Finally, no job is finished until the paperwork is done. I probably spent way more time [writing the documentation](https://netsim-tools.readthedocs.io/en/latest/index.html) than code, but in the end, it paid off. While "wasting" time on documentation, I figured out (and fixed) a few quirks in the system. I also [made parameter inheritance much more flexible](https://netsim-tools.readthedocs.io/en/latest/modules.html#merging-default-values) than what Ansible inventory groups could do.

Finally, Job#4: Commit, merge, push. Hope you'll find the [new release](https://github.com/ipspace/netsim-tools/releases/tag/release_0.4) useful and [install](https://netsim-tools.readthedocs.io/en/latest/install.html) and use it ;) -- if you do, I'd appreciate hearing from you. You could also open a GitHub issue if there's something you'd like to see in an upcoming release (no promises, though).

### Revision History

2021-07-12
: Replaced old CLI commands with **netlab** CLI introduced with release 0.8.

2021-10-13
: A bit of polishing
