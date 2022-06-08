---
title: "Router Interfaces and Switch Ports"
# date: 2022-06-08 08:42:00
tags: [ IP routing, bridging, networking fundamentals ]
draft: True
---
Rough ideas:

* Routers had interfaces with MAC/IP addresses attached to IP routing table
* Bridges had ports attached to the bridging code (MAC table), single MAC address per box

Router interfaces had to be configured before they would be operational, and you had to specify what they were meant to do.

Bridge ports were enabled and started forwarding traffic.

### Introducing VLANs:

* For routers, VLAN is just a tag on an interface used to create a (virtual) subinterface
* Bridges perform per-VLAN MAC forwarding, and have VLAN filters on trunk ports or push/pop tag on access/native ports

### Combining routing and bridging

* Bridging on routers
* Concurrent routing and bridging (CRB)
* Integrated routing and bridging (IRB)

### Layer-3 Switches

* Bridge model (switchports and VLAN interfaces)
* Router model (VLAN subinterfaces and bridge groups)