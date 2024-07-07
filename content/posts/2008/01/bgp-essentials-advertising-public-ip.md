---
date: 2008-01-23 06:53:00+01:00
tags:
- BGP
title: 'Advertising Public IP Prefixes into the Internet'
series: bgp-essentials
url: /2008/01/bgp-essentials-advertising-public-ip/
---
The routing information you source into the public Internet with BGP should be as accurate and stable as possible. The best way to achieve this goal is to statically configure the IP prefixes you've been allocated on your core routers and advertise them into BGP:

-   BGP will only advertise an IP prefix if a matching entry is found in the IP routing table. To ensure the IP prefix you want to advertise is always present, configure an IP static route to **null** interface, unless you\'re advertising a connected interface (example: Internet edge router on a DMZ segment).
-   Most public IP prefixes advertised today do not fall on the [classful network boundary](http://en.wikipedia.org/wiki/Classful). To advertise a classless prefix, you have to configure the prefix and the mask in the BGP routing process.
<!--more-->
**Important:** In large networks you should advertise your IP prefixes from your core routers, not from the edges of your network. If an edge router loses its link to the network core but still advertises your IP address space, all the traffic attracted by it will be blackholed. In enterprise networks using BGP for Internet multihoming, it might be safe to advertise directly connected interfaces on Internet edge routers.

You can set additional BGP attributes on the IP prefix you're advertising with a **route-map** attached to the network statement. For example, the following configuration could be used on one of your core routers to advertise IP prefix 172.16.128.0/18 and attach a BGP community to it:

``` {.code}
ip route 172.16.128.0 255.255.192.0 Null0
!
router bgp 65001
 network 172.16.128.0 mask 255.255.192.0 route-map SetCommunity
!
route-map SetCommunity permit 10
 set community 65001:101 additive
```
