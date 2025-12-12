---
title: "Lab: Multilevel IS-IS Deployments"
series_title: "Multilevel IS-IS Deployments"
date: 2025-12-12 11:45:00+01:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/advanced/1-multilevel/
---
Like OSPF, IS-IS was designed when router memory was measured in megabytes and clock speeds in megahertz. Not surprisingly, it includes a scalability mechanism similar to OSPF areas. An IS-IS router could be a level-1 router (having in-area prefixes and a default route), a level-2 router (knowing just inter-area prefixes), or a level-1-2 router (equivalent to OSPF ABR).

Even though multilevel IS-IS is rarely used today, it always makes sense to understand how things work, and the [Multilevel IS-IS Deployments](https://isis.bgplabs.net/advanced/1-multilevel/) lab exercise created by [Dan Partelly](https://github.com/danpartelly) gives you a perfect starting point.

{{<figure src="https://isis.bgplabs.net/advanced/topology-multiarea.png">}}

[Click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://isis.bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `advanced/1-multilevel` and execute **netlab up**.
