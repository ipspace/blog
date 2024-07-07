---
date: 2009-11-23 06:38:00.004000+01:00
ospf_tag: config
tags:
- OSPF
title: “ip ospf mtu-ignore” Is a Dangerous Command
url: /2009/11/ip-ospf-mtu-ignore-is-dangerous-command/
---
A while ago, I wrote about the [problems caused by MTU mismatch between OSPF neighbors](/2007/10/ospf-neighbors-stuck-in-exstart/) and warned that the **ip ospf mtu-ignore** interface configuration command that supposedly solves the problem could cause significant headaches. Last week's challenge was a simple illustration of what could happen if you [force OSPF neighbors to establish a session even though their interface MTUs don't match](/2009/11/challenge-ospf-neighbor-changing-state/) (the very first comment correctly identified the issue).
<!--more-->
This is the router configuration I've used to generate the problem:

{{<cc>}}A1 Configuration{{</cc>}}
```
hostname A1
!
interface Serial1/0
 description Link to C1
 ip address 10.0.7.5 255.255.255.252
 encapsulation ppp
 ip ospf cost 100
 ip ospf mtu-ignore
!
router ospf 1
 log-adjacency-changes
 redistribute static subnets
 network 0.0.0.0 255.255.255.255 area 1
 ```
 
{{<cc>}}C1 configuration{{</cc>}}
```
hostname C1
!
interface Serial1/0
 description Link to A1
 mtu 512
 ip address 10.0.7.6 255.255.255.252
 encapsulation ppp
 ip ospf cost 100
 ip ospf mtu-ignore
 ip ospf 1 area 1
!
router ospf 1
 log-adjacency-changes 
```

The problem occurs when C1 drops the *database description packet* or a flooding packet sent by A1 because it exceeds the MTU size. The dropped packets appear as *giants* or *overruns* in the **show interface** printout.

And now for the entertaining part:

-   The problem is only partially reproducible. Sometimes, the routers are willing to accept oversized packets; sometimes, they drop them. This behavior is probably related to the IOS release and hardware platform used in the tests; it might also be triggered by a particular sequence of configuration commands.
-   The problem appears (if at all) only when the OSPF database grows. Tests in a small lab might work fine, but the production network might crash.
-   When the MTUs differ by only a few bytes, the setup might work for a long time until you happen to stumble across the correct combination of LSAs that generate the DBD or update packet of just the right size.
