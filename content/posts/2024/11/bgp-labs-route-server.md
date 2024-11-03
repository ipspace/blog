---
title: "Using a BGP Route Server in an Internet Exchange Point"
date: 2024-11-06 07:25:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/session/5-routeserver/
---
A BGP route server is like a BGP route reflector but for EBGP sessions. In its simplest implementation, it receives BGP updates over EBGP sessions and propagates them over other EBGP sessions *without inserting its own AS number in the AS path* ([more details](https://datatracker.ietf.org/doc/html/rfc7947)).

BGP route servers are commonly used on Internet Exchange Points (IXPs), and that's what you can practice in the [BGP Route Server in an Internet Exchange Point](https://bgplabs.net/session/5-routeserver/) lab exercise.

{{<figure src="https://bgplabs.net/session/topology-routeserver.png" width="300">}}

[Click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `session/5-routeserver` and execute **netlab up**.
