---
date: 2020-02-02 11:21:00.001000+01:00
tags:
- SD-WAN
- performance
- worth reading
title: 'Worth Reading: SD-WAN Scalability Challenges'
url: /2020/02/worth-reading-sd-wan-scalability/
sd-wan_tag: reality
---
In January 2020 Doug Heckaman [documented his experience with VeloCloud SD-WAN](https://blog.heckanet.net/2020/01/17/vmware-velocloud-edge-configuration-quirks/). He tried to be positive, but for whatever reason this particular bit caught my interest:

> Edge Gateways have a limited number of tunnels they can support \[...\]

WTF? Wasn't x86-based software packet forwarding supposed to bring infinite resources and nirvana? How badly written must your solution be to have a limited number of IPsec tunnels on a decent x86 CPU?
<!--more-->
> But if you don't limit what traffic is allowed between branches, you could run into situations where some process \[...\] will trigger the creation of dynamic VPNs between ALL the branches. The Edges will run out of memory or CPU and start to drop traffic, OSPF will drop routes intermittently as the OSPF process competes for resources \[...\]

We've seen similar problems in DMVPN... a decade ago. One would have hoped that the industry would learn from past mistakes and shortcomings, separate data- and control-plane, protect control plane resources... but evidently *those who do not learn history are doomed to repeat it*, yet again using their customers as scalability testers.
