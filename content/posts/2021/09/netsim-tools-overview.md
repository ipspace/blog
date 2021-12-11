---
title: "netsim-tools: Overview"
date: 2021-09-09 07:16:00
tags: [ automation ]
series: netsim
series_weight: 100
netsim_tag: overview
series_title: Overview
---
In December 2020, I got sick-and-tired of handcrafting Vagrantfiles and decided to write a tool that would, given a target networking lab topology in a text file, produce the corresponding Vagrantfile for my favorite environment (libvirt on Ubuntu). Nine months later, that idea turned into a pretty comprehensive tool targeting *networking engineers who like to work with CLI and text-based configuration files*. If you happen to be of the GUI/mouse persuasion, please stop reading; this tool is not for you.

During those nine months, I slowly addressed most of the challenges I always had creating networking labs. Here's how I would typically approach testing a novel technology or software feature:
<!--more-->
* Figure out the required network topology (devices, links, endpoints)
* Create the network topology in whatever lab management system I happen to be using.
* Create an addressing plan for my lab.
* Deploy initial configurations on all devices.
* Configure interfaces and interface addresses.
* Configure IGP routing protocols.

Optional:

* Create autonomous systems
* Decide on IBGP topology, choose route reflectors, and configure BGP.

I may be slow, but it usually takes me a good part of an hour (plus some hard-to-troubleshoot typos) to get to the point where the going starts getting interesting. Even then, I often have to configure the same functionality (example: new BGP address family) on a large subset of lab devices.

In the past, I used Cisco VIRL to build my labs. The tool is relatively pleasant to use[^1], but it took me so long to get to a working lab that I would always try to reuse existing topologies and cram new ideas onto an existing setup. To make matters worse, chasing the parameters I want to set (like BGP AS numbers) through a series of GUI screens quickly becomes a frustrating exercise. Wouldn't it be great if one could get rid of all those chores and have a brand-new lab tailored to the job-at-hand in a minute or two (plus whatever time it takes Nexus 9000v to wake up)?

[netsim-tools](https://netsim-tools.readthedocs.io/) tries to provide just that:

* A YAML file describes lab topology and optional parameters like routing protocol areas or autonomous systems.
* The tool builds an IPv4 and IPv6 addressing plan[^2] and routing protocol setup (including BGP sessions) based on the lab topology, resulting in a detailed node-focused data model.
* The node-focused data model is used to generate Ansible inventory, virtualization configuration files, topology graphs, and device configurations. You could also export it into YAML or JSON and use it in your customized toolchain.
* After the lab is up and running, an Ansible playbook deploys the device configurations onto lab devices, resulting in a fully functional network running a combination of IPv4, IPv6, LLDP, OSPF, IS-IS, EIGRP, BGP, and SR-MPLS.

The current release of the tool is installed as a Python package and can be used to [install everything you need to set up a virtual lab on Ubuntu](https://netsim-tools.readthedocs.io/en/latest/netlab/install.html). It supports three virtualization environments (VirtualBox, libvirt, and Docker) and nine network operating systems (EOS, ArcOS, IOS, IOS XE, Nexus OS, Cumulus Linux, FRR, Junos, and Nokia SR Linux).

Interested? Check out the [documentation](https://netsim-tools.readthedocs.io/en/latest/index.html), in particular the [installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html), [tutorials](https://netsim-tools.readthedocs.io/en/latest/tutorials.html), and supported platforms. Need help? I created a channel in the network2code Slack team dedicated to netsim-tools.

[^1]: Even though it's a waste of resources caused by too many layers of abstraction. Why do you need to run OpenStack in a VM to create a few Linux bridges and start a few libvirt-based VMs?

[^2]: You can change the address pools or specify static IP addresses for individual link endpoints if you wish to do so.
