---
date: 2009-05-29 06:33:00+02:00
eigrp_tag: deploy
lastmod: 2020-12-29 09:34:00
tags:
- OSPF
- EIGRP
- RIP
- BGP
- MPLS VPN
title: Limitations of VRF Routing Protocols on Cisco IOS
url: /2009/05/vrf-routing-process-limitations.html
---
Cisco IOS allows up to 32 routing protocols contributing routes into a routing table (two of them are always *connected* and *static*). The limitation applies to the global routing table as well as to each individual VRF; the architectural reason for the limit is a 32-bit mask that's used in Cisco IOS to mark individual routing protocols. The routing protocol ID (as displayed by the **show ip protocol summary** command) is thus limited to values 0 to 31. With value 0 being reserved for connected routes and value 1 for static routes, 30 values are left to number the routing protocols.

Due to the implementation details of Cisco IOS, the BGP, RIP and each EIGRP routing process consume routing protocol ID in all VRFs (regardless of whether they are used or not). You can view the IDs of individual routing protocols with the **show ip protocol \[vrf *name*\] summary** command.
<!--more-->
{{<note info>}}VRF instances of an EIGRP process can use a different EIGRP autonomous system number. You don’t have to configure multiple EIGRP processes just to support different AS numbers used by MPLS VPN customers.{{</note>}}

OSPF routing process consumes a routing protocol ID only in the VRF in which it’s configured; however, due to the router-wide protocol ID sharing of the other three routing protocols, the actual number of OSPF processes in a VRF could be significantly less than 30.

Although OSPF processes can reuse the same routing protocol ID in different VRFs, they nonetheless start separate IOS processes. Likewise, an EIGRP routing protocol starts per-VRF processes for each VRF address family configured in the EIGRP process. The routing protocol ID assignment and the number of processes used by each routing protocol is summarized below:

**BGP**
* A single routing protocol ID is used in all VRFs.
* A single set of BGP processes is started regardless of the number of address families configured within **router bgp**.
* All BGP instances use the same AS number.

**RIP**
* A single routing protocol ID is used in all VRFs.
* A single set of RIP processes is started regardless of the number of address families configured within **router rip**.

**EIGRP**
* A unique routing protocol ID is used in all VRFs for each **router eigrp** configuration command.
* An *IP-EIGRP Router* process is started for each **router eigrp** configuration command.
* Two processes (*IP-EIGRP: PDM* and *IP-EIGRP: HELLO*) are started for each address family (including global IP routing) that has **network** statement configured.

**OSPF**
* OSPF router configured with **router ospf vrf** configuration command uses the first available protocol ID within the VRF.
* Two processes (*OSPF-X Hello* and *OSPF-X Router*) are started for each **router ospf** instance.