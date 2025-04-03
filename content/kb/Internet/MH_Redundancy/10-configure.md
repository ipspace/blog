---
kb_section: MH_Redundancy
minimal_sidebar: true
title: Configuring Internet Routing
alt_section: posts
index: true
---
The gateway routers' configuration follows the principles explained in the [Small Site Multihoming](/kb/Internet/MH_SOHO/) article. IP addressing and NAT are configured on both gateway routers, as shown in the following listing (only the GW-A configuration is included in most examples; the [complete router configurations are on GitHub](https://github.com/ipspace/netlab-examples/tree/master/multihoming/redundant-small-site)).

{{<cc>}}IP addressing, DHCP and NAT configuration on GW-A{{</cc>}}
```
ip dhcp pool LAN
   network 192.168.0.0 255.255.255.0
   default-router 192.168.0.1
exit
!
ip dhcp excluded-address 192.168.0.1 192.168.0.10
ip dhcp excluded-address 192.168.0.128 192.168.0.255
!
interface Ethernet0/1
 description gw_a -> [h1,h2,gw_b]
 ip address 192.168.0.1 255.255.255.0
 ip nat enable
!
interface Ethernet0/2
 description gw_a -> pe_a
 ip address 172.16.1.1 255.255.255.252
 ip nat enable
!
ip access-list standard Site
 10 permit 192.168.0.0 0.0.0.255
!
route-map Internet_Exit permit 10
 match ip address Site
!
ip nat inside source route-map Internet_Exit interface Ethernet0/2 overload
```

{{<long-quote>}}
**Notes:**

* The DHCP server runs on both gateway routers to increase the overall reliability. Use the **ip dhcp excluded-addresses** configuration commands to ensure the routers allocate addresses from non-overlapping pools.
* The NAT configuration is using the *NAT Virtual Interface*
* The NAT translation **must** use a route map to match the outgoing interface. Otherwise, GW-A would translate the host-originated packets routed to GW-B.
* The gateway router configuration was recreated on a [_netlab_ topology](https://github.com/ipspace/netlab-examples/blob/master/multihoming/redundant-small-site/topology.yml) using IOS-on-Linux (IOL) as the gateway router and a pair of FRRouting nodes acting as PE-routers.
* All nodes in _[netlab](https://netlab.tools/)_-powered labs use the first LAN interface as a management interface, which is why the first data plane (inside) interface is Ethernet0/1.
{{</long-quote>}}

To implement reliable static routes on both gateway routers, you have to configure:

* An IP SLA object to track end-to-end connectivity to an IP address that is “far enough” (at least within the ISP network's core; tracking an upstream ISP server is even better).
* A **track** object that monitors the state of the IP SLA object.
* A local routing policy ensuring the IP SLA measurements always use the Internet interface (otherwise, a gateway router with a failed upstream link might use the default path the other gateway router provided for its SLA measurements).
* A static default route based on the state of the **track** object.

The relevant parts of GW-A configuration are included in the following listing (the detailed description of the configuration and monitoring commands related to reliable static routing is available in the [Small Site Multihoming](/kb/Internet/MH_SOHO/) article).

{{<cc>}}Reliable static default route using IP SLA on GW-A{{</cc>}}
```
ip access-list extended Ping_probe
 10 permit icmp host 172.16.1.1 host 172.29.0.1
!
route-map LocalPolicy permit 10
 match ip address Ping_probe
 set ip next-hop 172.16.1.2
 set interface Ethernet0/2
!
ip local policy route-map LocalPolicy
!
ip sla 15
 icmp-echo 172.29.0.1 source-interface Ethernet0/2
  threshold 100
  timeout 200
  frequency 1
ip sla schedule 15 life forever start-time now
!
track 17 ip sla 15 state
 delay down 5 up 20
!
ip route 0.0.0.0 0.0.0.0 172.16.1.2 name ISP_A track 17
```

The setup on GW-B is much more straightforward, as we're using it just as a backup router. It has a floating static default route; if Internet connectivity on GW-A is operational, the default route received through the routing protocol should override the static default route.

{{<cc>}}Floating static default route on GW-B{{</cc>}}
```
ip route 0.0.0.0 0.0.0.0 172.17.3.2 name ISP_B 250
```
