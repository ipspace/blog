---
title: "Lab: Drain Traffic From an IS-IS Node Before Starting Maintenance"
series_title: "Drain Traffic From an IS-IS Node Before Starting Maintenance"
date: 2025-10-23 07:09:00+02:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/feature/5-drain/
---
Here's a cool feature every routing protocol should have: a flag that tells everyone a node is going down, giving them time to adjust their routing tables *before* disrupting traffic flow.

OSPF never had such a feature; common implementations set the cost of all interfaces to a very high value to emulate it. BGP got it (the [Graceful BGP Session Shutdown](https://datatracker.ietf.org/doc/html/rfc8326)) almost 30 years after it was created. IS-IS had the *overload* bit from day one, and it's just what an IS-IS router needs to tell everyone else they should stop using it for transit traffic. You can try it out in the [Drain Traffic Before Node Maintenance](https://isis.bgplabs.net/feature/5-drain/) lab exercise.

[Click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://isis.bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `feature/5-drain` and execute **netlab up**.
