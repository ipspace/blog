---
date: 2009-05-06 09:02:00.001000+02:00
tags:
- MPLS
- switching
- LAN
title: VPLS Is Not Aspirin
url: /2009/05/vpls-is-not-aspirin/
---
If you're old enough to remember the days when *switches* were still called *bridges* and were used to connect multiple sites over WAN links, you've probably experienced interesting network meltdowns caused by a single malfunctioning network interface card. Some of you might have had the "privilege" of encountering another somewhat failed attempt at WAN bridging: ATM LAN Emulation (LANE) service (not to mention the "famous" Catalyst 3000 switches with LANE uplink).

It looks like some people decided not to learn from others' mistakes: years later the bridging-over-WAN idea has resurfaced in the VPLS clothes. While there are legitimate reasons why you'd want to have a bridged connection across the Service Provider network, VPLS should not be used to connect regular remote sites to a central site without on-site routers, as I explained in the _VPLS: A secure LAN cloud solution for some, not all_ article I wrote in 2009 (republished below).
<!--more-->
{{<note info>}}I've learned a few things since I wrote that article; you might want to watch the [Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service) webinar for more details.{{</note>}}

## VPLS: Don’t Get Carried Away

VPLS is one of the recent buzzwords entering the Service Provider acronym crowd. Not surprisingly, some vendor marketing departments are touting it as the latest VPN panacea and there are Service Providers believing the story and offering VPLS in environments where it can do way more harm than good.

Security experts have already realized the “opportunities” (read: attack vectors) offered by an enterprise-wide LAN cloud and demonstrated practical VPLS-based attacks. It’s thus vital that you understand the VPLS advantages, limitations and threats in order to be able to offer a range of secure services matching your customer expectations.

### The Evolution

When the emerging Service Provider networking vendors tried to replace “old-world” SP technologies (Frame Relay and ATM) with “new-world” ones (IP), they focused on the majority of the IP-based market: the IP-based virtual private networks (VPN), which were very successfully implemented with the MPLS VPN technology.

However, the MPLS VPN technology did not fit all the needs of the incumbent Service Providers, who had to transport legacy traffic (for example, ATM-based video surveillance) across their infrastructure. The early adopters of MPLS VPN have also discovered that even though IP was ubiquitous at the time MPLS VPN was introduced, large enterprises still had to support small but significant amount of non-IP traffic. Even worse, some IP-based applications (including server clustering in disaster recovery scenarios) required transparent LAN communication.

The networking vendors obviously tried to cover all the SP needs and introduced the technologies that enabled point-to-point transport of any traffic across the SP infrastructure: AToM (Any Transport over MPLS) and L2TPv3 (Layer 2 Tunneling Protocol version 3). These point-to-point offerings allowed the SPs to create pseudo-wires carrying Ethernet, ATM or Frame Relay data across their MPLS or IP infrastructure, addressing the legacy needs of the enterprise customers.

With all the building blocks in place, it was inevitable that someone would try to replicate the Local Area Network Emulation (LANE) idea from the ATM world and build a technology that would dynamically create MPLS pseudowires to offer any-to-any bridged LAN service … and thus VPLS was born.

### What is VPLS?

VPLS is a technology that provides any-to-any bridged Ethernet transport between a number of customer sites across a Service Provider infrastructure. All the sites (of the same VPN) connected to a VPLS service offering belong to the same LAN (bridging domain) and the frames sent by workstations attached to the site LANs are forwarded according to the 802.1 bridging standards. VPLS offers none of the layer-3 security or isolation features offered by layer-3 VPN technologies (including MPLS VPN and IPSec).

### The VPLS Threats

The networking industry made numerous attempts to implement layer-2 switching (formerly known as *bridging*) across lower-speed WAN networks. All these attempts, including WAN bridges, brouters (WAN bridges with limited routing functionality) and ATM-based LANE have failed due to the inherent limitations of bridging. As I explained numerous times, “the world is not flat, and Layer 2 services cannot cover the needs of an entire network”.

A layer-2 end-to-end solution (including VPLS) has to permit every workstation to communicate with every other workstation in the extended LAN or send Ethernet packets to *all* workstations connected to the same bridging domain. VPLS thus provides no inter-site isolation:

* A single workstation can saturate the WAN links of all sites connected to the VPLS service.
* An intruder gaining access to a workstation on one site can try layer-2 penetration techniques on all workstations and servers connected to the VPLS cloud.
* VPLS-based services cannot implement traffic filters, as these filters would violate the “transparent LAN” principle.

With these threats in mind, it’s easy to see that you should offer VPLS services only to the customers actually requiring multi-site transparent LAN solution, not to everyone asking about a simple VPN service.

### VPLS Is a Perfect Fit For

If your customer has applications that use non-IP protocols (including legacy Microsoft or AppleTalk networks), VPLS is the best alternative as long as the customer understands its security implications. To implement a secure solution on top of a VPLS backbone, each customer site should use a router to connect to the VPLS backbone. Obviously, you should try to offer managed router service to achieve the maximum value add.

VPLS is also a perfect fit for disaster recovery scenarios, where you need to create an impression that servers located at different sites belong to the same LAN.

### Don’t Ever Offer VPLS To

When a customer with lack of IT knowledge approaches your sales team asking for a VPN solution linking numerous remote sites, don’t sell them VPLS, they probably need a managed on-site router solution. It’s true that it would be faster and easier to implement VPLS (more so since the customer is not networking-savvy), but after the first major incident (and it will happen eventually), you’ll be faced with an extremely unhappy customer and a tarnished reputation.
