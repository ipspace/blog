---
title: "Integrated Routing and Bridging (IRB) Design Models"
date: 2022-11-23 07:58:00
tags: [ IP routing, fabric, networking fundamentals ]
series: [ irb, anycast ]
irb_tag: design
anycast_tag: design
series_title: IRB Design Models Overview
---
Imagine you built a layer-2 fabric with tons of VLANs stretched all over the place. Now the users want to exchange traffic between those VLANs, and the obvious question is: which devices should do layer-2 forwarding (bridging) and which ones should do layer-3 forwarding (routing)?

There are four typical designs you can use to solve that challenge:

* Exchange traffic between VLANs outside of the fabric (edge routing)
* Route on core switches (centralized routing)
* Route on ingress (asymmetric IRB)
* Route on ingress and egress (symmetric IRB)

This blog post is an overview of the design models; we'll cover each design in a separate blog post.
<!--more-->
## Before We Start

* All network devices in this blog post will be called _switches_ even though they're really _bridges_ or _routers_ (or a combination of both). [Marketese](/2011/02/how-did-we-ever-get-into-this-switching.html) happens to be convenient at times.
* All the diagrams are from the _[Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)_ webinar. Watch it if you need more details.

## Edge Routing

You're doing edge routing if you use a router-on-a-stick to forward traffic between VLANs. Small campus networks usually use this design, with the WAN edge router forwarding traffic between the campus and WAN and between the VLANs.

{{<figure src="/2022/11/irb-edge-routing.png" caption="Routing outside of the fabric">}}

You might want to use the same design in data center fabrics to have centralized control of per-tenant traffic. Some organizations would [use a next-generation firewall instead of an edge router](/2015/05/replacing-central-router-with-next.html) and become major investors in their preferred networking vendor if they have too much inter-VLAN traffic.

{{<note info>}}I've seen an organization that used a central firewall to inspect the daily backup traffic. The results were not encouraging.{{</note>}}

## Centralized Routing

Centralized routing is a data center design from the old days when layer-3 forwarding at any decent speed was ridiculously expensive and available only on high-end switches. Access switches perform bridging, and core switches perform routing. 

{{<figure src="/2022/11/irb-centralized-routing.png" caption="Centralized routing">}}

The core switches have to forward intra-VLAN traffic (bridging) while also forwarding traffic between VLANs (routing), so they're doing Integrated Routing and Bridging.

{{<figure src="/2022/11/irb-core-forwarding.png" caption="Integrated Routing and Bridging on core switches">}}

Service provider networks often use a superficially similar design (cheap layer-2 access switches with routing deployed on PE routers), but you have to be a bit careful. You're dealing with centralized routing or edge routing, depending on whether the PE routers perform intra-VLAN bridging.

## Routing on Ingress

Centralized routing (on core or aggregation switches) was the only data center fabric design worth considering until Arista implemented Virtual ARP[^AGW] -- the ability to have the same IP/MAC address active on all edge switches.

[^AGW]: The functionality known as _anycast gateway_ in the EVPN world

In this design, all edge switches:

* Participate in all VLANs.
* Use the same IP/MAC address as the first-hop gateway.
* Forward packets between ingress and egress VLAN on the ingress switch. The packets are then bridged across the fabric within the egress VLAN.

{{<figure src="/2022/11/irb-ingress-routing.png" caption="Routing on ingress device">}}

The defining characteristic of routing on ingress is the asymmetric forwarding path -- routing is always performed on the ingress switch -- resulting in the more familiar Asymmetric IRB name.

## Routing on Ingress and Egress

Asymmetric IRB (routing on ingress) is a much better option than centralized routing in environments with a significant amount of traffic between hosts connected to the same leaf switch. Unfortunately, it has considerable scalability challenges (more about them in an upcoming blog post), prompting networking vendors to develop the fourth design: routing on ingress and egress.

{{<figure src="/2022/11/irb-ingress-egress-routing.png" caption="Routing on ingress and egress device">}}

Routing on ingress and egress looks like business as usual to anyone familiar with MPLS/VPN until we try to implement it in a VXLAN-based IRB environment, where we have to answer two interesting questions:

* Will the traffic within a subnet be routed or bridged?
* What will we use as the transport path between the ingress and the egress router? MPLS-based technologies can always throw another LSP into the mix; we have to do something else in an environment that supports only VLANs.

Regardless of how a particular implementation answers those questions, the forwarding path between a set of hosts in different subnets is always symmetrical, resulting in the Symmetric IRB name.

{{<next-in-series page="/posts/2023/02/irb-edge-routing.html" />}}