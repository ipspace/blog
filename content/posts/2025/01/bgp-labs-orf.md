---
title: "Use BGP Outbound Route Filters (ORF) for IP Prefixes"
date: 2025-01-24 08:11:00+01:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
---
When a BGP router cannot fit the whole BGP table into its forwarding table (FIB), we often use inbound filters to limit the amount of information the device keeps in its BGP table. That's usually a waste of resources:

* The BGP neighbor has to send information about all prefixes in its BGP table
* The device with an inbound filter wastes additional CPU cycles to drop many incoming updates.

Wouldn't it be better for the device with an inbound filter to push that filter to its BGP neighbors?
<!--more-->
Welcome to the magical world of *Outbound Route Filters*, an idea that looked great in PowerPoint when I was writing my MPLS books 25 years ago. Today, numerous BGP implementations support ORF (at least for IP prefixes), and it's fun to see how well it works in practice; kick the tires in the [next BGP lab exercise](https://bgplabs.net/policy/f-orf/).

{{<figure src="https://bgplabs.net/policy/topology-orf.png">}}

If you haven't [set up your own lab infrastructure](https://bgplabs.net/1-setup/), [click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/). After starting your codespace, change the directory to `policy/f-orf` and execute **netlab up**.
