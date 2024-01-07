---
title: "BGP Labs: Reuse BGP AS Number Across Sites"
series_title: "Reuse BGP AS Number Across Sites"
date: 2024-01-09 08:28:00+01:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
When I published the [Bidirectional Route Redistribution](https://bgplabs.net/basic/5-redistribute/) lab exercise, some readers were [quick to point out](https://blog.ipspace.net/2023/09/bgp-labs-redistribute.html#1920) that you'll probably have to reuse the same AS number across multiple sites in a real-life MPLS/VPN deployment. That's what you can practice in [today's lab exercise](https://bgplabs.net/session/1-allowas_in/) -- an MPLS/VPN service provider allocated the same BGP AS number to all your sites and expects you to deal with the aftermath.

{{<figure src="https://bgplabs.net/session/topology-allowas.png">}}

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/session/1-allowas_in/){{</jump>}}
