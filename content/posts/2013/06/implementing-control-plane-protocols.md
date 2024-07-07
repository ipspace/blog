---
date: 2013-06-18 07:40:00+02:00
tags:
- OSPF
- SDN
- data center
- OpenFlow
- overlay networks
title: Implementing Control-Plane Protocols with OpenFlow
url: /2013/06/implementing-control-plane-protocols/
---
The true OpenFlow zealots would love you to believe that you can drop whatever you've been doing before and replace it with a clean-slate solution using dumbest (and cheapest) possible switches and OpenFlow controllers.

In real world, your shiny new network has to communicate with the outside world ... or you could take the approach most controller vendors did, decide to pretend STP is irrelevant, and ask people to configure static LAGs because you're also not supporting LACP.
<!--more-->
### Hybrid-mode OpenFlow with traditional control plane

If you're implementing [hybrid-mode OpenFlow](/2012/06/hybrid-openflow-brocade-way/), you'll probably rely on the traditional software running in the switches to handle the boring details of [control-plane protocols](/2013/08/management-control-and-data-planes-in/) and use OpenFlow only to add new functionality (example: [edge access lists](/2011/11/openflow-enterprise-use-cases/)).

Needless to say, this approach usually won't result in better forwarding behavior. For example, it would be hard to implement layer-2 multipathing in hybrid OpenFlow network if the switches rely on STP to detect and break the loops.

### OpenFlow-based control plane

In an OpenFlow-only network, the switches have no standalone control plane logic, and thus the OpenFlow controller (or a cluster of controllers) has to implement the control plane and control-plane protocols. This is the approach [Google used in their OpenFlow deployment](/2012/05/openflow-google-brilliant-but-not/) -- the OpenFlow controllers run IS-IS and BGP with the outside world.

OpenFlow protocol provides two messages the controllers can use to implement any control-plane protocol they wish:

-   The **Packet-out** message is used by the OpenFlow controller to send packets through any port of any controlled switch.
-   The **Packet-in** message is used to send messages from the switches to the OpenFlow controller. You could configure the switches to send all unknown packets to the controller, or set up flow matching entries (based on controller's MAC/IP address and/or TCP/UDP port numbers) to select only those packets the controller is truly interested in.

For example, you could write a very simple implementation of STP (similar to what Avaya is doing on their ERS-series switches when they run MLAG) where the OpenFlow controller would always pretend to be the root bridge and shut down any ports where inbound BPDUs would indicate someone else is the root bridge:

-   Get the list of ports with **Read State** message;
-   Send BPDUs through all the ports claiming the controller is the root bridge with very high priority;
-   Configure flow entries that match the multicast destination address used by STP and forward those packets to the controller;
-   Inspect incoming BPDUs, and shut down the port if the BPDU indicates someone else claims to be a root bridge.

### Summary

OpenFlow protocol allows you to implement any control-plane protocol you wish in the OpenFlow controller; if a controller does not implement the protocols you need in your data center, it's not due to lack of OpenFlow functionality, but due to other factors (fill in the blanks).

If the OpenFlow product you're interested in uses hybrid-mode OpenFlow (where the control plane resides in the traditional switch software) or uses OpenFlow to program overlay networks (example: [Nicira's NVP](/2012/02/nicira-uncloaked/)), you don't have to worry about its control-plane protocols.

If, however, someone tries to sell you software that's supposed to control your physical switches, and does not support the usual set of protocols you need to integrate the OpenFlow-controlled switches with the rest of your network (example: STP, LACP, LLDP on L2 and some routing protocol on L3), think twice. If you use the OpenFlow-controlled part of the network in an isolated fabric or [small-scale environment](/2012/03/openflow-perfect-tool-to-build-smb-data/), you probably don't care whether the new toy supports STP or OSPF; if you want to integrate it with the rest of your existing data center network, be very careful.

### More information

To find more about OpenFlow, watch our [OpenFlow Deep Dive](https://www.ipspace.net/OpenFlow_Deep_Dive) webinar; you might also be interested in *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)*.