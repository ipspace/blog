---
date: 2021-01-28 06:47:00+00:00
netlab_tag: archive
series_title: VirtualBox Support
tags:
- netlab
title: 'Build Virtual Lab Topology: VirtualBox Support'
---
When I blogged about release 0.2 of my lab-building tool, [Kristian Larsson](https://twitter.com/plajjan/status/1351607368065445890) was quick to reply: "now do vrnetlab". You could guess what my reply was (hint: "submit a pull request"), but I did realize I'd have to add multi-provider support before that would make sense.

[Release 0.3](https://netlab.tools/release/0.3/) adds support for multiple virtualization providers. You can run [six different platforms](https://netlab.tools/platforms/) on vagrant-libvirt (assuming you build the boxes), and I added [rudimentary support](https://netlab.tools/labs/virtualbox/) for Vagrant provider for VirtualBox:
<!--more-->
* The framework to add new devices is in place if anyone feels like contributing corresponding Vagrantfile snippets.
* The topology transformation modules deal with the infinite messiness of VirtualBox port forwarding and forward SSH, HTTP, and NETCONF ports.
* Ansible inventory gets correct **ansible_host** (127.0.0.1) and **ansible_port** (forwarded SSH port) values.

However:

* The only tested device is Cisco Nexus 9300v.
* I was unable to get Arista vEOS to work on my Mac (macOS Catalina, Vagrant 2.2.14, VirtualBox 6.1.18).
* The code to deal with forwarded NETCONF and HTTP ports in Ansible inventory is not there. Both of them are pretty convoluted to implement correctly, and I'll only add them if there's significant interest (or you could fix it yourself and submit a pull request).

Want to know more? [Documentation is online](https://netlab.tools/), and the [source code is on GitHub](https://github.com/ipspace/netlab).
