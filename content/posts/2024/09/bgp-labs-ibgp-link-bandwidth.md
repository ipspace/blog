---
title: "IBGP Load Balancing with BGP Link Bandwidth"
date: 2024-09-23 07:13:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/lb/3-ibgp/
---
In the previous [BGP load balancing lab exercise](https://bgplabs.net/basic/#lb), I [described the BGP Link Bandwidth attribute](https://bgplabs.net/lb/2-dmz-bw/) and how you can use it on EBGP sessions. This lab moves the unequal-cost load balancing into your network; we'll [use the BGP Link Bandwidth attribute on IBGP sessions](https://bgplabs.net/lb/3-ibgp/).

{{<figure src="https://bgplabs.net/lb/topology-lb-ibgp-dmz-bw.png" width="300">}}
