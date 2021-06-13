---
title: Testing OSPF Anycast Behavior
tags: [ ospf ]
draft: True
date: 2021-06-12 09:09:00
---
## Single OSPF Area

```
s1#show ip ospf database router 10.0.0.4
...
  LS age: 272
  LS Type: Router Links
  Link State ID: 10.0.0.4
  Advertising Router: 10.0.0.4
  Number of Links: 4
...
    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.42.42.1
     (Link Data) Network Mask: 255.255.255.255
      Number of MTID metrics: 0
       TOS 0 Metrics: 1
```

```
s1#show ip ospf route | sect 10.42.42
*>  10.42.42.1/32, Intra, cost 3, area 0.0.0.0
      via 10.1.0.1, GigabitEthernet2
      via 10.1.0.5, GigabitEthernet3
```

```
s1#show ip route 10.42.42.1
Routing entry for 10.42.42.1/32
  Known via "ospf 1", distance 110, metric 3, type intra area
  Last update from 10.1.0.5 on GigabitEthernet3, 00:06:31 ago
  Routing Descriptor Blocks:
    10.1.0.5, from 10.0.0.6, 00:06:31 ago, via GigabitEthernet3
      Route metric is 3, traffic share count is 1
  * 10.1.0.1, from 10.0.0.4, 00:06:31 ago, via GigabitEthernet2
      Route metric is 3, traffic share count is 1
```

## Anycast Prefix as External Route

```
s1#show ip ospf data external | include State|Router|^$

            OSPF Router with ID (10.0.0.3) (Process ID 1)

		Type-5 AS External Link States

  Link State ID: 10.42.42.1 (External Network Number )
  Advertising Router: 10.0.0.4

  Link State ID: 10.42.42.1 (External Network Number )
  Advertising Router: 10.0.0.5

  Link State ID: 10.42.42.1 (External Network Number )
  Advertising Router: 10.0.0.6
```

```
s1#show ip ospf route | begin Path List
    Intra-area Router Path List

i 10.0.0.5 [2] via 10.1.0.1, GigabitEthernet2, ASBR, Area 0.0.0.0, SPF 13
i 10.0.0.4 [2] via 10.1.0.1, GigabitEthernet2, ASBR, Area 0.0.0.0, SPF 13
i 10.0.0.6 [2] via 10.1.0.5, GigabitEthernet3, ASBR, Area 0.0.0.0, SPF 13

    External Route List
*>  10.42.42.1/32, Ext2, cost 20, fwd cost 2, tag 100
      via 10.1.0.5, GigabitEthernet3
      via 10.1.0.1, GigabitEthernet2
```

```
s1#show ip route 10.42.42.1
Routing entry for 10.42.42.1/32
  Known via "ospf 1", distance 110, metric 20
  Tag 100, type extern 2, forward metric 2
  Last update from 10.1.0.1 on GigabitEthernet2, 00:03:36 ago
  Routing Descriptor Blocks:
  * 10.1.0.5, from 10.0.0.6, 00:03:36 ago, via GigabitEthernet3
      Route metric is 20, traffic share count is 1
      Route tag 100
    10.1.0.1, from 10.0.0.5, 00:03:36 ago, via GigabitEthernet2
      Route metric is 20, traffic share count is 1
      Route tag 100
```

## Redistributing Anycast Prefix From BGP

```
l1#show ip bgp 10.42.42.1
BGP routing table entry for 10.42.42.1/32, version 10
Paths: (3 available, best #3, table default)
Multipath: eBGP
  Advertised to update-groups:
     1          2
  Refresh Epoch 1
  65001
    10.1.0.9 from 10.1.0.9 (10.0.0.4)
      Origin IGP, metric 0, localpref 100, valid, external, multipath(oldest)
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  65001
    10.0.0.2 (metric 3) from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, valid, internal
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  65001
    10.1.0.13 from 10.1.0.13 (10.0.0.5)
      Origin IGP, metric 0, localpref 100, valid, external, multipath, best
      rx pathid: 0, tx pathid: 0x0
```

```
l1#show ip route 10.42.42.1
Routing entry for 10.42.42.1/32
  Known via "bgp 65000", distance 20, metric 0
  Tag 65001, type external
  Redistributing via ospf 1
  Advertised by ospf 1 subnets
  Last update from 10.1.0.13 00:02:34 ago
  Routing Descriptor Blocks:
    10.1.0.13, from 10.1.0.13, 00:02:34 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65001
      MPLS label: none
  * 10.1.0.9, from 10.1.0.9, 00:02:34 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65001
      MPLS label: none
```

```
l1#show ip ospf data external 10.42.42.1 | include State|Router|^$

            OSPF Router with ID (10.0.0.1) (Process ID 1)

		Type-5 AS External Link States

  Link State ID: 10.42.42.1 (External Network Number )
  Advertising Router: 10.0.0.1

  Link State ID: 10.42.42.1 (External Network Number )
  Advertising Router: 10.0.0.2
```
