---
date: 2007-08-14 07:15:00+02:00
ospf_tag: details
tags:
- OSPF
title: OSPF Graceful Shutdown
url: /2007/08/ospf-graceful-shutdown.html
---
Reloading a core router in a high-availability network is always a tricky proposition. Even if you tweak the routing protocol hello timers (or use fast L2 mechanisms to detect next-hop loss), it still takes a few seconds for the routing protocols to converge. For example, when using OSPF, the adjacent routers have to detect the neighbor loss, change their router LSAs, flood them (LSA flooding is rate-limited), the changed LSAs have to be propagated across the whole area and all routers in the area have to run SPF (which is also rate-limited).

It would be much better if you could gracefully take a router offline by increasing the OSPF cost on all its interfaces, thus forcing an OSPF SPF run while the router is still capable of forwarding the traffic (resulting in no packet loss).
<!--more-->
The [OSPF stub router advertisement](http://www.cisco.com/univercd/cc/td/doc/product/software/ios122/122newft/122t/122t4/ftospfau.htm) (as this feature is officially called) documented in [RFC 3137](http://www.faqs.org/rfcs/rfc3137.html) is implemented in Cisco IOS release 12.2(4)T and 12.3. To force the router into stub status (prior to reboot/shutdown), use the **max-metric router-lsa** router configuration command. This command will change the OSPF metric for all non-stub interfaces in the router LSA to 65535.

{{<note info>}}The *infinite* metric in the router LSA does not force the other routers to ignore the path, just nudge them into using alternate paths. The other routers in the network will thus select alternate OSPF paths (if they exist), but not the potential non-OSPF paths. Those will be selected only after the actual router reboot/shutdown.{{</note>}}
<!--more-->
This is a sample router LSA after the **max-metric router-lsa** has been configured:

``` code
b1#show ip ospf data router 172.16.0.21

OSPF Router with ID (172.16.0.21) (Process ID 1)

Router Link States (Area 0)

Exception Flag: Announcing maximum link costs
LS age: 18
Options: (No TOS-capability, DC)
LS Type: Router Links
Link State ID: 172.16.0.21
Advertising Router: 172.16.0.21
LS Seq Number: 80000003
Checksum: 0x88B2
Length: 72
Number of Links: 4

Link connected to: a Stub Network
(Link ID) Network/subnet number: 172.16.0.21
(Link Data) Network Mask: 255.255.255.255
Number of TOS metrics: 0
TOS 0 Metrics: 1

Link connected to: another Router (point-to-point)
(Link ID) Neighboring Router ID: 172.16.0.11
(Link Data) Router Interface address: 172.16.1.2
Number of TOS metrics: 0
 TOS 0 Metrics: 65535

Link connected to: a Stub Network
(Link ID) Network/subnet number: 172.16.1.0
(Link Data) Network Mask: 255.255.255.252
Number of TOS metrics: 0
TOS 0 Metrics: 50

Link connected to: a Transit Network
(Link ID) Designated Router address: 192.168.0.6
(Link Data) Router Interface address: 192.168.0.5
Number of TOS metrics: 0
 TOS 0 Metrics: 65535
```
