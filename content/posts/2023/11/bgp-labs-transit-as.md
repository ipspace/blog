---
title: "BGP Labs: Build a Transit Network with IBGP"
series_title: "Build a Transit Network with IBGP"
date: 2023-11-02 07:06:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/ibgp/2-transit/
---
Last time we [built a network with two adjacent BGP routers](https://bgplabs.net/ibgp/1-edge/). Now let's see what happens when we add a core router between them:

{{<figure src="https://bgplabs.net/ibgp/topology-ibgp-transit.png">}}
<!--more-->
There are at least four ways to get connectivity between PE2 and EXT routers. The [lab exercise](https://bgplabs.net/ibgp/2-transit/) doesn't allow you to use route redistribution or aggregation/default route. You could use MPLS (or SRv6) if you wish, or give up and do what's usually done in large networks running BGP.
