---
title: "Cisco IOS/XE Hates Redistributed Static IPv6 Routes"
date: 2025-07-18 07:41:00+0200
tags: [ netlab ]
netlab_tag: quirks
---
Writing tests that check the correctness of network device configurations is hard ([overview](/2024/05/netlab-integration-tests/), [more details](/2025/06/testing-ospf-configurations/)). It's also an interesting exercise in getting the timing just right:

* Routing protocols are an [eventually-consistent distributed system](/2021/02/routing-protocols-eventually-consistent/), and things eventually appear in the right place (if you got the configurations right), but you never know when exactly that will happen.
* You can therefore set some reasonable upper bounds on when things should happen, and declare failure if the timeouts are exceeded. Even then, you'll get false positives (as in: the test is telling you the configurations are incorrect, when it's just a device having a bad hair day).

And just when you think you nailed it, you encounter a device that blows your assumptions out of the water.
<!--more-->
The test was supposed to be simple: [check whether the route redistribution into BGP works](https://github.com/ipspace/netlab/blob/78fec5f07e22b83b63d83c0e0d82a5e59d0c25b4/tests/integration/bgp/30-import-ds-ospf.yml). The initial lab topology had a device under test (DUT) that redistributed OSPF into BGP, an OSPF-speaking router (R2), and a BGP-speaking router (X1). The validation tests carefully progressed down the [happy path](https://en.wikipedia.org/wiki/Happy_path):

* Do we have IPv4 and IPv6 EBGP sessions between X1 and DUT?
* Do we have OSPFv2 and OSPFv3 sessions between R2 and DUT?
* Do we see an OSPFv2 prefix advertised by R2 in the IPv4 BGP table on X1 (and likewise for IPv6)?

It worked on all the devices we tested, and then we added the static routes on the DUT to the mix. Not a big deal, right? Just add another test to check whether the static routes are propagated into BGP. The timing doesn't matter, right? After all, if a router manages to redistribute OSPF routes into BGP, it should have no problem redistributing its static routes into BGP at the same time.

And at that point, I entered a weird parallel universe of Cisco IOS/XE. Let's start with the OSPF-to-BGP redistribution scenario. Here are the IPv4 debugging printouts (generated with **debug ip routing** and **debug bgp all updates**) for 10.0.0.3/32 (the loopback interface of R1):

```
*Jul 15 12:08:48.766: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.0.3 on Ethernet0/2 from LOADING to FULL, Loading Done
*Jul 15 12:08:51.223: %OSPFv3-5-ADJCHG: Process 1, IPv6, Nbr 10.0.0.3 on Ethernet0/2 from LOADING to FULL, Loading Done
*Jul 15 12:08:51.424: BGP: topo global:IPv4 Unicast:base Remove_fwdroute for 10.0.0.3/32
*Jul 15 12:08:51.424: BGP(0): (base) 10.1.0.2 send UPDATE (format) 10.0.0.3/32, next 10.1.0.1, metric 10, path Local
*Jul 15 12:08:51.475: BGP(0): 10.1.0.2 rcv UPDATE about 10.0.0.3/32 -- DENIED due to: AS-PATH contains our own AS;
```

As you can see, it takes approximately three seconds from the OSPF adjacency establishment to the BGP UPDATE message.

What about IPv6? Here are the similar printouts for R1 IPv6 loopback:

```
*Jul 15 12:08:51.473: [OSPFv3R-1/6/0]IPv6RT[default]: ospf 1, Update 2001:DB8:1:3::/64 [110/10], 1 paths (valid:1 invalid:0) tag 0 regular paths: Yes
*Jul 15 12:08:51.473: [OSPFv3R-1/6/0]IPv6RT[default]: ospf 1, Route add 2001:DB8:1:3::/64 [new 110/10]
*Jul 15 12:08:51.473: [OSPFv3R-1/6/0]IPv6RT[default]: ospf 1, RIB change event queued 2001:DB8:1:3::/64 'ospf' <default>, code:0x1 nh_count:1 distance:110 metric:10 flags:0x0 tag:0
*Jul 15 12:08:51.473: [IPv6 RIB Event Handler]IPv6RT[default]: Event: 2001:DB8:1:3::/64, Add, owner ospf, previous None
*Jul 15 12:08:51.473: BGP(1): redist event (1) request for 2001:DB8:1:3::/64
*Jul 15 12:08:51.473: BGP(1) route 2001:DB8:1:3::/64 nh-1 FE80::A8C1:ABFF:FE05:56EB src_proto (ospf) path-limit 1
*Jul 15 12:08:51.473: BGP(1): sourced route for 2001:DB8:1:3::/64 created
*Jul 15 12:08:51.473: BGP(1): sourced route for 2001:DB8:1:3::/64 path 0x7FD4B09182A0 id 0 nh FE80::A8C1:ABFF:FE05:56EB created (weight 32768)
*Jul 15 12:08:51.473: BGP(1): redistributed route 2001:DB8:1:3::/64 modified added-nh FE80::A8C1:ABFF:FE05:56EB
*Jul 15 12:08:51.473: BGP(1): 2001:DB8:1:3::/64 route sourced locally
*Jul 15 12:08:51.473: BGP: topo global:IPv6 Unicast:base Remove_fwdroute for 2001:DB8:1:3::/64
*Jul 15 12:08:51.473: [BGP Router]IPv6RT[default]: bgp 65000, Delete request for route 2001:DB8:1:3::/64 from 'bgp'(0x0) metric:10 distance:110 tag:0 paths:1 route-type:0x2
*Jul 15 12:08:51.473: BGP(1): (base) 2001:DB8:3::2 send UPDATE (format) 2001:DB8:1:3::/64, next 2001:DB8:3::1, metric 10, path Local
*Jul 15 12:08:51.475: BGP(1): 2001:DB8:3::2 rcv UPDATE about 2001:DB8:1:3::/64 -- DENIED due to: AS-PATH contains our own AS;
*Jul 15 12:09:43.223: BGP(1): redistributed route 2001:DB8:1:3::/64 modified rib-nh FE80::A8C1:ABFF:FE05:56EB path-nh FE80::A8C1:ABFF:FE05:56EB [0x7FD4B09182A0:0]
```

IPv6 debugging is way more verbose than IPv4 debugging (but hey, it has four times as many bits in its addresses), but the gist is the same: it takes milliseconds to redistribute OSPFv3 routes into BGP IPv6 AF and send the BGP update message.

Now let's add the static routes to the mix. DUT has two static routes (10.0.0.42/32 and 2001:DB8:42::42/128). They are configured and redistributed using these configuration commands:

```
ip route 10.0.0.42 255.255.255.255 Ethernet0/2 10.1.0.6
ipv6 route 2001:DB8:42::42/128 Ethernet0/2 2001:DB8:3:1::2
!
router bgp 65000
 bgp nopeerup-delay cold-boot 1
 bgp nopeerup-delay user-initiated 1
 bgp update-delay 5
 !
 address-family ipv4
  bgp scan-time 5
  redistribute static
 !
 address-family ipv6
  redistribute static
  bgp scan-time 5
```

The IPv4 static route works as expected:

* It's redistributed into BGP
* It's advertised to the BGP neighbors as soon as the BGP session is up:

```
*Jul 15 12:24:40.392: RT: updating static 10.0.0.42/32 (0x0) omp-tag:0  :
*Jul 15 12:24:40.392: RT: add 10.0.0.42/32 via 10.1.0.6, static metric [1/0]
*Jul 15 12:24:47.805: BGP(0): sourced route for 10.0.0.42/32 created
*Jul 15 12:24:47.805: bgp_ipv4set_origin: redist 1, opaque 0x0, net 10.0.0.42
*Jul 15 12:24:47.805: ndb_get_local_label_info: SR local label information for prefix 10.0.0.42/32 is not owned by the owner of the route (ndb-pdb-index:1 label-pdb-index:0)
*Jul 15 12:24:47.805: BGP(0): sourced route for 10.0.0.42/32 path 0x7F8BC2E693D8 id 0 gw 10.1.0.6 created (weight 32768)
*Jul 15 12:24:47.805: BGP(0): redistributed route 10.0.0.42/32 added gw 10.1.0.6
*Jul 15 12:24:51.721: %BGP-5-ADJCHANGE: neighbor 10.1.0.2 Up
*Jul 15 12:24:55.081: BGP: topo global:IPv4 Unicast:base Remove_fwdroute for 10.0.0.42/32
*Jul 15 12:24:55.082: BGP(0): (base) 10.1.0.2 send UPDATE (format) 10.0.0.42/32, next 10.1.0.1, metric 0, path Local
*Jul 15 12:24:55.133: BGP(0): 10.1.0.2 rcv UPDATE about 10.0.0.42/32 -- DENIED due to: AS-PATH contains our own AS;
```

However, the BGP process ignores the IPv6 static route **for almost a minute** while it happily redistributes the OSPFv3 routes.

```
*Jul 15 12:24:40.642: [SSH Process]IPv6RT[default]: static, Update 2001:DB8:42::42/128 [1/0], 1 paths (valid:1 invalid:0) tag 0 regular paths: Yes
*Jul 15 12:24:40.642: [SSH Process]IPv6RT[default]: static, Route add 2001:DB8:42::42/128 [new 1/0]
*Jul 15 12:24:40.642: [SSH Process]IPv6RT[default]: static, RIB change event queued 2001:DB8:42::42/128 'static' <default>, code:0x1 nh_count:1 distance:1 metric:0 flags:0x0 tag:0
*Jul 15 12:24:40.642: [IPv6 RIB Event Handler]IPv6RT[default]: Event: 2001:DB8:42::42/128, Add, owner static, previous None
*Jul 15 12:24:51.722: %BGP-5-ADJCHANGE: neighbor 2001:DB8:3::2 Up
*Jul 15 12:25:46.879: BGP(1): sourced route for 2001:DB8:42::42/128 created
*Jul 15 12:25:46.879: BGP(1): sourced route for 2001:DB8:42::42/128 path 0x7F8BC2EE7260 id 0 nh 2001:DB8:3:1::2 created (weight 32768)
*Jul 15 12:25:46.879: BGP(1): redistributed route 2001:DB8:42::42/128 modified added-nh 2001:DB8:3:1::2
*Jul 15 12:25:46.894: BGP(1): 2001:DB8:42::42/128 route sourced locally
*Jul 15 12:25:46.894: BGP: topo global:IPv6 Unicast:base Remove_fwdroute for 2001:DB8:42::42/128
*Jul 15 12:25:46.894: [BGP Router]IPv6RT[default]: bgp 65000, Delete request for route 2001:DB8:42::42/128 from 'bgp'(0x0) metric:0 distance:1 tag:0 paths:1 route-type:0x0
*Jul 15 12:25:46.895: BGP(1): (base) 2001:DB8:3::2 send UPDATE (format) 2001:DB8:42::42/128, next 2001:DB8:3::1, metric 0, path Local
*Jul 15 12:25:46.945: BGP(1): 2001:DB8:3::2 rcv UPDATE about 2001:DB8:42::42/128 -- DENIED due to: AS-PATH contains our own AS;
```

Trying to figure out what's happening, I added **debug bgp \* all import events** and **debug bgp \* all events** to the mix. Here's what happens at the 1-minute mark:

```
*Jul 15 12:37:52.804: BGP(1): redistributed route 2001:DB8:1:3::1/128 modified rib-nh FE80::A8C1:ABFF:FE93:3614 path-nh FE80::A8C1:ABFF:FE93:3614 [0x7FD225EE9778:0]
*Jul 15 12:37:52.804: BGP(1): redistributed route 2001:DB8:1:3::/64 modified rib-nh FE80::A8C1:ABFF:FE93:3614 path-nh FE80::A8C1:ABFF:FE93:3614 [0x7FD225EE96D0:0]
*Jul 15 12:37:52.804: BGP(1): redistributed route 2001:DB8:3:1::2/128 modified rib-nh FE80::A8C1:ABFF:FE93:3614 path-nh FE80::A8C1:ABFF:FE93:3614 [0x7FD225EE9820:0]
*Jul 15 12:37:52.804: BGP(1): sourced route for 2001:DB8:42::42/128 created
*Jul 15 12:37:52.804: BGP(1): sourced route for 2001:DB8:42::42/128 path 0x7FD225EE9628 id 0 nh 2001:DB8:3:1::2 created (weight 32768)
*Jul 15 12:37:52.804: BGP(1): redistributed route 2001:DB8:42::42/128 modified added-nh 2001:DB8:3:1::2
*Jul 15 12:37:52.804: BGP(1): local route 2001:DB8:1:1::/64 modified rib-nh :: path-nh :: [0x7FD225EE9970:0]
*Jul 15 12:37:52.804: BGP: tbl IPv6 Unicast:base Performing BGP Nexthop scanning for general scan
*Jul 15 12:37:52.804: BGP(1): Future scanner version: 2, current scanner version: 1
*Jul 15 12:37:52.804: BGP: tbl IPv6 Unicast:base IMP Initial export complete.
*Jul 15 12:37:52.819: BGP(1): 2001:DB8:42::42/128 route sourced locally
*Jul 15 12:37:52.819: BGP: topo global:IPv6 Unicast:base Remove_fwdroute for 2001:DB8:42::42/128
*Jul 15 12:37:52.819: [BGP Router]IPv6RT[default]: bgp 65000, Delete request for route 2001:DB8:42::42/128 from 'bgp'(0x0) metric:0 distance:1 tag:0 paths:1 route-type:0x0
*Jul 15 12:37:52.819: BGP(1): (base) 2001:DB8:3::2 send UPDATE (format) 2001:DB8:42::42/128, next 2001:DB8:3::1, metric 0, path Local
```

If you happen to know what the above word salad means, please write a comment. Otherwise, we'll be [left with the mystery](https://xkcd.com/979/) of Cisco IOS/XE hating redistributed IPv6 static routes so much that it procrastinates for a minute before it starts handling them.
