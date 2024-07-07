---
date: 2010-03-01 06:34:00.002000+01:00
tags:
- BGP
- MPLS VPN
- QoS
title: QPPB in MPLS VPN
url: /2010/03/qppb-in-mpls-vpn/
---
**TL&DR**: [QPPB](https://en.wikipedia.org/wiki/QPPB) works in MPLS VPNs... with a few limitations (at least in Cisco IOS implementation).

And now for the long story: A while ago I've noticed that my LinkedIn friend [Joe Cozzupoli](http://au.linkedin.com/in/jcozzupoli) changed his status to something like "trying to get QPPB to work in MPLS VPN environment". I immediately got in touch with him and he was kind enough to send me working configurations; not just for the basic setup, but also for Inter-AS Option A, B and C labs.

Knowing that QPPB relies on CEF, I doubted it would work as well on VRF interfaces as it does in pure IP environments, so I decided to do a few tests of my own. Here are the limitations I found:
<!--more-->
### QPPB in MPLS/VPN: Limitations

The following limitations apply to QPPB used in MPLS VPN environment:

-   QPPB can be used to classify CEF-switched IP packets. It can thus be used on ingress traffic entering PE router through a PE-CE interface. Egress (PE-to-CE) MPLS VPN traffic is label-switched and thus not classified by QPPB.

-   QPPB can also be used on ingress interfaces of Inter-AS option-A links (autonomous systems linked with numerous VRFs), but not when option-B or option-C are used (these options use label switching between ASBR PE-routers).

-   QPPB was developed before MPLS VPN functionality and its route-map processing was never upgraded to support extended BGP communities. The **match extcommunity** statement cannot be used in the **route-map** specified in the **table-map** BGP router configuration command; you have to use standard BGP communities.

## Configure QPPB in MPLS VPN environment

To configure QPPB in MPLS VPN environment, perform the following steps:

1.  Configure propagation of standard BGP communities between PE-routers in the VPNv4 address family.
2.  Mark target networks with BGP communities when inserting them in the VPNv4 BGP table on the egress PE-router.
3.  Configure a QPPB route-map that sets QoS groups based on BGP attributes on the ingress PE-router.
4.  Apply QPPB route-map to BGP routes in individual VRFs.
5.  Configure ingress QPPB on VRF interfaces.
6.  Configure MQC class maps and policy maps.
7.  Apply inbound MQC service policy to VRF interfaces.
