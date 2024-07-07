---
date: 2006-11-18 12:22:00+01:00
tags:
- OSPF
title: Network Statements in the OSPF Process Are No Longer Order-Dependent
url: /2006/11/network-statements-in-ospf-process-are/
ospf_tag: config
---
When I was still teaching Cisco courses, we were telling the students that the order of **network** statements in an OSPF process was important if their ranges were overlapping; the first **network** statement that matched an interface IP address would place that interface in the corresponding area. This is no longer true; Cisco IOS now properly handles overlapping **network area** configuration commands.

Consider the following example:
<!--more-->
```
fw#conf t
Enter configuration commands, one per line. End with CNTL/Z.
fw(config)#router ospf 100
fw(config-router)#network 0.0.0.0 255.255.255.255 area 0
fw(config-router)#network 10.0.0.0 0.0.3.255 area 1
13:06:57: %OSPF-6-AREACHG: 10.0.0.0 255.255.252.0 changed from area 0 to area 1
fw(config-router)#network 10.0.0.0 0.0.0.7 area 2
13:07:10: %OSPF-6-AREACHG: 10.0.0.0 255.255.255.248 changed from area 1 to area 2
fw(config-router)#^Z
```

I've entered overlapping network statements, each one with a smaller address range. Not only does IOS detect that they overlap, but it also prints nice syslog messages and reorders the commands in the running configuration. Well done!

``` code
fw#show run | begin router ospf
router ospf 100
 log-adjacency-changes
 network 10.0.0.0 0.0.0.7 area 2
 network 10.0.0.0 0.0.3.255 area 1
 network 0.0.0.0 255.255.255.255 area 0
```
