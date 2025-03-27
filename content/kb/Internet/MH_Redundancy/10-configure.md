---
kb_section: MH_Redundancy
minimal_sidebar: true
title: Configuring Internet Routing
alt_section: posts
index: true
---
The configuration of the gateway routers follow the principles explained in the [Small Site Multihoming](/kb/Internet/MH_SOHO/) article. IP addressing and NAT is configured on both gateway routers, as shown in the next listing (only GW-A configuration is included in most examples).

{{<cc>}}IP addressing, DHCP and NAT configuration{{</cc>}}
```
hostname GW-A
!
ip cef
!
ip dhcp pool LAN
   network 192.168.0.0 255.255.255.0
   default-router 192.168.0.1
!
ip dhcp excluded-addresses 192.168.0.1 192.168.0.10
ip dhcp excluded-addresses 192.168.0.128 192.168.0.255
!
interface FastEthernet0/0
 description *** Inside LAN interface ***
 ip address 192.168.0.1 255.255.255.0
 ip nat inside
!
interface Serial0/0/0
 description *** Link to ISP A ***
 ip address 172.16.1.1 255.255.255.252
 ip nat outside
!
ip nat inside source route-map ISP_A interface Serial0/0/0 overload
!
route-map ISP_A permit 10
 match interface Serial0/0/0
```

{{<note>}}
* To increase the overall reliability, the DHCP server is running on both gateway routers. Use the **ip dhcp excluded-addresses** configuration commands to ensure the routers always allocate addresses from non-overlapping pools.
* The router configurations contain serial interfaces that should be replaced with Ethernet interfaces in modern deployments.
{{</note>}}

To implement reliable static routes on both gateway routers, you have to configure:

* An IP SLA object to track end-to-end connectivity to an IP address that is “far enough” (at least within the core of the ISP network, tracking a server of an upstream ISP is even better).
* A **track** object that monitors the state of the IP SLA object.
* A default route that is inserted in the IP routing table based on the state of the **track** object.
* Local policy routing to ensure that the IP SLA measurements always use the Internet interface (otherwise a gateway router with failed upstream link might use the default path provided by the other gateway router for its SLA measurements).

The relevant parts of GW-A configuration are included in the next list (the detailed description of the configuration and monitoring commands related to reliable static routing is available in the [Small Site Multihoming](/kb/Internet/MH_SOHO/) article).

The only major difference between GW-A and GW-B is the default route configuration, where you would use a high administrative on the backup router (GW-B in our example) to make the default route floating; if Internet connectivity on GW-A is operational, the default route received through the routing protocol should override the static default route.

{{<note warn>}}
Static routes pointing to Ethernet interfaces should always have a next hop ([more details](/2009/10/follow-up-interface-default-route/)). If you use this article as a blueprint for deployment with Ethernet uplinks, please add relevant next hops to the **ip route** commands.
{{</note>}}

{{<cc>}}Basic multihomed default routing setup{{</cc>}}
```
hostname GW-A
!
ip sla 15
 icmp-echo 172.29.0.1 source-interface Serial0/0/0
 timeout 200
 frequency 10
!
ip sla schedule 15 life forever start-time now
!
track 17 rtr 15 reachability
 delay down 10 up 20
!
ip local policy route-map LocalPolicy
!
ip access-list extended PingISP_A
 permit icmp host 172.16.1.1 host 172.29.0.1
!
route-map LocalPolicy permit 10
 match ip address PingISP_A
 set interface Serial0/0/0
!
ip route 0.0.0.0 0.0.0.0 Serial0/0/0 10 name ISP_A track 17
```
