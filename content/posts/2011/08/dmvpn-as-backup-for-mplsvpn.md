---
date: 2011-08-25 05:30:00+02:00
dmvpn_tag: design
tags:
- DMVPN
- OSPF
- BGP
- MPLS VPN
title: DMVPN as a Backup for MPLS/VPN
url: /2011/08/dmvpn-as-backup-for-mplsvpn.html
---
*SK* left a long comment to my [*More OSPF-over-DMVPN Questions*](https://blog.ipspace.net/2011/08/more-ospf-over-dmvpn-questions.html) post describing a scenario I find quite often in enterprise networks:

-   Primary connectivity is provided by an MPLS/VPN service provider;
-   Backup connectivity should use DMVPN;
-   OSPF is used as the routing protocol;
-   MPLS/VPN provider advertises inter-site routes as external OSPF routes, making it hard to properly design the backup connectivity.

If you're familiar with the way MPLS/VPN handles OSPF-in-VRF, you're probably already asking the question "how could the inter-site OSPF routes ever appear as E1/E2 routes?"
<!--more-->
The reason is quite simple: some service providers deploy their own CE-routers (see the diagram below, this time drawn with an [improved version of the diagramming tool](http://notepad-plus-plus.org/)):

{{<ascii>}}
Hub-------DMVPN--------------Spoke
 !                             !
 !                             !
HCE--SPCE--PE--MPLS--PE-SPCE—SCE
{{</ascii>}}

The MPLS/VPN SP deploying its own CE-routers commonly runs EBGP between PE- and CE-routers and deploys OSPF only between its CE-routers (SPCE) and customer's CE-routers (HCE and SCE). In this setup, the OSPF-specific MPLS/VPN attributes carried in MP-BGP are lost on the PE-CE router boundary and cannot be used to recreate the original OSPF route when the IP prefix is redistributed from BGP into OSPF on the provider's CE-router. All inter-site routes thus appear as E1 or E2 routes in OSPF.

If you decide to run OSPF across the DMVPN cloud, the inter-site routes received over DMVPN will appear as intra-area or inter-area OSPF routes, making them more preferred than the MPLS/VPN routes (which should provide primary connectivity). Unless you want to be like [Tom Cruise](http://en.wikipedia.org/wiki/Mission:_Impossible_(film)) or [MacGyver](http://en.wikipedia.org/wiki/MacGyver) (who would indubitably find a solution involving duct tape, NAT, PBR and GRE), you have only two options:

**Run a third routing protocol over DMVPN** and redistribute it into OSPF with cost worse than the MPLS/VPN E1/E2 routes. Obviously you need to redistribute per-site OSPF routes into both protocols and you don't know what the SP CE-routers are doing, which makes this design a nice two-way redistribution challenge worthy of the CCIE lab.

**Give up on OSPF and run EBGP everywhere**. Run EBGP between your CE-routers and SP's CE-routers as well as over DMVPN (making the MPLS/VPN routes directly comparable to DMVPN routes) and use local preference to implement the routing policy you want. Obviously you'd still need to run OSPF within each site and IBGP between all site transit routers.

For more details, read the _[Integrating DMVPN-based Internet VPN with MPLS/VPN WAN](https://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN)_ case study.
