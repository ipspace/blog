---
kb_section: MH_SOHO
minimal_sidebar: true
title: Configuring Small Multi-Homed Site
date: 2025-03-31 06:30:00+0200
alt_section: posts
summary: |
  The resurrected [Small Site Multihoming](/kb/Internet/MH_SOHO/) article used Cisco IOS configuration commands from 2007 (when the original article was published), including point-to-point serial interfaces and static routes pointing to interfaces.
  
  I recreated the network topology in _netlab_, created a new set of router configurations, and updated the article's configuration and monitoring parts. The lab topology and router configurations for each article section are [available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/multihoming/small-site).
---
Configuring the gateway router in a small multi-homed site is very simple. You start by configuring the private and public IP addresses:

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
interface GigabitEthernet0/1
 description gw -> [h1,h2] [stub]
 ip address 192.168.0.1 255.255.255.0
!
interface GigabitEthernet0/2
 description gw -> pe_a
 ip address 172.16.1.1 255.255.255.252
!
interface GigabitEthernet0/3
 description gw -> pe_b
 ip address 172.17.3.1 255.255.255.252
```

{{<long-quote>}}
The gateway router configuration was recreated on a [_netlab_ topology](https://github.com/ipspace/netlab-examples/blob/master/multihoming/small-site/topology.yml) using IOSv as the gateway router and a pair of FRRouting nodes acting as PE-routers.

All nodes in _[netlab](https://netlab.tools/)_-powered labs use the first LAN interface as a management interface, which is why the first data plane (inside) interface is GigabitEthernet0/1.
{{</long-quote>}}

NAT configuration is a bit more complex; you have to configure two NAT pools (one for each ISP):

{{<cc>}}Network Address Translation configuration{{</cc>}}
```
interface GigabitEthernet0/1
 ip nat inside
!
interface GigabitEthernet0/2
 ip nat outside
!
interface GigabitEthernet0/3
 ip nat outside
!
ip nat inside source route-map ISP_A interface GigabitEthernet0/2 overload
ip nat inside source route-map ISP_B interface GigabitEthernet0/3 overload
!
route-map ISP_A permit 10
 match interface GigabitEthernet0/2
!
route-map ISP_B permit 10
 match interface GigabitEthernet0/3
```

{{<note info>}}Having two **route-maps** matching outgoing interfaces (the **match interface** statement in a NAT **route-map** matches outgoing interface) is the only way to configure per-interface NAT pools in Cisco IOS.{{</note>}}

Most ISPs will not be willing to run a dynamic routing protocol with small sites, so you must configure static default routing on your router. As shown in the following printout, you would almost always prefer one provider over the other (therefore, one default route would have a lower administrative distance).

{{<cc>}}Basic multihomed default routing setup{{</cc>}}
```
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/2 172.16.1.2 10 name ISP_A
ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/3 172.17.3.2 251 name ISP_B
```

{{<note info>}}
* It’s possible (with CEF switching using per-destination load sharing) to use two default routes in a 1-to-1 load-balancing setup.
* The complete configuration of the gateway router is [available on GitHub](https://github.com/ipspace/netlab-examples/blob/master/multihoming/small-site/gw-basic-config.cfg). The configuration contains artifacts of Vagrant-powered labs like the management interface in a separate VRF, Vagrant user with SSH keys, and on-reload EEM applet.
{{</note>}}

The simplistic static routing we used represents a major availability issue; if you cannot reliably detect the link failure on the link toward ISP-A, the default static route toward ISP-B will never be used.

While you can almost always detect leased-line or cable failure (due to loss of carrier signal) and usually detect Frame-Relay failures through Local Management Interface (LMI) messages or end-to-end keepalives, it’s almost impossible to detect layer-2 failures in PPPoE (ADSL) or Metro Ethernet access layers. In these scenarios, the primary default route will never disappear (even though the next-hop router is no longer reachable), making static multi-homing impossible. This problem is solved, however, with static routes tied to IP SLA measurements.

### Revision History

2025-03-31
: Recreated the router configurations and printouts with IOSv release 15.6(1)T using Ethernet uplinks to the ISP routers.
