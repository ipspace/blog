---
date: 2008-07-21 07:35:00+02:00
tags:
- BGP
- load balancing
title: Unequal-Bandwidth EBGP Load Balancing
lastmod: 2020-12-28 12:44:00
url: /2008/07/unequal-bandwidth-ebgp-load-balancing/
---
EIGRP was always described as the only routing protocol that can do unequal-cost load sharing. As it turns out, BGP is another one (although it\'s way more limited than EIGRP). For example, if you have two links into a neighbor AS, you can load-share across them proportionally to their bandwidth.

{{<ct3_rescue>}}

EBGP load balancing was introduced with the *BGP 4 Multipath Support* feature in IOS release 11.2. Initially, EBGP supported up to six maximum paths; IOS release 12.0(S) increased that value to 8, IOS release 12.3T to 16 and 12.2S (including 12.2SRC) to 16.
<!--more-->
When the EBGP load balancing is enabled with the **maximum-paths _number_** router configuration command, the router with multiple EBGP sessions selects a single EBGP path as the best path (following the BGP best path selection algorithm). The selected path is marked as **best** in the BGP table. BGP might also select additional equivalent paths for multipath load sharing; all paths used for BGP load sharing are marked with **multipath**.

The BGP attributes *Local Preference, Multi-Exit Discriminator, Origin* and *AS-Path* of the selected multipath routes have to be identical to the best path. The AS-path of all multipath routes has to be an exact match of the AS-path of the best path. This requirement can be relaxed with the **bgp bestpath as-path multipath-relax** router configuration command, resulting in EBGP load balancing across multiple autonomous systems.

BGP performs equal-cost load balancing between all multipath routes, unless the **bgp dmzlink-bw** is configured within the BGP routing process and **dmzlink-bw** option is configured on EBGP neighbors.

### Simple EBGP Load Sharing

Router X1 in the sample network (see the following figure) has two links into AS 65001.

{{<figure src="/2008/07/EBGP_LS_SampleNetwork.png" caption="Lab network diagram">}}

Inter-AS interfaces and BGP neighbors are configured on X1:

{{<cc>}}Interface- and BGP configuration on X1{{</cc>}}
```
interface Serial1/5
 description Link to E1(ROUTER) s1/1
 bandwidth 4000
 ip address 10.0.7.45 255.255.255.252
!
interface Serial1/6
 description Link to E2(ROUTER) s1/0
 bandwidth 2000
 ip address 10.0.7.41 255.255.255.252
!
interface Serial1/7
 description Link to E3(ROUTER) s1/0
 bandwidth 3000
 ip address 10.0.7.33 255.255.255.252
!
router bgp 65000
 no synchronization
 bgp log-neighbor-changes
 neighbor 10.0.7.34 remote-as 65002
 neighbor 10.0.7.42 remote-as 65001
 neighbor 10.0.7.46 remote-as 65001
 no auto-summary
```

After the BGP sessions have been established and the routes exchanged, X1 has three alternate paths to 10.2.2.0/24, but only one of them is selected as best and used for IP routing:

```
X1#show ip bgp 10.2.2.0 | section ^ +65
  65002 65001
    10.0.7.34 from 10.0.7.34 (10.0.1.7)
      Origin IGP, localpref 100, valid, external
  65001
    10.0.7.42 from 10.0.7.42 (10.0.1.6)
      Origin IGP, metric 0, localpref 100, valid, external
  65001
    10.0.7.46 from 10.0.7.46 (10.0.1.5)
      Origin IGP, metric 0, localpref 100, valid, external, best
X1#show ip route 10.2.2.0 | begin Routing Descriptor
  Routing Descriptor Blocks:
  * 10.0.7.46, from 10.0.7.46, 00:01:36 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65001
```

When you configure **maximum-paths 4** in the BGP routing process, both paths received from AS 65000 are marked as *multipath* and the router uses them as equal-cost paths regardless of interface bandwidth:

```
X1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
X1(config)#router bgp 65000
X1(config-router)#maximum-paths 4
X1(config-router)#^Z
X1#show ip bgp 10.2.2.0 | section ^ +65
  65002 65001
    10.0.7.34 from 10.0.7.34 (10.0.1.7)
      Origin IGP, localpref 100, valid, external
  65001
    10.0.7.42 from 10.0.7.42 (10.0.1.6)
      Origin IGP, metric 0, localpref 100, valid, external, multipath
  65001
    10.0.7.46 from 10.0.7.46 (10.0.1.5)
      Origin IGP, metric 0, localpref 100, valid, external, multipath, best
X1#show ip route 10.2.2.0 | begin Routing Descriptor
  Routing Descriptor Blocks:
  * 10.0.7.46, from 10.0.7.46, 00:00:14 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65001
    10.0.7.42, from 10.0.7.42, 00:00:14 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65001
```

### Unequal-cost Load Sharing

EBGP load sharing ignores interface bandwidth unless you configure DMZ link bandwidth feature. To enable unequal-cost load sharing, you have to:

1.  Configure **dmzlink-bw** option on all EBGP neighbors to attach link bandwidths to EBGP routes;
2.  Configure **bgp dmzlink-bw** option in the BGP routing process; this option causes BGP to use the bandwidths attached to EBGP routes in the traffic share calculation algorithm.
3.  Clear the EBGP sessions to receive all the EBGP routes (soft clear is recommended); link bandwidth is attached to an EBGP route only during the incoming update processing.

After these configuration steps have been completed, the traffic is shared between multipath EBGP paths according to the bandwidths configured on outgoing interfaces:

```
X1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
X1(config)#router bgp 65000
X1(config-router)#bgp dmzlink-bw
X1(config-router)#neighbor 10.0.7.34 dmzlink-bw
X1(config-router)#neighbor 10.0.7.42 dmzlink-bw
X1(config-router)#neighbor 10.0.7.46 dmzlink-bw
X1(config-router)#^Z
X1#clear ip bgp * soft in
X1#show ip bgp 10.2.2.0 | section ^ +65
  65002 65001
    10.0.7.34 from 10.0.7.34 (10.0.1.7)
      Origin IGP, localpref 100, valid, external
      DMZ-Link Bw 375 kbytes
  65001
    10.0.7.42 from 10.0.7.42 (10.0.1.6)
      Origin IGP, metric 0, localpref 100, valid, external, multipath
      DMZ-Link Bw 250 kbytes
  65001
    10.0.7.46 from 10.0.7.46 (10.0.1.5)
      Origin IGP, metric 0, localpref 100, valid, external, multipath, best
      DMZ-Link Bw 500 kbytes
X1#show ip route 10.2.2.0 | begin Routing Descriptor
  Routing Descriptor Blocks:
    10.0.7.46, from 10.0.7.46, 00:00:24 ago
      Route metric is 0, traffic share count is 2
      AS Hops 1
      Route tag 65001
  * 10.0.7.42, from 10.0.7.42, 00:00:24 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65001
```

