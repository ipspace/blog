---
title: "OSPF ECMP with Unnumbered IPv4 Interfaces"
subtitle: "or how netlab made labbing fun again"
date: 2023-09-11 06:13:00
tags: [ OSPF, load balancing, netlab ]
netlab_tag: use
pre_scroll: true
series: unnumbered-interfaces
---
The [OSPF and ARP on Unnumbered IPv4 Interfaces](https://blog.ipspace.net/2023/08/unnumbered-ospf-arp.html) triggered an [interesting consideration](https://blog.ipspace.net/2023/08/unnumbered-ospf-arp.html#1903): does ECMP with across parallel unnumbered links?

**TL&DR**: Yes, it works flawlessly on Arista EOS and Cisco IOS/XE. Feel free to test it out on any other device on which _netlab_ supports [unnumbered interfaces with OSPF](https://netlab.tools/module/ospf/#platform-support).

In the good old days, it would take me forever to find the right boxes to do the tests. A few years ago, I would have to [chase a mouse around a GUI](https://blog.ipspace.net/2013/10/cisco-modeling-lab-virl-behind-scenes.html). This time, it took me 30 seconds (plus the [VM boot time](https://blog.ipspace.net/2023/02/virtual-device-boot-times.html)) to get the answer.

### Step 1: netlab topology

* We have two nodes running OSPF
* We want to have two parallel links between the nodes
* The point-to-point links should be unnumbered
* I'll throw in two stub links just to have some extra prefixes

Voila:

```
defaults.device: eos
addressing.p2p.ipv4: True
module: [ ospf ]

nodes: [ r1, r2 ]
links: [ r1-r2, r1-r2, r1, r2 ]
```

Save the above YAML configuration into `topology.yml`.

### Step 2: Start the lab

Execute `netlab up` (assuming someone already got the [prep work done](https://netlab.tools/install/)), and wait a bit. You'll get a fully-configured lab, and OSPF adjacencies might be established before you manage to log in (IOS XE took a bit longer).

### Step 3: Enjoy the results

Execute `netlab connect r1 show ip route ospf` and admire the parallel routes pointing to two outgoing interfaces.

{{<cc>}}OSPF routes over parallel unnumbered links on Arista EOS{{</cc>}}
```
$ netlab connect r1 show ip route ospf
Connecting to 192.168.121.101 using SSH port 22

VRF: default
Codes: C - connected, S - static, K - kernel,
       O - OSPF, IA - OSPF inter area, E1 - OSPF external type 1,
       E2 - OSPF external type 2, N1 - OSPF NSSA external type 1,
       N2 - OSPF NSSA external type2, B - Other BGP Routes,
       B I - iBGP, B E - eBGP, R - RIP, I L1 - IS-IS level 1,
       I L2 - IS-IS level 2, O3 - OSPFv3, A B - BGP Aggregate,
       A O - OSPF Summary, NG - Nexthop Group Static Route,
       V - VXLAN Control Service, M - Martian,
       DH - DHCP client installed default route,
       DP - Dynamic Policy Route, L - VRF Leaked,
       G  - gRIBI, RC - Route Cache Route

 O        10.0.0.2/32 [110/20] is directly connected, Ethernet1
                               is directly connected, Ethernet2
 O        172.16.1.0/24 [110/20] via 10.0.0.2, Ethernet1
                                 via 10.0.0.2, Ethernet2
```

### Step 4: Repeat the tests with Cisco IOS XE

Execute `netlab down` followed by `netlab up --device csr`. Wait a bit longer to get the lab up and running.

### Step 5: Enjoy the results

Execute `netlab connect r1 show ip route ospf`:

{{<cc>}}OSPF routes over parallel unnumbered links on Cisco IOS XE{{</cc>}}
```
...
Gateway of last resort is not set

      10.0.0.0/32 is subnetted, 2 subnets
O        10.0.0.2 [110/2] via 10.0.0.2, 00:07:09, GigabitEthernet3
                  [110/2] via 10.0.0.2, 00:07:19, GigabitEthernet2
      172.16.0.0/16 is variably subnetted, 3 subnets, 2 masks
O        172.16.1.0/24 [110/2] via 10.0.0.2, 00:07:09, GigabitEthernet3
                       [110/2] via 10.0.0.2, 00:07:18, GigabitEthernet2
```

### Step 6: Repeat the tests with Cisco IOS XR

Meh, no. My life is [too short for that](https://blog.ipspace.net/2023/02/virtual-device-boot-times.html) ;)

### Takeaway

You're missing out if you haven't invested into an [Infrastructure-as-Code virtual lab infrastructure](https://netlab.tools/). It costs you nothing apart from the underlying hardware (or you could [run it in the cloud](https://netlab.tools/install/cloud/)) and a non-trivial chunk of your time.

Alternatively, you could keep asking questions on various blogs and forums ;)
