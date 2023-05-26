---
url: /2010/01/ospf-flooding-filters-in-hub-and-spoke.html
title: "OSPF flooding filters in hub-and-spoke environment"
date: "2010-01-07T06:48:00.002+01:00"
tags: [ OSPF,WAN ]
---
Almost all articles describing large-scale DMVPN in combination with OSPF use the “magic” **ip ospf database-filter all out** command on the hub routers to minimize the OSPF traffic traversing the DMVPN part of the network.

NOTE: The same trick can be used in any hub-and-spoke network, including P2MP Carrier Ethernet networks.

What these articles usually fail to tell you is the true impact of this command: it stops all OSPF flooding from hub router. The spoke routers receive no OSPF information whatsoever; to establish connectivity to the network core, you have to use static default routes on the spoke routers.

{{<jump>}}[More details](/kb/tag/OSPF/OSPF_Flood_Reduction_Hub_Spoke.html){{</jump>}}
