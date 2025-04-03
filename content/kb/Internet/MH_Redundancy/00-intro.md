---
kb_section: MH_Redundancy
minimal_sidebar: true
title: Redundant Small Site Multihoming
toc_title: Introduction
url: /kb/Internet/MH_Redundancy/
tags: [ Internet ]
date: 2025-04-11 07:34:00+0100
alt_section: posts
index: true
---
The original *[Small Site Multihoming](/kb/Internet/MH_SOHO/)* article has generated many responses, most of them being questions about the redundant implementation of the same principles. In this article, we’ll thus add a second customer router to add redundancy to the small site multi-homing design. The final design will still retain the administrative simplicity of the original solution – with no need to own public IP address space, autonomous system number, or to run Border Gateway Protocol (BGP).
<!--more-->
{{<note migrated>}}
* This article was written in 2007 and has been updated and republished on ipSpace.net in April 2025. I also recreated the router configurations on a more recent version of Cisco IOS-XE using Ethernet uplinks.
* You wouldn't believe it, but I've seen a Fortune 100 company using an almost identical design on their headquarters site (using firewalls instead of routers as the WAN edge devices).
{{</note>}}

The basic design of a redundant multihomed small site is very similar to the one described in the IP Corner article *[Small Site Multihoming](/kb/Internet/MH_SOHO/)* (I would strongly suggest you read that article before this one). The public IP addresses used by the site are still within the address space of the two service providers, and the private IP addresses are used within the site. Each gateway router performs independent Network Address Translation (NAT) from the private IP addresses to the public IP address pool (or a single IP address) assigned by the ISP.

{{<figure src="/kb/Internet/MH_Redundancy/Redundant Multihoming_1.jpg" caption="IP addressing in a small multihomed site">}}

Static default routes are configured on both gateway routers. The availability of the primary default route depends on the tracked object configured on GW-A (see the section *[Not-so-Very-Static-Routes](/kb/internet/mh_soho/30-not-so-static/)* in the [Small Site Multihoming](/kb/Internet/MH_SOHO/) article); GW-B uses a floating static default route. The static default routes are redistributed into a dynamic routing protocol to ensure that both gateway routers (as well as any other additional router within the site) have the same view of the Internet connectivity:

{{<figure src="/kb/Internet/MH_Redundancy/Redundant Multihoming_2.jpg" caption="Static default routing">}}

Due to the gateway routers performing NAT, the return traffic is always handled correctly regardless of the outgoing packet's path. For example, if the outgoing packet is forwarded by GW B, the NAT performed by the gateway router would replace the source IP address with the IP address assigned by ISP B; the return packet would thus automatically take the path through ISP B (Figure 3).

{{<figure src="/kb/Internet/MH_Redundancy/Redundant Multihoming_3.jpg" caption="Symmetrical routing with NAT">}}

Although NAT solves the return path problem, the solution is not perfect. For example, if the traffic is flowing over the backup link and the primary link is reestablished, all the traffic will be shifted to the primary link (regardless of the TCP session status), resulting in a different public source IP address, and the workstations will lose all TCP sessions established at the switchover moment.
