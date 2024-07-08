---
title: "BGP Labs: Load Balancing across EBGP Paths"
series_title: "Load Balancing across EBGP Paths"
date: 2024-05-21 08:27:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/lb/1-ebgp/
---
Let's open another juicy can of BGP worms: [load balancing](https://bgplabs.net/basic/#lb). In the [first lab exercise](https://bgplabs.net/lb/1-ebgp/), you'll configure equal-cost load balancing across EBGP paths and tweak the "What is equal cost?" algorithm to consider just the AS path length, not the contents of the AS path.

{{<figure src="https://bgplabs.net/lb/topology-lb-ebgp.png" width="400">}}
