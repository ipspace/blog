---
title: "Largest netlab Topology I've Seen So Far"
date: 2022-05-23 06:41:00
tags: [ netlab ]
netlab_tag: use
---
I stumbled upon a blog post by [Diptanshu Singh](https://dipsingh.github.io/about/) discussing whether [IS-IS flooding in highly meshed fabric](https://dipsingh.github.io/IS-IS-Flooding/) is as much of a problem as some people would like to make it. I won't spoil the fun, read his blog post ;)

The really interesting part (for me) was the topology he built with *[netlab](https://netlab.tools/)* and *[containerlab](https://containerlab.dev/)*: seven leaf-and-spine fabrics connected with WAN links and superspines for a total of 68 instances of Arista cEOS. I hope he automated building the topology file (I'm a bit sorry we haven't implemented [composite topologies](https://github.com/ipspace/netlab/discussions/151) yet); after that all he had to do was to execute **[netlab up](https://netlab.tools/netlab/up/)** to get a fully-configured lab running IS-IS.
