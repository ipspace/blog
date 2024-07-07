---
date: 2011-01-26 06:45:00.011000+01:00
mlag_tag: server
series:
- mlag
tags:
- link aggregation
- switching
- virtualization
title: vSwitch in Multi-chassis Link Aggregation (MLAG) environment
url: /2011/01/vswitch-in-multi-chassis-link/
---
Yesterday I described how the [lack of LACP support in VMware's vSwitch and vDS can limit the load balancing options offered by the upstream switches](/2011/01/vmware-vswitch-does-not-support-lacp/). The situation gets totally out-of-hand when you connect an ESX server with two uplinks to two (or more) switches that are part of a Multi-chassis Link Aggregation (MLAG) cluster.

Let's expand the small network described in the previous post a bit, adding a second ESX server and another switch. Both ESX servers are connected to both switches (resulting in a fully redundant design) and the switches have been configured as a [MLAG cluster](/series/mlag/). Link aggregation is not used between the physical switches and ESX servers due to lack of LACP support in ESX.
<!--more-->
{{<figure src="/2011/01/s320-vSwitch_MLAG_Phy.png" caption="Two ESXi hosts connected to two ToR switches">}}

The physical switches are unaware of the physical connectivity the ESX servers have. Assuming that vSwitches use per-VM load balancing and each VM is pinned to one of the uplinks, source MAC address learning in the physical switches produces the following logical topology:

{{<figure src="/2011/01/s320-vSwitch_MLAG_Log.png" caption="Each ESXi hosts looks like multiple single-attached servers">}}

Each VM appears to be single-homed to one of the switches. The traffic between VM A and VM C is thus forwarded locally by the left-hand switch; the traffic between VM A and VM D has to traverse the inter-switch link because neither switch knows VM D can also be reached by a shorter path[^DROP].

[^DROP]: And even if the elf ToR switch would send the traffic toward VM D on the direct link, ESXi would drop it due to its built-in "_we don't need no STP_" loop prevention logic.

{{<figure src="/2011/01/s320-vSwitch_MLAG_Traffic.png" caption="End-to-end traffic flow is suboptimal">}}

When you use servers connected to a pair of edge switches[^REDUNDANCY] *and use all uplinks for VM traffic*, you risk overloading the inter-switch link as the traffic between adjacent ESX servers is needlessly sent across that link. There are at least two solutions to this challenge:

* Use Multi-chassis Link Aggregation (MLAG) and combine server uplinks into a link aggregation group. Don't even think about using static port channels, LACP is your only protection against wiring mistakes[^LICENSE]. When using this approach, it's probably best to configure IP-hash-based load balancing in vSwitch.
* Use active/standby failover policy and dedicate each server uplink to a subset of traffic. For example, use the left-hand uplink for VM and vMotion traffic, and the right-hand uplink for storage (iSCSI/NFS) traffic.

[^REDUNDANCY]: And who doesn't -- most of us can't afford to lose access to dozens of servers after a switch failure.

[^LICENSE]: And yes, I know VMware charges you extra (enterprise license) for the privilege of having a working LACP implementation on ESXi hosts.

### More information

Interaction of vSwitch with link aggregation is just one of many LAG-related topics covered in the _[Data Center 3.0 for Networking Engineers](https://www.ipspace.net/DC30)_ webinar. 

For even more details, watch the _[vSphere 6 Networking Deep Dive](https://www.ipspace.net/VSphere_6_Networking_Deep_Dive)_ and _[Designing Private Cloud Infrastructure](https://www.ipspace.net/Designing_Private_Cloud_Infrastructure)_ webinars.

### Revision History

2022-05-08
: Removed Cisco Nexus 1000v references, and added active/standby scenario
