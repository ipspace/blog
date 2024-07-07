---
date: 2023-09-25 11:43:00+00:00
evpn_tag: mpls
tags:
- VXLAN
- EVPN
- SD-WAN
title: Does EVPN/VXLAN over SD-WAN Make Sense?
---
It looks like we might be seeing VXLAN-over-SDWAN deployments in the wild. Here's the "why that makes sense" argument I received from a participant of the [ipSpace.net Design Clinic](https://designclinic.ipspace.net/posts/2022/06/) in which I wasn't exactly enthusiastic about the idea.

> Also, the EVPN-over-WAN idea is not hypothetical since EVPN+VXLAN is now the easiest way to build L3VPN with data center switches that don’t support MPLS LDP. Folks with no interest in EVPN’s L2 features are still using it for L3VPN.

Let's unravel this scenario a bit:
<!--more-->
* We want to implement multiple routing domains (L3VPN) across WAN.
* We're using IP transport as the WAN service
* MPLS/VPN with MPLS-over-GRE or EVPN/VXLAN are thus the only viable options

So far so good. We've been in similar situations before -- I know people running [MPLS-over-GRE-over-IPsec over MPLS/VPN service](/2011/03/mplsvpn-over-gre-over-ipsec-does-it/). However, imagine the encapsulation stack we're dealing with assuming the SD-WAN solution uses VXLAN-over-IPsec[^PS]:

[^PS]: Obviously an SD-WAN solution could use any proprietary encapsulation as long as it provides encryption and L3VPN functionality. However, many SD-WAN products are nothing more than orchestration glue around open-source components, and it's easy to set up VXLAN-over-IPsec on Linux, so there you go.

* End-user IP packet (the only useful part)
* End-user Ethernet header (needed because VXLAN is a L2 transport)
* Customer VXLAN+UDP header
* Customer IP headers
* Customer Ethernet headers (unless the SD-WAN solution uses IP-over-something encapsulation instead of VXLAN)
* SD-WAN VXLAN+UDP header (or whatever other encapsulation is sued)
* SD-WAN IPsec header (or a similar encryption header)
* SD-WAN IP+Ethernet headers (assuming the service provider uses Ethernet access)

It looks almost as good as running [Unix on a PDP-11 CPU emulated in Javascript](https://takahirox.github.io/pdp11-js/unixv6.html) and definitely proves [RFC 1925](https://datatracker.ietf.org/doc/html/rfc1925) rules 5 and 6.

You might be OK with this solution if you have too much WAN bandwidth, but even then you'd be paying for the L3VPN-over-L2VPN-over-VXLAN overhead because your SD-WAN boxes would be processing it. Maybe that's negligible compared to the benefits you get, so go for it. I'm just hoping you're not transporting VoIP data ;)

Could we reduce the overhead? Sure. There's a reason SD-WAN solutions use something like VXLAN on top of IPsec -- they have to offer L3VPN functionality. Instead of running one L3VPN solution (EVPN/VXLAN) on top of another one (SD-WAN) you could connect them using point-to-point VLANs similar to MPLS/VPN Inter-AS Option A. That would get rid of four layers of encapsulation, but tightly couple SD-WAN configuration with your data center configuration, and increase the complexity of the design. As Russ White would have said: [it's all about the tradeoffs](https://rule11.tech/tradeoffs/).