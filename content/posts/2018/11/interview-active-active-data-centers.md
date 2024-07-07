---
date: 2018-11-29 12:50:00+01:00
evpn_tag: intro
series_title: Active-Active Data Centers with VXLAN and EVPN
tags:
- VXLAN
- data center
- EVPN
title: 'Interview: Active-Active Data Centers With VXLAN and EVPN'
url: /2018/11/interview-active-active-data-centers/
---
Christoph Jaggi asked me a few questions about using VXLAN with EVPN to build data center fabrics and interconnects (including active/active data centers). The German version [was published on Inside-IT](https://www.inside-it.ch/articles/53019); here's the English version.

He started with an obvious one:

> What is an active-active data center, and why would I want to use it?

Numerous organizations have multiple data centers for load sharing or disaster recovery purposes. They could use one of their data centers and have the other(s) as warm or cold standby (active/backup setup) or use all data centers at the same time (active/active).
<!--more-->
It's also possible to have a hybrid architecture where a subset of workloads runs in each data center, but none runs in multiple data centers simultaneously. Data centers are active/standby from the workload perspective (simplifying the application architecture or infrastructure requirements) but still fully utilized.

> What is VXLAN, and what is EVPN? Are they independent of each other, or do they always come as a combination?

VXLAN is a simple data plane Ethernet-over-IP encapsulation scheme that enables us to tunnel Ethernet traffic across IP networks. It's commonly used to implement overlay virtual networking in large-scale data center environments and private- and public clouds.

EVPN is the control plane for layer-2 and layer-3 VPNs. It's similar to the well-known MPLS/VPN control plane, with added support for layer-2 (MAC) addresses, layer-3 (IPv4 and IPv6) addresses, and IPv4/IPv6 prefixes.

VXLAN can be used without a control plane, and EVPN works with numerous data plane encapsulations, including VXLAN and MPLS. Running VXLAN with EVPN is just the most popular combination.

> What benefits does EVPN offer that might not be achieved when using a straight Ethernet underlay without additional VXLAN overlay?

Traditional Ethernet solutions have two challenges: stability (due to spanning tree protocol challenges) and scalability (every switch has to know about every MAC address in the network).

VXLAN (but also VPLS, PBB, TRILL, SPB...) improves scalability - customer MAC addresses are not visible in the transport core.

Compared to most other solutions, VXLAN also improves network stability, as the core network uses well-tested IP transport and IP routing protocols.

EVPN is the icing on the cake. It improves VXLAN or MPLS deployments by replacing the dynamic MAC address learning used in traditional Ethernet networks with a deterministic control-plane protocol tested across the global Internet (BGP).

> What are the limitations and disadvantages of using VXLAN and EVPN?

Implementing VXLAN on hardware devices is still more expensive than implementing simple Ethernet switching or 802.1ad (Q-in-Q). Therefore, hardware supporting VXLAN is more expensive than simpler switching hardware.

EVPN is a complex control-plane protocol based on BGP, making it harder to understand and implement than simpler VLAN-based solutions.

> Which vendors offer VXLAN and EVPN support? Are the implementations fully interoperable?

Every single data center switching vendor (including Arista, Cisco, Cumulus, Extreme, and Juniper) has dropped whatever proprietary solution they were praising in the past (including FabricPath, DFA, VCS Fabric, IRF...) and implemented VXLAN encapsulation and EVPN control plane.

Unfortunately, EVPN has many options, and vendors implemented different subsets of those options, resulting in what I call _SIP of virtual networking_ (have you ever tried to get SIP working between VoIP products of different vendors?). While vendors claim their products interoperate (and participate in testing events to prove it), there are still many ways things can go wrong.

For example, the vendors can't agree on simple things like [what the best routing protocol is for the underlay](https://www.ipspace.net/Data_Center_BGP/BGP_Fabric_Routing_Protocol) and [how you should run BGP in the overlay](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics). Each vendor promotes a slightly different approach, making a designer's job a true nightmare.

> Is the implementation straightforward, or can things go wrong?

We're combining a complicated problem (large-scale bridging) with a complex protocol (BGP) often implemented on a code base built to support completely different solutions (Internet routing with BGP or MPLS/VPN). Many things can go wrong, including subtle hardware problems and software bugs, especially if you're trying to build an architecture that goes against what your vendor believes to be the right way to do things.

> What are the key things to look at when designing a data center solution using VXLAN and EVPN?

As always, start with simple questions:

-   What problem am I trying to solve?
-   Do I have to solve it, or would redesigning some other part of the system (for example, application architecture) give us better overall results?
-   What options do I have to solve the problem?
-   Assuming you have to build large-scale virtual Ethernet networks spanning one or few data centers, VXLAN might be better than the alternatives.

Next, you have to decide whether to implement VXLAN in hardware (on top-of-rack switches, the approach taken by data center switching vendors) or software (in hypervisors, the approach used by VMware, Microsoft, Juniper Contrail, many OpenStack implementations, and most large-scale public cloud providers).

Suppose it turns out that it's best to implement VXLAN in hardware (for example, due to many non-virtualized servers). In that case, you have to decide whether to use static configurations potentially augmented with simple automation or deploy EVPN.

Remember what I told you about EVPN interoperability challenges. Don't mix and match different vendors in the same fabric. Instead, build smaller pods (self-contained units of computing, storage, and virtualization) and connect them with traditional technologies like IP routing or VLANs.

Last but not least, while the EVPN control plane used with VXLAN has become more stable, it's not yet a rock-solid technology. Do thorough testing.
