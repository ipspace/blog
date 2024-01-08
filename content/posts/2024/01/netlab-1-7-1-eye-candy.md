---
title: "netlab 1.7.1: Eye Candy"
series_title: "Eye Candy (Release 1.7.1)"
date: 2024-01-11 08:20:00+01:00
tags: [ netlab ]
netlab_tag: release
---
![](/2024/01/xmas.jpg)
{.sideicon}

What do you get when you write code next to a Christmas tree? You can expect to get tons of eye candy, and that's what [_netlab_ release 1.7.1](https://netlab.tools/release/1.7/#release-1-7-1) is all about.

It all started with a cleanup idea: I could [replace the internal ASCII table-drawing code with the `prettytable` library](https://github.com/ipspace/netlab/issues/969). Stefan was quick to point out that I should be looking at the `rich` library, and the rest is history:
<!--more-->
* **netlab up/down/test** commands got nicer section headers and color-coded status messages.
* All error messages are now color-coded.
* Tables use Unicode characters that result in perfectly-looking tables.
* YAML and JSON printouts go through the `rich` library that prettifies them.

We also fixed way too many bugs and added a few things you might find helpful (as opposed to great-looking):

* You can [automatically create nodes from group members](https://netlab.tools/groups/#groups-auto-create), so you don't have to specify the same node twice.
* In validation tests, you can use the [‘wait’ parameter](https://netlab.tools/topology/validate/#validate-wait) to wait for the control-plane protocols to start.
* VXLAN module can use any loopback interface (not just the *Loopback0*) for the VTEP IP address
* You can run (properly packaged) Juniper vPTX can run as a container

### Upgrading or Starting from Scratch

* For more details, [read the release notes](https://netlab.tools/release/1.7/#release-1-7-1).
* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
