---
date: 2008-02-12 07:42:00+01:00
ospf_tag: unnumbered
tags:
- OSPF
title: Configure OSPF on Unnumbered Interfaces
url: /2008/02/configure-ospf-on-unnumbered-interfaces.html
---
When we've been assigning router interfaces in OSPF areas with the network router configuration command, it was impossible to start OSPF only on some unnumbered interfaces and not on others (or place the unnumbered interfaces in different areas). These restrictions are removed if you use the [**ip ospf area** interface configuration command](/2007/07/network-statements-are-no-longer-needed.html).
<!--more-->
For example, to put the loopback interface into another area than the WAN links using its IP address, use the following configuration commands:

``` code
router ospf 1
!
interface Loopback0
 ip address 10.0.0.3 255.255.255.255
 ip ospf 1 area 0
!
interface Serial1/0
 ip unnumbered Loopback0
 ip ospf 1 area 1
!
interface Serial1/1
 ip unnumbered Loopback0
 ip ospf 1 area 2
```
