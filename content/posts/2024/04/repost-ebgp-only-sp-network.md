---
title: "Repost: EBGP-Mostly Service Provider Network"
date: 2024-04-01 08:08:00+0200
tags: [ BGP, design ]
---
Daryll Swer [left a long comment](/2024/03/arista-interface-ebgp/#2157) describing how he designed a Service Provider network running in numerous private autonomous systems. While I might not agree with everything he wrote, it's an interesting idea and conceptually pretty similar to what we did 25 years ago (IBGP without IGP, running across physical interfaces, with every router being a route-reflector client of every other router), or how some very large networks were using BGP confederations.

Just remember (as someone from Cisco TAC told me in those days) that "_you might be the only one in the world doing it and might hit bugs no one has seen before_."
<!--more-->
---

I'm all up for 100% (okay, more like 99.99%) layer-3 eBGP driven networks. SP, DC, Enterprise, Home Lab? Everything 100% (meaning 99%) eBGP Driven networks. Easy to configure, easy to manipulate/traffic engineer with granular route filters with various attributes such as BGP communities, no full-mesh nonsense (or route reflectors) as was/is the case with iBGP. eBGP all the way to the host on DC networks, BGP multipathing included for your network-level load balancing for K8s (or possibly Docker Swarm) clusters etc, augmented with BGP communities to influence paths from host up to the DFZ even. With BGP, you can build unconventional topologies in any shape or form as you see fit. IGPs make the network flat and hence have some limitations.

[Here's an example](https://anuragbhatia.com/2022/04/networking/isp-column/inefficient-igp-can-make-ebgp-go-wild/) of why IGPs simply don't scale for TE properly

When I say eBGP driven layer 3-only networks, it does not imply that MPLS isn't in use, it doesn't imply that VXLAN/EVPN isn't in use (for DC networking), these “transport” protocols are very much in use, but they are BGP driven, such as BGP signalled VPLS. It also does not imply IGPs aren't in use - they are, but they are limited in functionality to the purpose of only establishing loopback learning/adjacency for adjacent peers in a network segment (like say an MPLS cloud) or path.

BGP, at most basic operational use, is very easy to work with and scales if you need it to.

However, currently, there's not much documentation or blog posts or tutorials on how to design eBGP driven SP networks (which is something I do in production), there is some documentation for DCs, but even that largely assumes a typical Spine/Leaf/Clos topology. I've worked in a DC environment where we took some inspiration from the hypercube network topology concept (and therefore, it really wasn't a Clos topology), and everything was 100% eBGP, up to the host, almost everything was interconnected on layer 1 for adjacent devices Spine<>Spine, Leaf<>Leaf etc — It was more like a mix of SP and DC networking.

The basic visual representation of this eBGP approach: Vertical paths = eBGP up/down with private ASN numbering and default routes for egress back up. remove-private-as on the edge routers that talks DFZ. Horizontal paths = IGP + iBGP or IGP/LDPv6 etc as and when required for loopback learning.

So, coming to “numbering”, I would probably be okay with “unnumbered” (link-local IPv6) interfaces for establishing adjacency for the horizontal paths. However, for the vertical paths, I'd still use route-able IPv6 GUA addressing to help make my life easier when running a traceroute or troubleshooting.

But at the same time, life's easy for numbered IPv6 GUA interfaces if you use something similar to my [geographical denomination model for IP(v6) addressing architecture](https://www.daryllswer.com/ipv6-architecture-and-subnetting-guide-for-network-engineers-and-operators/).

---

2024-04-03
: I slightly changed the title as it gave the impression that Daryll's network is not using IGP or IBGP. I also added a remark that some people used confederations to achieve similar results.