---
title: "Use Disaggregated BGP Prefixes to Influence Inbound Internet Traffic"
date: 2024-12-13 08:14:00+01:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/policy/b-disaggregate/
---
As much as I love explaining how to use BGP in an optimal way, sometimes we have to do what we know is bad to get the job done. For example, if you have to deal with clueless ISPs who cannot figure out how to use BGP communities, you might be forced to use the Big Hammer of disaggregated prefixes. You can practice how that works in the [next BGP lab exercise](https://bgplabs.net/policy/b-disaggregate/).

{{<figure src="https://bgplabs.net/policy/topology-disaggregate.png" width="300">}}

[Click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `policy/b-disaggregate` and execute **netlab up**.
