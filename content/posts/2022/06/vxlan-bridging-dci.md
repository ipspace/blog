---
title: "VXLAN-to-VXLAN Bridging in DCI Environments"
date: 2022-06-21 06:50:00
tags: [ VXLAN, data center, WAN ]
---
Almost exactly a decade ago I wrote that [VXLAN isn't a data center interconnect technology](/2012/11/vxlan-is-not-data-center-interconnect.html). That's still true, but you can make it a bit better with EVPN -- at the very minimum you'll get an ARP proxy and anycast gateway. Even this combo does not address the other requirements I listed a decade ago, but maybe I'm too demanding and _good enough_ works _well enough_.

However, there is one other bit that was missing from most VXLAN implementations: LAN-to-WAN VXLAN-to-VXLAN bridging. Sounds weird? Supposedly a picture is worth a thousand words, so here we go.
<!--more-->
Most VXLAN-with-EVPN implementations can handle a single unified  bridging domain -- an ingress VTEP sends traffic directly to an egress VTEP. 

{{<figure src="/2022/06/VXLAN-single-domain.jpg" caption="Single VXLAN domain stretched across multiple sites">}}

That works well in a data center environment but might result in two challenges when used over WAN links:

* You're probably using ingress replication (assuming you're not a great fan of enabling large-scale IP multicast), which means that every ingress ToR switch sends a separate copy of a flooded packet over the WAN link to every egress ToR switch in the remote data center. Not exactly what you'd like to see on your expensive WAN link, right?
* Switching ASICs support a limited number of VXLAN neighbors (usually 256) and a limited number of entries in the ingress replication list (usually 128). You might hit those limits when extending your VXLAN network across multiple sites[^NA]

Those challenges have a beautiful solution: VXLAN-to-VXLAN bridging between LAN and WAN bridging domains on the WAN edge switches:

* WAN edge switches act as final VXLAN VTEP for LAN and WAN peers. LAN peers do not need to care about VTEPs in remote sites. WAN peers do not need to care about local VTEPs.
* WAN edge switches receive a single copy of a flooded packet (from LAN or WAN side) and flood it further.

{{<figure src="/2022/06/VXLAN-hierarchy.jpg" caption="Hierarchical VXLAN with per-site bridging domains">}}

For more details, watch the excellent [Using VXLAN and EVPN in Multi-Pod and Multi-Site Fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) presentation by Lukas Krattiger, or read the [Multi-Domain EVPN VXLAN](https://www.arista.com/en/support/toi/eos-4-26-1f/14785-multi-domain-evpn-vxlan) document on Arista's web site (warning: regwall).

There's just a tiny little problem – the switching ASIC on the WAN edge devices has to implement VXLAN-to-VXLAN bridging which includes:

* Split-horizon forwarding: whatever is received from LAN peers should not be sent to WAN peers and vice versa
* Split-horizon flooding: whatever is received from LAN peers must be flooded to WAN peers and vice versa.
* No cheating with VXLAN VNI -- identification of LAN and WAN peers must be done based on source IP addresses, not based on different VNIs

For years, it looked like the only ASIC capable of doing VXLAN-to-VXLAN bridging was Cisco's Cloud Scale ASIC... until Arista decided that's a problem worth solving and figured out how to do it with Broadcom Jericho chipset. According to the [2022 EANTC test report](https://eantc.de/showcases/2022/mpls_sdn_interop.html), the VXLAN-to-VXLAN stitching also works on Juniper QFX10K and Nokia 7750 SR-1.

### More details

* Lukas Krattiger (and myself) talked about [multi-pod and multi-site fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) in _[Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)_ webinar.
* I mentioned VXLAN as a [potential layer-2 DCI transport technology](https://my.ipspace.net/bin/list?id=DCI#L2DCI) in _[Data Center Interconnects](https://www.ipspace.net/Data_Center_Interconnects)_ webinar.
* We discussed the [use of VXLAN and EVPN as DCI technologies](https://my.ipspace.net/bin/list?id=Design#2022_06) in June 2022 design clinic.

### Thank You

Remi Locherer sent me a nice email after the June 2022 design clinic saying "_your information is a bit outdated_" and included the link to 2022 EANTC test report and Arista documentation. I solemnly promise to augment those videos with _I was wrong_ callouts once I get them back from the editor.

[^NA]: Should that be the case, I'm hoping you're not designing your network based on generic blog posts. I'm trying to be less biased than [vendor white papers](/2022/06/beware-vendors-bringing-whitepapers.html), but if you have such a large network you're deep in the It Depends territory and need a proper network design.