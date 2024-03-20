---
date: 2023-10-07 06:18:00+00:00
evpn_tag: read
series_title: Introduction of EVPN at DE-CIX
tags:
- EVPN
- VXLAN
title: 'Worth Reading: Introduction of EVPN at DE-CIX'
---
Numerous Internet Exchange Points (IXP) started using VXLAN years ago to replace tradition layer-2 fabrics with routed networks. Many of them tried to avoid the complexities of EVPN and used VXLAN with statically-configured (and hopefully automated) ingress replication.

A few went a step further and decided to deploy EVPN, primarily to deploy Proxy ARP functionality on EVPN switches and reduce the ARP/ND traffic. Thomas King from DE-CIX [described their experience](https://blog.apnic.net/2023/08/16/peering-lan-2-0-introduction-of-evpn-at-de-cix/) on APNIC blog -- well worth reading if you're interested in layer-2 fabrics.
