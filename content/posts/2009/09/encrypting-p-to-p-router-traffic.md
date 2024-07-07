---
date: 2009-09-23 07:17:00.002000+02:00
tags:
- IPsec
- MPLS VPN
title: Encrypting P-to-P-router traffic
url: /2009/09/encrypting-p-to-p-router-traffic/
---
Rob sent me a really good question:

> I have an enterprise MPLS network. Two P routers are connected via carrier point-to-point Gigabit Ethernet and I would like to encrypt the MPLS traffic traversing the GE link. The PE-routers don\'t have hardware crypto accelerators, so I would like to keep the MPLS within the buildings running in cleartext and only encrypt the inter-site (P-to-P) MPLS traffic.

The only solution I could imagine would nicely fit the motto of one of our engineers: »Any time you have a problem, use more GRE tunnels« (if you have a better solution, please post it in the comments).
<!--more-->
As far as I understand Cisco\'s IPSEC implementation, IOS can encrypt only IP traffic. If you want to encrypt MPLS frames forwarded by a P-router, you have to convert them back to IP... and the only way to convert MPLS frames back into IP without losing the whole label stack which is vital to proper operation of MPLS VPN is to encapsulate them in a GRE tunnel and encrypting the MPLS-over-GRE traffic.

The \"obvious\" problem of this setup (apart from performance hit) is the MTU issue: the MTU on the GE link has to be high enough to support all the extra overhead on top of the 1500-byte payload. If that\'s not the case, you have to lower the MTU on the tunnel interface to ensure the GRE packets are not fragmented -- that would kill the receiving router.
