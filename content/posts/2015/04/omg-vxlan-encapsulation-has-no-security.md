---
date: 2015-04-24 11:32:00+02:00
tags:
- VXLAN
- security
title: OMG, VXLAN Encapsulation Has No Security!
url: /2015/04/omg-vxlan-encapsulation-has-no-security/
---
Every now and then someone actually looks at the VXLAN packet format and eventually figures out that VXLAN encapsulation doesn't provide any intrinsic security.

**TL&DR Summary**: That's old news, the sky is not falling, and deploying VXLAN won't make your network less secure than traditional VLAN- or MPLS-based networks.
<!--more-->
Let's start with the *old news* bit. This is a slide straight out of my [VMware NSX Architecture](https://my.ipspace.net/bin/list?id=NSXArch) webinar (you can also [watch the related video](https://my.ipspace.net/bin/get/NSXArch/2.3%20-%20Overlay%20Virtual%20Networks%20Data%20Plane.mp4)).

{{<figure src="/2015/04/s550-VXLAN+Security.jpg" caption="Typical overlay virtual networking encapsulations in mid 2010s">}}

As I clearly pointed out at that time, you (RFC 2119) MUST make the VXLAN transport network absolutely secure -- anyone gaining access to the VXLAN transport network can insert packets into any VXLAN segment and potentially glean packets traversing a VXLAN segment. The intruder can do even more havoc in multicast-based VXLAN implementations that rely on traditional Ethernet flooding-and-learning: packets sent from intruder's IP address can overwrite MAC-to-VTEP mapping entries in VXLAN endpoints, allowing the intruder to attract traffic sent to a particular MAC address.

Not surprisingly (as VXLAN is based on VLAN forwarding model), it's easy to do the same in any VLAN-based network. As soon as an intruder gains access to a trunked switch port or a core link, it's game over. VXLAN is thus no less secure than traditional VLAN-based networks.

MPLS networks are not much better. Once you have access to an MPLS-based backbone, you can insert packets into any LSP. This was evident to anyone who wanted to spend a few minutes thinking about MPLS security in the last decades. For more details, see this [excellent presentation by Enno Rey](https://www.blackhat.com/presentations/bh-europe-06/bh-eu-06-Rey-up.pdf).

{{<note>}}Diverting MPLS traffic would require more effort, particularly in layer-3 MPLS-based VPNs.{{</note>}}

Is it possible to insert VXLAN packets (and thus send traffic to other segments) from an end host? Sure -- all you need is someone crazy enough to connect a server (or a VM) to the VLAN used for VXLAN transport, probably through some misguided use of native VLANs. Unfortunately there's no easy cure for stupidity or fat fingers (in unrelated news, it's also possible to read physical disk of an ESXi server if someone is [stupid enough to allow customers to craft their own VMX files](http://www.insinuator.net/2012/05/vmdk-has-left-the-building/)).

VXLAN implementations using control-plane distribution of MAC-to-VTEP mappings (VMware NSX, Nuage VSP, Juniper Contrail, Cisco EVPN on Nexus 9K) are less vulnerable to traffic redirection attacks (unless, of course, they use a combination of control plane and dynamic MAC learning). They *might* also include anti-spoofing features, which would drop traffic sent from illegal source IP addresses (VTEPs), but that just shifts the problem to the core network, which has to validate source IP addresses based on input ports -- how many times have you seen that done in a data center environment?

The best way to deal with this problem seems to be to reuse the best practices we used to build secure VLAN-based backbones: make sure it's hard for an intruder to get access to the transport network. What I'm usually recommending in my [consulting engagements](http://www.ipspace.net/ExpertExpress) is to build a separate leaf-and-spine fabric used solely for VXLAN transport, and never connect it directly to the data center core. This slide from the [VMware NSX Architecture](http://content.ipspace.net/get/NSXArch) webinar illustrates a typical approach:

{{<figure src="/2015/04/s550-Cloud-as-Appliance.jpg" caption="Use VXLAN only over secure transport infrastructure">}}

### Need More Information?

Start with the free [VMware NSX Architecture](https://www.ipspace.net/VMware_NSX_Architecture) webinar, continue with [Overlay Virtual Networking](http://www.ipspace.net/Overlay_Virtual_Networking) and [VXLAN Technical Deep Dive](http://www.ipspace.net/VXLAN_Technical_Deep_Dive) webinars, and conclude with [Designing Private Cloud Infrastructure](http://www.ipspace.net/Designing_Private_Cloud_Infrastructure) and [VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive).
