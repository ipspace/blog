---
date: 2011-08-05T07:05:00.000+02:00
tags:
- switching
- workshop
- virtualization
title: VLANs used by Nexus 1000V
url: /2011/08/vlans-used-by-nexus-1000v/
---

Chris sent me an interesting question:

> Imagine L2 traffic between two VMs on different ESX hosts, both using Nexus 1000V. Will the physical switches see the traffic with source and destination MACs matching the VM's vNICs or traffic on NX1000V "packet" VLAN between VEMs (in this case, the packet VLAN would act as a virtual backplane)?

<!--more-->
{{<figure src="/2011/08/s320-NX1K_VLAN.png" caption="VLANs used by Nexus 1000V">}}

#### Digression into Nexus 1000V VLAN usage

Nexus 1000V uses up to three VLANs for its communication needs:

***Packet VLAN*** is a data-plane VLAN used to exchange control protocol packets between VEMs and VSMs. It’s used to send CDP (as well as LACP and IGMP) packets received by a VEM to the VSM. It’s also used by the VSM to send CDP (or LACP) packets through the desired physical port(s) on desired VEM.

***Control VLAN*** is a control-plane VLAN used by the VSM to download configuration information into individual VEMs.

{{<note info>}}VEM receives parts of initial configuration that it needs to establish VEM-to-VSM communication directly from vCenter.{{</note>}}

You also have to establish communication between VSM and vCenter using a ***Management VLAN***. VSM uploads parts of its configuration to the vCenter (to allow VEMs to start, see above) and uses vCenter API to create vCenter objects like port groups based on NX-OS configuration.

You can’t configure the management VLAN in VSM. You connect the management port of the VSM (a virtual machine) to a vCenter port group and specify the desired VLAN in the port group configuration ([follow this procedure](http://www.cisco.com/en/US/docs/switches/datacenter/nexus1000/sw/4_0_4_s_v_1_3/getting_started/configuration/guide/n1000v_gsg_5vsm_behind_vem.pdf) if the VSM uses a VEM to communicate with the physical network).

{{<note info>}}Read *[Management, Control, and Data Planes](/2013/08/management-control-and-data-planes-in/)* blog post if you're not familiar with typical network device architecture.{{</note>}}

You can use the same VLAN for all three purposes; you can also replace *packet* and *control* VLAN with layer-3 communication (using UDP). Using a separate management VLAN sounds like a good idea, but I fail to see why it would be a good idea to use separate *Packet* and *Control* VLANs.

#### Back to the original question

Have you noticed that I haven’t mentioned VM traffic in the previous section? VM traffic does not use the Nexus 1000V-specific VLANs; it gets a VLAN tag specified in the associated port profile (and reflected in the corresponding vCenter port group) and is sent toward the physical network using whatever load balancing mechanism you’ve configured.

The packet VLAN is never used for VEM-to-VEM communication. Even though the inter-VM traffic might pass through two VEMs, neither VEM is aware of that fact; they rely on the physical switches to sort out the MAC address information and forward the traffic toward destination VM.
