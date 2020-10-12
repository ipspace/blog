---
title: "Building Secure Layer-2 Data Center Fabric with Cisco Nexus Switches"
# date: 2020-10-05 10:42:00
tags: [ data center, switching, design ]
draft: True
---
One of my readers is designing a layer-2-only data center fabric  (no SVI interfaces on switches) with stringent security requirements using Cisco Nexus switches, and he wondered whether a host connected to such a fabric could attack a switch, and whether it would be possible to reach the management network in that way.

> Do you think it's possible to reach the MANAGEMENT PLANE from the DATA PLANE? Is it valid to think that there is a potential attack vector that someone can compromise to source traffic from the front of the device (ASIC) through the PCI bus across the CPU to the across the PCI bus to the Platform Controller Hub through the I/O card to spew out the Management Port onto that out-of-band network?

My initial answer was "_of course there's always a conduit from the switching ASIC to the CPU, how would you handle STP/CDP/LLDP otherwise_". I also asked Lukas Krattiger for more details; here's what he sent me:
<!--more-->

---

A destination MAC address that is not programmed in the ASIC as pointing to a local interface will not be considered local and hence will not be directed to the control/management plane. In a layer-2 switch, there is no ARP/ND process enabled and hence IPO traffic to local DMAC will not be processed. There are, however,  specific DMACs that need to be processed to support STP, IGMP... These layer-2 protocols are specifically programmed in the switching ASIC and responded to, and yes, the response comes from the control plane which runs things like STP or IGMP snooping.

Looking a bit beyond layer-2-only networks: of course every reachable IP interface of a router or switch is an attack vector. The only question is: how are you going to prevent the attacks? In Nexus OS, the first step is that not-enabled functions are not started and hence no protocol ports are listening. Second is the hardening of the operating system and closing unnecessary ports. Third is the using ACLs to protect Telnet, SSH, SNMP, and other protocols that need to be answered local. Fourth, limit the amount of protocols to a minimum; for example BGP is TCP/179 and for sure we have to listen to this.

Finally, with regard to the out-of-band management network, the answer is NO. Our out-of-band management has VRF separation, this means we use a dedicated routing table and do not allow ANY control-plane protocol to run. You will see that you don’t have access to routing protocols over the out-of-band port. Further, we are reducing the functions to what the out-of-band portion actually can and need to support. For example HW telemetry that is streamed from the ASIC is not available via out-of-band as it would have to cross the CPU.
