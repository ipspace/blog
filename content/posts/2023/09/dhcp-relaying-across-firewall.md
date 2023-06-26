---
title: "DHCP Relaying Across a Firewall"
date: 2023-09-23 11:36:00
tags: [ DHCP, firewalls ]
draft: True
---
Chinar Trivedi submitted the following comment to https://blog.ipspace.net/2023/05/dhcp-redundant-vrf-relay.html.

---

In actual production environments, if DHCP server is outside your fabric, then on border/service leafs the DHCP Server route will be learned via an edge firewall, and this will be the traffic flow:

DHCP Server IP X.X.X.X------&gt;Outside-VRF-Red(VRF-lite of Border Leaf)-------F/W Outside Zone-------&gt;Firewall (Does Inter-VRF routing)---------&gt;Inside-VRF-Green (EVPN-IP-VRF of Border Leaf now)-----Border Leaf--------&gt;Type-5-L3-EVPN Route within IP-VRF Green-------&gt;Access Leaf VTEP VRF Green------DHCP Client Y.Y.Y.Y (DHCP client is part of VRF Green)

1.  Curious in this entire DORA process and DHCP relaying, should the DHCP DORA messages ever be passing through a Firewall?
2.  If a Firewall has to definitely be in the path, will everything work hunky-dory the same way in the Inter-VRF DHCP Relaying, especially in EVPN DAG & Option 82 case?
3.  What's Ivan's recommendation?

thnx Chinar
