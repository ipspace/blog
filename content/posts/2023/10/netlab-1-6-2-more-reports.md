---
title: "netlab 1.6.2: More Reporting Goodies"
series_title: "Improved Reports (Release 1.6.2)"
date: 2023-10-05 06:19:00
tags: [ netlab ]
netlab_tag: release
---
*netlab* [release 1.6.2](https://netlab.tools/release/1.6/#release-1-6-2) improved reporting capabilities:

* BGP reports and IP addressing reports are fully IPv6-aware
* Some columns in BGP reports are optional to reduce the width of text reports
* You can filter the reports you're interested in when using **[netlab show reports](https://netlab.tools/netlab/show/#netlab-show-reports)** command
* Reports relying on **ipaddr** Ansible filter display warnings (instead of crashing) if you don't have Ansible installed.

In other news:

- Stefano Sasso added [support for ArubaOS-CX running within containerlab](https://netlab.tools/platforms/#supported-virtual-network-devices)
- You can use [inter-VRF route leaking](https://netlab.tools/module/vrf/#platform-support) with Cumulus Linux or FRR
<!--more-->
### Upgrading

To get more details and learn about additional features included in release 1.6.2, [read the release notes](https://netlab.tools/release/1.6/#release-1-6-2). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab). There's also a [*netlab* channel](https://networktocode.slack.com/archives/C022DQHK8BH) in networktocode Slack team, but you will get faster response time reporting your challenges in GitHub.
