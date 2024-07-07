---
date: 2008-02-07 07:05:00.001000+01:00
tags:
- BGP
title: 'BGP Essentials: AS-path Prepending'
url: /2008/02/bgp-essentials-as-path-prepending/
---
Enterprise networks primarily use BGP with their Internet Service Providers if they want to be multi-homed (connected to more than one ISP). A very common requirement in a multi-homed design is the primary/backup setup where the lower speed (or sometimes lower quality) link should only be used when the primary link fails.

Competent ISPs help their customers reach this goal by using *BGP local preference* within their network and giving the customers the ability to indicate the desired value of BGP local preference through *BGP communities*: if the route received directly from the customer has low local preference, all other routes are preferred, resulting in the desired traffic flow that avoids the backup link if at all possible as shown in the next diagram:
<!--more-->
{{<figure src="/2008/02/LocPref.jpg" caption="Using BGP communities to set local preference">}}

Sometimes you are forced to deal with less than ideal ISPs (or the two ISPs you're using are so far apart in the Internet topology that the BGP local preference solution doesn't work). In these cases, the only means of influencing BGP route selection in the Internet is the extension of the AS path attribute (routes with shorter AS paths are preferred) with multiple copies of your own AS number: AS-path prepending.

AS-path prepending is configured in Cisco IOS with **route-map** based per-neighbor outbound filter. The actual prepending is specified within the **route-map** with the **set as-path prepend** command, as illustrated in the following sample configuration:

``` {.code}
router bgp 65001
 neighbor 10.1.0.2 remote-as 65200
 neighbor 10.1.0.2 description Backup ISP
 neighbor 10.1.0.2 route-map prepend out
!
route-map prepend permit 10
 set as-path prepend 65001 65001 65001
```
