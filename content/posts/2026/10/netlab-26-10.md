---
title: "netlab 26.10: SRv6, More Netmiko"
series_title: "SRv6, More Netmiko (Release 26.10)"
date: 2026-10-05 07:53:00+02:00
tags: [ netlab ]
netlab_tag: release
---
_netlab_ release 26.10 adds [new SRv6 implementations and features](https://netlab.tools/module/srv6/#platform-support):

- Full SRv6 support (IS-IS, layer-3 services, L3VPN) on Junos
- SRv6 with IS-IS and SRv6 layer-3 services on Nokia SR Linux
- IPv4 layer-3 services with SRv6 locators exchanged over EBGP on FRRouting and Cisco IOS XR

Other new features include:

- [Generic prefix sets](https://netlab.tools/module/routing/#generic-routing-prefix-set) for static routes
- *containerlab* nodes can [start in batches](https://netlab.tools/labs/clab/#starting-containers-in-batches) or wait for other nodes to start.
- **[netlab install netmiko](https://netlab.tools/netlab/install/)** installs the Netmiko and Paramiko packages needed for Netmiko-based device configuration and helps you change the device configuration mode for [supported devices](https://netlab.tools/platforms/#platform-config-mode).
<!--more-->
Read the [release notes](https://netlab.tools/release/26.10/) for more details, new [device features](https://netlab.tools/release/26.10/#release-26-10-device-features), and [breaking changes](https://netlab.tools/release/26.10/#release-26-10-breaking)

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
