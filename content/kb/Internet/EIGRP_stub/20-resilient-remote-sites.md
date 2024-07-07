---
kb_section: EIGRP_stub
minimal_sidebar: true
pre_scroll: true
title: Resilient Remote Sites
url: /kb/Internet/EIGRP_stub/20-resilient-remote-sites/
---
Network designers aiming to increase overall network reliability usually deploy two routers at the remote offices, each one of them being connected to one of the upstream links:

{{<figure src="EIGRP_5.gif" caption="Dual-homed hub-and-spoke WAN network">}}

Heavy route summarization is usually deployed on the links between the core routers and remote offices to reduce the amount of routing information exchange. In our example, the core routers announce only a summary default route toward the remote offices:

{{<cc>}}IP routing and EIGRP configuration on core router (A1){{</cc>}}
```
hostname a1
!
interface Loopback0
 ip address 172.16.0.11 255.255.255.255
!
interface FastEthernet0/0
 ip address 10.0.0.5 255.255.255.0
!
interface Serial0/0/0.100 point-to-point
 ip address 172.16.1.1 255.255.255.252
 ip summary-address eigrp 1 0.0.0.0 0.0.0.0 5
 frame-relay interface-dlci 100   
!
router eigrp 1
 network 0.0.0.0
 no auto-summary
```

{{<cc>}}IP routing and EIGRP configuration remote site router (B1){{</cc>}}
```
hostname b1
!
interface Loopback0
 ip address 172.16.0.21 255.255.255.255
!
interface FastEthernet0/0
 ip address 192.168.0.5 255.255.255.0
 standby 1 ip 192.168.0.1
 standby 1 preempt
!
interface Serial0/0/0.100 point-to-point
 ip address 172.16.1.2 255.255.255.252
 frame-relay interface-dlci 100   
!
router eigrp 1
 network 0.0.0.0
 no auto-summary
 eigrp stub connected
```

The introduction of the EIGRP stub functionality in this design poses an interesting challenge: while the DUAL traffic is reduced (as expected), the routing might stop working when one of the upstream connections fails. For example, consider the scenario when the link between A2 and B2 fails.

{{<figure src="EIGRP_6.gif" caption="Remote site routing stops working after a WAN link failure">}}

B2 will still advertise its loopback interface to B1, but the host route will not be propagated to the core router (A1), making B2’s loopback inaccessible. If you use loopback interfaces for network management (and you should do that in any well-designed network), you’d lose access to B2 from the network management station.

Likewise, the default route A1 advertises to B1 is not propagated to B2. If the end station on remote office LAN sends its packets to B2, B2 drops them even though there is still a working link between the remote office and the central site.

The routing table on B2 after the WAN link failure is show in the following printout. As you can see, the only routes advertised from B1 to B2 are its directly connected interfaces:

{{<cc>}}Routes advertised from B1 to B2{{</cc>}}
```
b2#show ip route eigrp
     172.16.0.0 255.255.0.0 is variably subnetted, 3 subnets, 2 masks
D       172.16.0.21 255.255.255.255
           [90/156160] via 192.168.0.5, 00:02:54, FastEthernet0/0
D       172.16.1.0 255.255.255.252
           [90/2172416] via 192.168.0.5, 00:02:54, FastEthernet0/0
```

You could introduce another routing protocol (for example, RIPv2) at the remote site to solve this routing problem. That change would also require two-way redistribution between EIGRP and RIPv2, resulting in a pretty complex design. Fortunately, Cisco provided just the tool we need in IOS release 12.3(11)T – the **eigrp stub leak-map** option. With this option, you can specify a **route-map** that selects the routes a stub router propagates to its neighbors (effectively turning it into a not-so-stubby-router).

The **leak-map** option configured on the stub router does not its stub router status -- it still advertises itself as a stub router in EIGRP HELLO messages. Consequently, the  DUAL behavior on its neighbors (core routers) does not change; they still don't query the stub routers. Your network design must ensure that the exclusion of the stub router from the DUAL querying process does not lead to undesired side effects.

To configure the route leaking on the stub router, you have to configure a **route-map** that would usually refer to an **access-list** or a **prefix-list** which would in turn select the routes you want to leak. You could also decide to match other route properties (example: external EIGRP routes) with the route-map **match** keywords.

For example, in the final configuration of the B1 router (see the following printout), the *EigrpLeakedRoutes* access list permits:

* the default route -- B1 has to advertise default route received from A1 to B2
* loopback interfaces of the remote office routers -- B1 has to advertise B2's loopback interface to A1

{{<cc>}}Leak-map configuration on B1{{</cc>}}
```
router eigrp 1
 network 0.0.0.0
 no auto-summary
 eigrp stub connected leak-map EigrpLeakedRoutes
!
ip access-list standard EigrpLeakedRoutes
 permit 0.0.0.0
 permit 172.16.0.16 0.0.0.15
!
route-map EigrpLeakedRoutes permit 10
 match ip address EigrpLeakedRoutes
```

After this change, B1 advertises the default route to B2, and the EIGRP routing table on B2 includes the default route even if its WAN link has failed:

{{<cc>}}Routing table on B2 after we configured **leak-map** on B1{{</cc>}}
```
b2#show ip route eigrp
     172.16.0.0 255.255.0.0 is variably subnetted, 3 subnets, 2 masks
D       172.16.0.21 255.255.255.255
           [90/156160] via 192.168.0.5, 00:00:28, FastEthernet0/0
D       172.16.1.0 255.255.255.252
           [90/2172416] via 192.168.0.5, 00:00:28, FastEthernet0/0
D*   0.0.0.0 0.0.0.0 [90/2174976] via 192.168.0.5, 00:00:27, FastEthernet0/0
```
