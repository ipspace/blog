---
title: "Build Virtual Lab Topology: Dual Stack Addressing, ArcOS  and Junos Support"
date: 2021-01-18 07:32:00
lastmod: 2021-07-12 18:06:00
tags: [ automation ]
series: netsim
netsim_tag: release
---
In mid-December I [announced a set of tools](https://blog.ipspace.net/2020/12/build-labs-netsim-tools.html) that will help you build Vagrant-based remote labs much faster than writing Vagrantfiles and Ansible inventories by hand.

In early January I received a nice surprise: [Dave Thelen](https://www.linkedin.com/in/dave-thelen-10261312/) not only decided to use the tool, he submitted a pull request with full-blown (and correctly implemented) ArcOS support. A few days later I managed to figure out what needs to be configured on vSRX to make it work, added Junos support, and thus increased the [number of supported platforms](https://netsim-tools.readthedocs.io/en/latest/platforms.html) to six (spanning five different operating systems).
<!--more-->
I always felt that the initial approach to lab addressing was a dirty hack that would have to be fixed in the future... and that future arrived on January 12th when I released a totally refactored address allocation code supporting multiple address pools and IPv6. Now you can build IPv4-only labs, IPv6-only labs, or dual-stack labs (with each link using one or both protocols).

Dave's enthusiasm ("_I'm using the tool daily_") also prompted me to document most of what's available including a [lab topology tutorial](https://netsim-tools.readthedocs.io/en/latest/tutorials.html) and a full-blown description of how you define [nodes (network devices)](https://netsim-tools.readthedocs.io/en/latest/nodes.html), [links](https://netsim-tools.readthedocs.io/en/latest/links.html), and [address pools](https://netsim-tools.readthedocs.io/en/latest/addressing.html).

You can [download the tools from GitHub](https://github.com/ipspace/netsim-tools) or [install them as a Python3 package](https://netsim-tools.readthedocs.io/en/latest/install.html), and [read the documentation on ReadTheDocs](https://netsim-tools.readthedocs.io/en/latest/).

### What's Still Missing

A lot of things, including support for virtualization environments other than *vagrant-libvirt*. After I got that one up and running (you'll find [links to box-building recipes in my installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html)) I lost the willpower to ever touch VirtualBox again... so if you feel like adding your VirtualBox Vagrantfile recipes to the [Vagrant templates](https://github.com/ipspace/netsim-tools/tree/master/templates/vagrant) you're most welcome.

### Revision History

2021-07-12
: Updated documentation pointers.
