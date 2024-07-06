---
title: "BGP Labs: Work with FRR and Cumulus Linux"
series_title: "Work with FRR and Cumulus Linux"
date: 2024-01-19 09:45:00+01:00
tags: [ BGP, netlab ]
netlab_tag: bgplab
---
FRR or (pre-NVUE) Cumulus Linux are the [best bets](/2023/06/learn-routing-protocols-frr.html) if you want to run BGP labs in a resource-constrained environment like your laptop or a small public cloud instance. However, they both behave a bit differently from what one might expect from a networking device, including:

* Interfaces are created through standard Linux tools;
* You have to start the FRR management CLI from the Linux shell;
* If you need a routing daemon (for example, the BGP daemon), you must enable it in the FRR configuration file and restart FRR. 

A [new lab exercise](https://bgplabs.net/basic/0-frrouting/) covers these intricate details and will help you get fluent in configuring BGP on FRR or Cumulus Linux virtual machines or containers.

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/basic/0-frrouting/){{</jump>}}
