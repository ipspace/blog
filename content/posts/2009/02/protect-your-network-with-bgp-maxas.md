---
date: 2009-02-17 12:07:00.002000+01:00
tags:
- BGP
title: Protect Your Network with BGP maxas-limit
url: /2009/02/protect-your-network-with-bgp-maxas/
lastmod: 2020-12-05 07:59:00
---
In February 2009, a greenhorn ISP (they joined RIPE less than four months before the incident) in central Europe managed to generate a BGP update with too many AS numbers in the AS path, confusing older routers. [You can find the details in an old Renesys blog post](https://web.archive.org/web/20110211072612/http://www.renesys.com/blog/2009/02/the-flap-heard-around-the-worl.shtml); at the peak of the instability, they were receiving over 100.000 BGP updates *per second*.

It's very easy to protect yourself (and your downstream neighbors) from an operational error like this one. Cisco has [implemented the AS-path length limiting code in IOS release 12.2](http://www.cisco.com/en/US/docs/ios/iproute/command/reference/irp_bgp1.html). One would hope that the major ISPs would have started using this feature years ago; obviously that's not the case, so here's how you do it... just to make sure everyone understands what the **bgp maxas-limit** command does and hopefully implements it in this millennium.

{{<ct3_rescue>}}

BGP allows numerous attributes (including AS-path, metrics, local preference and communities) to be attached to every advertised IP prefix. The total length of BGP attributes attached to a single IP prefix can be very large (up to 64K bytes). IP prefixes with excessive amount of attribute data residing in the BGP table can results in significant memory utilization and trigger software bugs.

{{<note warn>}}
AS-path attribute having more than 255 AS numbers is expressed as multiple AS\_SEQUENCE segments. This unusual AS-path composition caused problems in older Cisco IOS releases and could result in continuously flapping BGP session. Using **bgp maxas-limit** avoids this behavior unless the **route-map** based AS-path prepending extends the AS-path length beyond 255 AS numbers.  
  
The *extended length* bit in the BGP UPDATE message that has to be used when the AS-path length exceeds 128 AS numbers also caused errors in older IOS releases (Cisco bug ID CSCdr54230).
{{</note>}}

Cisco IOS can limit the maximum length of the AS-path attribute with the **bgp maxas-limit _length_** router configuration command. It’s highly advisable that you use this command together with [other BGP security measures](https://tools.ietf.org/html/rfc7454) to reduce the potential impact of oversized AS-path attributes on the operation of your network. 

The maximum sensible length of the AS-path attribute depends on your position within the Internet. Core operators observe lower AS-path lengths than the edge points. Due to CSCdr54230, accepting AS-paths having more than approximately 100 AS numbers was best avoided; reasonable values are usually much lower... and as always, [Geoff Huston published a measurement](https://labs.apnic.net/?p=1264) giving you the answer to that question.

Configuring the **bgp maxas-limit** command does not impact the regular BGP operation. The **maxas-limit** is checked during the inbound update processing. Prefixes with oversized AS-path length are simply ignored; BGP sessions are not disrupted.

## Test bed description

The **bgp maxas-limit** functionality can be easily demonstrated in a test bed consisting of only two routers.

{{<cc>}}Configuration of R1 - the sender of long AS paths{{</cc>}}
```
hostname R1
!
ip cef
!
interface Loopback0
 ip address 10.0.1.1 255.255.255.255
!
interface Serial1/0
 description Link to R2 s1/0
 ip address 10.0.7.13 255.255.255.252
 encapsulation ppp
!
router bgp 65000
 no synchronization
 bgp log-neighbor-changes
 network 10.1.1.0 mask 255.255.255.0
 network 10.1.2.0 mask 255.255.255.0
 neighbor 10.0.7.14 remote-as 65100
 neighbor 10.0.7.14 route-map prepend out
 no auto-summary
!
ip classless
!
ip route 10.1.1.0 255.255.255.0 Null0
ip route 10.1.2.0 255.255.255.0 Null0
!
ip prefix-list prepend seq 5 permit 10.1.2.0/24
!
route-map prepend permit 10
 match ip address prefix-list prepend
 set as-path prepend 65000 65000 65000 65000
!
route-map prepend permit 20
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 transport preferred none
 stopbits 1
!
ntp logging
end 
```

{{<cc>}}Configuration of R2 - the receiver of long AS paths{{</cc>}}
```
hostname R2
!
ip cef
!
interface Loopback0
 ip address 10.0.1.2 255.255.255.255
!
interface Serial1/0
 description Link to R1 s1/0
 ip address 10.0.7.14 255.255.255.252
 encapsulation ppp
!
router bgp 65100
 no synchronization
 bgp log-neighbor-changes
 bgp maxas-limit 3
 neighbor 10.0.7.13 remote-as 65000
 no auto-summary
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 transport preferred none
 stopbits 1
!
ntp logging
end 
```

## Exception logging

The **bgp maxas-limit** functionality does not impact the regular BGP operation. Whenever an inbound BGP update is received with an oversized AS-path attribute, the router logs a warning message and ignores the update.

{{<cc>}}Log message generated after an inbound update has been ignored{{</cc>}}

```
%BGP-6-ASPATH: Long AS path 65000 65000 65000 65000 65000
 received from 10.0.7.13: More than configured MAXAS-LIMIT 
```

The AS-path length limiting functionality can also be observed with any of the **debug ip bgp update** commands. A sample printout is included below:

{{<cc>}}BGP debugging printout generated on R2{{</cc>}}
```
BGP(0): 10.0.7.13 rcv UPDATE w/ attr: nexthop 10.0.7.13, origin i,
  metric 0, originator 0.0.0.0, path 65000 65000 65000 65000 65000,
  community , extended community , SSA attribute
BGPSSA ssacount is 0
BGP(0): 10.0.7.13 rcv UPDATE about 10.1.2.0/24 -- DENIED due to:
  AS-PATH length over 4072;
BGP(0): 10.0.7.13 rcvd UPDATE w/ attr: nexthop 10.0.7.13, origin i,
  metric 0, path 65000
BGP(0): 10.0.7.13 rcvd 10.1.1.0/24...duplicate ignored 
```
