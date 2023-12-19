---
date: 2008-04-15 07:04:00.007000+02:00
ospf_tag: config
tags:
- OSPF
title: Subnet Masks in OSPF Network Statements
url: /2008/04/ai-artificial-intelligence-in-cisco-ios.html
pre_scroll: True
---
In a comment to my recent [NTP-related post mentioning OSPF configuration](https://blog.ipspace.net/2008/04/technology-is-supposed-to-be-simple.html), Wan Tajuddin [correctly stated that the OSPF **network** statement should contain the wildcard bits](https://blog.ipspace.net/2008/04/technology-is-supposed-to-be-simple.html?showComment=1208142000000#c1375575532105655159), not the subnet mask. However, I was positive I had running networks with the **network 0.0.0.0 0.0.0.0 area 0** OSPF configuration, so it was time for one more lab test. As it turns out, Cisco IOS started accepting either the wildcard bits or the subnet mask in the **network** OSPF configuration command.
<!--more-->
Here is the printout from the test run. First, the traditional configuration:

``` code
R1#show run ¦ sect router ospf
router ospf 1
 log-adjacency-changes
 network 0.0.0.0 255.255.255.255 area 0
R1#show ip ospf interface brief
Interface    PID   Area  IP Address/Mask    Cost  State Nbrs F/C
Lo0          1     0     10.0.1.1/32        1     LOOP  0/0
Se1/1        1     0     10.0.7.5/30        70    P2P   1/1
Se1/0        1     0     10.0.7.1/30        64    P2P   1/1
Fa0/0        1     0     10.0.0.1/24        10    WAIT  0/0
```

The configuration uses the wildcard bits, and all interfaces are in area 0 as expected. Now let\'s try to specify the 0.0.0.0/0 network:

```
R1#conf t
Enter configuration commands, one per line. End with CNTL/Z.
R1(config)#no router ospf 1
Mar 1 00:09:37.640: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.3 on Serial1/1 from FULL to DOWN, Neighbor Down: Interface down or detached
Mar 1 00:09:37.648: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.2 on Serial1/0 from FULL to DOWN, Neighbor Down: Interface down or detached
R1(config)#router ospf 1
R1(config-router)#network 0.0.0.0 0.0.0.0 area 0
R1(config-router)#^Z
R1#
Mar 1 00:09:50.944: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.3 on Serial1/1 from LOADING to FULL, Loading Done
Mar 1 00:09:51.104: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.2 on Serial1/0 from LOADING to FULL, Loading Done
R1#show ip ospf interface brief
Interface PID Area IP Address/Mask Cost State Nbrs F/C
Lo0        1    0      10.0.1.1/32    1 LOOP  0/0
Se1/1      1    0      10.0.7.5/30   70 P2P   1/1
Se1/0      1    0      10.0.7.1/30   64 P2P   1/1
Fa0/0      1    0      10.0.0.1/24   10 WAIT  0/0
```

OK, it works for the _all IP addresses_ prefix (default route). How about a specific subnet (10.0.7.0/24)?

```
R1#conf t
Enter configuration commands, one per line. End with CNTL/Z.
R1(config)#no router ospf 1
Mar 1 00:09:37.640: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.3 on Serial1/1 from FULL to DOWN, Neighbor Down: Interface down or detached
Mar 1 00:09:37.648: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.2 on Serial1/0 from FULL to DOWN, Neighbor Down: Interface down or detached
R1(config)#router ospf 1
R1(config-router)#network 10.0.7.0 255.255.255.0 area 0
R1(config-router)#^Z
R1#
Mar 1 00:09:50.944: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.3 on Serial1/1 from LOADING to FULL, Loading Done
Mar 1 00:09:51.104: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.1.2 on Serial1/0 from LOADING to FULL, Loading Done
R1#show ip ospf interface brief
Interface PID Area IP Address/Mask Cost State Nbrs F/C
Se1/1       1    0     10.0.7.5/30   70   P2P  1/1
Se1/0       1    0     10.0.7.1/30   64   P2P 1/1
```

As expected, only the WAN interfaces _with IP addresses in the specified IP address range_ are in the OSPF process -- Cisco IOS correctly recognizes IP prefix specifications, including subnet masks.

OK, but let's see how the router stores the OSPF configuration:

``` code
R1#show running-config ¦ section router ospf
router ospf 1
 log-adjacency-changes
 network 10.0.7.0 0.0.0.255 area 0
```

Cool. The router automatically inverts the subnet mask into wildcard bits, so even if you use the "wrong" format on the CCIE lab, the automatic grading program will get the expected results :)

### Further reading:

-   [Be smart when using the OSPF network statement](https://blog.ipspace.net/2007/07/be-smart-when-using-ospf-network.html)
-   [Network statements in the OSPF process are no longer order-dependent](https://blog.ipspace.net/2006/11/network-statements-in-ospf-process-are.html)
-   [Network statements are no longer needed in OSPF configuration](https://blog.ipspace.net/2007/07/network-statements-are-no-longer-needed.html)
