---
date: 2021-05-11 06:54:00+00:00
dcbgp_tag: relevant
series:
- dcbgp
tags:
- segment routing
- BGP
- MPLS
title: BGP-Free MPLS Core with Segment Routing
---
After I [created the Segment Routing lab](/2021/05/segment-routing-ids-mpls-labels/) to test the relationship between Node Segment ID (SID) and MPLS labels, I was just a minor step away from testing [BGP-free core](/2012/01/bgp-free-service-provider-core-in/) with [SR-MPLS](/2011/11/ldp-igp-synchronization-in-mpls/).

I added two nodes to my lab setup, this time [using IOSv](https://github.com/ipspace/netlab-examples/blob/master/routing/sr-mpls-bgp/sr%2Bbgp.yml) as those nodes need nothing more than EBGP support (and IOSv is tiny compared to IOS XE on CSR):
<!--more-->
{{<figure src="/2021/05/SR-BGP.png" caption="Extending SR/MPLS lab with BGP">}}

All four routers in AS 65000 run IS-IS with Segment Routing, but only E1 and E2 run BGP (with a direct IBGP session between them). The $1M question: can we ping between X1 and X2?

**TL&DR:** Yes

Let's inspect the BGP table on E1:

```
e1#sh ip bgp
BGP table version is 7, local router ID is 10.0.0.3
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
              t secondary path,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>   10.0.0.3/32      0.0.0.0                  0         32768 i
 r>i  10.0.0.4/32      10.0.0.4                      100      0 i
 *>   10.0.0.5/32      10.1.0.18                0             0 65001 i
 *>i  10.0.0.6/32      10.0.0.4                 0    100      0 65002 i
 *>   172.16.0.0/24    10.1.0.18                0             0 65001 i
 *>i  172.16.1.0/24    10.0.0.4                 0    100      0 65002 i
```

Next hop for X2 (172.16.1.0/24) is E2 (10.0.0.4). Do we have an MPLS path to get there?

```
e1#show mpls forwarding-table 10.0.0.4
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop
Label      Label      or Tunnel Id     Switched      interface
16004      16004      10.0.0.4/32      0             Gi2        10.1.0.1
           900004     10.0.0.4/32      0             Gi3        10.1.0.5
```

We do. Are these labels used for 172.16.1.0? We won't see them in the IP routing table (RIB), we have to look into IP forwarding table (FIB)[^1]

```
e1#show ip cef 172.16.1.0 detail
172.16.1.0/24, epoch 2, flags [rib only nolabel, rib defined all labels]
  recursive via 10.0.0.4
    nexthop 10.1.0.1 GigabitEthernet2 label 16004-(local:16004)
    nexthop 10.1.0.5 GigabitEthernet3 label 900004-(local:16004)
```

QED - our BGP-free core is using SR-MPLS labels for BGP next hops to get the traffic across AS 65000. 

Obviously I could just run a ping...

```
x1#ping 172.16.1.6 source GigabitEthernet 0/2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 172.16.1.6, timeout is 2 seconds:
Packet sent with a source address of 172.16.0.5
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 7/7/8 ms
```

... but that wouldn't have been nearly as much fun.

### Want to Reproduce It?

* [Lab setup](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-mpls-bgp) (including netsim topology and Vagrantfile)
* [Device configuration snippets](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-mpls-bgp/config)

### Want to Know More?

You might find these webinars useful:

* [Segment Routing Introduction](https://www.ipspace.net/Segment_Routing_Introduction)
* [MPLS Essentials](https://www.ipspace.net/MPLS_Essentials)
* [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)

[^1]: See also: [RIBs and FIBs](/2010/09/ribs-and-fibs/) and [Management, Control, and Data Planes in Network Devices and Systems](/2013/08/management-control-and-data-planes-in/)
