---
title: "netlab 1.6.3: BGP Nerd Knobs"
series_title: "BGP Nerd Knobs (Release 1.6.3)"
date: 2023-10-11 05:52:00
tags: [ netlab ]
netlab_tag: release
---
*netlab* [release 1.6.3](https://netlab.tools/release/1.6/#release-1-6-3) added numerous BGP nerd knobs:

- You can create [EBGP multihop sessions](https://netlab.tools/plugins/ebgp.multihop/) in the global routing table when using Arista EOS, Cisco IOSv, Cisco IOS-XE, FRR and Cumulus Linux 4.x.
- [ebgp.utils plugin](https://netlab.tools/plugins/ebgp.utils/) supports TCP-AO, configurable BGP timers, and Generic TTL Security Mechanism (TTL session protection)
- [BGP](https://netlab.tools/module/bgp/) neighbor reports hide irrelevant columns.

We also:
<!--more-->
- Added [OSPF reports](https://netlab.tools/module/ospf/) in Markdown, HTML and text format
- Implemented [BFD on Cumulus Linux](https://netlab.tools/module/bfd/#bfd-platform)
- Added *collect configuration* action for [FRR](https://netlab.tools/platforms/#platform-config-support) and changed default FRR release to 9.0.1
- Implemented [gRPC test topology](https://netlab.tools/netlab/test/) for users of Nokia SR Linux and SR OS devices

Finally, a few features for the advanced users:

- If you're relying on bleeding-edge _netlab_ features you can specify [minimum netlab version](https://netlab.tools/topology-reference/#topology-reference-extra-elements) in lab topology
- The new [‘disable’ link attribute](https://netlab.tools/links/#link-attributes) allows you to remove individual links from lab topology during the troubleshooting process.
- If you're writing plugins, you might like the ability to load plugin-related defaults (example: additional attributes) from a YAML file instead of defining them in Python code.
- If you don't like the way _netlab_ configures network devices, use your own configuration templates that can be [loaded from system- or user directory](https://netlab.tools/customize/#customize-templates)

### Upgrading

To get more details and learn about additional features included in release 1.6.3, [read the release notes](https://netlab.tools/release/1.6/#release-1-6-3). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab). There's also a [*netlab* channel](https://networktocode.slack.com/archives/C022DQHK8BH) in networktocode Slack team, but you will get faster response time reporting your challenges in GitHub.
