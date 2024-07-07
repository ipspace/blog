---
date: 2018-02-13 10:34:00+01:00
evpn_tag: intro
tags:
- EVPN
- MPLS VPN
title: EVPN Is More than VPLS on Steroids
url: /2018/02/evpn-is-more-than-vpls-on-steroids/
---
[Tiziano Tofoni](https://www.linkedin.com/in/tiziano-tofoni-1361759/) wrote a lengthy comment on my [EVPN in small data center fabrics](/2018/02/using-evpn-in-very-small-data-center/) blog post continuing the excellent discussion we started over a beer last October. Today, I'll address the first part:

> I think that EVPN is an excellent standard for those who love Layer 2 (L2) services; we may say that it is an evolution of the implementation of the VPLS service, which addresses some limits in the original standard (RFCs 4761 and 4762).

I might be missing something, but in my opinion, there's no similarity between EVPN and VPLS (apart from the fact that they're trying to solve the same problem).
<!--more-->
VPLS is the result of [organic evolution](https://en.wikipedia.org/wiki/Favela#/media/File:1_rocinha_favela_closeup.JPG) of [anything-over-MPLS](https://tools.ietf.org/html/rfc3251) idea:

-   The process started with P2P transport of Frame Relay frames and ATM cells over MPLS LSPs;
-   Ethernet transport was the next logical step, first as P2P circuits and later as emulated LANs;
-   BGP control plane was introduced to solve scalability challenges caused by lack of automation.

{{<note info>}}Want to know how to automate VPN service provisioning? I published a [simple case study on GitHub](https://github.com/ipspace/MPLS-infrastructure). You might also want to explore the [solution Francois Herbet built](/2018/02/automation-win-mplsvpn-service/) while attending [Building Network Automation Solutions](http://www.ipspace.net/Building_Network_Automation_Solutions) online course.{{</note>}}

At no time did VPLS evolve from a wire-focused service to an endpoint-focused service like MPLS/VPN, officially known as [BGP/MPLS IP VPN](https://tools.ietf.org/html/rfc4364).

EVPN is (almost) like MPLS/VPN but uses MAC and IP addresses and IP prefixes as endpoint identifiers. It also solved several other problems, including:

**Localization of dynamic MAC learning.** EVPN PE-routers gather MAC addresses and transport them across the core network in BGP updates. VPLS relied exclusively on dynamic MAC learning. You could use this behavior to block unknown unicast flooding across the EVPN backbone.

**Combining L2 and L3 forwarding information.** EVPN endpoint information can include MAC and IP addresses, enabling proxy ARP functionality on EVPN PE-routers and thus further reducing the flooding across the EVPN backbone.

**Support for host IP addresses and external prefixes.** EVPN can transport IP addresses of attached endpoints or external IP prefixes within the same address family, resulting in an (almost) universal L2+L3 control plane.

The missing bit: IP multicast (well, I'm not missing it ;).

**Edge multihoming**. Have you ever tried to implement multihoming at the VPLS edge? The STP tricks you had to use on top of a mesh of pseudowires got ridiculously complex — someone had to write a whole CiscoPress book dedicated primarily to this topic.

EVPN has built-in support for edge multihoming based on Ethernet Segment Identifiers (ESI). Preventing layer-2 forwarding loops is still tricky, but at least it's a contained problem solved within the standard, not a heap of kludges.

**Edge load balancing**. The EVPN standard describes how you can use ESI to enable load balancing across the EVPN backbone toward a device connected to two PE routers (MLAG). Using that functionality, some vendors (starting with Juniper) claim they eliminated the need for MLAG clusters at the network edge, further claiming a significant reduction in complexity ([more details](/tag/evpn.html#mlag)).

### Want to Know More?

Check out [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) and [NSX, ACI or EVPN](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN) webinars.
