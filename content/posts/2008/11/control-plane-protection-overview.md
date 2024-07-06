---
url: /2008/11/control-plane-protection-overview.html
title: "Control Plane Protection Overview"
date: "2008-11-12T06:57:00.003+01:00"
tags: [ switching,IP routing ]
lastmod: 2020-11-18 17:32:00
---
The *[control and management planes](/2013/08/management-control-and-data-planes-in.html)* in a network device run numerous mission-critical processes, including routing protocols and network management services (SNMP, telnet or SSH access to the router, web access to the router), and is thus the most vulnerable part of any network device.

A determined attacker can quickly overload the CPU of any router (or switch) with a targeted denial-of-service attack, either by sending IP packets that are propagated from the switching fabric (or interrupt code on software-only platforms) to the control plane processes or by targeting individual services running on the router. The situation is becoming worse with widespread use of high-speed hardware switching platforms that are connected to an underpowered CPU over a PCI bus; getting enough traffic to a network device to saturate the ASIC-to-CPU connection, or the CPU, is becoming trivial.
<!--more-->
The results of control plane CPU overload due to a denial-of-service attack could be disastrous: without adequate share of CPU and memory resources, the routing protocols cannot maintain sessions with adjacent routers, resulting in routing and packet forwarding disruptions. Likewise, attacks on individual control- or management-plane services could result in compromised network devices, impersonation attacks or denial-of-service attacks due to [incorrect routing information](/2011/11/ipv6-security-getting-bored-bru-airport.html) or routing instabilities.

The denial of service can target router-based processes (for example, Telnet server or OSPF routing protocol), control-plane mechanisms like ARP or IPv6 ND, or the shortcomings of data plane implementation that forces the control plane to handle parts of the switching load. For example, all IP datagrams with IP options are forwarded to the control plane unless you’ve the **ip options drop** global configuration option has been used.

Most modern network devices offer some form of _control plane protection_ -- filters and rate-limiters installed between the packet switching mechanisms, and the control-plane CPU

{{<figure src="ControlPlaneProtection.png" caption="Control-plane protection between switching ASIC and control plane CPU">}}

### Cisco IOS Control-Plane Protection Mechanisms

Cisco IOS gives you four categories of tools you can use to protect a Cisco router:

-   Inbound access lists control the traffic flow in the data plane. The access lists are commonly used to protect resources behind the router, but they are also very effective to protect the router itself.

You can use access lists to drop all traffic sent to the router’s IP addresses from untrusted interfaces.

-   Control Plane Policing (CoPP, available in IOS releases 12.2S, 12.3T and 12.4) and Control Plane Protection (CPPr, introduced in IOS release 12.4(4)T) limit the amount of traffic sent to the control plane, ensuring that the control plane CPU cannot be overloaded through a denial-of-service attack.
-   Management plane protection (introduced in IOS release 12.4(6)T) limits access to network management services.
-   Several IOS applications use per-application access lists to further limit their usage.

{{<figure src="CoPPMechanisms.png" caption="An overview of control plane protection mechanisms in Cisco IOS">}}

### Protection Granularity and Filtering Functionality

The inbound access lists offer you the greatest granularity, as you can apply them on individual interfaces (separating trusted and untrusted interfaces). They can inspect numerous fields in the IP, TCP or UDP packets, including source/destination addresses, IP protocols (TCP, UDP, ICMP, OSPF, EIGRP), port numbers TTL field and DSCP value.

Cisco IOS control plane policies can match source/destination addresses, but not on specific IP protocols (therefore you cannot rate-limit inbound OSPF or EIGRP traffic). They can match TCP and UDP ports, but not the TTL field.

Per-application access lists (for example, **access-class** configured on VTY **line** or globally-configured **ip http-server access-class**) are used to check the incoming application-level sessions. They can check the source address and source/destination port numbers, but not the destination address or any other values in the IP header.

{{<note warn>}}Per-application access lists are usually implemented in software. Their use in denial-of-service protection is therefore quite limited.{{</note>}}
