---
title: "BGP Labs: Advertise the Default Route"
series_title: "Advertise BGP Default Route"
date: 2024-03-28 08:44:00+01:00
tags: [ BGP, netlab ]
series: [ bgp_labs ]
netlab_tag: bgplab
---
If you're an Internet Service Provider running BGP with your customers, you might not want to send them the whole Internet routing table. Sending the regional prefixes *and the default route* is usually good enough.

{{<figure src="https://bgplabs.net/basic/topology-default-route.png">}}
<!--more-->
Likewise, you might want to send the default route in an enterprise network from WAN edge routers to site core routers and might have to use BGP to get the routing information across the firewalls.

In both cases, you have to advertise the default route in BGP updates, and we know that every routing protocol handles default routes slightly differently. You can practice the BGP way of advertising the default route in the [next BGP lab exercise](https://bgplabs.net/basic/c-default-route/).

{{<jump>}}[Explore the lab exercise](https://bgplabs.net/basic/c-default-route/){{</jump>}}
