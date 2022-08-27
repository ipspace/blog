---
title: "netsim-tools Release 1.1.4"
date: 2022-03-15 07:46:00
tags: [ automation ]
series: netlab
netlab_tag: archive
---
[*netsim-tools* release 1.1.4](https://netsim-tools.readthedocs.io/en/latest/release/1.1.html) includes a number of seemingly unrelated goodies; here's the the reasoning (or story) behind some of them:

> [netlab clab tarball](https://netsim-tools.readthedocs.io/en/latest/netlab/clab.html) creates a tar package that can be deployed with *containerlab* without *netsim-tools*

{{<note info>}}Starting with release 1.3, we [renamed *netsim-tools* to *netlab*](/2022/08/netsim-netlab.html).{{</note>}}
<!--more-->
Julio Perez wanted to [create ready-to-use labs running Arista cEOS on *containerlab*](https://juliopdx.com/2022/02/13/network-simulation-tools-and-containerlab/). Requiring the users of his labs to deploy *netsim-tools* and Ansible just to configure the lab devices is a clear overkill considering the *startup-config* support in *containerlab*. What he needed was:

* An easy mechanism to set up IP addressing plan and configure interfaces and routing protocols in a virtual lab (**[netlab up](https://netsim-tools.readthedocs.io/en/latest/netlab/up.html)** does all of that)
* A mechanism to collect final device configurations (**[netlab collect](https://netsim-tools.readthedocs.io/en/latest/netlab/collect.html)**)
* Something that would add pointers to startup device configurations to *containerlab* configuration file and package everything in a tarball -- **[netlab clab tarball](https://netsim-tools.readthedocs.io/en/latest/netlab/clab.html)**

> Add fetch_config action for SR Linux and SR OS. You can use netlab collect to get current configuration from these devices

[Jeroen van Bemmel](https://www.linkedin.com/in/jeroenvbemmel/) and SR Linux are the root cause for *containerlab* support in *netsim-tools* and it would be a shame if Julio couldn't create labs mixing Arista cEOS and SR Linux just because we had no way to collect device configuration from SR Linux devices. Jeroen quickly supplied the fix for that ;) Thank you!

> Added `--tar` and `-cleanup` options to **netlab collect**.

As I was starting to work on **netlab clab tarball** implementation, someone asked me "_could I get final device configurations for one of your labs?_". Wouldn't it be nice if I could collect the configurations, create a tarball, and do a cleanup all in one go? Now I can ;)

> Added `--cleanup` option to **netlab down**

Thinking about beginners trying to find their way around, Julio asked for an option that would delete all files created by **[netlab up](https://netsim-tools.readthedocs.io/en/latest/netlab/up.html)** command on **[netlab down](https://netsim-tools.readthedocs.io/en/latest/netlab/down.html)**, leaving them with a clean directory.

> Build recipes for Arista vEOS and Juniper vSRX use management VRF

Vagrant (libvirt and VirtualBox variants) as well as containerlab use a management network to connect to virtual network devices. Moving that interface into a VRF simplifies everyone's life -- we don't have to exclude it from a routing process, or stop LLDP on it, or...

Nexus OS uses management VRF by default, and I added similar functionality to Cisco IOSv and IOS/XE Vagrant box recipes, prompting [Stefano Sasso](http://stefano.dscnet.org/about/) to submit a PR for similar functionality on Arista vEOS and Juniper vSRX. Thank you!

> Use netlab_device_type instead of ansible_network_os to select configuration templates

Julio wanted to implement ExaBGP device in *netsim-tools*, and it doesn't make sense to invent bogus operating systems just to deploy a different configuration template. 

Now that the framework is in place, we could create tons of other pseudo-devices. For example, Dinesh Dutt was telling me the other day how easy it would be to deploy SuzieQ in a container.

