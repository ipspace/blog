---
title: "FRRouting RIB and FIB"
date: 2024-03-20 07:39:00+0100
tags: [ BGP, OSPF ]
pre_scroll: True
---
This is how we [described the interactions](/2010/09/ribs-and-fibs/) between routing protocol tables, RIB, and FIB in the ancient times:

* Routing protocols compute the best paths to all known prefixes.
* These paths compete for entry in the routing table. The path(s) with the lowest administrative distance win.
* The entries from the routing table are fully evaluated (in particular, their next hops) and entered in the forwarding table.

Let's use a simple BGP+OSPF network to illustrate what I'm talking about:
<!--more-->
{{<ascii>}}
┌─────────────────────────────────────────┐
│                                         │
│                  ┌────────┐  ┌────────┐ │
│ ┌─────────────┐  │   R1   │  │   R2   │ │
│ │172.16.0.0/24├──┤10.0.0.1├──┤10.0.0.2│ │
│ └─────────────┘  └────────┘  └────────┘ │
│ AS 65000                                │
└─────────────────────────────────────────┘
{{</ascii>}}

R1 advertises the prefix 172.16.0.0/24 in OSPF and IBGP. When running Arista EOS on R2, you can observe the BGP prefix in the BGP table, but only the OSPF prefix gets into the routing table:

```
r2>show ip bgp 172.16.0.0
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for 172.16.0.0/24
 Paths: 1 available
  Local
    10.0.0.1 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, IGP metric 20, weight 0, tag 0
      Received 00:03:01 ago, valid, internal, best
      Rx SAFI: Unicast

r2>show ip route | begin Gateway
Gateway of last resort is not set

 O        10.0.0.1/32 [110/20]
           via 10.1.0.1, Ethernet1
 C        10.0.0.2/32
           directly connected, Loopback0
 C        10.1.0.0/30
           directly connected, Ethernet1
 O        172.16.0.0/24 [110/20]
           via 10.1.0.1, Ethernet1
```

Recent releases of FRRouting are different. FRRouting uses its own IP routing manager ([zebra](https://docs.frrouting.org/en/latest/zebra.html)), which collects routes from various sources and stores *all of them* in the IP routing table.

When running FRRouting on R2, you can see OSPF and BGP entries for 172.16.0.0/24 in the IP routing table:

```
r2# show ip route
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

K>* 0.0.0.0/0 [0/0] via 192.168.121.1, eth0, 00:00:31
O>* 10.0.0.1/32 [110/20] via 10.1.0.1, eth1, weight 1, 00:00:12
O   10.0.0.2/32 [110/10] via 0.0.0.0, lo0 onlink, weight 1, 00:00:27
C>* 10.0.0.2/32 is directly connected, lo0, 00:00:29
O   10.1.0.0/30 [110/10] is directly connected, eth1, weight 1, 00:00:27
C>* 10.1.0.0/30 is directly connected, eth1, 00:00:29
B   172.16.0.0/24 [200/0] via 10.0.0.1 (recursive), weight 1, 00:00:11
                            via 10.1.0.1, eth1, weight 1, 00:00:11
O>* 172.16.0.0/24 [110/20] via 10.1.0.1, eth1, weight 1, 00:00:12
C>* 192.168.121.0/24 is directly connected, eth0, 00:00:31
```

The *route with the lowest admin distance wins* decision is made when the prefixes from the zebra IP routing table are copied into the kernel routing table, which FRRouting calls *forwarding table* (FIB):

```
r2# show ip fib
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

K>* 0.0.0.0/0 [0/0] via 192.168.121.1, eth0, 00:03:01
O>* 10.0.0.1/32 [110/20] via 10.1.0.1, eth1, weight 1, 00:02:42
C>* 10.0.0.2/32 is directly connected, lo0, 00:02:59
C>* 10.1.0.0/30 is directly connected, eth1, 00:02:59
O>* 172.16.0.0/24 [110/20] via 10.1.0.1, eth1, weight 1, 00:02:42
C>* 192.168.121.0/24 is directly connected, eth0, 00:03:01
```

To confuse you even further, the Linux **ip route** command does not print the /32 prefixes configured on the local interfaces:

```
r2(bash)#ip route
default via 192.168.121.1 dev eth0
10.0.0.1 nhid 20 via 10.1.0.1 dev eth1 proto ospf metric 20
10.1.0.0/30 dev eth1 proto kernel scope link src 10.1.0.2
172.16.0.0/24 nhid 20 via 10.1.0.1 dev eth1 proto ospf metric 20
192.168.121.0/24 dev eth0 proto kernel scope link src 192.168.121.102
```

To get those entries, use the **ip route list table local** command:

```
r2(bash)#ip route list table local
local 10.0.0.2 dev lo0 proto kernel scope host src 10.0.0.2
broadcast 10.0.0.2 dev lo0 proto kernel scope link src 10.0.0.2
local 10.1.0.2 dev eth1 proto kernel scope host src 10.1.0.2
broadcast 10.1.0.3 dev eth1 proto kernel scope link src 10.1.0.2
local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1
local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1
broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1
local 192.168.121.102 dev eth0 proto kernel scope host src 192.168.121.102
broadcast 192.168.121.255 dev eth0 proto kernel scope link src 192.168.121.102
```

Welcome to the confusing world of Linux networking, where everything is a tiny bit different than what you're used to.

### Replication Matters

You can use the following [netlab](https://netlab.tools/) topology to check my results:

```
defaults.device: frr
provider: clab

module: [ bgp, ospf ]
bgp.as: 65000

nodes: [ r1, r2 ]
links: [ r1-r2, r1 ]
```
