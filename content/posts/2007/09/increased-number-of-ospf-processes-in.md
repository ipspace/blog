---
date: 2007-09-13 08:34:00.001000+02:00
ospf_tag: config
tags:
- OSPF
- MPLS VPN
title: Increased Number of OSPF processes in MPLS VPN Environments
url: /2007/09/increased-number-of-ospf-processes-in.html
---
When we were writing the [MPLS and VPN architectures books](http://www.google.com/search?q=%22MPLS+VPN+architectures%22+site%3Aamazon.com), there was a limit on the number of OSPF processes you could configure per PE-router. The limit was based on the fact that IOS supports up to 32 routing information sources. Two of them are **static** and **connected**; you also need an IGP and BGP in the MPLS VPN backbone, resulting in 28 OSPF processes that could be configured on a single PE router. This "feature" severely limited OSPF-based MPLS VPN deployments until IOS release 12.3(4)T when the [limitation was removed](http://www.cisco.com/univercd/cc/td/doc/product/software/ios124/124cg/hirp_c/ch15/hospfvf.pdf), resulting in the availability of up to 30 routing processes per VRF.

RIP, BGP, and EIGRP never experienced the same limitations as you configure VRF-specific routing instances within address families of a single routing protocol
<!--more-->
The details of the actual change that took place are not obvious from the IOS documentation; they simply changed the global allocation of routing process identifiers to per-routing-table identifiers. For example, in the following **show ip protocol summary** printouts, the two OSPF processes (one in the global routing table, one in the VRF test) share the same index.

``` code
router#show ip protocols summary
Index Process Name
0 connected
1 static
2 ospf 112
router#show ip protocols vrf Test summary
Index Process Name
0 connected
1 static
2 ospf 111
```
