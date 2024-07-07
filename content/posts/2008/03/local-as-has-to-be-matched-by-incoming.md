---
date: 2008-03-20 07:32:00.002000+01:00
tags:
- BGP
title: Local-AS Has to Be Matched by Incoming Filter-List
url: /2008/03/local-as-has-to-be-matched-by-incoming/
---
In a previous post I\'ve described how you can use **neighbor local-as** feature to [fix AS-number mismatch](/2008/01/fix-bgp-as-number-mismatch/) between adjacent autonomous systems. However, without additional options, the **local-as** is inserted in the AS-path of incoming BGP updates *before any inbound filters*. Your inbound filters thus have to match the **local-as** as well.
<!--more-->
Consider, for example, the following configuration:

``` {.code}
router bgp 65001
 neighbor 10.1.0.2 remote-as 10
 neighbor 10.1.0.2 local-as 20
 neighbor 10.1.0.2 filter-list 1 in
!
ip as-path access-list 1 permit ^10$
```

Although the configuration looks correct, no routes are accepted from AS 10, as the inbound AS-path always contains locally prepended AS 20 as well as AS 10:

``` {.code}
R1#show ip bgp neighbor 10.1.0.2 received-routes | begin ^$
 
   Network     Next Hop      Metric LocPrf Weight Path
*  172.16.0.0  10.1.0.2           0             0 20 10 i
```

To fix this problem, you either have to include local AS in the AS-path access-list or [use the **no-prepend** option of the **neighbor local-as** command](/2008/01/fix-bgp-as-number-mismatch/).
