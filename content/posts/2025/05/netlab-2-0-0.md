---
title: "netlab 2.0.0: Hosts, Bridges, and SRv6"
series_title: "Hosts, Bridges, and SRv6 (Release 2.0.0)"
date: 2025-05-12 08:05:00+01:00
tags: [ netlab ]
netlab_tag: release
---
[_netlab_ release 2.0.0](https://netlab.tools/release/2.0/#release-2-0-0) is out. I spent the whole week fixing bugs and running integration tests, so I'm too brain-dead to go into the details. These are the major features we added (more about them in a few days; the details are in the [release notes](https://netlab.tools/release/2.0/#release-2-0-0)):

-   Well-defined [node roles](https://netlab.tools/node-roles/#node-router-host) (**host**, **router**, **bridge**) are now available on [multiple platforms](https://netlab.tools/platforms/#platform-host)
-   The **[firewall.zonebased](https://netlab.tools/plugins/firewall.zonebased/#plugin-firewall-zonebased)** plugin allows you to configure a rudimentary firewall
-   SRv6: [BGP L3VPN support](https://netlab.tools/module/srv6/#module-srv6) is now available for FRRouting, so you can go out and kick its (free) tires.
-   **bridge** nodes can be used as [simple bridges](https://netlab.tools/node-roles/#node-role-bridge) or to [implement multi-access links](https://netlab.tools/node-roles/#node-bridge-lan)
-   **[netlab defaults](https://netlab.tools/netlab/defaults/#netlab-defaults)** command provides **sysctl**-like CLI interface to user/system defaults.

Other changes include:
<!--more-->
-   _netlab_ is gathering usage statistics into a local file that is not shared with anyone, but can be inspected or managed with **[netlab usage](https://netlab.tools/netlab/usage/#netlab-usage)**
-   We use the **routing** module to configure static routes on [**host** devices](https://netlab.tools/node-roles/#node-role-host). VRF-aware devices can use a default route; other devices get more specific routes for address pools and named prefixes.
-   Multiple [EVPN import/export route targets](https://netlab.tools/module/evpn/#evpn-vlan-service) allow you to build complex EVPN-based services like *common services* or *hub-and-spoke connectivity*
-   I wanted to have better graphs, so I implemented [node/link styles for D2 graphs](https://netlab.tools/outputs/d2/#outputs-d2-style-attributes)
-   Finally, we implemented ‘delete communities matching a list’ in [routing policies](https://netlab.tools/module/routing/#generic-routing-policies)

On the other hand, there's time for a few retirements:

-   It's time to allow [Cumulus Linux 4.x to rest](https://netlab.tools/caveats/#caveats-cumulus). While there are no plans to remove it from *netlab*, we will not add new features or run integration tests.
-   [VirtualBox and direct Windows/macOS installations](https://netlab.tools/labs/virtualbox/#lab-virtualbox) are obsolete.

But wait, there's more:

-   Names of **defaults.const.validate** constants [can be used as wait times](https://netlab.tools/topology/validate/#validate-retry) in the validation **wait** parameter
-   You can use **all** and device types in the [node selection expressions](https://netlab.tools/netlab/inspect/#netlab-inspect-node) used in **netlab inspect**, **netlab report** and **netlab exec** commands
-   We use a different Ansible task list when reloading device configuration, which gives you the ability to reload device configuration on SR Linux
-   If you insist (but you shouldn't), you can use **int** values as offset of management IP addresses in the management subnet.
-   You can combine default tcpdump flags with user filter in the **[netlab capture](https://netlab.tools/netlab/capture/#netlab-capture)** command
-   We moved to Vagrant version to 2.4.3-1
-   _netlab_ checks reserved ranges (local network, multicast) during IPv4/IPv6 address/prefix validation. It also warns about EBGP ‘bgp’ attributes used on intra-AS links/vlans

Not enough? How about [new device features](https://netlab.tools/release/2.0/#release-2.0.0-device-features)? Here are just a few of them:

* Unnumbered interfaces on Aruba CX
* You can configure a half-dozen new BGP features on Bird, and use it in LAG and VLAN environments
* We started supporting numerous BGP features and routing policies on Dell OS10 and Junos
* There's also MAC-VRF implementation for Junos
* Finally, there's SRv6 with IS-IS and L3VPN services over SRv6 on FRRouting

### Upgrading or Starting from Scratch?

* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
