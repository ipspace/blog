---
date: 2011-09-14 06:36:00+02:00
dmvpn_tag: routing
ospf_tag: dmvpn
tags:
- DMVPN
- OSPF
title: OSPF-over-DMVPN Using Two Hub Routers
url: /2011/09/ospf-over-dmvpn-using-two-hub-routers/
---
One of my readers sent me the following question a few days ago:

> Do you have a webinar that covers Dual DMVPN HUB deployment using OSPF? If so, which webinar covers it?

I told him that the [*DMVPN: From Basics to Scalable Networks*](https://www.ipspace.net/DMVPN) webinar covers exactly that scenario (and numerous others), describing both Phase 1 DMVPN and Phase 2 DMVPN design and implementation guidelines. Interestingly, he replied that the information on this topic seems to be very scant:
<!--more-->
> There is very little information about how to accomplish a dual hub, dual cloud DMVPN using OSPF. (\"Maybe for good reasons?\")

I can't see a good reason why you wouldn't do that (assuming you keep the [number of remote sites reasonably low](/2010/10/dmvpn-scalability/) and use a stub/NSSA area over DMVPN) and the "little information" part is definitely fixed in my DMVPN webinar. Even more, you get [twenty sets of tested router configurations](https://www.ipspace.net/DMVPN#Router_configurations), covering everything from simple OSPF/BGP/EIGRP/RIP/ODR designs to IPsec offload and Inter-AS MPLS/VPN over Phase 2 DMVPN.

Speaking of dual-hub designs, there is a slight gotcha: if you're running [Phase 1 DMVPN and using P2MP OSPF](/2011/01/ospf-configuration-in-phase-1-dmvpn/), it doesn't matter if you place both hub routers in the same DMVPN cloud. You're way better off putting each hub in its separate DMVPN cloud (and IP subnet) in [Phase 2 DMVPN](/2011/01/configuring-ospf-in-phase-2-dmvpn/) or you'll eventually get hit by the [NHRP convergence issues](/2011/05/nhrp-convergence-issues-in-multi-hub/) which can disrupt the DMVPN traffic for up to three minutes.
