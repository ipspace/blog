---
title: "Dynamic BGP Peers"
date: 2024-11-22 07:58:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/session/9-dynamic/
---
You might have an environment where a [route reflector](https://bgplabs.net/ibgp/3-rr/) (or a [route server](https://bgplabs.net/session/5-routeserver/)) has dozens or hundreds of BGP peers. Configuring them by hand is a nightmare; you should either build a decent automation platform or use dynamic BGP neighbors -- a feature you can practice in the [next lab exercise](https://bgplabs.net/session/9-dynamic/).

{{<figure src="https://bgplabs.net/session/topology-dynamic-peers.png" width="300">}}

[Click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `session/9-dynamic` and execute **netlab up**.
