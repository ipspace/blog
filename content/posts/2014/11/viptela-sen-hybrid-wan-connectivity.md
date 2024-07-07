---
date: 2014-11-14 09:05:00+01:00
dmvpn_tag: other
media: http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_15-Viptela_Secure_Extensible_Network.mp3
tags:
- DMVPN
- podcast
- SDN
- WAN
- Software Gone Wild
title: 'Viptela SEN: Hybrid WAN Connectivity with an SDN Twist'
url: /2014/11/viptela-sen-hybrid-wan-connectivity/
---
Like many of us Khalid Raza wasted countless hours sitting in meetings discussing [hybrid WAN connectivity designs](http://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN) using a random combination of [DMVPN](http://www.ipspace.net/DMVPN), IPsec, PfR, and one or more routing protocols... and decided to try to create a better solution to the problem.

{{<note info>}}Viptela was acquired by Cisco not long after we recorded this podcast. I left the podcast online for historic reasons.{{</note>}}
<!--more-->
Viptela Secure Extensible Network (SEN) doesn't try to solve every networking problem ever encountered, which is why it's simpler to use in the use case it is designed to solve: multi-provider WAN connectivity.

Like everyone else these days, they decided to use an SDN controller, which gave them several advantages over traditional solutions:

-   Simple edge router configuration -- all an edge router (vEdge Router) has to do is to report its local connectivity (subnets, VLANs, local IP prefixes) to the controller and get the WAN connectivity information from it;
-   Simplified policy distribution -- the WAN policy is no longer configured on every WAN edge device, but distributed from the controller cluster;
-   Simple control plane -- SEN vEdge Routers still run traditional routing protocols (there's nothing wrong with using a technology that works well), but have a small set of adjacencies -- they talk with the controllers, not with the other routers. While this approach lacks [shared fate property](/2014/08/fate-sharing-in-ip-networks/) and thus complicates the data plane failure detection, it scales much better; the size of the WAN network is no longer limited by the CPU capabilities of the hub router (if you ever implemented large-scale DMVPN with Catalyst 6500 as the hub router you probably know what I'm talking about).

{{<jump>}}[Listen to the podcast](http://media.blubrry.com/ipspace/stream.ipspace.net/nuggets/podcast/Show_15-Viptela_Secure_Extensible_Network.mp3){{</jump>}}
