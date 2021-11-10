---
title: "Build Virtual Lab Topology: VirtualBox Support"
date: 2021-01-28 06:47:00
tags: [ automation ]
series: netsim-tools
series_tag: release
---
When I blogged about release 0.2 of my lab-building tool, [Kristian Larsson](https://twitter.com/plajjan/status/1351607368065445890) was quick to reply: "now do vrnetlab". You could guess what my reply was (hint: "submit a pull request"), but I did realize I'd have to add multi-provider support before that would make sense.

[Release 0.3](https://netsim-tools.readthedocs.io/en/latest/release/0.3.html) adds support for multiple virtualization providers. You can run [six different platforms](https://netsim-tools.readthedocs.io/en/latest/platforms.html) on vagrant-libvirt (assuming you build the boxes), and I added [rudimentary support](https://netsim-tools.readthedocs.io/en/latest/platforms.html#virtualbox-support-limitations) for Vagrant provider for VirtualBox:
<!--more-->
* The framework to add new devices is in place if anyone feels like contributing corresponding Vagrantfile snippets.
* The topology transformation modules deal with the infinite messiness of VirtualBox port forwarding and forward SSH, HTTP, and NETCONF ports.
* Ansible inventory gets correct **ansible_host** (127.0.0.1) and **ansible_port** (forwarded SSH port) values.

However:

* The only tested device is Cisco Nexus 9300v.
* I was unable to get Arista vEOS to work on my Mac (macOS Catalina, Vagrant 2.2.14, VirtualBox 6.1.18).
* The code to deal with forwarded NETCONF and HTTP ports in Ansible inventory is not there. Both of them are pretty convoluted to implement correctly, and I'll only add them if there's significant interest (or you could fix it yourself and submit a pull request).

Want to know more? [Documentation is online](https://netsim-tools.readthedocs.io/en/latest/), and the [source code is on GitHub](https://github.com/ipspace/netsim-tools).