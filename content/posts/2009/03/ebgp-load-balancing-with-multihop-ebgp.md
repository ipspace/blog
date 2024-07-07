---
date: 2009-03-13 06:41:00.005000+01:00
tags:
- BGP
- load balancing
title: EBGP Load Balancing with a Multihop EBGP Session
url: /2009/03/ebgp-load-balancing-with-multihop-ebgp/
lastmod: 2020-12-29 07:37
---
Multihop EBGP sessions are the traditional way to implement EBGP load balancing on parallel links. EBGP session is established between loopback interfaces of adjacent routers (see the next diagram; initial router configurations are included at the bottom of the article) and static routes (or an extra instance of a dynamic routing protocol) are used to achieve connectivity between loopback interfaces (BGP next-hops). The load balancing is an automatic result of the recursive route lookup of BGP next hops.

{{<ct3_rescue>}}
<!--more-->
{{<toc>}}

EBGP session between loopback interfaces is most appropriate in scenarios where all the links between the EBGP neighbors have identical bandwidth. To achieve proportional load balancing across links with different bandwidths, use [parallel EBGP sessions](/2008/08/load-balancing-with-parallel-ebgp/) in the [unequal-bandwidth scenarios](/2008/07/unequal-bandwidth-ebgp-load-balancing/).

We'll illustrate the concepts described in this article with a 2-router testbed shown in the following diagram:

{{<figure src="/2009/03/EBGP_LB_Loopback_Testbed.png" caption="EBGP load balancing testbed">}}

## Multihop EBGP Session with Static Routes

The following configuration steps are necessary when you decide to use static routes to provide connectivity between the loopback interfaces (endpoints of the EBGP session):

-   Configure static routes toward the loopback address of EBGP neighbor. The static routes can point to the next-hop (see the configuration of R1) or the physical interface (as configured on E1).

{{<cc>}}Static route configuration on R1{{</cc>}}
```
ip route 10.0.0.23 255.255.255.255 10.0.1.1
ip route 10.0.0.23 255.255.255.255 10.0.1.9
```

{{<cc>}}Static route configuration on E1{{</cc>}}
```
ip route 10.0.0.1 255.255.255.255 Serial1/0
ip route 10.0.0.1 255.255.255.255 Serial1/3
```

{{<note warn>}}Static routes pointing to the physical interface shall be used only on point-to-point interfaces.{{</note>}}

-   Configure EBGP neighbor. Use the neighbor’s loopback address and specify the source address of the EBGP session with the **neighbor _address_ update-source loopback _x_** router configuration command.

{{<cc>}}BGP neighbor configuration on R1{{</cc>}}
```
router bgp 64800
 neighbor 10.0.0.23 remote-as 65000
 neighbor 10.0.0.23 update-source Loopback0
```

{{<cc>}}BGP neighbor configuration on E1{{</cc>}}
```
router bgp 65000
 neighbor 10.0.0.1 remote-as 64800
 neighbor 10.0.0.1 update-source Loopback0
```

{{<note warn>}}If you don’t use the **neighbor update-source** router configuration command, the EBGP session will not be established. When the source interface of the BGP session is not specified, the router uses the IP address of the outgoing link as the source address of the BGP session and the EBGP peer will reset the incoming BGP session coming from an unknown IP address.{{</note>}}

-   Configure multihop EBGP session with **neighbor ebgp-multihop** router configuration command.

{{<cc>}}EBGP multihop configuration on R1{{</cc>}}
```
router bgp 64800
 neighbor 10.0.0.23 ebgp-multihop 2
```

{{<cc>}}EBGP multihop configuration on E1{{</cc>}}
```
router bgp 65000
 neighbor 10.0.0.1 ebgp-multihop 2
```

{{<note warn>}}Without the **neighbor ebgp-multihop** router configuration command, the EBGP session will not be established as Cisco IOS expects a regular EBGP neighbor to be directly connected unless you disable the directly-connected check (see below).{{</note>}}

