---
date: 2011-10-11T06:17:00.000+02:00
tags:
- SDN
- data center
- OpenFlow
- virtualization
title: What Is OpenFlow (Part 2)?
url: /2011/10/what-is-openflow-part-2.html
---
Got this set of questions from a CCIE pondering emerging technologies that could be of potential use in his data center:

> I don’t think OpenFlow is clearly defined yet. Is it a protocol? A model for Control plane – Forwarding plane FP interaction? An abstraction of the forwarding-plane? An automation technology? Is it a virtualization technology? I don’t think there is consensus on these things yet.

OpenFlow is [very well defined](https://blog.ipspace.net/2011/04/what-is-openflow.html). It’s a [control plane (controller) – data plane (switch)](/2013/08/management-control-and-data-planes-in.html) protocol that allows control plane to:
<!--more-->
-   Modify forwarding entries in the data plane;
-   Send control protocol (or data) packets through any port of any controlled data-plane devices;
-   Receive (and process) packets that cannot be handled by the data plane forwarding rules. These packets could be control-plane protocol packets (for example, LLDP) or user data packets that need special processing.

As part of the protocol, OpenFlow defines abstract data plane structures (forwarding table entries) that have to be implemented by OpenFlow-compliant forwarding devices (switches).

**Is it an abstraction of the forwarding plane?** Yes, as far as it defines data structures that can be used in OpenFlow messages to update data plane forwarding structures.

**Is it an automation technology?** No, but it can be used to automate the network deployments. Imagine a cluster of OpenFlow controllers with shared configuration rules that use packet carrying capabilities of OpenFlow protocol to discover network topology (using LLDP or a similar protocol), build a shared topology map of the network, and use it to download forwarding entries into the controlled data planes (switches). Such a setup would definitely automate new device provisioning in a large-scale network.

Alternatively, you could use OpenFlow to create additional forwarding (actually packet dropping) entries in access switches or wireless access points deployed throughout your network, resulting in a scalable multi-vendor ACL solution.

**Is it a virtualization technology?** Of course not. However, its data structures can be used to perform MAC address, IP address or MPLS label lookup and push user packets into VLANs (or push additional VLAN tags to implement Q-in-Q) or MPLS-labeled frames, so you can implement most commonly used virtualization techniques (VLANs, Q-in-Q VLANs, L2 MPLS-based VPNs or L3 MPLS-based VPNs) with it.

There’s no reason you couldn’t control [soft switch](https://blog.ipspace.net/2011/08/soft-switching-might-not-scale-but-we.html) (embedded in the hypervisor) with OpenFlow. An open-source hypervisor switch implementation ([Open vSwitch](http://openvswitch.org/)) that has “[many extensions for virtualization](http://openvswitch.org/features/)” is already available and can be used with Xen/XenServer (it’s the default networking stack in XenServer 6.0) or KVM.

I’m positive the list of Open vSwitch extensions is hidden somewhere in its somewhat cryptic documentation (or you could try to find them in the source code), but the [list of OpenFlow 1.2 proposals](http://www.openflow.org/wk/index.php/OpenFlow_1_2_proposal) implemented by Open vSwitch or sponsored by Nicira should give you some clues:

-   IPv6 matching (cool, finally IPv6 support) with IPv6 header rewrite (so they must be aiming at L3 hypervisor switch ... even cooler);
-   Virtual Port Tunnel configuration protocol and GRE/L3 tunnel support. Obviously they’re developing a VXLAN competitor or even IP-over-IP solution.
-   Controller master/slave switch. A must for resilient large-scale solutions.

**Summary**: OpenFlow is like C++. You can use it to implement all sorts of interesting solutions, but it’s just a tool.

#### More information

Start with [What is OpenFlow](https://blog.ipspace.net/2011/04/what-is-openflow.html), and then check out these webinars:

* [OpenFlow Deep Dive](https://www.ipspace.net/OpenFlow_Deep_Dive)
* [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics)
* [Introduction to Virtualized Networking](https://www.ipspace.net/Introduction_to_Virtualized_Networking)

You get all of them with the [yearly subscription](http://www.ipspace.net/Subscription).
