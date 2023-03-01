---
title: "Help Appreciated: netsim-tools Device Features"
date: 2022-06-20 06:17:00
tags: [ netlab ]
netlab_tag: contribute
---
There are (at least) two steps to get new functionality (like VLANs) implemented in [netsim-tools](https://netsim-tools.readthedocs.io/en/latest/):

* We have to develop a data transformation module that takes high-level lab-, node-, link- or interface attributes and transforms them into device data.
* Someone has to create Jinja2 templates _for each supported device_ that transform per-device *netsim-tools* data into device configurations.

I usually implement new features on Cisco IOSv and Arista EOS[^OT], [Stefano Sasso](https://www.linkedin.com/in/ssasso/) adds support for VyOS, Dell OS10, and Mikrotik RouterOS, and [Jeroen van Bemmel](https://www.linkedin.com/in/jeroenvbemmel/) adds Nokia SR Linux and/or SR OS support. That's less than [half of the platforms supported by netsim-tools](https://netsim-tools.readthedocs.io/en/latest/platforms.html), and anything you could do to help us increase the coverage would be highly appreciated.
<!--more-->
[^OT]: Being an old-timer, I still believe in the ancient "_have two independent interoperable implementations_" IETF mantra.

[GitHub Issues](https://github.com/ipspace/netlab/issues) always contain the up-to-date list of missing devices, at this moment we'd appreciate:

* [VLAN support](https://netsim-tools.readthedocs.io/en/latest/platforms.html#supported-configuration-modules) for CSR 1000v, Nexus OS, Junos, and Cumulus Linux (old-style config and NVUE)
* [MPLS LDP support](https://netsim-tools.readthedocs.io/en/latest/module/mpls.html#platform-support) for most platforms, including Nexus OS and Junos
* [BGP-LU support](https://netsim-tools.readthedocs.io/en/latest/module/mpls.html#bgp-labeled-unicast-bgp-lu) for the same set of platforms
* [VRF support](https://netsim-tools.readthedocs.io/en/latest/module/vrf.html) for old-style Cumulus Linux and Junos (someone is [already working on Cisco Nexus OS implementation](https://github.com/ipspace/netlab/issues/314)).
* [OSPFv3 support](https://netsim-tools.readthedocs.io/en/latest/module/ospf.html) on Nexus OS and Cumulus Linux

Willing to help? [Contributor Guidelines](https://netsim-tools.readthedocs.io/en/latest/dev/guidelines.html) will give you more information (in particular [New Configuration Features for an Existing Device](https://netsim-tools.readthedocs.io/en/latest/dev/device-features.html)); once you're ready to get started open a GitHub issue saying "_I'm working on this bit_", and submit a pull request when you're done. Thanks a million!

