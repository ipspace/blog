---
date: 2022-09-20 07:55:00+00:00
evpn_tag: design
mlag_tag: design
series:
- mlag
tags:
- EVPN
- data center
- design
title: EVPN/VXLAN or Bridged Data Center Fabric?
---
An attendee in the [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course sent me an interesting dilemma:

> Some customers don’t like EVPN because of complexity (it is required knowledge BGP, symmetric/asymmetric IRB, ARP suppression, VRF, RT/RD, etc). They agree, that EVPN gives more stability and broadcast traffic optimization, but still, it will not save DC from broadcast storms, because protections methods are the same for both solutions (minimize L2 segments, storm-control).

We'll deal with the unnecessary EVPN-induced complexity some other time, today let's start with a few intro-level details.
<!--more-->
The ancient way of building data center fabrics was to deploy MLAG clusters at the leaf- and the spine layer, pretending the spine layer is a single "node", and running STP to prevent any potential forwarding loops. Core convergence relied on LACP, UDLD, and STP.

{{<figure src="/2022/09/fabric-bridging.jpg" caption="Traditional MLAG-based bridged fabric">}}

The currently-hip data center fabric design[^NF] starts with an IP network, adds VXLAN transport on top of that, and uses EVPN as the control plane[^BGP]. Core convergence relies on BFD, IP routing protocols and Fast Reroute (if needed).

{{<figure src="/2022/09/fabric-evpn.jpg" caption="EVPN/VXLAN-based data center fabric">}}

[^NF]: Now that all vendors apart from a few SPBM stalwarts [abandoned routed layer-2 fabrics](/2022/05/cisco-fabric-path-and-friends/).

[^BGP]: For extra-hipness, replace OSPF with EBGP and run IBGP EVPN sessions on top of EBGP-only underlay because you REALLY SHOULD design [your 4-node network](/2018/02/using-evpn-in-very-small-data-center/) in the [same way hyperscalers build their data centers](/2018/05/is-ospf-or-is-is-good-enough-for-my/).

Before digging into the details, it's worth noting that it's perfectly possible to build VXLAN-based fabrics without EVPN and the associated complexity. All you have to do is to configure static ingress replication lists, trading protocol complexity for configuration complexity. 

{{<figure src="/2022/09/fabric-vxlan-static.jpg" caption="VXLAN-based data center fabric with static ingress replication">}}

I'm not saying that's the recommended way of doing things, but it's a viable option usually not mentioned by the networking vendors[^NV]. Just keep in mind that EVPN and associated complexity is **not** a mandatory bit of VXLAN-based fabrics.

[^NV]: Vendors can't resist the urge to brag about the most-complex-possible design after investing so much into implementing a complex control plane protocol. Nobody wants you to use a simple setup that could be easily replicated on more affordable gear the next time you're upgrading your hardware.

{{<note info>}}I would also strongly recommend generating the ingress replication lists with an automation tool if you want to stay sane.{{</note>}}

### Which Design Should I Use?

I wouldn't think about building bridged fabric in 2022. MLAG remains a kludge[^BR] and I've seen too many data center meltdowns caused by MLAG bugs.

Furthermore, building a bridged fabric forces you to use MLAG on the spine layer (where bugs matter most), even if the end-hosts don't need link aggregation -- a highly debatable topic we covered in the [December 2021](https://my.ipspace.net/bin/list?id=Design#2021_12) session of the [Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic).

Without going into the details: you MIGHT need link aggregation on storage nodes and you PROBABLY SHOULD NOT use link aggregation on hypervisor hosts like VMware ESXi. Should you agree with this _best practice[^BP]_ you could build a VXLAN-based fabric without ever opening the Pandora box of MLAG complexity.

For more details, watch the _[Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)_ and _[EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)_ webinars. 

Want to kick the tires of the EVPN/VXLAN "beauty"? netlab release 1.3 added VXLAN and EVPN support for a half-dozen platforms.

[^BR]: So does bridging, but let's not go there

[^BP]: Best practice: a procedure that will cause the least harm (as compared to random ramblings and cut-and-paste of Google-delivered configuration snippets) when executed by people who don’t know what they’re doing.
