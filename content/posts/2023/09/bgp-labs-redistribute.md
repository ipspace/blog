---
title: "BGP Labs: Bidirectional Route Redistribution"
series_title: "Bidirectional Route Redistribution"
date: 2023-09-13 06:32:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
In the next [BGP labs](https://bgplabs.net/) exercise you'll build the [customer part of an MPLS/VPN solution](https://bgplabs.net/basic/5-redistribute/). You'll use bidirectional OSPF-to-BGP route redistribution to connect two sites running OSPF over a Service Provider MPLS backbone.

{{<figure src="https://bgplabs.net/basic/topology-2-sites.png">}}

I would strongly recommend to [run labs with _netlab_](https://bgplabs.net/1-setup/), but if you like extra work, feel free to use [any system you like including physical hardware](https://bgplabs.net/external/).