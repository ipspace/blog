---
date: 2023-09-18 06:34:00+00:00
evpn_tag: intro
tags:
- EVPN
- bridging
title: Dataplane MAC Learning with EVPN
---
Johannes Resch submitted the following comment to the _[Is Dynamic MAC Learning Better Than EVPN?](/2023/04/evpn-dynamic-mac-learning/)_ blog post:

> I've also recently noticed some vendors claiming that dataplane MAC learning is so much better because it reduces the number of BGP updates in large scale SP EVPN deployments. Apparently, some of them are working on IETF drafts to bring dataplane MAC learning "back" to EVPN. Not sure if this is really a relevant point - we know that BGP scales nicely, and its relatively easy to deploy virtualized RR with sufficient VPU resources.

While he's absolutely correct that BGP scales nicely, the questions to ask is "_what is the optimal way to deliver a Carrier Ethernet service?_"
<!--more-->
_Carrier Ethernet_ service should (by definition) emulate Ethernet, which means it's just a glorified bit transport[^DT] with a bit of MAC filtering and BUM flooding thrown in. Carrier Ethernet services have been (successfully) implemented with dynamic MAC learning for ages, so it's fair to ask "_what exactly is EVPN bringing to the table?_"

[^DT]: As pointed out by Bela Varkonyi: Carrier Ethernet devices receive and forward [Ethernet frames](/2022/10/ethernet-encapsulations/) and perform error checking on those frames, so they provide more than just a bitstream service.

EVPN is definitely a major step forward when [compared to the mess called VPLS](/2018/02/evpn-is-more-than-vpls-on-steroids/). It can run on top of multiple transport technologies ([MPLS](/2022/04/do-you-care-about-mpls/), [VXLAN](/2020/05/need-vxlan-transport/), SR-MPLS, SRv6), carries enough information to build deterministic flooding trees, and has built-in mechanisms to deal with [Multi-Chassis Link Aggregation](/series/mlag/) (MLAG) and primary/backup attachments to multi-homed customer sites. However, does it really need to do control-plane MAC learning? After all, Cisco successfully implemented an early version of EVPN with dynamic MAC learning on Nexus 1000v.

There are two scenarios I could find where control-plane MAC learning works better than dynamic MAC learning: ARP proxy, where you want to have deterministic IP-to-MAC mapping information, and MLAG. I don't want a service provider to do ARP proxying as part of a Carrier Ethernet service; I want them to [stay as far away from complex (and potentially buggy) stuff](/2014/03/whose-failure-domain-is-it/) as possible and efficiently [deliver the bits](/2018/03/whos-pushing-layer-2-vpn-services/)[^DGA] I'm paying for.

[^DGA]: OK, frames ;)

How about MLAG? We've been doing MLAG for ages before EVPN appeared, and while it's been a mess in the traditional MPLS world, it's well known how to make it [work reasonably well in VXLAN environments with anycast VTEPs](/2022/09/mlag-deep-dive-vxlan-fabric/). The same trick could be used with MPLS transport, but you'd have to replace LDP with SR-MPLS to get anycast SID. Also, you don't need MLAG if you [use Carrier Ethernet service as a bit transport between sites](/2012/07/the-difference-between-metro-ethernet/) not as the enabler of stretched VLANs.

One has to ask: is it worth dealing with the extra complexity of EVPN control-plane MAC learning and [MLAG handling](/2022/11/mlag-vxlan-evpn/) just to be able to deploy Ethernet service over any transport network without having to invest in proper network design? The vendors definitely think so -- after all, the "_trust me, it works_" fairy tales are what makes their quarterly earnings -- but is it the best choice for the service providers and their customers? I don't think so, and I'm glad to see at least some vendors waking up from the hype-induced daze and thinking about alternatives.

Want to know more? Check out:

* [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)
* [VXLAN Technical Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive)
* [Carrier Ethernet discussions](https://my.ipspace.net/bin/list?id=Design#2022_04) in [ipSpace.net Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic)

### Revision History

2023-09-25
: Carrier Ethernet is a frame-based not a bitstream service.
