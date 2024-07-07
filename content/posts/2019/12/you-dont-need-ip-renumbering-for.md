---
date: 2019-12-12 08:54:00+01:00
series_weight: 1000
dr_tag: stretch
high-availability_tag: dr
series:
- dr
tags:
- design
- data center
- WAN
- high availability
title: You Don't Need IP Renumbering for Disaster Recovery
url: /2019/12/you-dont-need-ip-renumbering-for/
---
This is a common objection I get when trying to persuade network architects they don't need stretched VLANs (and IP subnets) to implement data center disaster recovery:

> Changing IP addresses when activating DR is hard. You'd have to weigh the manageability of stretching L2 and protecting it, with the added complexity of breaking the two sites into separate domains \[and subnets\]. We all have apps with hardcoded IP's, outdated IPAM's, Firewall rules that need updating, etc.

Let's get one thing straight: when you're doing disaster **recovery** there are no live subnets, IP addresses or anything else along those lines. The disaster has struck, and your data center infrastructure is **gone**.
<!--more-->
{{<note warn>}}
On a related topic, don't ever start the disaster recovery process until the primary site is gone for good. I've heard horror stories of people managing to reconnect a newly-activated DR site back to the still-operational (but previously disconnected) primary site. It wasn't pretty...
{{</note>}}

What could be the simplest solution to get the same subnets and IP addresses you had in the now-destroyed data center reawakened in the new site? Obviously the IP addresses will start popping up as soon as the virtual machines are restarted, but what about the networking infrastructure?

Here are just a few simple ideas:

**When using data center switches as first-hop routers**: Pre-provision all VLANs and shut down SVI interfaces. Enable SVI interfaces as part of the disaster recovery process.

**When using firewalls as first-hop routers**: Pre-provision all VLANs and firewall contexts, and shut down the unused contexts (or interfaces in those contexts). Enable the firewall as part of the disaster recovery process.

**When using virtual firewall appliances**: Pre-provision all VLANs and everything else happens auto-magically once the firewall VMs are restarted in the disaster recovery site.

**When you know how to spell MPLS/VPN**: Pre-provision the whole infrastructure in another VRF (that you can also use for DR testing) and enable it by changing import route targets on WAN edge routers.

I'm positive you can quickly find a few others. However, all of these ideas have a series of "shortcomings":

-   They cannot be used for [disaster recovery test faking](/2019/09/disaster-recovery-test-faking-another/) (that [often fails anyway](/2019/10/disaster-recovery-faking-take-two/));
-   They require the networking team to be involved in disaster recovery process (OMG, what a weird idea!)
-   They require continuous synchronization of configuration changes between primary and disaster recovery infrastructure. Not a big deal if you automated configuration changes, use [infrastructure-as-code principles](/series/niac/), or use something as simple as [Oxidized](https://github.com/ytti/oxidized)... and obviously a total deal-breaker if you're in habit of randomly clicking various GUI options on a Friday evening trying to fix a botched deployment.

**Long story short**: PLEASE don't ever tell me you NEED stretched VLANs for disaster recovery. There is absolutely no technical need for them.

Your organization might decide to go down the stretched VLAN path because [consultants told them to do so](/2013/01/long-distance-vmotion-stretched-ha/), because [you have broken processes](/2013/11/typical-enterprise-application/), because the virtualization team and the networking team cannot stand each other, or because the application or virtualization teams [fake DR tests to get a tick-in-the-box during the annual audit](/2019/09/disaster-recovery-test-faking-another/).

In any case, stretched VLANs are a wrong tool to build disaster recovery infrastructure, and when implementing them you created a [permanent ticking bomb](/2019/05/real-life-data-center-meltdown/) that you'll be blamed for when it goes off just to solve someone else's problem. Good job.

Fortunately, even though [most everyone else is selling you VXLAN/EVPN-based stretched VLAN as the latest miracle cure](/2019/11/the-evpn-dilemma/), VMware finally realized that you should recover networking infrastructure as the first step of overall workload recovery, and their [*disaster recovery* approach to multi-site NSX-T deployments](https://my.ipspace.net/bin/list?id=NSX#CROSS) makes a lot of sense (active-active multi-site NSX-T deployments are [still as bad in release 2.5 as they were before](/2019/08/brief-history-of-vmware-nsx/)).

{{<note>}}
There might be other reasons why you might be asked to implement stretched VLANs. [Most of them are equally bogus](/2018/01/revisited-need-for-stretched-vlans/).
{{</note>}}

### More Information

-   You might want to watch [Building Active-Active and Disaster Recovery Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar;
-   [Multi-site fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) are covered in the [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar. The underlying technologies are described in [EVPN](https://www.ipspace.net/EVPN_Technical_Deep_Dive) and [VXLAN](https://www.ipspace.net/VXLAN_Technical_Deep_Dive) webinars;
-   I described NSX-T multi-site deployment as the last topic in [November 2019 NSX-T update sessions](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive).

All these webinars are part of [Standard ipSpace.net Subscription](https://www.ipspace.net/Subscription/). For even more goodies check out the [Building Next-Generation Data Center online course](https://www.ipspace.net/Building_Next-Generation_Data_Center) (part of [Expert ipSpace.net Subscription](https://www.ipspace.net/Subscription/Individual)).
