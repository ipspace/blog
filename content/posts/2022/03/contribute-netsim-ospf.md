---
title: "Contribute to netsim-tools: OSPFv3"
date: 2022-03-02 07:30:00
tags: [ automation ]
series: netsim
netsim_tag: contribute
---
Every other blue moon I get a question along the lines of "_how could I contribute to netsim-tools_". The process is pretty streamlined and reasonably (I hope) documented in _[Contributor Guidelines](https://netsim-tools.readthedocs.io/en/latest/dev/guidelines.html)_; if you want to get started with an easy task, try [implementing OSPFv3](https://github.com/ipspace/netsim-tools/issues/220) for one of almost a dozen devices:
<!--more-->
* Check the list of [supported device platforms](https://netsim-tools.readthedocs.io/en/latest/platforms.html) to see if it contains a device that you're familiar with ([adding a new device](https://netsim-tools.readthedocs.io/en/latest/dev/devices.html) is a totally different can of worms).
* Check the list of devices for which we [already implemented OSPFv3](https://netsim-tools.readthedocs.io/en/latest/module/ospf.html).
* If you don't have a running *netsim-tools* environment, start with the [installation instructions.](https://netsim-tools.readthedocs.io/en/latest/install.html). You will probably have to build a Vagrant box for your device: follow [VirtualBox](https://netsim-tools.readthedocs.io/en/latest/labs/virtualbox.html) or [libvirt](https://netsim-tools.readthedocs.io/en/latest/labs/libvirt.html) box building instructions.
* Read the [OSPF developer documentation](https://netsim-tools.readthedocs.io/en/latest/dev/config/ospf.html) to figure out how to create OSPFv3 configuration template.
* [Fork the netsim-tools repository](https://netsim-tools.readthedocs.io/en/latest/dev/guidelines.html).
* Write a comment in [OSPFv3 support GitHub issue](https://github.com/ipspace/netsim-tools/issues/220) to let everyone know you're working on a new device.
* Get the job done.
* Run tests -- between two instances of your device, and between your device and some other device.
* Submit a PR.

When testing your implementation, please test:

* P2P, LAN and stub links
* Numbered and unnumbered IPv6 links
* Different network types
* Multiple OSPF areas and OSPF costs

Finally a word of caution: we follow the _you wrote it, you own it_ principle, so be ready to fix the bugs if needed.
