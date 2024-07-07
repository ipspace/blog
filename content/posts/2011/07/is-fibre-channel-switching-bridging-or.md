---
date: 2011-07-13 07:04:00+02:00
tags:
- data center
- SAN
title: Is Fibre Channel Switching Bridging or Routing?
url: /2011/07/is-fibre-channel-switching-bridging-or/
---
A comment left on my [dense-mode FCoE](/2011/06/beauties-of-dense-mode-fcoe/) post is a perfect example of the dangers of using vague, marketing-driven and ill-defined word like "switching". The author wrote: "*FC-SW is by no means routing... Fibre* *Channel is switching*." As [I explained in one of my previous posts](/2011/02/how-did-we-ever-get-into-this-switching/), switching can mean anything, from circuit-based activities to bridging, routing and even load balancing (I am positive some vendors claim their ~~load balancers~~ application delivery controllers  are L4-L7 switches), so let's see whether Fibre Channel "switching" is closer to bridging or routing.
<!--more-->
One should always start with the standards. The FC-SW-5 standard (Fibre Channel Switch Fabric) is quite explicit. Every FC switch has an *FC switching element* (Figure 2 in FC-SW-5) with four control-plane components: Fabric controller, Address manager, Path selector and *Router*. The *Switching characteristics* section (section 4.6 of FC-SW-5) is also extremely clear: an FC switch performs *path and circuit switching* and *frame routing*. FC devices (hosts and storage) typically use datagram service. Case closed. FC switching commonly used today is routing, loud and clear.

Next let's try to dig a bit deeper and compare what FC fabric does to what [bridges or routers typically do](/2010/07/bridging-and-routing-is-there/).

**Forwarding**. FC switches don't do blind bridge-like flooding of unknown addresses. They rely on explicit forwarding tables built by FSPF.

**Loop detection**. This one is trickier. The FC frame header has no hop count. I am positive the fabric reconfiguration mechanisms ensure there are no forwarding loops, but I simply didn't have the nerves to dig so deep into FC-SW-5.

**Forwarding tables**. FC switches use a routing protocol (FSPF) to build their forwarding tables.

**Addressing**. FC addresses are hierarchical, with the first 8 bytes indicating the switch (Domain ID). While this address structure limits the size of a single fabric (which can have at most 239 switches), there are provisions for inter-fabric routing.

**Spoofing**. Almost impossible in FC. Every device has to log into the fabric and it's trivial to implement RPF checks on F_ports as the host addresses are tied to physical ports.

**Fragmentation**. Not relevant. FC has hard-coded MTU size.

**Mixed media**. You can run FC over point-to-point fiber links, over Ethernet (FCoE), over IP (FCIP) and there's even [provision in FC-BB-5 for running it over MPLS](/2011/02/fcompls-attack-of-zombies/) (which luckily never resulted in an actual implementation).

**Host-to-router communication**. The FC end hosts can exchange numerous informational or error messages with the FC switches.

The only reason someone might claim FC is bridging is the lack of hop count (see above) and lack of distinct L2 and L3 addresses, but then you don't have them on PPP links either (you don't need L2 addresses on point-to-point links). I don't know enough about FC history, but I would guess they started with a simple flat access network, slowly evolved it into a routed network and tried to minimize the impact of the changes.

As for the second part of the same comment, "*A single flat switched network with 9,000+ ports is exactly what makes FC impressive*", I fail to be impressed by a routed network with very clear hierarchical addressing structure running single-area OSPF with 9000 hosts attached to it.
