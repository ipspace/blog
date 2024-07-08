---
title: "BGP Challenge: Build BGP-Free MPLS Core Network"
series_title: "Build BGP-Free MPLS Core Network"
date: 2024-04-04 08:22:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/challenge/40-mpls-core/
---
Here's another challenge for BGP aficionados: [build an MPLS-based transit network without BGP running on core routers](https://bgplabs.net/challenge/40-mpls-core/).

{{<figure src="https://bgplabs.net/challenge/topology-mpls-core.png">}}

That should be an easy task if you configured MPLS in the past, so try to spice it up a bit:

* Use SR/MPLS instead of LDP
* Do it on a platform you're not familiar with (hint: Arista vEOS is a bit different from Cisco IOS)
* Try to get it running on FRR containers.
