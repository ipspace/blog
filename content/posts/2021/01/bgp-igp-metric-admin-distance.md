---
date: 2021-01-06 06:39:00+00:00
eigrp_tag: deploy
networking-fundamentals_tag: deep
tags:
- BGP
- EIGRP
- networking fundamentals
title: IBGP, IGP Metrics, and Administrative Distances
---
**TL&DR**: If you run multiple IGP protocols in your network, and add BGP on top of that, you might get the results you deserve. Even better, the results are platform-dependent.

One of my readers sent me a link to an [interesting scenario described by Jeremy Filliben](https://www.jeremyfilliben.com/2009/08/when-administrative-distance-doesnt.html) that results in totally unexpected behavior when using too many routing protocols in your network (no surprise there).

Imagine a network in which two edge routers advertise the same (external) BGP prefix. All other things being equal, it would make sense that other routers in the same autonomous system should use the better path out of the autonomous system. Welcome to the final tie-breaker in BGP route selection process: IGP metric.
<!--more-->
{{<note>}}Jeremy tried to create a realistic scenario that would resemble a real-life network design; I decided to [minimize it to a bare minimum](/2017/11/run-well-designed-experiments-to-learn/) when reproducing it with a recent Cisco IOS version.{{</note>}}

{{<figure src="/2021/01/BGP-IGP-metric.png" caption="Simplest possible network demonstrating BGP interaction with IGP metric">}}

When using a single routing protocol, BGP selects the closer AS exit point. BGP table on PE1 has two (almost) identical entries, the only difference being the IGP metric toward the BGP next hop. The path with the lower IGP metric is selected.

{{<cc>}}BGP paths for IP prefix 172.16.0.0/16{{</cc>}}
```
BGP routing table entry for 172.16.0.0/16, version 4
Paths: (2 available, best #2, table default)
  Not advertised to any peer
  Refresh Epoch 1
  Local
    10.0.0.2 (metric 101) from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, valid, internal
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  Local
    10.0.0.1 (metric 2) from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      rx pathid: 0, tx pathid: 0x0
```

Now let's add EIGRP to the mix. OSPF is running throughout the whole network, EIGRP is running only between PE1 and E1.

{{<figure src="/2021/01/BGP-IGP-metric-dual-IGP.png" caption="Adding EIGRP as the second IGP">}}

{{<cc>}}OSPF and EIGRP neighbors on PE1{{</cc>}}
```
pe1#show ip ospf neighbor

Neighbor ID     Pri   State       Dead Time   Address         Interface
10.0.0.2          1   FULL/BDR    00:00:39    10.1.0.6        GigabitEthernet3
10.0.0.1          1   FULL/BDR    00:00:34    10.1.0.2        GigabitEthernet2

pe1#show ip eigrp neighbors
EIGRP-IPv4 Neighbors for AS(1)
H   Address           Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)   (ms)       Cnt Num
0   10.1.0.2          Gi2                      14 00:00:15    1   100  0  3
```

Not surprisingly, the route to E1 is now learned through EIGRP, and the route to E2 is still an OSPF route:

{{<cc>}}Routes to BGP next hops on PE1{{</cc>}}
```
pe1#show ip route 10.0.0.0 255.255.255.0 longer-prefixes
[...]
Gateway of last resort is 192.168.121.1 to network 0.0.0.0

      10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
D        10.0.0.1/32 [90/130816] via 10.1.0.2, 00:02:59, GigabitEthernet2
O        10.0.0.2/32 [110/101] via 10.1.0.6, 03:55:39, GigabitEthernet3
C        10.0.0.3/32 is directly connected, Loopback0
```

And now for the (not so) big surprise: BGP best path to the external destination goes *over the slower link* to E2:

{{<cc>}}Changed BGP best path goes over E2{{</cc>}}
```
pe1#show ip bgp 172.16.0.0
BGP routing table entry for 172.16.0.0/16, version 8
Paths: (2 available, best #1, table default)
  Not advertised to any peer
  Refresh Epoch 1
  Local
    10.0.0.2 (metric 101) from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      rx pathid: 0, tx pathid: 0x0
  Refresh Epoch 1
  Local
    10.0.0.1 (metric 130816) from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, valid, internal
      rx pathid: 0, tx pathid: 0
```

As expected: when you over-complicate your network design, you get the troubleshooting experience you were looking for.

### What's Going On?

In a nutshell:

* When selecting identical prefixes from multiple routing protocols, the prefix with the lowest *administrative distance* is used and appears in the routing table.
* When calculating BGP best paths, BGP takes *IGP metric* from the IP routing table and it just so happens that a good EIGRP metric is higher than a not-so-good OSPF metric, and so a BGP next hop learned by OSPF is preferred over a BGP next hop learned by EIGRP.

Please note that this behavior is not IGP-specific. You get the same results as long as the network-wide routing protocol has higher administrative distance and lower metrics than the additional routing protocol - it's easy to reproduce it using IS-IS as the primary routing protocol and OSPF running between PE1 and E1.

### Other Platforms

Nexus OS behaves in exactly the same way as Cisco IOS (tested with OSPF and IS-IS), but it seems like vEOS takes administrative distance in account when comparing IGP costs.

I configured OSPF and IS-IS on Arista vEOS 4.25.0FX-LDP-RSVP (with OSPF taking the role of EIGRP in the above example). These are the entries from the main IP routing table:

{{<cc>}}E1 is reachable over OSPF, E2 is reachable over IS-IS with lower metric and higher admin distance{{</cc>}}
```
pe1#show ip route 10.0.0.0/24 longer-prefixes
[...]
 O        10.0.0.1/32 [110/101] via 10.1.0.2, Ethernet1
 I L2     10.0.0.2/32 [115/30] via 10.1.0.6, Ethernet2
 C        10.0.0.3/32 is directly connected, Loopback0
```

Regardless of the lower IGP cost, the next hop reachable via OSPF (lower admin distance) is preferred when selecting the best BGP route:

{{<cc>}}OSPF next hop is preferred on Arista vEOS even though the IGP metric is higher{{</cc>}}
```
pe1#show ip bgp 172.16.0.0/16 detail
BGP routing table information for VRF default
Router identifier 10.0.0.3, local AS number 65000
BGP routing table entry for 172.16.0.0/16
 Paths: 2 available
  Local
    10.0.0.1 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric 0, localpref 100, IGP metric 101, weight 0, ↩
      received 00:05:22 ago, valid, internal, best
      Rx SAFI: Unicast
  Local
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, IGP metric 30, weight 0, ↩
      received 00:05:20 ago, valid, internal
      Rx SAFI: Unicast
      Not best: IGP cost
```

### More Details

<!-- More details coming in another blog post describing the interactions between routing protocols, routing table, and forwarding table. -->

Want to try it yourself? The lab topology (using *vagrant-libvirt*) and device configurations are in [*netlab-examples* GitHub repository](https://github.com/ipspace/netlab-examples/tree/master/BGP/IGP-metric).
