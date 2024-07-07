---
title: "Why Would You Need VXLAN Transport?"
date: 2020-05-28 06:01:00
tags: [ VXLAN, MPLS ]
---
It's amazing how sometimes people fond of sharing their opinions and buzzwords on various social media can't answer simple questions. Today's blog post is based on a true story... a "senior network architect" fully engaged in a recent hype cycle couldn't answer a simple question:

> Why exactly would you need VXLAN and EVPN?

We could spend a day (or a week) discussing the nuances of that simple question, but all I have at the moment is a single web page, so here we go...
<!--more-->
### End-to-End Ethernet Transport

The only reason you need VXLAN is to provide end-to-end Ethernet service across a layer-3 transport network ([more details on why that makes sense](/2020/03/should-i-go-with-vxlan-or-mlag-with-stp/)). The sane use cases include:

**Carrier Ethernet services**. Even though it hurts me immensely as an author of an early MPLS/VPN book, offloading your routing to one or more Service Providers is **not** a good idea, and I would always prefer to [get an Ethernet transport service if I'd need VPN connectivity](https://my.ipspace.net/bin/list?id=ChooseVPN), and [some smart Service Providers started using VXLAN to build their transport fabrics](/2017/06/packet-fabric-on-software-gone-wild/). VXLAN is also often used to build Internet Exchange Points (IXP).

**Networking for virtualized compute workloads**. While some people would love to debate whether it makes sense to provide bridging functionality in virtual networks (TL&DR: NO), everything you connect to a virtual network (including containers) [expects to send and receive Ethernet frames](/2015/04/what-is-layer-2-and-why-do-we-need-it/). 

Whether your system performs packet forwarding between endpoints based on MAC or L3 addresses is irrelevant for this discussion - unless you're OK with connecting all your customers to a single flat network (aka The Internet), you have to transport Ethernet frames across the data center fabric.

I collected [several insane use cases](/2018/01/revisited-need-for-stretched-vlans/) in a previous blog post. You might want to enjoy them for a moment and then come back for more details.

Finally, I don't know enough about campus networks to have more than an opinion (as you might expect it is not favorable to [earth is flat theory](/2015/11/stretched-firewalls-across-layer-3-dci/)).

### But Do We Really Need VXLAN?

VXLAN is obviously not the only way to transport Ethernet frames across a transport network. We've been doing that with Frame Relay, ATM, MPLS, pigeons (not really, but [ping-over-pigeons does work](https://en.wikipedia.org/wiki/IP_over_Avian_Carriers), and extending that to support Ethernet frames would be trivial), so why do we need yet another technology?

Ignoring the ancient technologies, and the miserable details of broken VPLS control plane (fixed with EVPN), why would one prefer VXLAN over Ethernet-over-MPLS? In a word (actually two): loose coupling.

In an MPLS world, the edge device has to be tightly coupled with the network core, as it needs an end-to-end LSP to provide Ethernet transport services. Even if you manage to implement partial decoupling with some sort of hierarchical MPLS and on-demand circuit establishment, at least parts of the network core still need to keep some state for every edge device using it.

All we need in a VXLAN world is IP connectivity... and some hope that the core IP network plans to deliver the traffic (more details in [Can We Trust BGP Next Hops](/2020/04/can-we-trust-bgp-next-hops-part-1/)). 

VXLAN is thus a much better choice in environments in which you want to keep some separation between edge- and core devices, for example: 

* Data center virtual networking where the true edge devices are hypervisor virtual switches regardless of what the vendor marketers would love you to believe;
* Service provider networks that want to keep the separation between edge (customer-facing) and core (transport) networks.

Want more details? Check out these webinars:

* [Overlay Virtual Networking](https://www.ipspace.net/Overlay_Virtual_Networking)
* [Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service)
* [VXLAN Technical Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive)
* [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)