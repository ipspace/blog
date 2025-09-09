---
title: "Lab: Running IS-IS over IPv4 Unnumbered and IPv6 LLA Interfaces"
series_title: "Running IS-IS over IPv4 Unnumbered and IPv6 LLA Interfaces"
date: 2025-09-12 07:41:00+02:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/basic/7-unnumbered/
---
IS-IS does not use IPv4 or IPv6, so it should be a no-brainer to run it over IPv4 unnumbered or IPv6 LLA interfaces. The latter is true; the former is smack in the middle of the *It Depends&trade;* territory.

Want to know more or test the devices you're usually working with? The [Running IS-IS Over Unnumbered/LLA-only Interfaces](https://isis.bgplabs.net/basic/7-unnumbered/) lab exercise is just what you need.

{{<figure src="https://isis.bgplabs.net/basic/topology-unnumbered.png">}}

[Click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/) (or [set up your own lab infrastructure](https://isis.bgplabs.net/1-setup/)). After starting the lab environment, change the directory to `basic/7-unnumbered` and execute **netlab up**.
