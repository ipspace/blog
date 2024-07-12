---
title: "EBGP Load Balancing with BGP Link Bandwidth"
date: 2024-07-16 07:04:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/lb/2-dmz-bw/
---
The first [BGP load balancing lab exercise](https://bgplabs.net/basic/#lb) described the [basics of EBGP equal-cost load balancing](https://bgplabs.net/lb/1-ebgp/). Now for the fun part: what if you want to spread traffic across multiple links in an unequal ratio? There's a nerd knob for that: the [BGP Link Bandwidth extended community](https://datatracker.ietf.org/doc/html/draft-ietf-idr-link-bandwidth-07) that you can test-drive in [this lab exercise](https://bgplabs.net/lb/2-dmz-bw/).

{{<figure src="https://bgplabs.net/lb/topology-lb-dmz-bw.png">}}
