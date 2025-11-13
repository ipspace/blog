---
title: "netlab 25.11: SRv6 on IOS/XE, Streamlined Graphs and Reports"
series_title: "SRv6 on IOS/XE, Streamlined Graphs and Reports (Release 25.11)"
date: 2025-11-13 10:02:00+01:00
tags: [ netlab ]
netlab_tag: release
---
I managed to push out [*netlab* release 25.11](https://netlab.tools/release/25.11/) yesterday. Here are the highlights:

- SRv6 on IOS/XE. It works with Catalyst 8000v, IOL, and IOL layer-2 image, and can be used to build L3VPNs (the IOS/XE image I have supports no other service on top of SRv6)
- RIPv2/RIPng on OpenBSD
- A more streamlined way to create [reports](https://netlab.tools/netlab/report/#netlab-report) and [graphs](https://netlab.tools/netlab/graph/#netlab-graph)
- The **netlab graph** command [creates the SVG/PNG/JPEG/PDF graph](https://netlab.tools/netlab/graph/#generating-image-files) instead of a graph description file if you've installed D2/Graphviz on your system.

We also had to make a few [potentially-breaking changes](https://netlab.tools/release/25.11/#breaking-changes), fixed a [bunch of bugs](https://netlab.tools/release/25.11/#bug-fixes), and added [over a dozen](https://netlab.tools/release/25.11/#new-functionality) small improvements.

You'll find all the details in the [release notes](https://netlab.tools/release/25.11/).
<!--more-->
### Upgrading or Starting from Scratch?

* To upgrade your *netlab* installation, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
