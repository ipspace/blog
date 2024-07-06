---
comment: 'The fundamental principle underlying [OpenFlow](/series/openflow_101.html)
  and [Software Defined Networking](/series/sdn_101.html) (as defined by Open Networking
  Foundation) is the decoupling of control- and data plane, with data (forwarding)
  plane running in a networking device (switch or router) and control plane being
  implemented in a central controller, which controls numerous dumb devices. Let’s
  start with the basics: what are data, control and management planes in a network
  device?

  '
date: 2013-08-13 07:22:00+02:00
lastmod: 2020-11-18 15:42:00
openflow_101_tag: intro
series:
- openflow_101
series_weight: 300
tags:
- networking fundamentals
- OpenFlow
title: Management, Control, and Data Planes in Network Devices and Systems
url: /2013/08/management-control-and-data-planes-in.html
---
Every single network device (or a distributed system like [QFabric](/2011/09/qfabric-part-1-hardware-architecture.html)) has to perform at least three distinct activities:

-   Process the transit traffic (that’s why we buy them) in the **data plane**;
-   Figure out what’s going on around it with the **control plane** protocols;
-   Interact with its owner (or NMS) through the **management plane**.

Routers are used as a typical example in every text describing the three planes of operation, so let’s stick to this time-honored tradition:
<!--more-->
-   Interfaces, IP subnets and routing protocols are configured through **management plane protocols**, ranging from CLI to [NETCONF](/2012/06/netconf-expect-on-steroids.html) and the latest buzzword – northbound [RESTful API](/2012/08/why-is-restful-api-better-than-snmp.html);
-   Router runs **control plane** routing protocols (OSPF, EIGRP, BGP …) to discover adjacent devices and the overall network topology (or reachability information in case of distance/path vector protocols);
-   Router inserts the results of the control-plane protocols into [Routing Information Base (RIB) and Forwarding Information Base (FIB)](/2010/09/ribs-and-fibs.html). **Data plane** software or ASICs uses FIB structures to forward the transit traffic.
-   **Management plane** protocols like SNMP can be used to monitor the device operation, its performance, interface counters …

{{<figure src="DevicePlanes.png" caption="Management, Control, and Data Planes in a Router">}}

The management plane is pretty straightforward, so let’s focus on a few intricacies of the control and data planes.

We usually have routing protocols in mind when talking about **Control plane protocols**, but in reality the control plane protocols perform numerous other functions including:

-   Interface state management (PPP, LACP);
-   Connectivity management (BFD, CFM);
-   Adjacent device discovery (hello mechanisms present in most routing protocols, ES-IS, ARP, IPv6 ND, uPNP SSDP);
-   Topology or reachability information exchange (IP/IPv6 routing protocols, IS-IS in TRILL/SPB, STP);
-   Service provisioning (RSVP for IntServ or MPLS/TE, uPNP SOAP calls);

Data plane should be focused on forwarding packets but is commonly burdened by other activities:

-   NAT session creation and NAT table maintenance;
-   Neighbor address gleaning (example: [dynamic MAC address learning in bridging](/2010/07/bridging-and-routing-is-there.html), [IPv6 SAVI](/2013/03/ipv6-source-address-validation.html));
-   Netflow Accounting (sFlow is cheap compared to Netflow);
-   ACL logging;
-   Error signaling (ICMP).

Data plane forwarding is hopefully performed in dedicated hardware or in high-speed code (within the interrupt handler on low-end Cisco IOS routers), while the overhead activities usually happen on the device CPU, often in userspace processes – -[the switch from high-speed forwarding to user-mode processing is commonly called punting](/2013/02/process-fast-and-cef-switching-and.html).

{{<note warn>}}In [reactive](http://networkstatic.net/openflow-proactive-vs-reactive-flows/) OpenFlow architectures [a punting decision sends a packet all the way to the OpenFlow controller](/2013/03/controller-based-packet-forwarding-in.html).{{</note>}}

### Typical Architectures

The management and control planes are typically implemented in a CPU, while the data plane could be implemented in numerous ways:

* Optimized code running on the same CPU;
* Code running on a dedicated CPU core (typical for high-speed packet switching on Linux servers);
* Code running on linecard CPUs (example: Cisco 7200);
* Dedicated processors (sometimes called NPUs)
* Switching hardware (ASICs);
* Switching hardware on numerous linecards.

Based on the capabilities of the switching hardware, a device might run some simple time-critical control-plane protocols (example: BFD) in hardware or on NPUs.

### Processing of Inbound Control-Plane Packets

In most router implementations, the data plane receives and processes all inbound packets and selective forwards packets destined for the router (for example, SSH traffic or routing protocol updates) or packets that need special processing (for example, IP datagrams with IP options or IP datagrams that have exceeded their TTL) to the control plane.

{{<note info>}}Management ports on some devices, including data center switches, are connected directly to the control-plane CPU and thus bypass the switching ASIC. For more details read *[Building Secure Layer-2 Fabrics](/2020/10/building-secure-layer-2-fabric.html)*){{</note>}}

The control plane might pass outbound packets to the data plane, or use its own forwarding mechanisms to determine the outgoing interface and the next-hop router (for example, when using the local policy routing).

{{<figure src="ControlPlanePunting.png" caption="Processing of Inbound and Outbound Control-Plane Packets">}}

Regardless of the implementation details, it’s obvious the device CPU represents a significant bottleneck (in some cases the switch to CPU-based forwarding causes several magnitudes lower performance) – the main reason one has to rate-limit ACL logging and protect the device CPU with *Control Plane Protection* features.
