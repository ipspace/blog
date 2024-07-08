---
title: "BGP Labs: Build Larger Networks with IBGP"
series_title: "Build Larger Networks with IBGP"
date: 2023-10-18 06:14:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/ibgp/1-edge/
---
After [going through the BGP basics](https://bgplabs.net/#setting-up-bgp), it's time to [build a network that has more than one BGP router in it](https://bgplabs.net/ibgp/1-edge/), starting with the simplest possible topology: a site with two WAN edge routers.

{{<figure src="https://bgplabs.net/ibgp/topology-ibgp.png">}}
<!--more-->
You SHOULD use IBGP to get that done, but there are a few gotchas along the way (I'm positive seasoned networking engineers can immediately figure out at least a couple of them). Instead of writing down a step-by-step recipe, I decided to guide the students through things that ~~can~~ will go wrong, hoping that might help them when they get stuck deploying IBGP in real life.
