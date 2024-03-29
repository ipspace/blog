---
title: "FRRouting Loopback Interfaces and OSPF Costs"
date: 2024-04-17 08:56:00+0100
tags: [ OSPF ]
---
**TL&DR:** FRRouting advertises the IP prefix on the **lo** loopback interface with zero cost.

Let's start with the background story. When we added FRRouting containers support to _netlab_, someone decided to use **lo0** as the loopback interface name. That device doesn't exist in a typical Linux container, but it's not hard to add it:

```
$ ip link add lo0 type dummy
$ ip link set dev lo0 up
```
<!--more-->
However, when I tried to use OSPF with SR/MPLS, FRRouting complained that **lo0** is not a loopback interface. Technically, that's true; let's take a look at the **ip link** printout:

```
$ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: lo0: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/ether 36:8e:4a:ad:3c:85 brd ff:ff:ff:ff:ff:ff
4433: eth0@if4434: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:c0:a8:79:67 brd ff:ff:ff:ff:ff:ff link-netnsid 0
4441: eth1@if4442: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether aa:c1:ab:3f:97:50 brd ff:ff:ff:ff:ff:ff link-netnsid 1
```

Not a big deal. It was time to fix that discrepancy and use **lo** as the loopback interface on FRRouting (and bring the configuration templates in line with the Cumulus Linux ones). I was ready to run the integration tests a few minor edits later, but the OSPF tests kept failing.

As I started investigating the root cause of the failure, I found an amazing detail: the default OSPF cost is ten on the **lo0** interface and **zero** on the **lo** interface:[^PE]

```
x2# show ip ospf int
eth1 is up
  Internet Address 10.1.0.6/30, Broadcast 10.1.0.7, Area 0.0.0.0
  Router ID 10.0.0.3, Network Type POINTOPOINT, Cost: 10
lo is up
  Internet Address 10.0.0.3/32, Broadcast 10.0.0.3, Area 0.0.0.0
  Router ID 10.0.0.3, Network Type LOOPBACK, Cost: 0
lo0 is up
  This interface is UNNUMBERED, Area 0.0.0.0
  Router ID 10.0.0.3, Network Type BROADCAST, Cost: 10
```

[^PE]: Printout has been edited to include only the relevant details.

There's nothing wrong with what FRRouting does; RFC 2328 allows OSPF cost on stub networks to be zero. It's just different from what we've seen in other OSPF implementations.