---
date: 2023-01-16 07:26:00+00:00
netlab_tag: archive
series_title: Cisco IOS XRv, MPLS on FRR (Release 1.4.3)
tags:
- netlab
title: 'netlab Release 1.4.3: Cisco IOS XRv, MPLS on FRR'
---
I had tons of plans to implement new _netlab_ features during the last week of December, but then (fortunately) reality intervened and I spent my time relaxing and enjoying the break. I still managed to add IOS XRv support to [netlab release 1.4.3](https://netlab.tools/release/1.4/#release-1-4-3) though ;). Other new features include:

-   [MPLS, LDP and L3VPN](https://netlab.tools/module/mpls/) support on FRR by [Oleg A. Arkhangelsky](https://github.com/sysoleg)
-   Optimized [Linux container deployment](https://netlab.tools/labs/clab/#clab-linux) that removes dependencies on Python and `ip`
-   [Custom templates for container configuration files](https://netlab.tools/labs/clab/#clab-config-template)

To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
