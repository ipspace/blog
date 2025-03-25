---
title: "Passive BGP Sessions"
date: 2025-03-28 07:40:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/session/8-passive/
---
The [Dynamic BGP Peers](https://bgplabs.net/session/9-dynamic/) lab exercise gave you the opportunity to build a large-scale environment in which routers having an approved source IP addresses (usually matching an ACL/prefix list) can connect to a BGP [route reflector](https://bgplabs.net/ibgp/3-rr/) or [route server](https://bgplabs.net/session/5-routeserver/).

In a more controlled environment, you'd want to define BGP neighbors on the BGP RR/RS but not waste CPU cycles trying to establish BGP sessions with unreachable neighbors. Welcome to the world of [passive BGP sessions](https://bgplabs.net/session/8-passive/).

{{<figure src="https://bgplabs.net/session/topology-passive-bgp.png" width="300">}}

[Click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `session/8-passive` and execute **netlab up**.
