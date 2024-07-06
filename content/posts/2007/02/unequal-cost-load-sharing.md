---
date: 2007-02-08 13:47:00+01:00
tags:
- CEF
- load balancing
- MPLS
- traffic engineering
title: Unequal Cost Load-Sharing with MPLS TE
url: /2007/02/unequal-cost-load-sharing.html
---
One of the most commonly asked load-sharing-related questions is "*can I load-share traffic across unequal-cost links?*". In general, the answer is no. In order to load-share the traffic, you need more than one path to the destination and the only way to get multiple routes toward a destination in the IP routing table is to make them equal-cost (the only notable exception being EIGRP that supports unequal-cost load-sharing with the **variance** parameter).

There are, however, two cases where you can force unequal traffic split across equal-cost paths toward a destination: when using [inter-AS BGP with the link bandwidth parameter](/2008/07/unequal-bandwidth-ebgp-load-balancing.html), and when using unequal-bandwidth traffic-engineering tunnels.
<!--more-->
Due to the way MPLS TE autoroute is implemented in Cisco IOS, all tunnels toward the same destination appear as equal-cost paths, even when their TE bandwidths are not the same. For example, using a simple TE configuration...

``` {.code}
interface Tunnel0
 ip unnumbered Loopback0
 tunnel destination 172.16.0.21
 tunnel mode mpls traffic-eng
 tunnel mpls traffic-eng autoroute announce
 tunnel mpls traffic-eng priority 7 7
 tunnel mpls traffic-eng bandwidth  300
 tunnel mpls traffic-eng path-option 1 explicit identifier 1
 no routing dynamic
!
interface Tunnel1
 ip unnumbered Loopback0
 tunnel destination 172.16.0.21
 tunnel mode mpls traffic-eng
 tunnel mpls traffic-eng autoroute announce
 tunnel mpls traffic-eng priority 7 7
 tunnel mpls traffic-eng bandwidth  500
 tunnel mpls traffic-eng path-option 1 explicit identifier 2
 no routing dynamic
```

... you get two equal-cost paths in your IP routing table even though the **tunnel mpls traffic-eng bandwidths** are different:

``` {.code}
a1#show ip route ospf
  172.16.0.0 255.255.0.0 is variably subnetted, 6 subnets, 2 masks
O  172.16.0.21 255.255.255.255 [110/51] via 0.0.0.0, 00:11:06, Tunnel0
                               [110/51] via 0.0.0.0, 00:11:06, Tunnel1
O  172.16.0.22 255.255.255.255 [110/52] via 0.0.0.0, 00:11:06, Tunnel0
                               [110/52] via 0.0.0.0, 00:11:06, Tunnel1
```

When transferring the IP routing table into the CEF table, the router takes MPLS TE bandwidth in consideration, [resulting in unequal traffic split](/2006/10/cef-load-sharing-details.html) proportional to the MPLS TE bandwidth:

``` {.code}
a1#show ip cef 172.16.0.21 internal
172.16.0.21/32, version 55, epoch 1, per-destination sharing
0 packets, 0 bytes
  tag information set
    local tag: tunnel-head
  via 0.0.0.0, Tunnel0, 0 dependencies
    traffic share 3
    next hop 0.0.0.0, Tunnel0
    valid adjacency
    tag rewrite with Tu0, point2point, tags imposed: {}
  via 0.0.0.0, Tunnel1, 0 dependencies
    traffic share 5
    next hop 0.0.0.0, Tunnel1
    valid adjacency
    tag rewrite with Tu1, point2point, tags imposed: {}

  0 packets, 0 bytes switched through the prefix
  tmstats: external 0 packets, 0 bytes
           internal 0 packets, 0 bytes
  Load distribution: 0 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 (refcount 1)

  Hash  OK  Interface                 Address         Packets  Tags imposed
  1     Y   Tunnel0                   point2point           0    {}
  2     Y   Tunnel1                   point2point           0    {}
  3     Y   Tunnel0                   point2point           0    {}
  4     Y   Tunnel1                   point2point           0    {}
  5     Y   Tunnel0                   point2point           0    {}
  6     Y   Tunnel1                   point2point           0    {}
  7     Y   Tunnel0                   point2point           0    {}
  8     Y   Tunnel1                   point2point           0    {}
  9     Y   Tunnel0                   point2point           0    {}
  10    Y   Tunnel1                   point2point           0    {}
  11    Y   Tunnel0                   point2point           0    {}
  12    Y   Tunnel1                   point2point           0    {}
  13    Y   Tunnel1                   point2point           0    {}
  14    Y   Tunnel1                   point2point           0    {}
  15    Y   Tunnel1                   point2point           0    {}
  16    Y   Tunnel1                   point2point           0    {}
```
