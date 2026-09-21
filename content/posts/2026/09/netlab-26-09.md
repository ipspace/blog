---
title: "netlab 26.09: Syslog, More DNS, Netmiko"
series_title: "Syslog, More DNS, Netmiko (Release 26.09)"
date: 2026-09-21 07:36:00+02:00
tags: [ netlab ]
netlab_tag: release
---
_netlab_ release 26.09 brings more *network services* goodies:

- The [**services** module](https://netlab.tools/module/services/#module-services) supports [Syslog clients and servers](https://netlab.tools/module/services/#services-syslog-parameters).
- DNS and Syslog are implemented on most supported platforms.

Other new features include:

- The new **netmiko** [device configuration mode](https://netlab.tools/platforms/#platform-config-mode) for virtual machines
- [Generic prefix sets](https://netlab.tools/module/routing/#generic-routing-prefix-set) that simplify writing ACL rules and prefix lists
<!--more-->
We also decided to [deprecate the ancient Cisco IOSv](https://netlab.tools/caveats/#caveats-iosv) (Cisco IOS/XE support is unaffected) and [sunset the libvirt (Vagrant) provider](https://netlab.tools/labs/libvirt/#libvirt-sunset).

Read the [release notes](https://netlab.tools/release/26.09/#release-26-09) for more details, new [device features](https://netlab.tools/release/26.09/#release-26-09-device-features), and [breaking changes](https://netlab.tools/release/26.09/#release-26-09-breaking)

### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues/new/choose) in [netlab GitHub repository](https://github.com/ipspace/netlab).
