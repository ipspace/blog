---
kb_section: MH_Redundancy
minimal_sidebar: true
title: Configuring Intra-Site Routing
alt_section: posts
index: true
---
The static default route configured on GW-A and GW-B has to be propagated between them to ensure that both routers have the same view of the Internet connectivity. The easiest way to implement this requirement is to redistribute the static default route into a dynamic routing protocol configured between the two routers, as shown in the next listing:

{{<cc>}}Redistributing the static default route{{</cc>}}
```
router ospf 1
 redistribute static metric 10
 default-information originate
!
interface Ethernet0/1
 ip ospf 1 area 0
```

{{<note>}}
OSPF will not announce the redistributed default route until you configure **default-information originate** within the OSPF process.
{{</note>}}

If no workstations are attached to the LAN between GW-A and GW-B, we’re finished; all routers attached to that LAN will get the default route pointing to the currently active gateway router through a dynamic routing protocol (Figure 4).

{{<figure src="/kb/Internet/MH_Redundancy/Redundant Multihoming_4.jpg" caption="Intra-site routing in a large site">}}

Intra-site routing with workstations attached to the same LAN as GW-A and GW-B is a bit more complex. You can usually configure only a single default gateway on the workstations, so you have to provide a dynamic switchover of the default gateway with a first-hop redundancy protocol (FHRP), for example, Virtual Router Redundancy Protocol (VRRP) or Hot Standby Router Protocol (HSRP). The configuration is straightforward since the **track** object that you can use to adjust the router’s HRSP priority based on the state of the upstream link has already been configured (see the following two listings; the only difference is the default HSRP priority, which is higher on GW A).

{{<cc>}}HSRP configuration on GW A{{</cc>}}
```
interface Ethernet0/1
 ip address 192.168.0.3 255.255.255.0
 standby 1 priority 100
 standby 1 ip 192.168.0.1
 standby 1 preempt
 standby 1 track 17 decrement 20
```

{{<cc>}}HSRP configuration on GW B{{</cc>}}
```
interface Ethernet0/1
 ip address 192.168.0.4 255.255.255.0
 standby 1 priority 90
 standby 1 ip 192.168.0.1
 standby 1 preempt
```
