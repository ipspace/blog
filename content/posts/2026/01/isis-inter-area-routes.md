---
title: "Lab: Distributing Level-2 IS-IS Routes into Level-1 Areas"
series_title: "Distributing Level-2 IS-IS Routes into Level-1 Areas"
date: 2026-01-21 08:06:00+01:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
---
One of the major differences between OSPF and IS-IS is their handling of inter-area routes. Non-backbone OSPF intra-area routes are copied into the backbone area and later (after the backbone SPF run) copied into other areas. IS-IS does not copy level-2 routes into level-1 areas; level-1 areas (by default) behave like totally stubby OSPF areas with the level-1 routers using the Attached (ATT) bit of level-1-2 routers in the same area to generate the default route.
<!--more-->
As always, there's a nerd knob to change that behavior, and you can explore it (and its consequences) in the [Distributing Level-2 IS-IS Routes into Level-1 Areas](https://isis.bgplabs.net/advanced/2-route-leak/) lab exercise created by [Dan Partelly](https://github.com/danpartelly).

{{<figure src="https://isis.bgplabs.net/advanced/topology-multiarea.png">}}

[Click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://isis.bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `advanced/2-route-leak` and execute **netlab up**.

{{<jump>}}[Explore the lab exercise](https://isis.bgplabs.net/advanced/2-route-leak/){{</jump>}}