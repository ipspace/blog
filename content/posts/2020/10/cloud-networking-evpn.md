---
date: 2020-10-06 06:36:00+00:00
dcbgp_tag: design
evpn_tag: rant
series:
- dcbgp
series_weight: 450
tags:
- cloud
- EVPN
- AWS
- Azure
title: EVPN Control Plane in Infrastructure Cloud Networking
---
One of my readers sent me this question (probably after stumbling upon a remark I made in the [AWS Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) webinar):

> You had mentioned that AWS is probably not using EVPN for their overlay control-plane because _it doesn't work for their scale_. Can you elaborate please? I'm going through an EVPN PoC and curious to learn more.

It's safe to assume AWS uses some sort of overlay virtual networking (like every other sane large-scale cloud provider). We don't know any details; AWS never felt the need to [use conferences as recruitment drives](https://blog.ipspace.net/2018/03/before-commenting-on-someone-mentioning.html), and [what little they told us at re:Invent](https://blog.ipspace.net/2018/10/figuring-out-aws-networking.html) described the system mostly from the customer perspective.
<!--more-->
It's also safe to assume they have hundreds of thousands of servers (overlay virtual networking endpoints) in a single region. Making BGP run on top of that would be an interesting engineering challenge, and filtering extraneous information not needed by the hypervisor hosts (RT-based ORF) would be great fun. However, that's not why I'm pretty sure they're not using EVPN - EVPN is simply the wrong tool for the job.

While it seems like EVPN and whatever AWS or Azure are using solve the same problem (mapping customer IP- and MAC addresses into transport next hops), there are tons of fundamental differences between the environments EVPN was designed for and IaaS public cloud infrastructure.

{{<note note>}}I'll use VTEP acronym for transport next hops throughout the rest of this article even though it's highly unlikely that AWS uses VXLAN - AWS had a running system before VXLAN was ever invented. Pretend that VTEP stands for _Virtual Tunnel EndPoint_.{{</note>}}

Typical L2VPN environment has **dynamic endpoints**. MAC- and IP addresses are discovered locally with whatever discovery tool (MAC learning, DHCP/ARP snooping...) and have to be propagated to all other network edge devices. In a properly-implemented scalable cloud infrastructure the orchestration system controls MAC- and IP-address assignments. There's absolutely no need for dynamic endpoint discovery or dynamic propagation of endpoint information. Once a VM is started through the orchestration system, the MAC-to-VTEP mapping is propagated to all other hypervisor hosts participating in the same virtual network.

**Endpoints can move** in a L2VPN environment. While moving endpoints tend to be uncommon across WAN, they do move a lot in enterprise data centers - vMotion in all its variants (including the [bizarre ones](https://blog.ipspace.net/2015/02/before-talking-about-vmotion-across.html)) is the most popular virtualization thingy out there. Even worse, when using technologies like VMware HA or DRS, the endpoints move _without the involvement of the orchestration system_. EVPN would be a perfect fit for such an environment. 

In most large-scale public clouds the endpoints don't move, the only way to get a VM off a server is to restart it, and if a server crashes, the VMs running on it have to be restarted through the orchestration system. There's absolutely no need for an autonomous endpoint propagation protocol.

EVPN is trying to deal with **all sorts of crazy scenarios** like emulating MLAG or having multiple connections into a bridged network. No such monstrosities have ever been observed in large-scale public clouds... maybe because the people running them have too much useful work to do to stretch VLANs all over the place. It also helps if you're big enough not to care about redundant server connections because you can afford to lose all 40+ servers connected to a ToR switch without batting an eyelid.

To make matters more interesting: virtual networking in infrastructure clouds **needs more than just endpoint reachability**. At the very minimum you have to implement packet filters (security groups) and while a True BGP Believer might want to use FlowSpec to get that done, most sane people would give up way before that.

Considering all of the above, what could be a useful control plane between a cloud orchestration system and hypervisor endpoints? Two mechanisms immediately come to mind:

* An API on the hypervisor that is called by the orchestration system whenever it needs to configure the hypervisor parameters (start a VM, create a network/subnet/security group, establish MAC-to-VTEP mapping...)
* A message bus between the orchestration system and the hypervisors. Whoever has some new bit of information drops it on the message bus, and it gets magically propagated to all the recipients interested in that information in due time.

Based on my experience with the speed of AWS and [Azure orchestration systems](https://blog.ipspace.net/2019/06/how-microsoft-azure-orchestration.html) I would suspect that AWS uses the former approach while Azure uses the latter.

EVPN is neither of those. Without information filtering in place, BGP is an eventually-consistent database that pushes the same information to all endpoints. Not exactly what we might need in this particular scenario.

**Long story short**: EVPN is an interesting bit of technology, but probably the wrong tool to implement control plane of an infrastructure cloud that has to provide tenant virtual networks. It does get used as the gateway technology between such a cloud and physical devices though. Juniper Contrail was the first one (I'm aware of) that used it that way, and even VMware gave up their attempts to push everyone else to adopt the  odd baby they got with the Nicira acquisition (OVSDB) and switched to EVPN in NSX-T 3.0.

### More information

Want to know how networking in public clouds works? 

* Start with [AWS Networking 101](https://blog.ipspace.net/2020/05/aws-networking-101.html) and [Azure Networking 101](https://blog.ipspace.net/2020/05/azure-networking-101.html).
* When you're ready for more dive into [AWS Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) and [Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) webinars.
* When you feel it's time to truly master cloud networking, go for the [Networking in Public Cloud Deployments online course](https://www.ipspace.net/PubCloud/).

Interested in EVPN? We have you covered - there are [tons of EVPN-related blog posts](https://blog.ipspace.net/tag/evpn.html), and we explored EVPN from data center and service provider perspective in the [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar.

Finally, I described both NSX-V and NSX-T in [VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) webinar and compared it with Cisco ACI in [VMware NSX, Cisco ACI or Standard-Based EVPN](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN) webinar.