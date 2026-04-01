---
title: "Lab: Summarizing IS-IS Level-1 Routes"
series_title: "Summarizing IS-IS Level-1 Routes"
date: 2026-04-03 08:02:00+01:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
---
IS-IS was designed to carry [node addresses](https://blog.ipspace.net/2024/02/interface-node-addresses/) (NSAPs) between level-1 routers (called *Intermediate Systems*) within an area and area prefixes between level-2 routers, resulting in a perfect separation of concerns and forwarding information summarization. When IETF tried to use the same routing protocol for a networking stack with a [completely different addressing mentality](https://blog.ipspace.net/2021/05/fundamentals-need-interface-addresses/), something had to give.
<!--more-->
By default, IS-IS in the IP world (like OSPF) does not do prefix summarization, and the summarization ranges must be configured by the network operator. Want to try out how that works? The [Summarizing Level-1 Routes into Level-2 Backbone](https://isis.bgplabs.net/advanced/3-summarization/) lab exercise is waiting for you.

{{<figure src="https://isis.bgplabs.net/advanced/topology-summarization.png">}}

If you already set up your own _netlab_ environment, you probably know what to do (or you can get the [details here](https://isis.bgplabs.net/1-setup/)). Alternatively, you can [click here](https://github.com/codespaces/new/bgplab/isis) to start the lab in your browser [using GitHub Codespaces](https://isis.bgplabs.net/4-codespaces/). After starting the lab environment, change the directory to `advanced/3-summarization` and execute **netlab up**.

{{<jump>}}[Explore the lab exercise](https://isis.bgplabs.net/advanced/3-summarization/){{</jump>}}