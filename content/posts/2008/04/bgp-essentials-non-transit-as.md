---
date: 2008-04-08 07:34:00.001000+02:00
tags:
- BGP
title: 'BGP Essentials: Non-transit AS'
url: /2008/04/bgp-essentials-non-transit-as.html
---
One of the first things you have to do when configuring BGP with your ISP is to ensure you won't become a transit AS. Decent ISPs filter out things that don't belong to you from your updates, but not everyone cares ([including some really big names](/2019/07/rant-some-internet-service-providers.html)), and so small organizations manage to bring down large parts of the Internet just with a few fat fingers.

Here's the BGP configuration you should use on Cisco IOS: apply AS-path access-list to outbound updates with **neighbor filter-list** command:
<!--more-->
``` {.code}
router bgp 65000
 neighbor 10.1.1.1 filter-list 1 out
!
ip as-path access-list 1 permit ^$
```

Of course you can make things really interesting by [introducing BGP communities](/2008/02/bgp-essentials-bgp-communities.html): if you mark all routes received from the EBGP peers with the [NO_EXPORT community](/2008/01/redistributing-customer-routes-into-bgp.html), they will be filtered out on other EBGP sessions automatically :) Here\'s a sample configuration:

``` {.code}
router bgp 65001
 neighbor 10.0.1.2 route-map setNoExport in
 neighbor 10.0.1.3 route-map setNoExport in

!
route-map setNoExport permit 10
 set community no-export additive
```
