---
title: "BGP Labs: Protect EBGP Sessions"
series_title: "Protect EBGP Sessions"
date: 2023-09-21 06:32:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/basic/6-protect/
---
I published another [BGP labs](https://bgplabs.net/) exercise a few days ago. You can use it to [practice EBGP session protection](https://bgplabs.net/basic/6-protect/), including [Generalized TTL Security Mechanism (GTSM)](https://blog.ipspace.net/2023/03/advantages-bgp-gtsm.html) and TCP MD5 checksums[^AO].

[^AO]: I would love to add TCP-AO to the mix, but it's not yet supported by the Linux kernel, and so cannot be used in Cumulus Linux or FRR containers.

{{<figure src="https://bgplabs.net/basic/topology-protect.png">}}
