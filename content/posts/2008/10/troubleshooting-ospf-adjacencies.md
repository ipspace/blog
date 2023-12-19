---
date: 2008-10-15 07:24:00.001000+02:00
ospf_tag: adj
tags:
- OSPF
title: Troubleshooting OSPF Adjacencies
url: /2008/10/troubleshooting-ospf-adjacencies.html
---
Troubleshooting OSPF adjacencies can be a nightmare: if you've misconfigured the OSPF interface parameters (the timers or the subnet mask), the adjacency will not form, but the router will not tell you why. The only mechanism you can use to detect the mismatch is the **debug ip ospf hello** command ... just don't try to use it on a console session of a router running OSPF across hundreds of interfaces.

The OSPF hello event debugging does not display OSPF packets received from a different subnet. If you configure mismatched IP subnets (not the subnet mask) on adjacent routers, you will not see any received hello packets.

{{<note info>}}To limit the debugging outputs to a single interface, use the **debug interface** command.{{</note>}}
<!--more-->
For example, in my test network, the routers did not want to establish adjacency on the Fast Ethernet interface:

``` code
C1#show ip ospf interface brief
Interface    PID   Area    IP Address/Mask    Cost  State Nbrs F/C
Fa0/0        1     0       10.0.1.1/25        10    DR    0/0
Lo0          1     0       10.0.0.11/32       1     LOOP  0/0
Se1/0.101    1     1       0.0.0.0/0          64    P2P   1/1
Se1/0.100    1     1       0.0.0.0/0          64    P2P   1/1
C1#show ip ospf neighbor

Neighbor ID  Pri   State        Dead Time   Address    Interface
10.0.0.2       0   FULL/  -     00:00:38    10.0.0.2   Serial1/0.101
10.0.2.2       0   FULL/  -     00:00:36    10.0.0.1   Serial1/0.100
```

Using the OSPF hello debugging limited to the Fast Ethernet interface, I quickly discovered the source of the problem: the subnet mask mismatch between the adjacent routers.

``` code
C1#debug interface FastEthernet 0/0
Condition 1 set
C1#debug ip ospf hello
OSPF hello events debugging is on
C1#
OSPF: Rcv hello from 10.0.0.12 area 0 from FastEthernet0/0 10.0.1.2
OSPF: Mismatched hello parameters from 10.0.1.2
OSPF: Dead R 40 C 40, Hello R 10 C 10  Mask R 255.255.255.0 C 255.255.255.128
```
