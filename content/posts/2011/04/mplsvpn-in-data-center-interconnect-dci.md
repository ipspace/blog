---
date: 2011-04-14 10:02:00+02:00
tags:
- data center
- MPLS VPN
- design
title: MPLS/VPN in Data Center Interconnect (DCI) Designs
url: /2011/04/mplsvpn-in-data-center-interconnect-dci/
---
Yesterday I was [describing a dreamland in which hypervisor switches would use MPLS/VPN](/2011/04/vcloud-architects-ever-heard-of-mpls/) to implement seamless scalable VM mobility across IP+MPLS infrastructure. Today I'll try to get down to earth; there are exciting real-life design using MPLS/VPN between data centers. You can implement them with Catalyst 6500/Cisco 7600 or ASR1K and will soon be able to do the same with Nexus 7000.

Most data centers have numerous security zones, from external network, DMZ, web servers and applications servers to database servers, IP-based storage and network management. When you design active/active data centers, you want to keep the security zones strictly separate and the "usual" solution proposed by L2-crazed crowd is to bridge multiple VLANs across the DCI infrastructure (in the next microsecond they start describing the beauties of their favorite L2 DCI technology).
<!--more-->
If you have well-designed applications that don't need L2 interconnect to scale out and you don't rely too heavily on [brokenware from Microsoft](/2012/02/microsoft-network-load-balancing-behind/), you can solve the *end-to-end path isolation* challenge (that's the buzzword you'll find in Cisco's design documents) with VRFs or full-blown MPLS/VPN. VRFs are simpler to implement, but don't scale well: you define multiple VRFs in the DC edge routers, one per security zone, multiple VLANs across DCI link (which has to provide layer-1 or layer-2 transport) and link each VRF to one of the DCI VLANs. While you're still using VLANs on the DCI link, they just provide isolation on the DCI link; they are routed and not bridged into the data center cores.

{{<figure src="/2011/04/s1600-DC_MPLSVPN_VLAN.png" caption="VLAN encapsulation on DCI link terminated in VRFs">}}

To make your design scale (as well as to avoid excessive VLAN usage and numerous instances of routing protocols running on inter-DC link), you can go for full-blown MPLS/VPN implementation, with MPLS labeling between DC edge routers. This design still needs layer-1 or layer-2 inter-DC transport, but no longer needs VLANs (path isolation is provided by MPLS labels).

{{<figure src="/2011/04/s1600-DC_MPLSVPN_Label.png" caption="MPLS/VPN over DCI link">}}

Going even further, you can use MPLS/VPN over point-to-point GRE tunnels with Catalyst 6500 or ASR1K to transport labeled packets across generic IP infrastructure, allowing you to retain perfect isolation between security zones while using any infrastructure that your chosen SP decides to sell you (including MPLS/VPN or even public Internet \... not that I would use the latter for inter-DC connectivity).

{{<figure src="/2011/04/s1600-DC_MPLSVPN_IP.png" caption="MPLS/VPN over GRE tunnels">}}

Last but definitely not least, ASR1K (IOS XE release 3.1S and above) or Cisco 7600 (IOS release 12.2(33)SRE) support MPLS/VPN over mGRE (official name of the feature is [L3VPN over mGRE](http://www.cisco.com/en/US/docs/ios/interface/configuration/guide/ir_mplsvpnomgre.html)), giving you a clean design and configuration with no point-to-point GRE tunnels.

The only hurdle you have to overcome to start using these design is the subconscious fear of the unknown (and the complexity FUD spread around MPLS/VPN technology). My webinars might be a good starting point:

* I'm describing all the designs mentioned here in the [*Data Center Interconnects*](http://www.ipSpace.net.info/DCI) webinar
* In the [*Enterprise MPLS/VPN Deployment*](http://www.ipspace.net/EnterpriseMPLS) webinar you'll get exposed to typical MPLS use cases in enterprise networks, the underlying technology and high-level design and implementation guidelines. 
