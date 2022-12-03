---
title: "Why Would You Need an Overlay Network?"
date: 2022-12-07 07:25:00
tags: [ overlay networks, VXLAN ]
---
I got this question from one of ipSpace.net subscribers:

> My VP is not a fan of overlays and is determined to move away from our legacy implementation of OTV, VXLAN, and EVPN[^EL]. We own and manage our optical network across all sites; however, it's hard for me to picture a network design without overlays. He keeps asking why we need overlays when we own the optical network.

[^EL]: Look how far we got -- people are calling VXLAN/EVPN "legacy implementation" 😁

There are several reasons (apart from RFC 1925 Rule 6a) why you might want to add another layer of abstraction (that's what overlay networks are in a nutshell) to your network.
<!--more-->
You want to **keep the forwarding tables on interim devices small and stable** and don't want to insert endpoint addresses or prefixes into them. That's why we use VXLAN or Provider Backbone Bridging (PBB) to build layer-2 fabrics. Service providers use [MPLS-based BGP-free core](https://blog.ipspace.net/2012/01/bgp-free-service-provider-core-in.html) for the same reason.

**Path separation**. Most network devices (including bridges and routers) perform hop-by-hop destination-only forwarding. To separate two traffic streams, you must implement parallel forwarding domains on every device in the path or hide the user payload into a transport envelope (tunneling).

You might need path separation for security reasons (security domains or multi-tenant networking) or to deal with overlapping address spaces (the original use case for VRFs).

**Legacy protocols**. Tunneling is the easiest way to provide connectivity services for a protocol or technology you don't want to see in the core of your network -- be it IPv6, voice, SCSI, bridging, IPX, or AppleTalk.

I mentioned tunneling several times. We could debate for hours what tunneling is and whether MPLS is tunneling, However, there's no doubt that transporting layer-2 frames (VXLAN) or layer-3 packets (GRE) inside another layer-3 (or higher) envelope is tunneling, and a network built out of tunnels is usually called an overlay network.

Finally, you could use VLANs or xWDM wavelengths (lambdas) instead of tunnels. Dedicating a lambda to every tenant (or legacy protocol) might be a bit expensive, and VLANs turn your whole network into a single failure domain. If you want to build a stable transport network, you usually use layer-3 technologies; overlays often happen to be the best tool for the job.

### More Information

If you're interested in this topic, you might want to watch these webinars (all of them part of [Standard ipSpace.net subscription](https://www.ipspace.net/Subscription/)):

* [Overlay Virtual Networking](https://www.ipspace.net/Overlay_Virtual_Networking)
* [VXLAN Technical Deep Dive](https://www.ipspace.net/VXLAN_Technical_Deep_Dive)
* [Enterprise MPLS VPN Deployment](https://www.ipspace.net/Enterprise_MPLS_VPN_Deployment)
* [Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service)

Haven't found what you're looking for? Send me an [interesting question for the ipSpace.net design clinic](https://designclinic.ipspace.net/pages/submit/).
