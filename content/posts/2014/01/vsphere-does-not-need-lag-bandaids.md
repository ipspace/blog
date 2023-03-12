---
date: 2014-01-20 07:13:00+01:00
mlag_tag: design
series:
- mlag
tags:
- link aggregation
- data center
- virtualization
title: vSphere Does Not Need LAG Bandaids – the Network Might
url: /2014/01/vsphere-does-not-need-lag-bandaids.html
---
Chris Wahl [claimed in one of his recent blog posts](http://wahlnetwork.com/2014/01/13/vsphere-need-lag-bandaids/) that *vSphere doesn\'t need LAG band-aids*. He\'s absolutely right -- [vSphere's loop prevention logic alleviates the need for STP-blocked links](https://blog.ipspace.net/2010/11/vmware-virtual-switch-no-need-for-stp.html), allowing you to use full server uplink bandwidth without the complexity of link aggregation. Now let's consider the networking perspective.
<!--more-->
The conclusions Chris reached are perfectly valid in a classic data center or VDI environment with majority of the VM-generated traffic leaving the data center; the situation is drastically different in data centers with predominantly east-west traffic (be it inter-server or IP-based storage traffic).

Let's start with a simple scenario:

- Data center is small enough to have [only two switches](https://blog.ipspace.net/2014/10/all-you-need-are-two-top-of-rack.html).
- Two vSphere servers are connected to the two data center switches in a fully redundant setup (each server has one uplink to each ToR switch).
- Load-Based Teaming (LBT) is used within vSphere instead of IP-based hash (vSphere terminology for a Link Aggregation Group).

The two ToR switches are not aware of the exact VM placement, [resulting in traffic flowing across inter-switch link even when it could be exchanged locally](https://blog.ipspace.net/2011/01/vswitch-in-multi-chassis-link.html).

{{<figure src="/2014/01/s320-vSwitch_MLAG_Phy.png" caption="Physical connectivity">}}

{{<figure src="/2014/01/s320-vSwitch_MLAG_Log.png" caption="VM MAC reachability as seen by the switches">}}

{{<figure src="/2014/01/s320-vSwitch_MLAG_Traffic.png" caption="Traffic flow between VMs on adjacent hypervisor hosts">}}

### Can We Fix It?

You can fix this problem by making most endpoints equidistant. You could introduce a second layer of switches (resulting in a full-blown leaf-and-spine fabric) or you could connect the servers to a layer of fabric extenders[^NOFEX], which would also ensure the traffic between any two endpoints gets equal treatment.

{{<figure src="/2014/01/s400-FEX_LAG.png">}}

[^NOFEX]: I wouldn't, fabric extenders are a nightmare. Also, try to get better pricing for leaf switches by mentioning other vendors ;)

Traffic between VMs appearing near to each other in a leaf-and-spine fabric gets better treatment than any other traffic (no leaf-to-spine oversubscription); in the FEX scenario all traffic gets identical treatment as [FEX still doesn't support local switching](http://www.cisco.com/en/US/docs/switches/datacenter/nexus2000/sw/configuration/guide/rel_6_2/b_Configuring_the_Cisco_Nexus_2000_Series_Fabric_Extender_rel_6_2_chapter_01.html).

The leaf-and-spine (or FEX) solution obviously costs way more than a simple two-switch solution, so might consider:

* Using link aggregation and LACP with vSphere or
* Changing your mind and not using all uplinks for VM traffic.

### But LBT Works So Much Better

Sure it does (and Chris provided some very good arguments for that claim in his blog post), but there's nothing in the 802.1ax standard dictating the traffic distribution mechanism on a LAG. VMware could have decided to use LBT with a LAG, but they didn't (because deep inside the virtual switch they tie the concept of a link aggregation group to the IP hash load balancing mechanism). Don't blame standards and concepts for suboptimal implementations ;)

### But Aren't Static Port Channels Unreliable?

Of course they are; I wouldn't touch them with a 10-foot pole. You should always use LACP to form a LAG, but VMware supports LACP only in the distributed switch which requires Enterprise Plus or NSX license[^MAYBE]. Yet again, don't blame the standards or network design requirements, blame a vendor that wants to charge extra for baseline layer-2 functionality.

[^MAYBE]: Like all other vendors, VMware loves to change its licensing. Check VMware documentation for up-to-date details.

### Is There Another Way Out?

Buying extra switches (or fabric extenders) is too expensive. Buying Enterprise Plus license for every vSphere host just to get LACP support is clearly out of question. Is there something else we could do? Of course:

* Don't spread VM traffic across all server uplinks. Dedicate uplinks connected to one switch primarily to VM traffic and use other uplinks primarily for vMotion or storage traffic. Use active/standby failover on uplinks to make sure you don't lose connectivity after a link failure.
* Make sure the inter-switch link gets enough bandwidth.

Typical high-end ToR switches (from almost any vendor) have 48 10GE/25GE/100GE ports[^MOD] and four ports that are four times faster (40GE/100GE/400GE). Using the faster ports for inter-switch links results in worst-case 3:1 oversubscription (48 lower-speed ports on the left-hand switch communicate exclusively with the 48 10GE ports on the right-hand switch over an equivalent of 16 10GE ports). Problem solved.

[^MOD]: Depending on switch model and when you're reading this blog post.