---
date: 2010-06-16 07:33:00+02:00
tags:
- MPLS
- IP routing
- WAN
title: BFD Has Reached RFC Status
url: /2010/06/bfd-has-reached-rfc-status.html
---
Bidirectional Forwarding Detection (BFD) protocol has finally been published as a series of RFCs. BFD gives you [quick failure detection between L3 hops](https://blog.ipspace.net/2008/11/bidirectional-forwarding-detection.html) (routers) regardless of the underlying technology and equipment (modems, media converters, bridges). It's been gradually introduced in Cisco IOS during the last few years; release 15.0M and 12.2SRE contain almost everything you'll ever need (missing: multihop BGP support and MPLS LSP support).

I wrote about BFD in *Improve the Convergence of Mission-Critical Networks with Bidirectional Forwarding Detection (BFD)* article (you'll find it somewhere in [this list](/kb/Internet/)). To learn more, read the RFCs in this order:
<!--more-->
-   [When, where and how should BFD be used (RFC 5882)](http://tools.ietf.org/html/rfc5882). This one is mandatory; it gives you a good overview of what BFD can and cannot do as well as where and how to use it.
-   [BFD: the protocol (RFC 5880)](http://tools.ietf.org/html/rfc5880). The protocol description. Not as boring as some other protocol descriptions are. If you want to understand how the *Echo* function works, make sure you read this one.
-   [BFD for single-hop IPv4 and IPv6 (RFC 5881)](http://tools.ietf.org/html/rfc5881). The dirty details of using BFD for single-hop IPv4 and IPv6 failure detection.
-   [Multihop BFD (RFC 5883)](http://tools.ietf.org/html/rfc5883). Extensions to RFC 5881 needed to support BFD in multihop scenarios (IBGP sessions, multihop EBGP sessions, OSPF virtual links).
-   [BFD for MPLS LSP (RFC 5884)](http://tools.ietf.org/html/rfc5884). This one allows you to test PE-to-PE forwarding path. Ideal for very quick rerouting around data-plane failures in MPLS VPN networks (not implemented in IOS yet).
-   [BFD for pseudowires (RFC 5885)](http://tools.ietf.org/html/rfc5885). Allows you to test data-plane consistency of pseudowires established across your MPLS network.
