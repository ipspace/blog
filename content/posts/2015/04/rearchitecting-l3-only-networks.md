---
date: 2015-04-21 13:53:00+02:00
tags:
- bridging
- data center
- fabric
- IP routing
title: Rearchitecting L3-Only Networks
url: /2015/04/rearchitecting-l3-only-networks.html
---
One of the responses I got on my "[*What is Layer-2*](https://blog.ipspace.net/2015/04/what-is-layer-2-and-why-do-we-need-it.html)" post was

> Ivan, are you saying to use L3 switches everywhere with /31 on the switch ports and the servers/workstation?

While that solution would work (and I know a few people who are using it with reasonable success), it's nothing more than creative use of existing routing paradigms; we need something better.
<!--more-->
### Why Are We Talking About This?

In case you stumbled upon this blog post by accident, I'd strongly recommend you read a few other blog posts first to get the context:

-   [What is layer-2 and why do we need it](https://blog.ipspace.net/2015/04/what-is-layer-2-and-why-do-we-need-it.html)?
-   [Why is IPv6 layer-2 security so complex](https://blog.ipspace.net/2014/06/why-is-ipv6-layer-2-security-so-complex.html)?
-   [Compromised security zone = game over](https://blog.ipspace.net/2013/04/compromised-security-zone-game-over-or.html)

Ready? Let's go.

### Where Do We Have a Problem?

Obviously we only experience problems described in the above blog posts if we have hosts that should not trust each other (individual users, servers from different applications) in the same security domain (= VLAN).

If you're operating a mobile or PPPoX network, or if your data center uses proper segmentation with [each application being an independent tenant](https://blog.ipspace.net/2013/11/make-every-application-independent.html), you should stop reading. If you're not so lucky, let's move forward.

{{<note info>}}In PPPoX and mobile networks every user (CPE device or phone) appears on a virtual dial-up interface and gets a /64 IPv6 prefix or an IPv4 host route. In any case, the point-to-point layer-2 link terminates on BRAS/GGSN.{{</note>}}

### What Are We Doing Today?

Many environments (including campus, wireless and data center networks) use large layer-2 domains (VLANs) to support random IP address assignment or IP address mobility (from this point onwards IP means IPv4 and/or IPv6).

Switches in these networks perform layer-2 forwarding of packets sent within an IP subnet *even though they might be capable of performing layer-3 forwarding.*

{{<figure src="/2015/04/s400-FHRP_DC.jpg" caption="Data center fabrics perform a mix of L2 and L3 forwarding">}}

The situation is ridiculous in extreme in environments with anycast layer-3 gateways (example: Arista VARP, Cisco ACI) -- even though every first-hop switch has full layer-3 functionality and is even configured to perform layer-3 switching between subnets, it still forwards packets based on layer-2 (MAC) address within a subnet.

{{<figure src="/2015/04/s400-VARP_Design.png" caption="Anycast gateway implemented with Arista VARP">}}

For further information on layer-3 forwarding in data centers and anycast layer-3 gateways, read these blog posts:

-   [Does optimal L3 forwarding matter in data centers](https://blog.ipspace.net/2012/05/does-optimal-l3-forwarding-matter-in.html)?
-   [VRRP, anycast, fabrics and optimal forwarding](https://blog.ipspace.net/2013/06/vrrp-anycasts-fabrics-and-optimal.html)
-   [Optimal L3 forwarding with VARP and active/active VRRP](https://blog.ipspace.net/2013/05/optimal-l3-forwarding-with-varp-and.html)
-   [Arista EOS Virtual ARP (VARP) behind the scenes](https://blog.ipspace.net/2013/06/arista-eos-virtual-arp-varp-behind.html)

### What If...

Now imagine a slight change in IP forwarding behavior:

-   Every first-hop switch tracks attached IP addresses;
-   A switch creates a host route (/32 in IPv4 world, /128 in IPv6 world) for every directly-attached IP host;
-   The host routes are redistributed into routing protocol, allowing every other layer-3 switch in the network to perform layer-3 forwarding toward any host *regardless of host's location in the network*.

{{<figure src="/2015/04/s550-Screenshot+2015-04-16+13.55.54.png" caption="Intra-subnet layer-3 forwarding">}}

Does this sound like [Mobile ARP](https://blog.ipspace.net/2011/02/local-area-mobility-lam-true-story.html) from 20 years ago? Sure it does -- see also RFC 1925 section 2.11.

For more details, watch the [recording of the IPv6 Microsegmentation](https://blog.ipspace.net/2015/04/video-ipv6-microsegmentation.html) presentation I had at Troopers 15, or the [IPv6 Microsegmentation webinar](http://www.ipspace.net/IPv6_Microsegmentation) if you need sample Cisco IOS configurations.

### Will It Work?

It already does. [Microsoft Hyper-V Network Virtualization](https://blog.ipspace.net/2013/12/hyper-v-network-virtualization-packet.html), Juniper Contrail and Nuage VSP use this forwarding behavior in virtual networks. Cisco's Dynamic Fabric Automation (DFA) used the same forwarding behavior in physical data center fabric, and Cisco ACI might be doing something similar. That's also how some advanced EVPN deployments work. Not surprisingly, most of these solutions use BGP as the routing protocol.

Finally, if you're using Cumulus Linux, try out the [Redistribute Neighbor](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-53/Layer-3/Routing/Redistribute-Neighbor/), which redistributes ARP cache into a routing protocol.

Interested in dirty details? You'll find in-depth explanation in [Overlay Virtual Networking](http://www.ipspace.net/Overlay_Virtual_Networking) webinar, which also includes step-by-step packet traces.

### Revision History

2015-04-22
: Added a link to Cumulus Linux *Redistribute Neighbor* feature.

2023-02-01
: * Removed links to (now obsolete) Cisco DFA
  * Updated a link to Cumulus (now NVIDIA) documentation
