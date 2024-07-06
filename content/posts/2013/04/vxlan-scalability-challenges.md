---
date: 2013-04-18 07:07:00+02:00
tags:
- VXLAN
- workshop
- overlay networks
- virtualization
title: VXLAN scalability challenges
url: /2013/04/vxlan-scalability-challenges.html
---
[VXLAN](/2011/08/finally-mac-over-ip-based-vcloud.html), one of the first MAC-over-IP (overlay) virtual networking solutions is definitely a major improvement over traditional VLAN-based virtual networking technologies ... but not without its own [scalability limitations](/2011/12/vxlan-ip-multicast-openflow-and-control.html).
<!--more-->
### Implementation issues

VXLAN was first implemented in Nexus 1000v, which presents itself as a Virtual Distributed Switch (vDS) to VMware vCenter. A single Nexus 1000V instance cannot have more than 64 VEMs (vSphere kernel modules), limiting the Nexus 1000v domain to 64 hosts (or approximately two racks of UCS blade servers).

{{<note update>}}2020-11-19: Nexus 1000v is long gone, but VXLAN is still very much alive, and used in almost all data center virtual networking implementations.{{</note>}}

It's definitely possible to configure the same VXLAN NVI and IP multicast address on different Nexus 1000v switches (either manually or using vShield Manager), but you cannot vMotion a VM out of the vDS (that Nexus 1000v presents to vCenter).

VXLAN on Nexus 1000v is thus a great technology if you want to implement HA/DRS clusters spread across multiple racks or rows (you can do it without configuring end-to-end bridging), but falls way short of the "deploy any VM anywhere in the data center" holy grail.

VXLAN is also available in VMware's vDS switch \... but can only be managed through vShield Manager. vDS can span 500 hosts (the vMotion domain is \~8 times bigger than if you use Nexus 1000V), and supposedly vShield Manager configures VXLAN segments across multiple vDS (using the same VXLAN VNI and IP multicast address on all of them).

{{<note update>}}2020-11-19: vShield is also gone, it's been replaced by NSX-V which was obsoleted when [NSX-T](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) came along..{{</note>}}

### IP multicast scalability issues

VXLAN floods layer-2 frames using IP multicast (Cisco has [demonstrated unicast-only VXLAN](http://blogs.cisco.com/datacenter/cisco-vxlan-innovations-overcoming-ip-multicast-challenges/) but there's nothing I could touch on their web site yet), and you can either manually associate an IP multicast address with a VXLAN segment, or let vShield Manager do it automatically (using IP multicast addresses from a single configurable pool).

{{<note update>}}2020-11-19: Most modern VXLAN implementations also support ingress node replication, obviating the need for IP multicast.{{</note>}}

The number of IP multicast groups (together with the size of the network) obviously influences the overall VXLAN scalability. Here are a few examples:

**One or few multicast groups for a single Nexus 1000v instance**. Acceptable if you don't need more than 64 hosts. Flooding wouldn't be too bad (not many people would put more than a few thousand VMs on 64 hosts) and the core network would have a reasonably small number of (S/\*,G) entries (even with source-based trees the number of entries would be linearly proportional to the number of vSphere hosts).

**Many virtual segments in large network with a few multicast groups**. This would make VXLAN as "scalable" as [vCDNI](/2011/04/vcloud-director-networking.html). Numerous virtual segments (and consequently numerous virtual machines) would map into a single IP multicast address (vShield Manager uses a simple wrap-around IP multicast address allocation mechanism), and vSphere hosts would receive flooded packets for irrelevant segments.

**Use per-VNI multicast group**. This approach would result in minimal excessive flooding but generate large amounts of (S,G) entries in the network.

The size of the multicast routing table would obviously depend on the number of hosts, number of VXLAN segments, and PIM configuration -- do you use shared trees or switch to source tree as soon as possible ... and keep in mind that [Nexus 7000 doesn't support more than 32000 multicast entries](http://www.cisco.com/en/US/docs/switches/datacenter/sw/verified_scalability/b_Cisco_Nexus_7000_Series_NX-OS_Verified_Scalability_Guide.html#reference_04BA8513CF3140D2A2A6C5E5B4E7C60C) and Arista's 7500 [cannot have more than 4000 multicast routes on a linecard](http://www.aristanetworks.com/media/system/pdf/Datasheets/7500_Datasheet.pdf).

### Rules-of-thumb

VXLAN has no flooding reduction/suppression mechanisms, so the rules-of-thumb from [RFC 5556](http://tools.ietf.org/html/rfc5556#page-9) still apply: a single broadcast domain should have around 1000 end-hosts. In VXLAN terms, that's around 1000 VMs per IP multicast address.

However, it might be simpler to take another approach: use shared multicast trees (and hope the amount of flooded traffic is negligible ;), and assign anywhere between 75% and 90% of (lowest) IP multicast table size on your data center switches to VXLAN. Due to vShield Manager's wraparound multicast address allocation policy, the multicast traffic should be well-distributed across all the whole allocated address range.

### More information

VXLAN is also mentioned in the [Introduction to Virtual Networking](http://www.ipspace.net/Introduction_to_Virtualized_Networking) webinar and described in details in the [VXLAN Technical Deep Dive](http://www.ipspace.net/VXLAN_Technical_Deep_Dive) webinar. You'll find some VXLAN use cases in [Cloud Computing Networking](http://www.ipspace.net/Cloud_Computing_Networking) webinar. All three webinars are available with the [yearly subscription](http://www.ipspace.net/Subscription)... and if you need design help/review or a second opinion, check the [ExpertExpress](http://www.ipspace.net/ExpertExpress) service.
