---
title: "netsim-tools release 0.6.2"
date: 2021-05-17 06:26:00
tags: [ netlab ]
netlab_tag: archive
---
Last week we pushed out netsim-tools release 0.6.2. It's a maintenance release, so mostly full of bug fixes apart from awesome contributions by [Leo Kirchner](https://blog.kirchne.red/) who 

* Made vSRX 3.0 work on AMD CPU (warning: totally unsupported).
* Figured out how to use **vagrant mutate** to use *virtualbox* version of Cisco Nexus 9300v Vagrant box with *libvirt* 

[Other bug fixes](https://netlab.tools/release/0.6/#bug-fixes) include:

* Numerous fixes in Ansible installation playbook
* LLDP on all vSRX interfaces as part of initial configuration
* Changes in FRR configuration process to use bash or vtysh as needed
* **connect.sh** executing inline commands with **docker exec**

{{<jump>}}[Download the new release](https://github.com/ipspace/netlab)\
[Read the docs](https://netlab.tools/){{</jump>}}