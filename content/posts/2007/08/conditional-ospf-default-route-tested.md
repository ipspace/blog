---
date: 2007-08-01 07:47:00.002000+02:00
ospf_tag: default
series_title: tested configuration
tags:
- OSPF
- IP routing
title: 'Conditional OSPF Default Route: Tested Configuration'
url: /2007/08/conditional-ospf-default-route-tested.html
---
One of my readers asked for a working configuration of the [conditional OSPF default route advertisement feature](https://blog.ipspace.net/2007/06/ospf-default-route-design-scenarios.html). In my scenario, the OSPF default route would be announced whenever an Internet prefix (172.18.0.0/16) would be present in the IP routing table.

``` code
router ospf 1
 log-adjacency-changes
 network 0.0.0.0 255.255.255.255 area 0
 default-information originate always route-map FromInternet
!
router bgp 11
 bgp log-neighbor-changes
 neighbor 172.16.1.2 remote-as 21
!
ip access-list standard FromInternet
 permit 172.18.0.0
!
route-map FromInternet permit 10
 match ip address FromInternet
```

**Caveats:**

-   The route map configured in the **default-information originate** command tests the IP prefixes in the IP routing table. You can thus match only on those attributes that are present in the IP routing table (IP prefix, metric, next-hop), not on additional BGP attributes (like AS-path), which would be really cool
-   Contrary to what [Sebastian wrote in his comment](https://blog.ipspace.net/2007/06/ospf-default-route-design-scenarios.html#comment-5507351136262865205), you don't have to redistribute the BGP route into OSPF to make it work in IOS release 12.4(11)T or 12.2SRC, but it looks the IP prefix you test cannot be a subnet.
