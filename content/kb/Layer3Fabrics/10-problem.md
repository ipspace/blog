---
kb_section: Layer3Fabrics
minimal_sidebar: true
title: The Problem
url: /kb/Layer3Fabrics/10-problem.html
---
In most small-to-medium-sized leaf-and-spine fabric deployments you’d want to have the servers redundantly connected to two leaf switches (also called *top-of-rack* or *ToR* switches) to reduce the impact of a leaf switch failure or software upgrade. Usually this requires a single IP subnet and thus a single VLAN spanning both leaf switches.

{{<figure src="Redundant-Connectivity-Basics.png" caption="Typical implementation of redundant server connections. Source: [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)">}}

{{<note info>}}Most of the diagrams in this section are taken straight from the [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar. That webinar explains the problem in great details; here’s just a quick summary.{{</note>}}

You could configure the server uplinks in active/standby mode, in active/active mode (example: vSphere load-based teaming), or bundle them in a link aggregation group (LAG, aka port channel). No solution is ideal; each one introduces its own set of complexities. For example, the LAG approach requires MLAG functionality on the two ToR switches.

{{<note info>}}We covered various server connectivity options in [Redundant Server-to-Network Connectivity](https://my.ipspace.net/bin/get/ExpressSample/Redundant%20Server-to-Network%20Connectivity.pdf?doccode=ExpressSample) ExpertExpress [case study](https://www.ipspace.net/ExpertExpress_Case_Studies).{{</note>}}

{{<figure src="Redundant-Connectivity-MLAG.png" caption="Server-to-fabric link aggregation with MLAG on leaf switches. Source: [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)">}}

{{<note warn>}}MLAG tends to be more brittle than simple VLAN stretching or IP routing. I have several customers who lost their data centers when an MLAG bug resulted in a forwarding loop.{{</note>}}

### Potential Solutions

In the ideal world, a data center fabric would be a simple leaf-and-spine layer-3 fabric with IP subnets bound to ToR switches, no inter-switch VLAN connectivity, and no inter-ToR-switch links… assuming the servers could use IP addresses from multiple subnets.

{{<figure src="Server-Two-Subnets.png" caption="Server residing in two subnets">}}

Alternatively, you could use fabric-based solutions to stretch the inter-ToR VLAN across the spine switches instead of using a dedicated inter-ToR-switch link. Several EVPN-based solutions and proprietary solutions like Cisco ACI or Extreme Networks’ SPB implementation can be used to implement this design.

{{<figure src="Multihoming-EVPN-ESI.png" caption="Multihoming with EVPN ESI. Source: [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)">}}

You could also use one of the _routing on IP addresses_ solutions to stretch a subnet across multiple leaf switches without stretching a VLAN[^1], for example Cumulus Linux' _redistribute ARP_[^2]. Obviously, this approach only works if the servers don't use anything else but unicast IP.

Finally, the servers could use a routing protocol to advertise their loopback addresses to both ToR switches. This approach works really well for servers, but not for clients. The proof is left as an exercise for the reader; if you feel like you found a good answer do [send me an email](https://www.ipspace.net/Contact#Tech).

In the rest of this document we’ll focus primarily on the challenges of using server- or client IP addresses from multiple subnets.

[^1]: Rearchitecting layer-3-only networks,
https://blog.ipspace.net/2015/04/rearchitecting-l3-only-networks.html

[^2]: Layer-3-Only Data Center Networks with Cumulus Linux on Software Gone Wild, https://blog.ipspace.net/2015/08/layer-3-only-data-center-networks-with.html