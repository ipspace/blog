---
title: "Lab: Hide Transit Subnets in IS-IS Networks"
series_title: "Hide Transit Subnets in IS-IS Networks"
date: 2025-10-17 07:46:00+02:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/feature/4-hide-transit/
---
Sometimes you want to assign IPv4/IPv6 subnets to transit links in your network (for example, to identify interfaces in *traceroute* outputs), but don't need to have those subnets in the IP routing tables throughout the whole network. Like OSPF, IS-IS has a nerd knob you can use to exclude transit subnets from the router PDUs.

Want to check how that feature works with your favorite device? Use the [Hide Transit Subnets in IS-IS Networks](https://isis.bgplabs.net/feature/4-hide-transit/) lab exercise.

{{<figure src="https://isis.bgplabs.net/feature/topology-hide-transit.png">}}

[Click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://isis.bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `feature/4-hide-transit` and execute **netlab up**.
