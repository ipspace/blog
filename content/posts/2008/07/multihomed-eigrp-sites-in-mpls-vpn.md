---
date: 2008-07-02 07:07:00+02:00
tags:
- EIGRP
- BGP
- MPLS VPN
title: Multihomed EIGRP Sites in MPLS VPN Network
url: /2008/07/multihomed-eigrp-sites-in-mpls-vpn.html
---
Deploying EIGRP as the PE-CE routing protocol in MPLS VPN networks is easy if [all sites have a single PE-CE link and there are no backdoor links between the sites](/2008/06/simple-eigrp-in-mpls-vpn-networks.html). Real life is never as simple as that; you have to cope with various (sometimes undocumented) network topologies. Even that would be manageable if the customer networks would have a clean addressing scheme that would allow good summarization (that happens once in a blue moon) or if the MPLS VPN core could announce the default route into the EIGRP sites (wishful thinking; the customer probably has one or more Internet exit points).

In the end, you're left with two-way route redistribution between core MP-BGP and edge EIGRP, resulting in nightmarish scenarios (probably a good half of the blog posts of the CCIE candidates talk about redistribution horrors). Fortunately, Cisco implemented two extra features supporting EIGRP-to-MP-BGP redistribution: BGP cost community and BGP Site-of-Origin. I described them both in an article that is long gone; [its shadow has been preserved on archive.org](https://web.archive.org/web/20151121114235/http://wiki.nil.com/Multihomed_MPLS_VPN_sites_running_EIGRP).

{{<ct3_query>}}
