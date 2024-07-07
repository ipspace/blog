---
date: 2022-09-14 07:31:00+00:00
series:
- if_port
tags:
- switching
- IP routing
- networking fundamentals
title: VLAN Interfaces and Subinterfaces
---
Early bridges [implemented a single bridging domain across all ports](/2022/09/interfaces-ports/). Within a few years, we got multiple bridging domains within a single device (including [bridging implementation in Cisco IOS](/2022/09/routers-bridges-crb-irb/)). The capability to have multiple bridging domains stretched across several devices was still missing... until the modern-day Pandora opened the VLAN box and forever swamped us in the complexities of large-scale bridging.
<!--more-->
VLANs were first introduced in bridges and followed the usual "_keep things simple, just plug it in and pray_" mentality. You could assign a port to a VLAN (access port) or filter VLANs on a trunk port. Layer-3 switches added VLAN interfaces (a logical interface representing the whole bridging domain), resulting in the configuration model you get on modern layer-3 switches when configuring `switchport` on an interface.

The first router-focused VLAN use case was _router on a stick_ -- a device with a single physical interface that had to forward network-layer packets between VLANs. Routers always performed packet forwarding between interfaces; the typical device configuration model followed that paradigm and introduced VLAN subinterfaces -- a logical interface receiving all packets belonging to a single VLAN that _arrive through the parent physical interface_.

{{<note info>}}It's worth noting that the switch VLAN interface behaves like an umbrella interface for a set of (VLAN slices of) physical interfaces. In contrast, the router VLAN subinterface behaves like a child interface of a physical interface.{{</note>}}

Linux networking supports both concepts. The VLAN interface used in the switch configuration model maps pretty well into a Linux bridge (a virtual interface-like object to which other interfaces are connected). The VLAN subinterface used in router configurations maps into a Linux VLAN interface (a child interface of a particular physical interface).

The different implementations of these configuration models resulted in hilarious headaches:

* Layer-3 switches like Arista EOS or Cisco Nexus OS have a split personality -- they can behave like a router (with VLAN subinterfaces) or a switch (with VLAN interfaces) simultaneously, but you cannot combine the two on the same physical interface.
* You would configure Cisco routers running Cisco IOS completely differently than Cisco switches running the same operating system.
* Cisco IOS routers still use the ancient bridge groups and Bridge Virtual Interface. To implement VLAN bridging, you have to create VLAN subinterfaces and assign them to a bridge group.
* To ensure you remain thoroughly confused, Cisco IOS XE uses Bridge Domain Interfaces instead of Bridge Virtual Interfaces.

What else would you expect to get from an industry that firmly believes in recycling old code and _doing more with less_?