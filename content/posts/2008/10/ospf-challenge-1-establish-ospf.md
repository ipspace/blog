---
date: 2008-10-18 07:02:00.005000+02:00
ospf_tag: adj
tags:
- OSPF
title: 'Challenge: Establish OSPF Adjacency on a LAN Interface'
url: /2008/10/ospf-challenge-1-establish-ospf/
---
You could get something like this only in a CCIE lab (I would hope): R1 and R2 should establish OSPF adjacency, but you cannot change or remove any of the existing configuration commands (you can add new commands).
<!--more-->
{{<cc>}}R1 configuration{{</cc>}}
```
hostname R1
!
interface FastEthernet 0/0
 ip address 192.168.1.17 255.255.255.0
 ip ospf 1 area 1
!
router ospf 1
```

{{<cc>}}R2 configuration{{</cc>}}
```
hostname R1
!
interface FastEthernet 0/0
 ip address 192.168.1.18 255.255.255.252
 ip ospf 1 area 1
!
router ospf 1
```

You can find the solution [here](/2008/10/ospf-challenge-1-final-results/).
