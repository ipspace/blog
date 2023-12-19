---
date: 2008-02-14 07:44:00+01:00
ospf_tag: details
tags:
- OSPF
title: Common Sense Prevails Over RFC 2328
url: /2008/02/common-sense-prevails-over-rfc-2328.html
---
When trying to extract the OSPF route selection rules from [RFC 2328](http://rfc.net/rfc2328.html), I\'ve stumbled across a [very weird rule (section 16.4.1)](http://rfc.net/rfc2328.html#p175): if an ASBR within a non-backbone area advertises an external route (or if the forwarding address is within the non-backbone area), it\'s preferred over external routes advertised by ASBRs in other areas *regardless of its metric*. I simply had to test this on Cisco IOS ... and found out that Cisco engineers prefer common sense to OSPF RFC.
<!--more-->
I\'ve built a sample network where two routers (*10.0.0.11* in area 1, *10.0.0.3* in the backbone area) advertise the same external routes. The router in area 1 advertises the routes with a higher metric:

``` code
S2#ospfExternals
 
External OSPF routes for OSPF process ID 1
 
  Prefix                Cost   Tag            ASBR Forward addr
==================================================================
> 10.1.0.1/32          10 E1     1        10.0.0.3
  10.1.0.1/32        2000 E1     1       10.0.0.11
> 10.1.0.2/32           5 E2     2        10.0.0.3
  10.1.0.2/32         200 E2     2       10.0.0.11
```

You can use the **show ip ospf route** command to verify which ASBR is within the area. An abbreviated printout is included:

``` code
S2#show ip ospf route
 
    Intra-area Router Path List
i 10.0.0.11 [64] via 10.0.2.17, Serial1/2, ASBR, Area 1, SPF 2
i 10.0.0.2 [64] via 10.0.2.13, Serial1/1, ABR, Area 1, SPF 2
i 10.0.0.1 [64] via 10.0.2.5, Serial1/0, ABR, Area 1, SPF 2
 
    Inter-area Router Path List
I 10.0.0.3 [128] via 10.0.2.5, Serial1/0, ASBR, Area 1, SPF 2
```

As you can see, 10.0.0.11 is within area 1, whereas 10.0.0.3 is in another area. Still, IOS prefers external routes advertised by 10.0.0.3 due to their lower metric:

``` code
S2#show ip ospf route
    External Route List
*>  10.1.0.1/32, Ext1, cost 138, tag 1
      via 10.0.2.5, Serial1/0
*>  10.1.0.2/32, Ext2, cost 5, tag 2
      via 10.0.2.5, Serial1/0
```
