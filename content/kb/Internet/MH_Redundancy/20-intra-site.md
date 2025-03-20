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
interface FastEthernet0/0
 ip ospf 1 area 0
```

{{<note>}}
OSPF will not announce the redistributed default route until you configure **default-information originate** within the OSPF process.
{{</note>}}

If there are no workstations attached to the LAN between GW-A and GW-B, we’re finished; all routers attached to that LAN will get the default route pointing to the currently-active gateway router through a dynamic routing protocol (Figure 4).

{{<figure src="Redundant Multihoming_4.jpg" caption="Intra-site routing in a large site">}}

Intra-site routing with workstations attached to the same LAN as GW-A and GW-B is a bit more complex. You can usually configure only a single default gateway on the workstations, so you have to provide dynamic switchover of the default gateway with Hot Standby Router Protocol (HSRP) or an equivalent (for example, Gateway Load Balancing Protocol; GLBP, or Virtual Router Redundancy Protocol; VRRP). The configuration is very simple, since the **track** objects that you can use to adjust the router’s HRSP priority based on the state of the upstream link have already been configured (see the next two listings; the only difference is the default HSRP priority, which is higher on GW A).

{{<note>}}
HSRP and VRRP address only the needs of primary/backup router scenarios, whereas GLBP supports outbound load balancing. As our design does not address load balancing toward the Internet, HSRP nicely fits the requirements.
{{</note>}}

{{<cc>}}HSRP configuration on GW A{{</cc>}}
```
interface FastEthernet0/0
 ip address 10.0.0.5 255.255.255.0
 standby 1 priority 95
 standby 1 ip 10.0.0.1
 standby 1 preempt
 standby 1 track 17 decrement 20
```

{{<cc>}}HSRP configuration on GW B{{</cc>}}
```
interface FastEthernet0/0
 ip address 10.0.0.6 255.255.255.0
 standby 1 ip 10.0.0.1
 standby 1 priority 90
 standby 1 preempt
 standby 1 track 17 decrement 20
```
