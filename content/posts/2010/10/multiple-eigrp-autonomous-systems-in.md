---
date: 2010-10-04 06:50:00+02:00
eigrp_tag: deploy
tags:
- EIGRP
- MPLS VPN
title: Multiple EIGRP Autonomous Systems in a VRF
url: /2010/10/multiple-eigrp-autonomous-systems-in/
---
A while ago Ron sent me an intriguing question: "Is it possible to have two EIGRP AS numbers in the same VRF?" Obviously he's working on a network with multiple EIGRP processes (not an uncommon pre-MPLS/VPN solution; I did a network design along the same lines almost 20 years ago).

It's easy to run multiple EIGRP autonomous systems in the global IP routing table; just create more than one EIGRP process. They can even run over the same set of interfaces. EIGRP-in-a-VRF implementation is slightly different; you configure an **address family** within another EIGRP process and (optionally) specify an AS number that does not have to match the AS number of the EIGRP process.
<!--more-->
My first (pretty lame) reply was obvious: why don't you create two EIGRP processes and specify the same VRF **address family** in both? Unfortunately this trick doesn't work; although you could use multiple EIGRP processes, each VRF can be specified only in one of them.

In the end, I had to admit that the only viable solution is creation of two VRFs (with the same route targets and different route distinguishers), one for each EIGRP AS number. Ron's reply: "*Yeah, I know that works, but I was trying to figure out how to do it within EIGRP*. " Obviously you can't.

Just in case you'd need to do something similar, here's the relevant part of the PE-router configuration (note that we're using **eigrp 11** everywhere even though the AS numbers in the VRFs are 1 and 2).

```
ip vrf Cust_AS_1
 rd 65000:1
 route-target export 65001:1
 route-target import 65001:1
!
ip vrf Cust_AS_2
 rd 65000:2
 route-target export 65001:1
 route-target import 65001:1
!
router eigrp 11
 !
 address-family ipv4 vrf Cust_AS_1
  autonomous-system 1
  network 0.0.0.0
  no auto-summary
  redistribute bgp 65000 metric 128 10000 255 1 1500
 exit-address-family
 !
 address-family ipv4 vrf Cust_AS_2
  autonomous-system 2
  network 0.0.0.0
  no auto-summary
  redistribute bgp 65000 metric 128 10000 255 1 1500
 exit-address-family
!
router bgp 65000
 no synchronization
 bgp log-neighbor-changes
 !
 address-family ipv4 vrf Cust_AS_1
  no synchronization
  redistribute eigrp 11
!
 address-family ipv4 vrf Cust_AS_2
  no synchronization
  redistribute eigrp 11
```
