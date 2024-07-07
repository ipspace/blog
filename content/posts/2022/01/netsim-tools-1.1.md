---
date: 2022-01-11 08:01:00+00:00
netlab_tag: archive
tags:
- netlab
title: 'Just Out: netsim-tools Release 1.1'
---
New Year break was probably my busiest time (programming-wise) in years. [Jeroen van Bemmel](https://github.com/jbemmel) continued generating great ideas (and [writing code and device configuration templates](https://github.com/ipspace/netlab/graphs/contributors)), and I found myself saying, "_why not, let's do the right thing!_" more often than I expected. In parallel, [Stefano Sasso](https://github.com/ssasso) fixed configuration templates for Junos, Mikrotik Router OS, and VyOS, and we were good to go.

To give you an idea of [how fast we were moving](https://github.com/ipspace/netlab/pulse/monthly): issue #84 was created on December 22nd, Sunday's pull request that pushed release 1.1 into the master branch was #135 (GitHub numbers everything you do sequentially).

{{<note info>}}Starting with release 1.3, we [renamed *netsim-tools* to *netlab*](/2022/08/netsim-netlab/).{{</note>}}
<!--more-->
In the meantime, we rewrote most of the topology transformation code, changed major data structures, simplified configuration templates, and added BFD support for Arista EOS, Cisco IOS, IOS XE, and Nexus OS, Junos, Nokia SR OS and SR Linux, Mikrotik RouterOS, and VyOS.

You'll find more details in the [release notes](https://netlab.tools/release/1.1/); if you're not familiar with netsim-tools yet, you might want to start with the [Installation Guide](https://netlab.tools/install/) and [Getting Started](https://netlab.tools/tutorials/) document.

