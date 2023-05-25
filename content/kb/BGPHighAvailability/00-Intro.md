---
index: true
kb_section: BGPHighAvailability
minimal_sidebar: true
title: BGP as High-Availability Protocol
toc_title: Overview
url: /kb/BGPHighAvailability/
---
It seems incredible how often networking engineers still discuss Border Gateway Protocol (BGP), and how often it's still the best tool for the job. In this article I'll describe a solution I designed and developed for enterprise data centers: using BGP in data centers to manage high availability (HA) with firewalls, hosts and even Network Function Virtualization (NFV) chains.

## Why BGP?

BGP is used here as a solution simply because it is the protocol to which the design of the various data centers of any dimension are converging on, especially with the increasing adoption of IP fabrics and overlays. I do not want to touch on a [topic already widely discussed in this site](https://www.ipspace.net/Data_Center_BGP) - using BGP to build data center transport network (underlay) - but will focus on overlay, where we are witnessing a convergence towards EVPN. In those scenarios using BGP as control-plane allows a native integration with type-5 routes ([more information for those who want to go deep on EVPN](https://www.ipspace.net/EVPN_Technical_Deep_Dive). As BGP is available and widely supported in the majority of network devices, it therefore allows Enterprises to obtain a highly integrated and uniform solution.

I started by using BGP to monitor and manage high availability of firewall clusters. Here is a high-level network diagram to help you understand the focus of this scenario:

{{<figure src="bgp-for-HA-00.png" caption="Network diagram">}}

Let's briefly analyze the solution.

First of all, the use of BGP imposes a full Layer-3 (L3) solution. The two firewall nodes are connected to routed interfaces in different subnets and require the use of separated L3 network on the border leaf and on external routers. This overcomes the typical solutions adopted in enterprise networks, just based on firewall clusters with static routing and some sort of First Hop Redundancy Protocol (FHRP) that also relays on layer-2 (L2) connectivity between the two members for proper HA operation.

With the proposed design, hosts cannot directly use the pair of firewalls as a default gateway, so it is mandatory to delegate all L3 functions to the fabric, where functionality like anycast gateway will result in a completely distributed routing and switching environment. Moreover, this guarantees a future expansion of this security zone with addition of further subnets without major interventions.

Like most high-availability firewall clusters, the two members operate in an active/standby configuration, but in the proposed solution, the active node is elected by BGP path selection. BGP is also responsible for a uniform convergence between all the six devices involved, with the purpose to avoid asymmetric traffic flow, typically not well accepted by firewalls.

In the case of predominantly HTTP traffic, it is not necessary to have sessions persistence between the nodes. In the case of failover, the end-to-end recovery is unnoticeable, however in many enterprise scenarios, a state-full failover is still expected. Most firewall vendors provide solutions for this with either session alignment on completely disjoined firewall nodes or Active/Active clustering solutions with unaligned and independent routing through the members. The desired Active/Backup device role is then implemented with a routing protocol or a pair of load balancers.

## Advantages of Using BGP

What are the advantages introduced by BGP in this this solution? In addition to the required L3 separation described above, there are other advantages:

-   The availability of the entire system is not tied to the state of the interfaces or link or the failure of some tracking pings. It is done through a complete BGP state monitoring of next-(and next)-hop, and in the case of EVPN also, most of the control-plane it is constantly checked.
-   The traffic flow through the firewall nodes is externally controlled by routing and orchestrated within all the involved devices, allowing controlled maintenance procedures, independent node upgrades and rollback capability without downtime, which is extremely useful for always-on systems.

But be careful, BGP must be used exclusively for HA. This means that it must not allow modifications to the topology, but only verification of the reachability through the firewall. For the sceptics, conservatives or extremely cautious, it is also possible to use only static routing on firewalls and configure a multi-hop BGP sessions between external routers and leafs, passing through the firewall, as illustrated below:

{{<figure src="bgp-for-HA-01.png" caption="Running BGP Across a Firewall">}}

In the next part of this article we'll discuss BGP configuration and the associated routing policies.
