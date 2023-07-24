---
date: 2011-01-20 07:02:00.002000+01:00
dmvpn_tag: design
tags:
- DMVPN
- VPN
title: "VPN Network Design: Selecting the Technology"
url: /2011/01/vpn-network-design-part-1.html
---
After all the [DMVPN-related posts](https://blog.ipspace.net/tag/dmvpn.html) I've published in the last days, we're ready for the [OSPF-over-DMVPN design challenge](https://blog.ipspace.net/2011/01/sometimes-you-need-to-step-back-and.html), but let's step back a few more steps and start from where every design project should start: deriving the technical requirements and the WAN network design from the business needs.

### Do I Need a VPN?

Whenever considering this question, you're faced with a buy-or-build dilemma. You could buy MPLS/VPN (or VPLS) service from a Service Provider or get your sites hooked up to the Internet and build a VPN across it. In most cases, the decision is cost-driven, but don't forget to consider the hidden costs: increased configuration and troubleshooting complexity, lack of QoS over the Internet and increased exposure of Internet-connected routers.
<!--more-->
In some cases, deploying a VPN-over-Internet solution forces you to buy more expensive equipment or additional software licenses. For example, you need just the IP Base functionality to connect an ISR G2 router to an MPLS/VPN cloud. If you want to implement your own IPsec- or DMVPN-based VPN, you need additional Security license, not to mention hardware encryption modules for sites having higher-speed links.

### Which VPN Technology Should I Use?

If you decide to build a VPN, your decision-making process does not stop. Cisco IOS offers you numerous combinations of GRE and IPSec, ranging from point-to-point GRE and crypto maps to DMVPN with tunnel protection or GETVPN. The questions you have to answer when selecting the VPN technology are:

-   Do I have to encrypt my VPN data?
-   Do I need to transport packets with private IP addresses across public IP infrastructure?
-   What are the redundancy requirements of the remote sites?
-   Do I need to run a routing protocol with the remote sites?
-   Is my network multi-protocol (is it running a combination of IPv4, IPv6 and MPLS)?

I'll focus on these questions in another post; you'll find an extensive discussion of their impact on your VPN design in the [Choose the Optimal VPN Service webinar](https://www.ipspace.net/Choose_the_optimal_VPN_service).

### DMVPN Phase 1, 2 or 3?

When you decide you want to implement your VPN with DMVPN, you still need to select one of the three available design/deployment paradigms (DMVPN Phase 1, 2 or 3).

The fundamental question you have to consider is the need for direct spoke-to-spoke traffic flow. If the spoke sites need to communicate directly, you need DMVPN Phase 2 or 3; if it's OK for the inter-spoke traffic to flow through the hub router, use simpler DMVPN Phase 1.

Be pragmatic: hub-and-spoke DMVPN Phase 1 might be the best solution even if your users claim they need spoke-to-spoke traffic, as long as the application exchanging data between the spoke sites is not latency-sensitive and the amount of inter-spoke traffic is low.

For example: Active Directory deployment does not require Phase 2 DMVPN. The amount of traffic exchanged between spoke sites is relatively low and AD is a TCP-based application and thus survives a bit of extra delay. VoIP is a different story; the latency introduced by the extra hop through the hub router might break the maximum latency limit.
