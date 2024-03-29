---
title: "BGP Labs: Protect EBGP Sessions"
series_title: "Protect EBGP Sessions"
date: 2023-09-21 06:32:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
I published another [BGP labs](https://bgplabs.net/) exercise a few days ago. You can use it to [practice EBGP session protection](https://bgplabs.net/basic/6-protect/), including [Generalized TTL Security Mechanism (GTSM)](https://blog.ipspace.net/2023/03/advantages-bgp-gtsm.html) and TCP MD5 checksums[^AO].

[^AO]: I would love to add TCP-AO to the mix, but it's not yet supported by the Linux kernel, and so cannot be used in Cumulus Linux or FRR containers.

{{<figure src="https://bgplabs.net/basic/topology-protect.png">}}

I would strongly recommend to [run BGP labs with _netlab_](https://bgplabs.net/1-setup/), but if you like extra work, feel free to use [any system you like including physical hardware](https://bgplabs.net/external/).
