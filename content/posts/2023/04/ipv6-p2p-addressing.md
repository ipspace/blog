---
title: "IPv6 Addressing on Point-to-Point Links"
date: 2023-04-18 06:15:00
tags: [ IPv6 ]
---
One of my readers sent me this question:

> In your observations on IPv6 assignments, what are common point-to-point IPv6 interfaces on routers?  I know it always depends, but I'm hearing /64, /112, /126 and these opinions are causing some passionate debate.

(Checks the calendar) It's 2023, [IPv6 RFC](https://www.rfc-editor.org/rfc/rfc2460) has been published almost 25 years ago, and there are still people debating this stuff and confusing those who want to deploy IPv6? No wonder we're not getting it deployed in enterprise networks ;)
<!--more-->
{{<tldr model="ChatGPT GPT-4">}}IPv6 prefix length debates persist, but key recommendations are to use /64 for consistent prefix sizes or /127 for point-to-point links. Utilize infrastructure ACLs to block external access to infrastructure IPv6 subnets for security. Be mindful of potential hardware limitations when using prefixes longer than /64.{{</tldr>}}

For people who would love to get a job done (as opposed to appear smart), several organizations published "_this is how you do IPv6 addressing_" documents:

* RIPE _[Create an Addressing Plan](https://www.ripe.net/publications/ipv6-info-centre/deployment-planning/create-an-addressing-plan)_ document contains recommendations for service providers requesting IPv6 address allocation plus links to several other documents.
* SURFnet [Preparing an IPv6 Addressing Plan Manual](https://www.ripe.net/support/training/material/IPv6-for-LIRs-Training-Course/Preparing-an-IPv6-Addressing-Plan.pdf) covers most things one needs to know, including the _use /64 everywhere_ recommendation.
* ISOC [IPv6 Address Planning: Guidelines and Resources](https://www.internetsociety.org/resources/deploy360/2013/ipv6-address-planning-guidelines-for-ipv6-address-allocation/) document goes even deeper. Definitely worth reading.
* NANOG had a _Best Current Operational Practices_ site which included IPv6 subnetting, but it looks like it disappeared.

The above documents should answer any questions you might have on IPv6 addressing, but if you insist on discussing prefix lengths, let's do it:

* /64 is the way to go if you want to have consistent prefix sizes on all subnets. There you have it; you can stop reading.
* /112 is an unusual suggestion[^PC]. I would love to hear the arguments for using it (or maybe not).
* /126 is probably recommended by people who are not aware of /127 being the right answer[^HIP] (due to [RFC 6164](https://www.rfc-editor.org/rfc/rfc6164)[^6164]) if you're worried about the neighbor discovery (ND) cache exhaustion denial-of-service attacks. Please don't tell me you're considering /126 prefixes to conserve the address space.
* As recommended by [RFC 7404](https://www.rfc-editor.org/rfc/rfc7404.html), link-local-only IPv6 interfaces might be a perfect solution for intra-AS P2P links, and if you bought your data center gear from a vendor interested in operational simplicity you could run EBGP over those interfaces with absolutely no hassle. OSPFv3 and IS-IS work just fine with IPv6 LLA on [every device I tested in _netlab_](https://netsim-tools.readthedocs.io/en/latest/platforms.html#supported-configuration-modules).

[^HIP]: On a more serious note, using /126 prefixes is as valid as using /127 prefixes, it's just not cool enough ;)

[^PC]: I'm trying to be diplomatic and politically correct these days. I would use a slightly different wording in private conversations.

[^6164]: Here's a funny story: There was an [RFC published in 2003](https://www.rfc-editor.org/rfc/rfc3627) saying "/127 prefix considered harmful" until [another RFC came along](https://www.rfc-editor.org/rfc/rfc6164) saying "/127 is the way to go", so they [needed a third RFC](https://www.rfc-editor.org/rfc/rfc6547) saying "the first one is obsoleted by the second one." Dotting the I-s and crossing the T-s is important ;)

### Off-Topic: ND Cache Exhaustion DoS Attack

Just in case you're not aware what I'm talking of: an intruder could scan billions of addresses in an /64 prefix, triggering a neighbor discovery process for every one of them on the directly-attached (last hop) router. That process would burn CPU cycles and consume hardware resources and (if the attack persists) could result in severe connectivity failures once the existing ND entries time out or can't be refreshed due to control-plane policing.

The obvious solution you OUGHT TO[^YRS] use are infrastructure ACLs that block external access to infrastructure IPv6 subnets. Obviously you'd have to deploy them on all network edge interfaces and be consistent about that (I've heard automation helps). However, there were rumors ages ago that some vendor's hardware started ND process in parallel with ingress ACL check -- while an ingress ACL dropped the offending packet(s), neighbor discovery proceeded to waste the resources. Lovely ;)

For more details watch the [Network Security Fallacies](https://my.ipspace.net/bin/list?id=Net101#NETSEC) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.

[^YRS]: See [RFC 6919](https://www.rfc-editor.org/rfc/rfc6919) for details

### Back to Prefix Sizes on P2P Links

Anyway, while I understand the reasons behind recommending /127 (or /126) on P2P links, that recommendation does have its drawbacks. Data center switches[^FG] cut down on lookup table requirements by assuming that most IPv6 prefixes are /64 (or larger) so each prefix needs just 64 bits (or two IPv4 prefix entries) in the prefix lookup table. For example, Broadcom ASICs support only a small (configurable) amount of IPv6 prefixes longer than /64. I have no idea what happens when your routing table has more of them. Software-based switching? That would be a bonanza for a would-be attacker ;)

[^FG]: And other forwarding great that cannot afford to be reassuringly expensive.

Based on the potential problems /127 prefixes might cause, some people advocate allocating each /127 out of a distinct /64 to ensure you can quickly switch back to having /64s on every link. 
Similarly, I've heard ideas to use /120 (yet again, each /120 coming from a different /64) on server VLANs that don't use SLAAC[^MC] to prevent ND attacks on server VLANs.

### More to Explore

I'm pretty sure I mentioned these details in [some IPv6 webinar](https://www.ipspace.net/IPv6), and we might have covered them in the [October 2021 Design Clinic](https://my.ipspace.net/bin/list?id=Design#2021_10).

[^MC]: That probably won't play well with merchant silicon, but it definitely looks great in blog posts and PowerPoints.
