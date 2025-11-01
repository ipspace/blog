---
title: "Lab: Adjust IS-IS Timers"
series_title: "Adjust IS-IS Timers"
date: 2025-11-07 07:37:00+01:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/feature/6-timers/
---
Like any other routing protocol, IS-IS has several timers you can tweak to improve the convergence speed of your network, or make your network unstable (eventually breaking it completely) if you reduce them too much (if you care about fast convergence, you REALLY SHOULD use BFD).

You'll find more details (and the opportunity to tweak the timers in a safe environment) in the [Adjust IS-IS Timers](https://isis.bgplabs.net/feature/6-timers/) lab exercise.

{{<figure src="https://isis.bgplabs.net/feature/topology-timers.png">}}

[Click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://isis.bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `feature/6-timers` and execute **netlab up**.
