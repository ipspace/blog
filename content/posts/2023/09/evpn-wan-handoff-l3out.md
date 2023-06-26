---
title: "Layer-3 WAN Handoff (L3Out) in VXLAN/EVPN Fabrics"
date: 2023-09-06 09:05:00
tags: [ EVPN, VXLAN, WAN ]
---
I got a question from a few of my students regarding the best way to implement end-to-end EVPN across multiple locations. Obviously there’s the multi-pod and multi-site architecture for people believing in the magic powers of stretching VLANs across the globe, but I’m looking for something that I could recommend to people who understand that you have to have a L3 boundary if you want to have multiple independent failure domains (or availability zones).
<!--more-->
The theory seems to be simple: WAN edge devices advertise LAN prefixes (or even host routes turned into type-5 prefixes) with themselves as the next hop and the WAN transit VNI as the encapsulation. Dataplane-wise the solution would do VXLAN-to-VXLAN routing on the WAN edge devices, which should be supported on a decent range of recent ASICs.

### Lukas

Multi-Pod or Super-Spine is the stupidity per-se. It is a extended underlay with no controller in the overlay. You just do L2/L3 everywhere, which we learned is just nonsense - 100% agree.

The part you mention in regards to L3 handoff can be done in 3 different ways:

#1 VXLAN to IP
#2 VXLAN to VXLAN
#3 VXLAN to MPLS, SR, SRv6

In the 1st option, you do a Inter-AS Option A. You bring the IP prefixes into individual VRFs on the Border node. From there, you use, preferably, sub-interfaces and per-VRF eBGP peering to get these prefixes to the “outside world”. In that operation, you have all the goodies of classic BGP filtering on the per-VRF eBGP session. Simple and straight forward. You can, of course, do this also with IGPs and/or SVIs but that is another moronity as then mutual redistribution comes into the game and other drama. See here this session for the RIGHT way and all the convoluted ways :-)

https://www.ciscolive.com/on-demand/on-demand-details.html?#/session/1655424224206001QF9P

For the 2nd option, you actually use the Multi-Site BGW, which is able to do just the routing part. Yes, you can do the bridging but that is more of a add-on. The reason why you need to have some function of EVPN reorigination at such a BGW (Border Gateway) is that EVPN uses a RMAC extended community. This is the inner-DMAC for the VXLAN encap that is part of the route. When you receive this route from a Leaf, it has to be changed to the Border node that does re-originates the route towards the remote domain. So just RIOT is not working, you need to proper change the next-hop with the correct RMAC. Our GW does that and it works fine for L3 only.

The 3rd option is pretty much the same as the 2nd with the difference we use other encaps and predominantly L3VPN (VPNv4, VPNv6). LDP, SR, Labeld Unicast or whatever you can think of is possible. 

EVPN to EVPN or EVPN to L3VPN re-origination allows the filtering of routes as you would do with BGP anyway. On the sessions or, if there, at re-distribution. Also, the table-maps for intra-VRF filtering is also possible.

Option 1 is extensively in the link while Option 2 and 3 is at the very end mentioned.
