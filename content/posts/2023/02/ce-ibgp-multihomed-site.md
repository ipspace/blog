---
date: 2023-02-15 07:13:00+00:00
multihoming_tag: bgp
series:
- multihoming
tags:
- BGP
- design
- WAN
title: CE-to-CE IBGP Session in a Multihomed Site
---
One of my readers sent me a question along these lines:

> Do I have to have an IBGP session between Customer Edge (CE) routers in a multihomed site if they run EBGP with the upstream provider(s)?

Let's start with a simple diagram and a refactoring of the question:
<!--more-->
{{<figure src="/2023/02/ce-ibgp-l2.png">}}

* A multihomed site has two WAN edge (CE) routers
* Each CE-router runs EBGP with the adjacent PE-router.
* Do we need an IBGP session between CE-A and CE-B?

{{<note info>}}Please note that it doesn't matter if we're talking about an MPLS/VPN- or a redundant Internet access deployment. There's no difference between the two scenarios from the CE-router perspective.{{</note>}}

Our multihomed site is small enough to have a single L2 switch, and both CE-routers act as a default gateway for the attached hosts[^FHRP]. Now imagine a scenario where:

[^FHRP]: Ignoring for the moment the [intricacies of first-hop redundancy protocols](/2023/02/irb-edge-routing.html) and [ICMP redirects](/2022/11/what-causes-icmp-redirects.html).

* CE-A receives a routing update for destination X from its upstream PE-router, but CE-B receives no corresponding update from its EBGP peer.
* A host sends a packet for X toward CE-B.

It's obvious that CE-B should have the information that it can reach X via CE-A, and there are two ways to achieve that:

1. Exchange the information over an IBGP session between CE-A and CE-B
2. Redistribute EBGP information into an IGP (for example, OSPF)

As you might be running an IGP within the site and redistribute IGP information into EBGP anyway, you'll quickly land in a two-way redistribution morass if you choose option#2. Running IBGP between CE-routers is a much better approach, and gives you the ability to have site-wide consistent routing policy. For example, you could use BGP local preference to indicate which paths should be preferred[^IGPJS], causing the other CE-router to prefer IBGP paths over EBGP ones.

Finally a word of caution: establishing an IBGP session between CE-routers that do not support [RFC 8212](https://www.rfc-editor.org/rfc/rfc8212) could turn your site into a transit site. Not fun if you happen to be a [steel manufacturer attracting Cloudflare traffic](/2019/07/rant-some-internet-service-providers.html). Make sure you have deployed outbound AS-path filters dropping transit paths on all EBGP sessions.

### More Details

* [Consistent routing within a multihomed site](https://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN) is one of the [Expert Express Case Studies](https://www.ipspace.net/ExpertExpress_Case_Studies) (disguised as an "MPLS/VPN + IPsec" question)
* We discussed redundant BGP-based Internet access in [September 2022](https://my.ipspace.net/bin/list?id=Design#2022_09) session of ipSpace.net Design Clinic. In the same session we also discussed [secure multi-homed customer BGP configurations](https://my.ipspace.net/bin/get/Design/22.09.05%20-%20Securing%20Multi-Homed%20Customer%20BGP%20Configuration.mp4?doccode=Design).
* We'll do a deep dive into securing BGP routing (including a brief history of well-known global routing FUBARs) in the [Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security) webinar.

[^IGPJS]: Obviously you could also use a route map to set tags or metrics in OSPF type-5 LSA when doing BGP-to-OSPF redistribution, and use that information to set administrative distance of OSPF routes (assuming your device can do something as abhorrent as that) if your primary design goal is to have infinite job security.