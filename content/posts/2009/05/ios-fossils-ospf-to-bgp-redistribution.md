---
date: 2009-05-13 06:27:00.004000+02:00
ospf_tag: config
tags:
- OSPF
- IOS fossils
- BGP
title: 'IOS Fossils: OSPF-to-BGP Redistribution'
url: /2009/05/ios-fossils-ospf-to-bgp-redistribution.html
---
Here's a weird requirement that you could get on a really hard CCIE preparation lab (and hopefully never in a live network): redistribute external OSPF routes from selected ASBRs into BGP without using a route map on the redistribution router.

For example, assuming R1 and R2 insert external routes into OSPF, you want only routes from R1 to be redistributed into BGP on R3, but you cannot use route maps on R3.
<!--more-->
**Answer:** OSPF external routes with tags greater than 3758096384 are not redistributed into BGP.

**Solution:** You can set the OSPF route tags on the originating ASBRs with the **redistribute ... tag _value_**router configuration command, and the router performing OSPF-to-BGP redistribution configured with **redistribute ospf _pid_** performs automatic filtering.

**Sample configurations**: I used the following OSPF configurations on R1 and R2

{{<cc>}}OSPF configuration on R1{{</cc>}}
``` code
R1#show run | section router ospf
router ospf 1
 log-adjacency-changes
 redistribute static subnets
 network 10.0.0.0 0.255.255.255 area 0
```

{{<cc>}}R2 is redistributing static routes into OSPF{{</cc>}}
```
R2#show run | section router ospf
router ospf 1
 log-adjacency-changes
 redistribute static subnets tag 3758096385
 network 0.0.0.0 255.255.255.255 area 0
```

You can inspect the OSPF external routes on R3 and verify that only one of them gets inserted into BGP, even though all OSPF external routes should be redistributed.

{{<cc>}}OSPF routes and the BGP table on R3{{</cc>}}
``` code
R3#show run | section router bgp
router bgp 65000
 no synchronization
 bgp log-neighbor-changes
 redistribute ospf 1 match external 1 external 2
 neighbor 10.0.1.1 remote-as 65000

R3#show ip ospf data external | inc Link State|Tag
                Type-5 AS External Link States
  Link State ID: 10.2.1.0 (External Network Number )
        External Route Tag: 3758098606
  Link State ID: 10.2.2.0 (External Network Number )
        External Route Tag: 0

R3#show ip bgp | begin Network
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.2.2.0/24      10.0.7.10               20         32768 ?
```

By now, you're probably wondering what's going on. The behavior is the result of section 4.4.6 of [RFC 1403](http://www.ietf.org/rfc/rfc1403.txt) (3758096384 = 14 \* 2\^28), which was published in 1993 (and that's the reason this post belongs to "IOS Fossils").
