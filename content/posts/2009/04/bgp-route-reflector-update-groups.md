---
date: 2009-04-02 07:05:00.002000+02:00
tags:
- BGP
title: BGP Route Reflector Update Groups (technical details)
url: /2009/04/bgp-route-reflector-update-groups/
---
One of the readers of my [BGP Route Reflectors](/2008/08/bgp-route-reflector-details/) article spotted an "_obvious deviation from how we always though the route reflectors work_":

> An IBGP route received from a route-reflector client is sent to all IBGP peers, **including the client from which it was received.** 

A quick lab test confirmed the validity of my claims: a BGP route reflector does send an update back to the client from which it was received (and it's perfectly legal according to the [updated BGP Route Reflector RFC](http://tools.ietf.org/html/rfc4456)).
<!--more-->
### Why Are We Discussing This?

The traditional BGP route reflector (RR) rules (specified in [RFC 1966](http://tools.ietf.org/html/rfc1966)) stipulated that a BGP RR shall not send an update received from a RR client back to the same client. The RR thus had to treat each RR client individually and could not reuse outbound BGP updates sent to one RR client for other RR clients, resulting in significant performance degradation in scenarios where a RR had numerous RR clients.

[RFC 4456](http://tools.ietf.org/html/rfc4456) has relaxed the update propagation requirements of RFC 1966 and specifies that a _RR sends the same update to all RR clients_ (even if the original route was received from an RR client). The ORIGINATOR ID BGP attribute is _used by the RR clients to detect propagation loops_. The relaxed rules of RFC 4456 allow a route reflector to group all the RR clients into a single update group, resulting in significant performance improvements, as the RR computes a single outbound BGP update which is sent to all RR clients.

### Test Network Diagram

The behavior of Cisco IOS BGP Route Reflector code was tested in the following network. All routers were running IOS release 12.2(33)SRC3 (other recent IOS releases exhibit the same behavior).

{{<figure src="/2009/04/RR_Update_Testbed.png" caption="Route Reflector testbed">}}

## Router Configurations

The following printouts include relevant parts of configurations of R1 and RR.

{{<cc>}}Configuration of the BGP route reflector (RR){{</cc>}}
```
hostname RR
!
interface Loopback0
 ip address 10.0.1.2 255.255.255.255
!
interface FastEthernet0/0
 description LAN 1 (R1)
 ip address 10.2.1.1 255.255.255.0
 speed auto
 duplex auto
!
interface Serial1/0
 description Link to POP(ROUTER) s1/0
 ip address 10.0.7.2 255.255.255.252
 encapsulation ppp
 serial restart-delay 0
!
router ospf 1
 log-adjacency-changes
 passive-interface default
 no passive-interface FastEthernet0/0
 no passive-interface Serial1/0
 network 0.0.0.0 255.255.255.255 area 0
!
router bgp 64500
 no synchronization
 bgp log-neighbor-changes
 neighbor 10.0.7.1 remote-as 64500
 neighbor 10.0.7.1 route-reflector-client
 neighbor 10.2.1.2 remote-as 64500
 neighbor 10.2.1.2 route-reflector-client
 no auto-summary
```

{{<cc>}}Configuration of the RR client with an EBGP session (R1){{</cc>}}
```
hostname R1
!
interface Loopback0
 ip address 10.0.1.3 255.255.255.255
!
interface FastEthernet0/0
 description LAN 1 (RR)
 ip address 10.2.1.2 255.255.255.0
 speed auto
 duplex auto
!
interface Serial1/1
 description Link to Customer
 ip address 10.0.7.9 255.255.255.252
 encapsulation ppp
 serial restart-delay 0
!
router ospf 1
 log-adjacency-changes
 passive-interface default
 no passive-interface FastEthernet0/0
 network 0.0.0.0 255.255.255.255 area 0
!
router bgp 64500
 no synchronization
 bgp log-neighbor-changes
 neighbor 10.0.7.10 remote-as 65100
 neighbor 10.2.1.1 remote-as 64500
 no auto-summary
```

### Test results

The **show ip bgp update-groups** command executed on RR clearly indicates that the BGP update process computes a single outbound BGP update for both RR clients:

```
RR#show ip bgp update-group 
BGP version 4 update-group 2, internal, Address Family: IPv4 Unicast
  BGP Update version : 7/0, messages 0
  Route-Reflector Client
  Update messages formatted 6, replicated 6
  Number of NLRIs in the update sent: max 1, min 0
  Minimum time between advertisement runs is 0 seconds
  Has 2 members (* indicates the members currently being sent updates): 
   10.0.7.1         10.2.1.2        
```

The printouts of the **debug ip bgp updates** command on R1 also demonstrate the low-level details of IBGP update processing. When R1 receives an update from the EBGP peer, it propagates the update to RR:

```
19:58:28.151: BGP(0): 10.0.7.10 rcvd UPDATE w/ attr: nexthop 10.0.7.10,↲
origin i, metric 0, path 65100
19:58:28.155: BGP(0): 10.0.7.10 rcvd 10.9.9.0/24
19:58:28.171: BGP(0): Revise route installing 1 of 1 routes↲
for 10.9.9.0/24 -> 10.0.7.10(global) to main IP table
19:58:28.171: BGP(0): 10.2.1.1 NEXT_HOP is on same subnet↲
as the bgp peer and set to 10.0.7.10 for net 10.9.9.0/24
19:58:28.171: BGP(0): 10.2.1.1 send UPDATE (format) 10.9.9.0/24, ↲
next 10.0.7.10, metric 0, path 65100
```

Almost immediately, the same route is received back from the route reflector, but R1 ignores it because the RR inserted R1’s router ID into the ORIGINATOR ID attribute of the route:

```
19:58:28.191: BGP: 10.2.1.1 Local router is the Originator; ↲
Discard update
19:58:28.191: BGP(0): 10.2.1.1 rcv UPDATE w/ attr: nexthop 10.0.7.10, ↲
origin i, localpref 100, metric 0, originator 10.0.1.3, ↲
clusterlist 10.0.1.2, path 65100
19:58:28.191: BGP(0): 10.2.1.1 rcv UPDATE about 10.9.9.0/24↲
 -- DENIED due to: ORIGINATOR is us;
```
