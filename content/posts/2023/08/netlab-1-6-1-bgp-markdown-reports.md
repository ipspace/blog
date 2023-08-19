---
title: "netlab 1.6.1: BGP Reports, Markdown Support"
series_title: "BGP- and Markdown Reports (Release 1.6.1)"
date: 2023-08-21 06:08:00
tags: [ netlab ]
netlab_tag: release
---
We added just a few small features in *netlab* release 1.6.1[^HPO]:

* **Markdown reports**: **[netlab report](https://netlab.tools/netlab/report/)** command can produce Markdown-formatted reports, making it extremely easy to include them in your documentation (assuming you're using Markdown to write it)
* If you're using BGP in your labs, you can generate reports on BGP autonomous systems and BGP neighbors.
* I made [locations of default files configurable](https://netlab.tools/defaults/#defaults-locations). I'm using this feature in large projects where I want to have a shared set of project-wide defaults for topologies stored in different directories.

[^HPO]: To be honest, I had to push it out in a hurry because I forgot to include the **netlab show** help file in Python package.
<!--more-->
### Upgrading

To get more details and learn about additional features included in release 1.6.1, [read the release notes](https://netlab.tools/release/1.6/#release-1-6-1). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).

Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab). There's also a [*netlab* channel](https://networktocode.slack.com/archives/C022DQHK8BH) in networktocode Slack team, but you will get faster response time reporting your challenges in GitHub.
