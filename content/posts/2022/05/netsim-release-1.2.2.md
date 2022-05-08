---
title: "netsim-tools: VLANs, Hardware Labs, VRF Loopbacks"
date: 2022-05-11 06:36:00
tags: [ automation ]
series: netsim
netsim_tag: release
---
Here's a short list of major goodies included in netsim-tools release 1.2.2:

- [Access VLANs, VLAN trunks and native VLANs](https://netsim-tools.readthedocs.io/en/latest/module/vlan.html) implemented on Cisco IOS, Arista EOS, VyOS, and Dell OS10 (VyOS and OS10 support contributed by Stefano Sasso)
- [Hardware labs](https://blog.ipspace.net/2022/05/netsim-hardware-lab.html) implemented with [_external_ topology provider](https://netsim-tools.readthedocs.io/en/latest/providers.html) (contributed by Stefano Sasso)
- [VRF loopback interfaces](https://netsim-tools.readthedocs.io/en/latest/module/vrf.html#vrf-loopback) (contributed by Stefano Sasso)

More details in the [release notes](https://netsim-tools.readthedocs.io/en/latest/release/1.2.html).

To upgrade *netsim-tools*, use `pip3 install --upgrade netsim-tools`; if you're starting from scratch, read the [installation instructions](https://netsim-tools.readthedocs.io/en/latest/install.html).
