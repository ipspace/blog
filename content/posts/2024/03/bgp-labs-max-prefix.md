---
title: "BGP Labs: Limit the Number of Accepted BGP Prefixes"
series_title: "Limit the Number of Accepted BGP Prefixes"
date: 2024-03-07 09:27:00+01:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
Here's an easy way to stop fat-finger incidents in which an end-user autonomous system redistributes IGP into BGP or advertises the whole DFZ routing table from affecting the entire Internet: limit the number of BGP prefixes your routers accept from your customers. You can practice this nifty feature in the [next BGP lab exercise](https://bgplabs.net/basic/b-max-prefix/).

{{<figure src="https://bgplabs.net/basic/topology-max-prefix.png">}}

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/basic/b-max-prefix/){{</jump>}}
