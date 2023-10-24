---
title: "netlab 1.6.4: Support for Multi-Lab Projects; More BGP Goodies"
series_title: "Support for Multi-Lab Projects; More BGP Goodies (Release 1.6.4)"
date: 2023-10-24 05:52:00
tags: [ netlab ]
netlab_tag: release
---
Features in *netlab* [release 1.6.4](https://netlab.tools/release/1.6/#release-1-6-4) were driven primarily by the needs of my [BGP labs](https://bgplab.github.io/bgplab/) project:

- [**bgp.session** plugin](https://netlab.tools/plugins/bgp.session/) (formerly known as **ebgp.utils** plugin) got support for BFD, passive BGP peers and **remove-private-as** option.
- [**bgp.policy** plugin](https://netlab.tools/plugins/bgp.policy/) implements basic BGP routing policy tools, including per-neighbor weights, local preference and MED.
- You can [enable external tools](https://netlab.tools/extools/#tools-enable-default) in user defaults and use [default groups](https://netlab.tools/groups/#default-groups) to create  user- or project-wide groups in the defaults files.
- [Version-specific lab topology files](https://netlab.tools/dev/versioning/) allow _netlab_ to select a lab topology that is a best fit for the _netlab_ release you're running.

Numerous platforms already support the new BGP nerd knobs:
<!--more-->
-   Arista EOS, Cisco IOSv, Cisco IOS/XE, Cumulus Linux and FRR support all new BGP session nerd knobs and BGP policy features.
-   Stefano Sasso contributed [bgp.session](https://netlab.tools/plugins/bgp.session/), [bgp.policy](https://netlab.tools/plugins/bgp.policy/) and [ebgp.multihop](https://netlab.tools/plugins/ebgp.multihop/) support for Aruba AOS-CX
-   Jeroem van Bemmel contributed [ebgp.multihop](https://netlab.tools/plugins/ebgp.multihop/) support for SR Linux and SR OS
-   You can use [BFD](https://netlab.tools/module/bfd/) for OSPFv2, OSPFv3 and BGP on FRR

I also made several changes to make plugins easier to use (more about that in a separate blog post):

* Plugins can use global module variables as metadata to tell _netlab_ what they want/expect/offer.
* `_requires` metadata handles mandatory plugin dependencies
* `_config_name` plugin metadata can be used instead of an API call to get the name of plugin template directory
* Plugins are sorted based on their dependencies documented in `_execute_after` metadata

Finally, a hodgepodge of other features:

* **bgp.session** plugin can apply BGP session attributes to IBGP and EBGP sessions.
* **[netlab show attributes](https://netlab.tools/netlab/show/#netlab-show-attributes)** command displays valid lab topology attributes and their expected data types. Failed validation checks tell you about that command to make your troubleshooting a bit easier.
* **[netlab show defaults](https://netlab.tools/netlab/show/#netlab-show-defaults)** command displays user/system defaults without starting a lab.
* For people who don't believe in prefix consistency we added [configurable IPv6 prefix length](https://netlab.tools/addressing/#address-pool-specs) to address pools

### Upgrading

To get more details and learn about additional features included in release 1.6.4, [read the release notes](https://netlab.tools/release/1.6/#release-1-6-4). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab). There's also a [*netlab* channel](https://networktocode.slack.com/archives/C022DQHK8BH) in networktocode Slack team, but you will get faster response time reporting your challenges in GitHub.