The **neighbor ebgp-multihop** command makes EBGP sessions vulnerable to TCP session hijacking. To minimize this risk, use the lowest possible TTL value (2) as the *maximum hop count* parameter in this command. The default TTL value setting (when the **neighbor ebgp-multihop** is used without the *maximum hop count* parameter) is 255. For more details on securing BGP routing, read [RFC 7454](https://tools.ietf.org/html/rfc7454).

After the **neighbor ebgp-multihop** has been configured, the EBGP session is established and E1 advertises a BGP prefix to R1:

{{<cc>}}EBGP session on R1{{</cc>}}
```
R1#show ip bgp summary | begin Neighbor
Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.0.0.23       4 65000      20      18        6    0    0 00:06:53        1
```

The **show ip bgp neighbor** indicates that the neighbor 10.0.0.23 is indeed an EBGP neighbor that is up to two hops away:

{{<cc>}}EBGP neighbor details on R1{{</cc>}}
```
R1#show ip bgp neighbor 10.0.0.23
BGP neighbor is 10.0.0.23, remote AS 65000, external link
  BGP version 4, remote router ID 10.0.0.23
  BGP state = Established, up for 00:07:50

  … deleted …

  Address tracking is enabled, the RIB does have a route to 10.0.0.23
  Connections established 2; dropped 1
  Last reset 00:07:59, due to Peer closed the session
  External BGP neighbor may be up to 2 hops away.
  Transport(tcp) path-mtu-discovery is enabled

  … deleted …
```

After BGP has converged, the BGP routing table on R1 contains a single copy of the prefix 10.7.1.0/24 advertised by E1.

{{<cc>}}BGP table on R1{{</cc>}}
```
R1#show ip bgp | begin Network
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.7.1.0/24      10.0.0.23                0             0 65000 i 
```

The IP routing table also contains a single copy of the prefix …

{{<cc>}}Route to 10.7.1.0/24 in the IP routing table{{</cc>}}
```
R1#show ip route 10.7.1.0
Routing entry for 10.7.1.0/24
  Known via "bgp 64800", distance 20, metric 0
  Tag 65000, type external
  Last update from 10.0.0.23 00:12:34 ago
  Routing Descriptor Blocks:
  * 10.0.0.23, from 10.0.0.23, 00:12:34 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 65000 
```

… but the CEF table (which contains the results of the recursive lookup) has two equal-cost paths to the prefix:

{{<cc>}}Multiple entries to 10.7.1.0/24 in the CEF table{{</cc>}}
```
R1#show ip cef 10.7.1.0
10.7.1.0/24
  nexthop 10.0.1.1 Serial1/0
  nexthop 10.0.1.9 Serial1/2 
```

### Fast Failover of a Multihop EBGP Session

Cisco IOS release 15.2(4)S and IOS XE release 3.6S added support for multihop BFD checks on multihop EBGP sessions. To use BFD to detect EBGP multihop session failure configure **neighbor fall-over bfd multi-hop**. If you're running an earlier Cisco IOS release or if one of the EBGP peers doesn't support multihop BFD, use BGP **fall-over** functionality.

BGP *fast external failover* that is enabled by default on all EBGP sessions does not work on multihop EBGP sessions. Fast external failover is tied to the changes in physical interface status and does not use the IP routing table to check EBGP neighbor reachability.

For example, after both links from R1 to E1 fail, R1 detects the failure only after the BGP keepalive timer (with the default value of 3 minutes) expires.

{{<cc>}}BGP keepalive timer detects EBGP neighbor failure{{</cc>}}
```
16:45:41.127: %LINEPROTO-5-UPDOWN: Line protocol on Interface Serial1/0,↩
 changed state to down
16:45:47.619: %LINEPROTO-5-UPDOWN: Line protocol on Interface Serial1/2,↩
 changed state to down
16:48:17.091: %BGP-5-ADJCHANGE: neighbor 10.0.0.23 Down↩
 BGP Notification sent
16:48:17.095: %BGP-3-NOTIFICATION: sent to neighbor 10.0.0.23 4/0↩
 (hold time expired) 0 bytes 
```

To improve the detection of an EBGP session failure when the EBGP session uses the **neighbor ebgp-multihop** option, you have to configure *fast BGP neighbor loss detection* with the **neighbor fall-over** command. It’s recommended to use a **route-map** matching only host routes with the **neighbor fall-over** command to ensure that the router does not interpret a summary route or a default route as a viable path toward the EBGP neighbor. The fast BGP neighbor loss configuration on E1 is shown in the following printout:

{{<cc>}}Fast BGP neighbor loss detection configuration on E1{{</cc>}}
```
router bgp 65000
 neighbor 10.0.0.1 fall-over route-map EBGP_multihop
!
ip prefix-list EBGP_multihop seq 5 permit 0.0.0.0/0 ge 32
!
route-map EBGP_multihop permit 10
 match ip address prefix-list EBGP_multihop 
```

After the **neighbor fall-over** has been configured on E1, the EBGP session failure detection improves dramatically (the session failure is detected within a few seconds after the last link toward the neighbor fails).

{{<cc>}}Fast BGP neighbor loss detection on E1{{</cc>}}
```
16:57:11.391: %LINEPROTO-5-UPDOWN: Line protocol on Interface Serial1/0,↩
 changed state to down
16:57:13.915: %LINEPROTO-5-UPDOWN: Line protocol on Interface Serial1/3,↩
 changed state to down
16:57:15.231: %BGP-5-ADJCHANGE: neighbor 10.0.0.1 Down Route to peer lost 
```

### Final Router Configurations

{{<cc>}}Final configuration of E1{{</cc>}}
```
service timestamps debug uptime
service timestamps log datetime msec
no service password-encryption
!
hostname E1
!
no aaa new-model
no ip source-route
ip cef
!
archive
 log config
  hidekeys
!
interface Loopback0
 ip address 10.0.0.23 255.255.255.255
!
interface Serial1/0
 ip address 10.0.1.1 255.255.255.252
 encapsulation ppp
 no peer neighbor-route
 keepalive 3
!
interface Serial1/3
 ip address 10.0.1.9 255.255.255.252
 encapsulation ppp
 no peer neighbor-route
 keepalive 3
!
router bgp 65000
 no synchronization
 bgp log-neighbor-changes
 network 10.7.1.0 mask 255.255.255.0
 neighbor 10.0.0.1 remote-as 64800
 neighbor 10.0.0.1 ebgp-multihop 2
 neighbor 10.0.0.1 update-source Loopback0
 neighbor 10.0.0.1 fall-over route-map EBGP_multihop
 no auto-summary
!
ip forward-protocol nd
ip route 10.0.0.1 255.255.255.255 Serial1/0
ip route 10.0.0.1 255.255.255.255 Serial1/3
ip route 10.7.1.0 255.255.255.0 Null0
no ip http server
no ip http secure-server
!
ip prefix-list EBGP_multihop seq 5 permit 0.0.0.0/0 ge 32
!
route-map EBGP_multihop permit 10
 match ip address prefix-list EBGP_multihop
!
control-plane
!
line con 0
 stopbits 1
line aux 0
 stopbits 1
line vty 0 4
 login
!
end 
```

{{<cc>}}Final configuration of R1{{</cc>}}
```
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname R1
!
no aaa new-model
no ip source-route
ip cef
!
archive
 log config
  hidekeys
!
interface Loopback0
 ip address 10.0.0.1 255.255.255.255
 ip ospf 1 area 0
!
interface FastEthernet0/0
 ip address 10.2.0.1 255.255.255.0
 ip ospf 1 area 0
 duplex half
!
interface Serial1/0
 ip address 10.0.1.2 255.255.255.252
 encapsulation ppp
 no peer neighbor-route
 keepalive 3
 serial restart-delay 0
!
interface Serial1/2
 ip address 10.0.1.10 255.255.255.252
 encapsulation ppp
 no peer neighbor-route
 keepalive 3
 serial restart-delay 0
!
!
router ospf 1
 log-adjacency-changes
 passive-interface default
 no passive-interface FastEthernet0/0
!
router bgp 64800
 no synchronization
 bgp log-neighbor-changes
 neighbor 10.0.0.23 remote-as 65000
 neighbor 10.0.0.23 ebgp-multihop 2
 neighbor 10.0.0.23 update-source Loopback0
 neighbor 10.0.0.23 fall-over route-map EBGP_multihop
 no auto-summary
!
ip forward-protocol nd
ip route 10.0.0.23 255.255.255.255 10.0.1.1
ip route 10.0.0.23 255.255.255.255 10.0.1.9
no ip http server
no ip http secure-server
!
ip prefix-list EBGP_multihop seq 5 permit 0.0.0.0/0 ge 32
!
route-map EBGP_multihop permit 10
 match ip address prefix-list EBGP_multihop
!
control-plane
!
line con 0
 stopbits 1
line aux 0
 stopbits 1
line vty 0 4
 login
!
end 
```

## Single-hop EBGP session between loopback interfaces

IOS releases prior to 12.2(13)T and 12.0(22)S required a *multihop* EBGP session between loopback interfaces of adjacent routers. Adjacent routers are by definition not using true multihop session, but the **neighbor ebgp-multihop** router configuration command was still needed to bypass the “directly connected EBGP neighbor” check built into Cisco IOS. 

The **neighbor disable-connected-check** router configuration command disables that check without changing the TTL value in outgoing TCP packets. The fast failover behavior or BFD support remains unchanged: since the neighbor’s IP address is not directly connected the default failover detection does not work. You have to use multihop BFD or the **neighbor fall-over** router configuration command.

BGP configurations of E1 and R1 where the **neighbor ebgp-multihop** has been replaced with the **neighbor disable-connected-check** command are included below:

{{<cc>}}Configuration of E1{{</cc>}}
```
router bgp 65000
 no synchronization
 bgp log-neighbor-changes
 network 10.7.1.0 mask 255.255.255.0
 neighbor 10.0.0.1 remote-as 64800
 neighbor 10.0.0.1 disable-connected-check
 neighbor 10.0.0.1 update-source Loopback0
 neighbor 10.0.0.1 fall-over route-map EBGP_multihop
 no auto-summary
!
ip route 10.0.0.1 255.255.255.255 Serial1/0
ip route 10.0.0.1 255.255.255.255 Serial1/3
ip route 10.7.1.0 255.255.255.0 Null0
!
ip prefix-list EBGP_multihop seq 5 permit 0.0.0.0/0 ge 32
!
route-map EBGP_multihop permit 10
 match ip address prefix-list EBGP_multihop 
```

{{<cc>}}Configuration of R1{{</cc>}}
```
router bgp 64800
 no synchronization
 bgp log-neighbor-changes
 neighbor 10.0.0.23 remote-as 65000
 neighbor 10.0.0.23 disable-connected-check
 neighbor 10.0.0.23 update-source Loopback0
 neighbor 10.0.0.23 fall-over route-map EBGP_multihop
 no auto-summary
!
ip route 10.0.0.23 255.255.255.255 10.0.1.1
ip route 10.0.0.23 255.255.255.255 10.0.1.9
!
ip prefix-list EBGP_multihop seq 5 permit 0.0.0.0/0 ge 32
!
route-map EBGP_multihop permit 10
 match ip address prefix-list EBGP_multihop 
```

After the BGP session between E1 and R1 is established, you can use the **show ip bgp neighbor** command to inspect the details of the EBGP session. The output of this command on R1 confirms that the E1 is an EBGP neighbor that is not directly connected, but R1 nonetheless uses TTL=1 in outgoing TCP packets.

{{<cc>}}BGP neighbor details on R1{{</cc>}}
```
R1#show ip bgp neighbor 10.0.0.23
BGP neighbor is 10.0.0.23,  remote AS 65000, external link
  BGP version 4, remote router ID 10.0.0.23
  BGP state = Established, up for 00:33:08

  … deleted …

  Address tracking is enabled, the RIB does have a route to 10.0.0.23
  Connections established 1; dropped 0
  Last reset never
  External BGP neighbor not directly connected.
  Transport(tcp) path-mtu-discovery is enabled
Connection state is ESTAB, I/O status: 1, unread input bytes: 0
Connection is ECN Disabled, Mininum incoming TTL 0, Outgoing TTL 1
Local host: 10.0.0.1, Local port: 39201
Foreign host: 10.0.0.23, Foreign port: 179
Connection tableid (VRF): 0

  … deleted …
```
