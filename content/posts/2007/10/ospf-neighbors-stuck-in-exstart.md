---
date: 2007-10-24 07:06:00+02:00
ospf_tag: adj
tags:
- OSPF
title: OSPF Neighbors Stuck in EXSTART
url: /2007/10/ospf-neighbors-stuck-in-exstart/
---
This problem is rare but tantalizing enough to warrant mentioning: OSPF neighbors are forever stuck in the EXSTART state (occasionally going DOWN and back to EXSTART).

{{<note>}}I've stumbled across it accidentally in my lab and have luckily seen it before, so I knew immediately what it was.{{</note>}}
<!--more-->
The moment you start suspecting that something might be wrong with the OSPF adjacencies and use **debug ip ospf adj** command, the problem becomes obvious: the Database Description packet contains an *Interface MTU* field and if the value received from the neighbor is higher than the [IP MTU configured on the inbound interface](/2007/10/tale-of-three-mtus/), the DBD packet is rejected (section 10.6 of the [RFC 2328](http://www.faqs.org/rfcs/rfc2328.html)). The router with the lower MTU complains that "*Nbr x.x.x.x has larger interface MTU*"; the other router moans about protocol violations (*First DBD and we are not SLAVE*).

As always, there are two ways to solve this problem:

-   The correct one: fix the MTU issues;
-   The other one: disable MTU checks with the **ip ospf mtu-ignore** interface configuration command (which might be OK if the hardware can receive oversized packets and the router is not using fixed-size input buffers).
