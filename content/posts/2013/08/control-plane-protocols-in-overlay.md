---
date: 2013-08-14 07:38:00+02:00
tags:
- data center
- overlay networks
- virtualization
title: Control Plane Protocols in Overlay Virtual Networks
url: /2013/08/control-plane-protocols-in-overlay/
---
Multiple overlay network encapsulations are nothing more than a [major inconvenience](/2013/08/s1600-DayLifeOverlayPacket_6.png) (and religious wars based on individual bit fields close to meaningless) for anyone trying to support more than one overlay virtual networking technology (just ask F5 or Arista).

The key differentiator between scalable and not-so-very-scalable architectures and technologies is the [control plane](/2013/08/management-control-and-data-planes-in/) -- the mechanism that maps (at the very minimum) remote VM MAC address into a transport network IP address of the target hypervisor (see [A Day in a Life of an Overlaid Virtual Packet](/2013/08/a-day-in-life-of-overlaid-virtual-packet/) for more details).
<!--more-->
Overlay virtual networking vendors chose a plethora of solutions to solve this problem, ranging from Ethernet-like dynamic MAC address learning to complex protocols like MP-BGP. Here's an overview of what they're doing:

{{<note warn>}}This blog post was written in 2013. In the meantime, most vendors implemented a proper control plane for their overlay networking solutions, either using EVPN or a proprietary technology. Also, most of the products mentioned in the blog post are obsolete, and the startups worth acquiring have been acquired.{{</note>}}

**The original VXLAN** as implemented by Cisco's Nexus 1000V, VMware's vCNS release 5.1, Arista EOS, and F5 BIG-IP TMOS release 11.4 has *no control plane*. It relies on transport network IP multicast to [flood BUM traffic](/2012/05/transparent-bridging-aka-l2-switching/) and [uses Ethernet-like MAC address learning to build mapping between virtual network MAC address and transport network IP addresses](/2011/12/vxlan-ip-multicast-openflow-and-control/).

**Unicast VXLAN** as [implemented in Cisco's Nexus 1000V release 4.2(1)SV2(2.1)](/2013/07/unicast-only-vxlan-finally-shipping/) has something that resembles a control plane. VSM distributes segment-to-VTEP mappings to VEMs to replace IP multicast with headend unicast replication, but the VEMs still use dynamic MAC learning.

**VXLAN MAC distribution mode** in Nexus 1000V is a proper control plane implementation in which the VSM distributes VM-MAC-to-VTEP-IP information to VEMs. Unfortunately it seems to be based on a proprietary protocol, so it won't work with hardware gateways from Arista or F5.

**Hyper-V Network Virtualization** [uses PowerShell cmdlets](/2012/12/hyper-v-network-virtualization-wnvnvgre/) to configure VM-MAC-to-transport-IP mappings, virtual network ARP tables and virtual network IP routing tables. The same cmdlets can be implemented by hardware vendors to configure NVGRE gateways.

**Nicira NVP** (part of VMware NSX) uses OpenFlow to install forwarding entries in the hypervisor switches and [Open vSwitch Database Management Protocol](http://tools.ietf.org/html/draft-pfaff-ovsdb-proto-02) to configure the hypervisor switches. NVP uses OpenFlow to implement L2 forwarding and VM NIC reflexive ACLs (L3 forwarding uses another agent in every hypervisor host).

**Midokura Midonet** doesn't have a central controller or control-plane protocols. Midonet agents residing in individual hypervisors use [shared database to store control- and data-plane state](/2012/08/midokuras-midonet-layer-2-4-virtual/).

**Contrail** (now [Juniper JunosV Contrail](http://www.juniper.net/us/en/dm/junos-v-contrail/)) seems to be using MP-BGP to pass MPLS/VPN information between controllers and [XMPP to connect hypervisor switches to the controllers](http://tools.ietf.org/html/draft-ietf-l3vpn-end-system).

**IBM SDN-VE** (SDN for Virtual Environments) uses a hierarchy of controllers and appliances to implement NVP-like control plane for L2 and L3 forwarding using VXLAN encapsulation. I wasn't able to figure out what protocols they use from their whitepapers and user guides.

**Nuage Networks** is using \$Something and **PLUMgrid** is using \$SomethingElse. I will tell you what the values of these two variables are when I manage to get product documentation from these vendors. PowerPoint and whitepapers clearly get way more attention in the startup world than something an actual user might find useful when deploying the product.
