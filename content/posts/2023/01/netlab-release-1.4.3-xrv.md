---
title: "netlab Release 1.4.3: Cisco IOS XRv, MPLS on FRR"
date: 2023-01-16 07:26:00
series_title: "Cisco IOS XRv, MPLS on FRR (Release 1.4.3)"
tags: [ automation ]
series: netlab
netlab_tag: release
---
I had tons of plans to implement new _netlab_ features during the last week of December, but then (fortunately) reality intervened and I spent my time relaxing and enjoying the break. I still managed to add IOS XRv support to [netlab release 1.4.3](https://netsim-tools.readthedocs.io/en/latest/release/1.4.html#release-1-4-3) though ;). Other new features include:

-   [MPLS, LDP and L3VPN](https://netsim-tools.readthedocs.io/en/latest/module/mpls.html) support on FRR by [Oleg A. Arkhangelsky](https://github.com/sysoleg)
-   Optimized [Linux container deployment](https://netsim-tools.readthedocs.io/en/latest/labs/clab.html#clab-linux) that removes dependencies on Python and `ip`
-   [Custom templates for container configuration files](https://netsim-tools.readthedocs.io/en/latest/labs/clab.html#clab-config-template)

To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netsim-tools.readthedocs.io/en/latest/tutorials.html) and the [installation guide](https://netsim-tools.readthedocs.io/en/latest/install.html).
