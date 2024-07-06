---
date: 2008-10-16 06:34:00.001000+02:00
ospf_tag: config
tags:
- OSPF
- WAN
title: OSPF Ignores Subnet Mask Mismatch on Point-to-Point Links
url: /2008/10/ospf-ignores-subnet-mask-mismatch-on.html
---
The common wisdom says that the [subnet mask mismatch will stop the OSPF adjacency from forming](/2008/10/troubleshooting-ospf-adjacencies.html). In reality, the subnet mask is checked only on the multi-access interfaces and is ignored on point-to-point links. The source of this seemingly weird behavior is the Section 10.5 of [RFC 2328](http://tools.ietf.org/html/rfc2328), which says:

> The generic input processing of OSPF packets will have checked the validity of the IP header and the OSPF packet header. **Next, the values of the Network Mask, HelloInterval, and RouterDeadInterval fields in the received Hello packet must be checked against the values configured for the receiving interface. Any mismatch causes processing to stop and the packet to be dropped.** In other words, the above fields are really describing the attached network\'s configuration. **However, there is one exception to the above rule: on point-to-point networks and on virtual links, the Network Mask in the received Hello Packet should be ignored.**
<!--more-->
Cisco conforms strictly to the RFC and allows OSPF neighbors to form adjacency over a point-to-point link (for example, Frame Relay subinterfaces, but also [unnumbered Ethernet interfaces](../series/unnumbered-interfaces.html)) even when the subnet masks don't match. The routers in my lab happily formed the OSPF adjacency even though I've used a /24 mask on one end of the link and a /30 mask on the other end:

``` code
S1#show ip ospf interface brief
Interface    PID   Area    IP Address/Mask    Cost  State Nbrs F/C
Se1/0.100    1     1       10.0.8.1/24        64    P2P   1/1
Lo0          1     1       10.0.0.1/32        1     LOOP  0/0
S1#show ip ospf neighbor Serial1/0.100
Neighbor ID     Pri   State       Dead Time   Address    Interface
10.0.0.11         0   FULL/  -    00:00:38    10.0.8.2   Serial1/0.100

C1#show ip ospf interface brief
Interface    PID   Area    IP Address/Mask    Cost  State Nbrs F/C
Fa0/0        1     0       10.0.1.1/24        10    BDR   1/1
Lo0          1     0       10.0.0.11/32       1     LOOP  0/0
Se1/0.100    1     1       10.0.8.2/30        64    P2P   1/1
Se1/0.101    1     1       0.0.0.0/0          64    P2P   1/1
C1#show ip ospf neighbor Serial1/0.100
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.0.2.2          0   FULL/  -        00:00:37    10.0.8.1        Serial1/0.100
```
