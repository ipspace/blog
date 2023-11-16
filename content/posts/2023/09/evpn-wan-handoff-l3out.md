---
title: "Layer-3 WAN Handoff (L3Out) in VXLAN/EVPN Fabrics"
date: 2023-09-06 15:02:00
tags: [ EVPN, VXLAN, WAN ]
---
I got a question from a few of my students regarding the best way to implement end-to-end EVPN across multiple locations. Obviously there’s the multi-pod and multi-site architecture for people believing in the magic powers of stretching VLANs across the globe, but I was looking for something that I could recommend to people who understand that you have to have a L3 boundary if you want to have multiple [independent failure domains](https://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html) (or availability zones).
<!--more-->
The theory seems to be simple: WAN edge devices advertise LAN prefixes (or even host routes turned into type-5 prefixes) with themselves as the next hop and the WAN transit VNI as the encapsulation. Dataplane-wise the solution would do VXLAN-to-VXLAN routing on the WAN edge devices, which should be supported on a decent range of recent ASICs.

I could have started digging through vendor documentation to figure out what's supported, but I decided to take the easy way out: I asked Lukas Krattiger (Cisco Systems) and Massimo Magnani (Arista) what their platforms could do. The material for the rest of this blog post was supplied by Lukas and describes what Cisco is doing in this space; we'll cover what Arista can do in a follow-up blog post.

---

Multi-Pod or Super-Spine is just an extended underlay with no controller in the overlay. You just do L2/L3 everywhere, which we learned doesn't work that well at scale. The part you mention in regards to L3 WAN handoff can be done in 3 different ways:

1. VXLAN to IP
2. VXLAN to VXLAN
3. VXLAN to MPLS, SR, SRv6

In the first option, you do Inter-AS Option A. You bring the IP prefixes into individual VRFs on the Border node. From there, you use, preferably, sub-interfaces and per-VRF eBGP peering to get these prefixes to the “outside world”. In that operation, you have all the goodies of classic BGP filtering on the per-VRF eBGP session -- simple and straightforward.

You can, of course, do this also with IGPs and/or SVIs but then mutual redistribution comes into the game. You might want to watch [this Cisco Live](https://www.ciscolive.com/on-demand/on-demand-details.html?#/session/1655424224206001QF9P) session for the RIGHT way and all the convoluted ways of implementing this design.

For the second option, you use the Multi-Site Border Gateway (BGW), which is able to do just the routing part (you can also do the bridging but that is more of a add-on). The reason why you need to have some function of EVPN re-origination at BGW is that EVPN uses an RMAC extended community -- the inner destination MAC address for the VXLAN encapsulation that is part of the route. When you receive such a route from a Leaf, that community has to be changed to the Border node that re-originates the route towards the remote domain.

Having just VXLAN routing (RIOT -- Routing In and Out of Tunnels) on the data plane is not enough and changing the BGP next hop is not enough; you need to change the next-hop with the correct RMAC. Our BGW does that and it works fine in L3-only deployments.

The third option is pretty much the same as the second one with the difference that we use other encapsulations and predominantly L3VPN (VPNv4, VPNv6). You can use whatever you like to build the underlay: LDP, SR, or labeled unicast (BGP-LU) are all possible. 

EVPN to EVPN or EVPN to L3VPN re-origination allows the filtering of routes as you would do with BGP anyway -- on the sessions or at the redistribution point. Also, there are table-maps for intra-VRF filtering.

{{<next-in-series page="/posts/2023/11/arista-evpn-l3out-handoff.html">}}**Coming up next:** L3 WAN handoff on Arista EOS{{</next-in-series>}}
### Revision History

2023-09-06
: A draft version of this blog post escaped into the wild, was caught after a few hours, tamed and republished.
