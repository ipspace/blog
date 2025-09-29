---
title: "Using BIRD BGP Daemon as a BGP Route Reflector"
date: 2025-10-03 07:51:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/challenge/01-bird-rr/
---
In this challenge lab, you'll configure a BIRD daemon running in a container as a BGP route reflector in a transit autonomous system. You should be familiar with the configuration concepts if you completed the [IBGP lab exercises](https://bgplabs.net/basic/#ibgp), but will probably struggle with BIRD configuration if you're not familiar with it.

{{<figure src="https://bgplabs.net/challenge/topology-bird-rr.png" width="300">}}

[Click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `challenge/01-bird-rr`, build the BIRD container with **netlab clab build bird** if needed, and execute **netlab up**.
