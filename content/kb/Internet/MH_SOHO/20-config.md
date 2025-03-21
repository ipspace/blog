---
kb_section: MH_SOHO
minimal_sidebar: true
title: Configuring Small Multi-Homed Site
alt_section: posts
---
Configuring the gateway router in a small multi-homed site is very simple. You start by configuring the private and public IP addresses:

{{<note warn>}}The router configurations contain serial interfaces that should be replaced with Ethernet interfaces in modern deployments.{{</note>}}

{{<cc>}}Initial router configuration{{</cc>}}
```
hostname GW
!
ip cef
!
ip dhcp pool LAN
   network 192.168.0.0 255.255.255.0
   default-router 192.168.0.1
!
interface FastEthernet0/0
 description Inside LAN interface
 ip address 192.168.0.1 255.255.255.0
!
interface Serial0/0/0
 description Link to ISP 1
 ip address 172.16.1.1 255.255.255.252
!
interface Serial0/0/1
 description Link to ISP 2
 ip address 172.17.3.1 255.255.255.252
```

NAT configuration is a bit more complex; you have to configure two NAT pools (one for each ISP):

{{<cc>}}Network Address Translation configuration{{</cc>}}
```
interface FastEthernet0/0
 ip nat inside
!
interface Serial0/0/0
 ip nat outside
!
interface Serial0/0/1 point-to-point
 ip nat outside
!
ip nat inside source route-map ISP_A interface Serial0/0/0 overload
ip nat inside source route-map ISP_B interface Serial0/0/1 overload
!
route-map ISP_A permit 10
 match interface Serial0/0/0
!
route-map ISP_B permit 10
 match interface Serial0/0/1
```

{{<note info>}}Having two **route-maps** matching outgoing interfaces (the **match interface** statement in a NAT **route-map** matches outgoing interface) is the only way to configure per-interface NAT pools in Cisco IOS.{{</note>}}

Most ISPs will not be willing to run a dynamic routing protocol with small sites, so you must configure static default routing on your router. As shown in the following printout, you would almost always prefer one provider over the other (therefore, one default route would have a lower administrative distance).

{{<cc>}}Basic multihomed default routing setup{{</cc>}}
```
ip route 0.0.0.0 0.0.0.0 Serial0/0/0 10 name ISP_A
ip route 0.0.0.0 0.0.0.0 Serial0/0/1 251 name ISP_B
```

{{<note>}}It’s possible (with CEF switching using per-destination load sharing) to use two default routes in a 1-to-1 load-balancing setup.
{{</note>}}

{{<note warn>}}
Static routes pointing to Ethernet interfaces should always have a next hop ([more details](/2009/10/follow-up-interface-default-route/)). If you use this article as a blueprint for deployment with Ethernet uplinks, please add relevant next hops to the **ip route** commands.
{{</note>}}

The simplistic static routing we used represents a major availability issue: if you cannot reliably detect the link failure on the link toward ISP-A, the default static route toward ISP-B will never be used.

While you can almost always detect leased-line or cable failure (due to loss of carrier signal) and usually detect Frame-Relay failures through Local Management Interface (LMI) messages or end-to-end keepalives, it’s almost impossible to detect layer-2 failures in PPPoE (ADSL) or Metro Ethernet access layers. In these scenarios, the primary default route will never disappear (even though the next-hop router is no longer reachable), making static multi-homing impossible. This problem is solved, however, in the Cisco IOS Release 12.3(8)T (integrated in release 12.4) with static routes tied to IP SLA measurements.
