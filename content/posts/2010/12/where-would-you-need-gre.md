---
date: 2010-12-15 07:11:00.002000+01:00
dmvpn_tag: other
tags:
- DMVPN
- VPN
- IPsec
- MPLS VPN
title: Where Would You Need GRE?
url: /2010/12/where-would-you-need-gre/
---
After I made the "_duct tape of networking_" joke, I quickly became a *GRE lover* (according to @Neelixx -- another Twitter account lost in the mists of time). Jokes aside, let's see where it makes sense to use GRE.

{{<figure src="/2010/12/networking-duct-tape.jpg">}}
<!--more-->
Whenever you want to transport your data over a third-party IP infrastructure without exposing your addressing and routing structure (example: building a VPN across a public IP infrastructure), you need a mechanism that allows you to encapsulate your IP packets (which are not routable by the third-party IP infrastructure) into routable IP envelopes.

There are at least five mechanisms that can do that (please add the ones I've missed in the comments):

-   IPsec tunneling mode, which encrypts *private* IP packet and transports it in a *public* IP datagram with *Encapsulated Security Payload* header;
-   GRE, which puts *private* IP packet in a GRE envelope (IP+GRE header);
-   LISP, which uses LISP-over-UDP-over-IP headers;
-   Various SSL VPNs, which put private IP packets into SSL (encrypted HTTP);
-   IP-over-IP tunnels.

In redundant scenarios, it usually makes sense to run a routing protocol between VPN sites -- failure detection is more consistent and it's easier to reroute around failed links. Most routing protocols expect the routing protocol neighbors to be adjacent and Cisco IOS implementation of routing protocols requires the protocols to be associated with interfaces. To run routing protocols across an IP-over-IP technology with Cisco IOS you therefore need tunnel interfaces. We've managed to get RIP and BGP running across IPsec implementations using crypto maps, but trust me: you don't want to do that.

{{<note>}}Alternatively (if you need encryption), you could use Reverse Route Injection feature of IPsec, but then you're back in (somewhat reliable) static routing world with all its "beauties" we've learned to hate in the last decades.{{</note>}}

If you need encryption, IPsec Virtual Tunnel Interface (VTI) will give you encryption and a point-to-point tunnel interface. If you just need IP-over-IP transport, GRE is probably the best option; more so as it's multi-protocol: you can run IPv4, IPv6 and MPLS across the same GRE tunnel concurrently. Last but definitely not least, you can use *multipoint* GRE tunnels, where the same tunnel interface connects you to a number of remote sites. You can't do anything remotely similar with IP-over-IP tunnels or IPsec.

{{<note>}}Just in case you're wondering: yes, you can also run transparent bridging, CLNS, IPX, DECnet and AppleTalk across the same GRE tunnel.{{</note>}}

Now that you know *why* you'd need GRE, let's see *where* you would use it:

-   **DMVPN** -- multipoint GRE technology allows you to build scalable networks where a single tunnel interface can be used to reach numerous remote sites.
-   **MPLS/VPN** **WAN** -- once you get sick-and-tired of service provider incompetence (you want to hear a good rant -- listen to Greg Ferro every time someone mentions VPLS in Packet Pusher podcasts), you can build GRE tunnels across their MPLS/VPN infrastructure and have a smoothly running network even when they manage to create yet another byzantine failure.
-   **Enterprise MPLS/VPN** -- if you decide to build your own MPLS/VPN network across a public IP infrastructure (including building your own MPLS/VPN service across a SP MPLS/VPN WAN), you need GRE tunnels.

### More Information

-   If you're interested in basics of various VPN technologies and their benefits/drawbacks, [*Choose the Optimal VPN Service*](https://www.ipspace.net/Choose_the_optimal_VPN_service) webinar is just what you need.
-   You'll learn everything you ever wanted to know about DMVPN in the [*DMVPN:* *from Basics to Scalable Networks*](https://www.ipspace.net/DMVPN) webinar.
-   Building your own enterprise MPLS/VPN service? Get started with the [*Enterprise MPLS VPN Deployment*](https://www.ipspace.net/EnterpriseMPLS) webinar.
