---
date: 2011-02-02 06:27:00.005000+01:00
dmvpn_tag: integrate
tags:
- DMVPN
- workshop
- MPLS VPN
- QoS
title: End-to-End QoS marking in MPLS/VPN-over-DMVPN networks
url: /2011/02/end-to-end-qos-marking-in-mplsvpn-over/
---
I got a great question in one of my [Enterprise MPLS/VPN Deployment](http://www.ipspace.net/EnterpriseMPLS) webinars when I was describing how you could run MPLS/VPN across DMVPN cloud:

> That sounds great, but how does end-to-end QoS work when you run IP-over-MPLS-over-GRE-over-IPSec-over-IP?

My initial off-the-cuff answer was:

> Well, when the IP packet arriving through a VRF interface gets its MPLS label, the IP precedence bits from the IP packet are copied into the MPLS EXP (now TC) bits. As for what happens when the MPLS packet gets encapsulated in a GRE packet and when the GRE packet is encrypted... I have no clue. I need to test it.
<!--more-->
Finally I found some time to do proper lab tests. I fired up one of my MPLS/VPN-over-DMVPN labs, turned one of the remote site routers (R1A in the following diagram) into a traffic source host (by disabling all its interface but its LAN interface) and started my tests.

{{<figure src="/2011/02/s1600-ADV_PhaseI_MPLSVPN_Topology.png" caption="Lab topology">}}

**MPLS label imposition**. The default behavior of Cisco IOS is to copy IP precedence bits (the upper part of DSCP value) into MPLS EXP (aka TC) bits during label imposition.

You can change the default behavior by specifying the desired value in a **policy-map** that you apply as *inbound* **service-policy** on the VRF interface (VPN label imposition seems to be conceptually tied to the incoming VRF interface, not the outgoing MPLS interface). For example, to ignore the IP precedence bits on untrusted interfaces and set MPLS EXP/TC bits to zero, use the following QoS service policy:

``` {.code}
policy-map SetMPLSExp
 class class-default
  set mpls experimental imposition 0
!
interface FastEthernet0/0
 ip vrf forwarding VPN
 ip address 172.16.10.2 255.255.255.0
 service-policy input SetMPLSExp
```

{{<note>}}The need to configure *inbound* service policy surprised me (I wanted to configure *outbound* service policy on the DMVPN interface), but is actually a great solution: you can apply different policies to different VRF interfaces and trust IP precedence markings on per-interface basis.{{</note>}}

**Propagation of MPLS EXP bits into GRE/IPSec headers**. I was pleasantly surprised to find out that the MPLS EXP bits get copied into IP precedence bits of the GRE envelope with no extra configuration. As I'm always using IPSec in transport mode in DMVPN designs, IPSec encryption does not touch the IP header (including IP precedence) and thus we get the desired end-to-end IP precedence markings with minimal efforts.
