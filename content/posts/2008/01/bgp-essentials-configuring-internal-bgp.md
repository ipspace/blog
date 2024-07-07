---
date: 2008-01-22 10:02:00
tags:
- BGP
title: 'Configuring Internal BGP Sessions'
series: bgp-essentials
url: /2008/01/bgp-essentials-configuring-internal-bgp/
---
Internal BGP (IBGP) sessions (BGP sessions within your autonomous system) are identified by the neighbor's AS number being identical to your AS number. While the external BGP (EBGP) sessions are usually established between directly connected routers, IBGP sessions are expected to be configured across the network.

The current best practice is to configure IBGP sessions between the loopback interfaces of the BGP neighbors, ensuring that the TCP session between them (and the BGP adjacency using the TCP session) will not be disrupted after a physical link failure as long as there is an alternate path toward the adjacent router.
<!--more-->
To configure an IBGP session following that best practice on Cisco IOS, specify the neighbor's loopback address in all **neighbor** commands and use the **neighbor update-source** command to specify the source IP address of the TCP session. 

{{<note warn>}}Without the neighbor **update-source** configuration command, the TCP session will use the IP address of the outgoing physical interface and the neighbor will reject the incoming TCP SYN packet as it's not coming from a recognized BGP neighbor.{{</note>}}

### Sample Configuration

To configure IBGP session between R1 and R2 use the following configuration commands:

{{<cc>}}BGP configuration on R1{{</cc>}}
```
hostname R1
!
interface Loopback 0
 ip address 10.0.0.1
!
router bgp 65001
 neighbor 10.0.0.2 remote-as 65001
 neighbor 10.0.0.2 description R2 
 neighbor 10.0.0.2 update-source loopback 0
```

{{<cc>}}BGP configuration on R2{{</cc>}}
```
hostname R2
!
interface Loopback 0
 ip address 10.0.0.2
!
router bgp 65001
 neighbor 10.0.0.1 remote-as 65001
 neighbor 10.0.0.1 description R1
 neighbor 10.0.0.1 update-source loopback 0
```

