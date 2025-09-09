---
title: "Use Additional BGP Paths for IBGP Load Balancing"
date: 2025-09-19 08:01:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/lb/4-ibgp-add-path/
---
I wrote about the [optimal BGP path selection with BGP additional paths](https://blog.ipspace.net/2021/12/bgp-multipath-addpath/) in 2021, and I probably mentioned (in one of the [360 BGP-related blog posts](https://blog.ipspace.net/tag/bgp/)) that you need it to implement IBGP load balancing in networks using BGP route reflectors. If you want to try that out, check out the [IBGP Load Balancing with BGP Additional Paths](https://bgplabs.net/lb/4-ibgp-add-path/) lab exercise.

{{<figure src="https://bgplabs.net/lb/topology-ibgp-add-path.png" width="300">}}

[Click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `lb/4-ibgp-add-path` and execute **netlab up**.
