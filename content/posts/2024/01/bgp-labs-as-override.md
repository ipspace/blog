---
title: "BGP Labs: Override Neighbor AS Number in AS Path"
series_title: "Override Neighbor AS Number in AS Path"
date: 2024-01-30 09:47:00+01:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
When I described the [need to turn off the BGP AS-path loop prevention logic](https://blog.ipspace.net/2024/01/bgp-labs-reuse-as-number.html) in scenarios where a Service Provider expects a customer to reuse the same AS number across multiple sites, someone quipped, "_but that should be fixed by the Service Provider, not offloaded to the customer._" 

Not surprisingly, there's a nerd knob for that (AS override), and you can practice it in the next BGP lab exercise: [Fix AS-Path in Environments Reusing BGP AS Numbers](https://bgplabs.net/session/2-asoverride/).

{{<figure src="https://bgplabs.net/session/topology-asoverride.png">}}

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/session/2-asoverride/){{</jump>}}
