---
date: 2020-06-16 06:23:00+00:00
dcbgp_tag: design
evpn_tag: intro
series:
- dcbgp
series_weight: 500
tags:
- EVPN
- VPN
- MPLS
title: 'EVPN: The Great Unifying Theory of VPN Control Planes?'
---
I claimed that “*EVPN is the control plane for layer-2 and layer-3 VPNs*” in the *[Using VXLAN and EVPN to Build Active-Active Data Centers](/2018/11/interview-active-active-data-centers/)* interview a long long while ago and got this response from one of the readers:

> To me, that doesn’t compute. For layer-3 VPNs I couldn’t care less about EVPN, they have their own control planes.

Apart from EVPN, there’s a single standardized scalable control plane for layer-3 VPNs: BGP VPNv4 address family using MPLS labels. Maybe EVPN could be a better solution (opinions differ, see [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar for more details).
<!--more-->
> For layer-2 VPNs (Carrier Ethernet) I couldn’t care less either.

The L2VPN control plane protocols are a total mess. Either you’re working exclusively on layer-2 with Ethernet switches (have fun), or you had to use MPLS with LDP or BGP to build E-LAN meshes.

EVPN is an attempt at the great unifying theory of control plane protocols. It can carry MAC address, so it’s useful as L2VPN control plane. It can also carry IPv4/IPv6 prefixes, so it can be used as L3VPN control plane. As a bonus, it can also carry IPv4/IPv6 addresses (host routes), so you can use it to build a routed VPN (VPN forwarding on IPv4/IPv6 addresses instead of MAC addresses) that looks like an E-LAN but scales much better.

> It looks different for VXLAN though, as layer-2 and layer-3 are mixed (transport of layer-2 over layer-3). That is the instance, where EVPN can be the control plane for layer-2 and layer-3.

Don’t conflate data plane encapsulation with VPN service or VPN control plane.

Prior to VXLAN/Geneve you could use these standard-based implementations to build L2VPN service: QinQ, PBB (including SPBM), TRILL (rarely), or MPLS (which makes it possible to run L2VPN and L3VPN on shared MPLS backbone).

If you wanted to build a VPN on top of IP infrastructure you could choose between IPsec-based solutions, running MPLS over GRE or UDP, or the granddaddy of layering: [Ethernet-over-MPLS-over-GRE-over-IPsec-over-UDP-over-IP](/2011/03/mplsvpn-over-gre-over-ipsec-does-it/).

VXLAN added an interesting option: transporting Ethernet frames across IP backbones using a simpler encapsulation stack. Whether you use that encapsulation stack with EVPN, with controller-based data-plane programming, or static configuration is a totally different question.

On the other hand, EVPN can work with a dozen data-plane encapsulations, including MPLS, VXLAN, MPLS-over-whatever, NVGRE, Geneve… It has a mechanism to signal what encapsulation to use for what next hop (not that I would want to use more than one encapsulation in my network).

Do I expect VXLAN and/or EVPN to replace all other technologies I mentioned above? Probably not; COBOL programmers are still making a decent living. Traditional L3VPN (RFC 4364) will be around for a very long time and might be a bit more optimal than EVPN when used to implement a pure L3VPN. We’ll keep seeing MPLS in transport backbones for ages… but we might see modern backbones like [Packet Fabric](/2017/06/packet-fabric-on-software-gone-wild/) built with minimum complexity:

* Simple IP routing protocol potentially augmented with traffic engineering when needed… but see also [Terastream ideas](/2013/11/deutsche-telekom-terastream-designed/).
* Simplest possible encapsulation stack (VXLAN)
* Single VPN control plane protocol (EVPN).

## More to Explore

* If you want to build EVPN-based transport fabrics, you’ll find tons of details in the [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar
* If all you need is a simple VPN to transport your company’s data, [Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service) webinar might be exactly what you need.
