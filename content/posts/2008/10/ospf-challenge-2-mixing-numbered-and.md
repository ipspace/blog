---
date: 2008-10-29 07:29:00.003000+01:00
ospf_tag: adj
series_title: "Challenge: Mixing Numbered and Unnumbered Interfaces"
tags:
- OSPF
title: 'OSPF Challenge: Mixing Numbered and Unnumbered Interfaces'
url: /2008/10/ospf-challenge-2-mixing-numbered-and.html
---
Assuming you have the following configurations on R1 and R2:

{{<cc>}}R1 configuration{{</cc>}}
```
hostname R1
!
interface Loopback 0
 ip address 10.0.0.1 255.255.255.255
!
interface Serial 0
 encapsulation ppp
 ip unnumbered Loopback0
 ip ospf 1 area 1
!
router ospf 1
```

{{<cc>}}R2 configuration{{</cc>}}
```
hostname R2
!
interface Serial 0
 encapsulation ppp
 ip address 10.1.2.3 255.255.255.248
 ip ospf 1 area 1
!
router ospf 1
```

What IP address can you use on the loopback interface of R1 to establish adjacency between R1 and R2? Can you use more than one IP address?

You can find the solution [here](/2008/11/ospf-challenge-2-final-results.html).