---
date: 2010-10-01 07:24:00.008000+02:00
lastmod: 2022-05-08 09:21:00
mlag_tag: overview
series:
- mlag
tags:
- link aggregation
- switching
- data center
title: Multi-Chassis Link Aggregation (MLAG) Basics
url: /2010/10/multi-chassis-link-aggregation-basics/
---
If you ask any networking engineer building layer-2 fabrics the traditional way about his worst pains, I'm positive Spanning Tree Protocol (STP) will be very high on the shortlist. In a well-designed fully redundant hierarchical bridged network where every device connects to at least two devices higher in the hierarchy, you lose half the bandwidth to STP loop prevention whims.

{{<figure src="/2010/10/s320-STP_Blocking.png">}}
<!--more-->
You [REALLY SHOULD not build layer-2 data center fabrics with spanning tree anymore](/2020/03/should-i-go-with-vxlan-or-mlag-with-stp/)[^NOTRILL], but if you're still stuck in STP land, you can try to dance around the problem:

[^NOTRILL]: You should also forget about the "wonderful" [proprietary fabric technologies](/2022/05/cisco-fabric-path-and-friends/) promised by the networking vendors during the early 2010s.

-   Push routing as close to the network edge as you can. This works if your environment already uses overlay virtual networking (for example, VMware NSX or Docker/Kubernetes), otherwise you might get a violent kickback from the server admins when they realize [they cannot move the VMs at will anymore](/2010/09/vmotion-elephant-in-data-center-room/);
-   Play with per-VLAN costs in PVST+ or MSTP, ensuring the need for constant supervision and magnificent job security;

Considering the alternatives, multi-chassis link aggregation just might be what you need.

### Link Aggregation Basics

Link aggregation is an ancient technology that allows you to bond multiple parallel links into a single virtual link (link aggregation group -- LAG). With parallel links being replaced by a single virtual link, STP detects no loops and all the physical links can be fully utilized.

{{<figure src="/2010/10/s200-LAG_Basic.png">}}

{{<note>}}Vendors like to use snazzy marketing terms instead of *link aggregation*. You'll hear about *port channel*, *Etherchannel*, *link bonding* or *multi-link trunking*.{{</note>}}

I was also told that link aggregation makes your bridged network more stable[^STABLE]. Every link state change triggers a Topology Change Notification in spanning tree, potentially sending a large part of your network through the STP listening-learning-forwarding state diagram. A link failure of a LAG member does not change the state of the aggregation group (unless it was the last working link in the group), and since STP rides on top of aggregated interfaces, it does not react to the failure.

[^STABLE]: Considering we're discussing bridged fabrics, I should probably say _less unstable_.

### Multi-Chassis Link Aggregation

Imagine you could pretend two physical boxes use a single control plane and coordinated switching fabrics. The links terminated on two physical boxes would seem to terminate within the same control plane and you could aggregate them using LACP. Welcome to the wonderful world of Multi-Chassis Link Aggregation (MLAG).

{{<figure src="/2010/10/s200-MCLA.png">}}

MLAG nicely solves two problems:

* When used in the network core, multiple links appear as a single link. No bandwidth is wasted due to STP loop prevention while you still retain almost full redundancy -- just make sure you always read the smallprint to understand what happens when one of the two switches in the MLAG pair fails.
* When used between a server and a pair of top-of-rack switches, it allows the server to use the full aggregate bandwidth while still retaining resiliency against a link or switch failure.

### Standardization? Not Really

MLAG could be a highly desirable tool in your design/deployment toolbox, but few vendors have taken the pains to start the standardization effort, the notable exception being Juniper with ICCP ([RFC 7275](https://datatracker.ietf.org/doc/html/rfc7275)). EVPN is also supposed to be able to solve most of the MLAG control-plane challenges, but it's questionable whether the resulting complexity is worth the effort.

### Architectural Approaches

If you want to make two (or more) devices act like a single device, you have to build some sort of a clustering solution. Doing it from scratch shouldn't be too hard, but when you have to bolt this functionality on top of a decade-old heap of real-time kludges[^NOS] the challenges become interesting.

[^NOS]: Called *Network Operating System* because marketing

The architectural approaches used by individual vendors are widely different: 

* A common early approach was to turn all but one of the control planes of MLAG cluster members into half-comatose state. Cisco VSS could do that with two devices, Juniper (Virtual Chassis) or HP ([IRF](/2011/01/intelligent-redundant-framework-irf/)) reused their stackable switch technologies.
* Modern implementations use cooperative control planes (Cisco vPC, Arista or Cumulus MLAG)
* [Centralized control plane](/2015/05/link-aggregation-in-openflow-environment/) was also a popular solution in the heydays of [orthodox SDN](/2014/01/what-exactly-is-sdn-and-does-it-make/).

### More information

You'll get a high-level overview of network virtualization, LAN reference architectures, multi-chassis link aggregation, port extenders and large-scale bridging in [Data Center 3.0 for Networking Engineers](https://www.ipspace.net/DC30) webinar.

### Revision History

2022-05-08
: Significant rewrite, removing references to old technologies and obsolete marketing gimmicks, and added a brief mention of ICCP and EVPN.
