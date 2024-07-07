---
date: 2008-08-01 07:00:00+02:00
ospf_tag: config
tags:
- OSPF
- MPLS VPN
title: OSPF in a VRF Requires a Box-Unique Router ID
url: /2008/08/ospf-in-vrf-requires-box-unique-router/
---
It's obvious why two routers in the same OSPF domain cannot have the same router ID. However, requiring unique router IDs on OSPF processes running in different VRFs is probably too harsh, even though it does prevent confusion if two VRFs ever get connected through a customer site. Anyhow, if you have overlapping IP addresses on loopback interfaces in *different VRFs*, OSPF process might not start.
<!--more-->
Here's a short example: two VRFs have loopback interfaces with the same IP address. Perfectly legal setup from the MPLS/VPN perspective.

``` code
c7200#show ip vrf interfaces
Interface    IP-Address   VRF            Protocol
Lo1003       10.0.0.1     EIGRP_OSPF     up
Lo1001       10.0.0.1     OSPF_1         up
```

However, when you try configuring the second OSPF process, it fails to start as it cannot get a box-unique router ID. You have to enter a different router ID manually.

``` code
c7200#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
c7200(config)#router ospf 1 vrf OSPF_1
c7200(config-router)#network 0.0.0.0 255.255.255.255 area 0
c7200(config-router)#exit
c7200(config)#router ospf 3 vrf EIGRP_OSPF
%OSPF-4-NORTRID: OSPF process 3 cannot pick a router-id.
  Please configure manually or bring up an interface with an ip address.
c7200(config-router)#router-id 10.0.0.2
```
