---
title: "netlab 1.8.2: Bug Fixes, Usability Improvements"
series_title: "Bug Fixes, Usability Improvements (Release 1.8.2)"
date: 2024-05-14 08:01:00+02:00
tags: [ netlab ]
netlab_tag: release
---
[_netlab_ release 1.8.2](https://netlab.tools/release/1.8/#release-1-8-2) contains dozens of bug fixes and minor tweaks to device configuration templates. We also added a few safeguards including:

* Check for Vagrant boxes or Docker containers before starting the lab and display pointers to build recipes.
* Check installed Ansible collections before trying to configure the lab devices.
* Display a warning if the lab topology was modified after the lab was created
<!--more-->
You might also enjoy:

* [Creating reports](https://netlab.tools/netlab/report/#netlab-report) from a subset of nodes (I use that to display BGP neighbors of customer routers in the [BGP labs](https://bgplabs.net/))
* [Inspecting the same variable(s) across multiple nodes](https://netlab.tools/netlab/inspect/#node-inspection-examples) (an ideal tool to find data model discrepancies)
* [Improved Vagrant-box-building process](https://netlab.tools/release/1.8/#release-1-8-2-vagrant)

Finally, someone asked for Sonic support, so I added a minimal implementation based on what I could squeeze from Azure VM images after [wasting too much time trying to get Dell Enterprise Sonic to work](/2024/05/too-stupid-to-make-it-work.html).

### Upgrading or Starting from Scratch

* For more details, [read the release notes](https://netlab.tools/release/1.8/#release-1-8-2).
* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
