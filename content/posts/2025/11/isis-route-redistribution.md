---
title: "Lab: IS-IS Route Redistribution"
series_title: "IS-IS Route Redistribution"
date: 2025-11-28 07:45:00+01:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/feature/7-redistribute/
---
Route redistribution into IS-IS seems even easier than its OSPFv2/OSPFv3 counterparts. There are no additional LSAs/LSPs; the redistributed prefixes are included in the router LSP. Things get much more interesting once you start looking into the gory details and exploring how different implementations use (or do not) the various metric bits and TLVs.

You'll find more details (and the opportunity to explore the LSP database contents in a safe environment) in the [IS-IS Route Redistribution](https://isis.bgplabs.net/feature/7-redistribute/) lab exercise.

{{<figure src="https://isis.bgplabs.net/feature/topology-redistribute.png">}}

[Click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://isis.bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `feature/7-redistribute` and execute **netlab up**.
