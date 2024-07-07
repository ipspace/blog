---
date: 2007-03-12 09:33:00+01:00
eigrp_tag: details
tags:
- EIGRP
title: EIGRP Goodbye Message
url: /2007/03/eigrp-goodbye-message/
pre_scroll: true
---
In IOS release 12.3(1.4), Cisco has added Goodbye message to EIGRP protocol. Previously, whenever the router would need to tear down EIGRP adjacency (for example, due to changed summary addresses), it would simply erase the neighbor from its EIGRP neighbor table and pretend the it's just encountered a new neighbor on the next hello message. As the adjacent device does not participate in this charade, it becomes confused resulting in delayed adjacency establishment. The whole process is described in details in [my EIGRP book](http://www.amazon.com/EIGRP-Network-Design-Solutions-Definitive/dp/1578701651), which is unfortunately out-of-print and is available only as an [on-line book on Safari](http://safari.ciscopress.com/1578701651).
<!--more-->
With the Goodbye message, both neighbors tear down the adjacency in an orderly fashion and reestablish it immediately after receiving the EIGRP HELLO message.

You can monitor the new EIGRP hello messages with the **debug eigrp packet hello** command, the Goodbye message also triggers a logging message if the EIGRP logging is enabled with the **eigrp log-neighbor-changes** command (default settings):

```
a1#debug eigrp packet hello
EIGRP Packets debugging is on
(HELLO)
21:27:50: EIGRP: Received HELLO on Serial0/0/0.100 nbr 172.16.1.2
21:27:50: AS 1, Flags 0x0, Seq 0/0 idbQ 0/0 iidbQ un/rely 0/0 peerQ un/rely 0/0
21:27:50: Inteface goodbye received
21:27:50: %DUAL-5-NBRCHANGE: IP-EIGRP(0) 1: Neighbor 172.16.1.2 (Serial0/0/0.100) is down: Interface Goodbye received
21:27:54: EIGRP: Sending HELLO on Serial0/0/0.100
21:27:54: AS 1, Flags 0x0, Seq 0/0 idbQ 0/0 iidbQ un/rely 0/0
21:27:54: EIGRP: Received HELLO on Serial0/0/0.100 nbr 172.16.1.2
21:27:54: AS 1, Flags 0x0, Seq 0/0 idbQ 0/0
21:27:54: %DUAL-5-NBRCHANGE: IP-EIGRP(0) 1: Neighbor 172.16.1.2 (Serial0/0/0.100) is up: new adjacency
```
