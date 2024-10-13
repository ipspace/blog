---
title: "Using BGP NO_EXPORT Community to Filter Transit Routes"
date: 2024-10-14 07:25:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/policy/d-no-export/
---
In [previous BGP policy lab exercises](https://bgplabs.net/policy/), we covered several mechanisms you can use to ensure your autonomous system is not leaking transit routes (because [bad things happen when you do](https://blog.ipspace.net/2021/11/internet-keeps-breaking/), particularly when [your upstream ISP is clueless](https://blog.ipspace.net/2019/07/rant-some-internet-service-providers/)). 

As you probably know by now, there's always more than one way to get something done with BGP. Today, we'll explore how you can [use the NO_EXPORT community to filter transit routes](https://bgplabs.net/policy/d-no-export/).

{{<figure src="https://bgplabs.net/policy/topology-no-export.png" width="300">}}

[Click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `policy/d-no-export` and execute **netlab up**.
