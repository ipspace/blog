---
date: 2011-05-26 09:35:00+02:00
tags:
- workshop
- MPLS VPN
- virtualization
title: MPLS/VPN Transport Options
url: /2011/05/mplsvpn-transport-options.html
---
Jason sent me an interesting question a few days ago: "*assuming a* [*vSwitch \*did\* support MPLS/VPN PE router functionality*](/2011/04/vcloud-architects-ever-heard-of-mpls.html)*, what type of protocol support would be needed on the access layer switches?*"

While the MPLS/VPN support in hypervisor switches remains in the realm of science fiction, it's worth knowing that there are at least five different transport options you can use between PE-routers. Here they are, from the most decoupled to the most tightly coupled ones:
<!--more-->
{{<note update>}}**Update 2020-12-26**: This discussion is mostly academic. Since this blog post has been written everyone went down VXLAN/GENEVE path using IP transport in fabric core and Ethernet-over-something encapsulation on ToR switches or hypervisor virtual switches.{{</note>}} 

**MPLS/VPN-over-mGRE**. PE routers send VPN traffic + MPLS labels encapsulated in GRE datagrams directly to BGP next hops (see RFC 4023 for details). The core network has to provide IP connectivity (or just L2 connectivity assuming the number of PE routers is small enough).

**One-hop MP-BGP session on directly connected subnet**. Ingress PE-router does not need a label switched path (LSP) to send an MPLS frame to a directly-connected egress PE-router; it can create an MPLS frame solely from the VPN label assigned by the egress PE-router.

That's how Inter-AS MPLS/VPN Option B works; the same trick also works for IBGP sessions although it does generate a warning message on Cisco IOS.

In a data center environment, all PE-routers would have to belong to the same layer-2 (bridged) domain. However, they wouldn't have to run IGP (they could behave as IP hosts).

**One-hop MP-BGP session between loopback interfaces**. PE-routers attached to the same L2 subnet don't need P-routers even when you configure IBGP sessions between their loopback interfaces.

This design has serious scalability problems (and is thus largely useless) -- PE-routers have to advertise their loopback interfaces in IGP and they have to establish a full mesh of LDP sessions just to exchange null labels for their loopback interfaces.

**Full-blown MPLS network with P-routers**. In this scenario, the PE-routers and P-routers run IGP (OSPF comes to mind in a data center environment) and exchange MPLS labels with LDP. PE-routers *must* run IBGP sessions between loopback interfaces (running BGP sessions between LAN interfaces of PE-routers would break end-to-end LSP due to premature penultimate hop popping).

PE-routers and P-routers don't have to be directly connected. You could use L2 ToR switches and MPLS-enabled core switches. MPLS traffic between PE-routers and the core switches would be bridged; MPLS traffic traversing a core switch would use LFIB in the core switch.

**MPLS network with traffic engineering**. You can transport MPLS/VPN traffic over MPLS TE tunnels established directly between PE-routers, between core P-routers or between PE-routers and P-router.

There aren't too many data center switches supporting MPLS TE, so this design remains "somewhat" academic from the data center perspective.

### Summary

The minimum requirement for access-layer switches supporting MPLS/VPN-capable vSwitch is layer-2 connectivity (bridging). L3 access switches can be used if the PE-routers support MPLS/VPN-over-mGRE transport, otherwise the L3 devices have to support LDP (or MPLS/TE) and MPLS forwarding.
