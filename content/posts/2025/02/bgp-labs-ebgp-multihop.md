---
title: "Run BGP Across a Firewall"
date: 2025-02-21 08:29:00+01:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
redirect: https://bgplabs.net/basic/e-ebgp-multihop/
---
When I [asked my readers what they would consider a good use case for EBGP multihop](/2024/06/ebgp-multihop-use-cases/) (thanks again to everyone who answered!), many suggested running BGP across a layer-3 firewall (Running BGP across a "transparent" (bump-in-the-wire) firewall is trivial). I turned that suggestion into a [lab exercise](https://bgplabs.net/basic/e-ebgp-multihop/) in which you have to establish an EBGP multihop session across a "firewall" simulated by a Linux host.

{{<figure src="https://bgplabs.net/basic/topology-ebgp-multihop.png">}}

If you haven't [set up your own lab infrastructure](https://bgplabs.net/1-setup/), [click here](https://github.com/codespaces/new/bgplab/bgplab) to start the lab in your browser [using GitHub Codespaces](https://bgplabs.net/4-codespaces/). After starting your codespace, change the directory to `basic/e-ebgp-multihop` and execute **netlab up**.
