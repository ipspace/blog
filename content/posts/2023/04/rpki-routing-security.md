---
title: "Should I Care About RPKI and Internet Routing Security?"
date: 2023-04-12 06:46:00
tags: [ BGP, security ]
---
One of my subscribers sent me this question:

> I'm being asked to enter a working group on RPKI and route origination. I'm doing research, listening to Jeff Tantsura, who seems optimistic about taking steps to improve BGP security vs Geoff Huston, [who isn't as optimistic](https://www.potaroo.net/ispcol/2022-12/securedrouting.html). Should I recommend to the group that the application security is the better investment?

You need both. RPKI is slowly becoming the baseline of global routing hygiene (like washing hands, only virtual, and done once every blue moon when you get new IP address space or when the certificates expire). More and more Internet Service Providers (including many tier-1 providers) [filter RPKI invalids](https://www.manrs.org/netops/participants/) thus preventing the worst cases of unintentional route leaks.
<!--more-->
{{<note info>}}Things will get even better when we start using ASPA and eventually BGPsec. For a good overview of the differences between the two read the [Fastly comments to FCC Secure Internet Routing inquiry](https://sobornost.net/~job/fastly-fcc-noi-secure-internet-routing-reply-comments-20220510-201259363-pdf.pdf) by Job Snijders.{{</note>}}

If you’re providing content or e-commerce services from your own infrastructure, you SHOULD read and implement [MANRS recommendations for CDN/cloud providers](https://www.manrs.org/cdn-cloud-providers/), in particular if you care about a clueless fat-fingered router configurator accidentally advertising your IP address space (even better: [more-specific prefixes](/2019/07/rant-some-internet-service-providers/)) to the global Internet.

If you’re an ISP, then you MUST consider [MANRS for Network Operators](https://www.manrs.org/netops/). Obviously you could also pretend you don't need Internet routing security and blame everyone else[^T1] (as in: The Internet is down today)... until your customers discover The Internet still works for everyone using your competitor.

[^T1]: That strategy worked extremely well for some tier-1 providers in the past. See also: [YouTube hijack](https://www.ripe.net/publications/news/industry-developments/youtube-hijacking-a-ripe-ncc-ris-case-study).

Regardless of what your motivation might be, using RPKI will make the global routing infrastructure more secure -- we might have to deal with fewer unintentional leaks and successful hijacks. Widespread implementation of MANRS guidelines would also reduce source IP address spoofing. Ideally, we'd get to a strict global clampdown on source IP address spoofing, but I don't expect to see that in my lifetime[^LT].

[^LT]: I also didn't expect to have a reasonable conversation with an AI bot, so feel free to apply [Clarke's First Law](https://en.wikipedia.org/wiki/Clarke%27s_three_laws).

Unfortunately, infrastructure security won’t help much when another botnet exploits clueless organizations who can’t be bothered to configure ACLs in front of their [public cloud workloads](https://blog.cloudflare.com/memcrashed-major-amplification-attacks-from-port-11211/) or [VoIP gateways](https://blog.cloudflare.com/cve-2022-26143/). For that you need application security.

### In a Nutshell

Jeff Tantsura [posted](https://www.linkedin.com/feed/update/urn:li:activity:7051954643303571457/) a great summary of this topic in a LinkedIn comment:

---

It is important to understand that BGP security has many interrelated features, with different requirements with regard to full vs partial support and ROI, e.g BGPSEC benefits in a mixed environment are rather questionable (politely put), basic hygiene (read MANRS) will immediately bring better results, BGP RPKI benefits from “network effect” phenomenon - it brings value added even with a limited number of participants, however as the number grows, every participant benefits more and more.
There’s no “green day” BGP will suddenly become completely secure, there are many steps to get there.

---

### Want to Learn More

* I covered [network security fallacies](https://my.ipspace.net/bin/list?id=Net101#NETSEC), including Internet routing security, in [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar. Eventually, you'll be able to view those videos with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).
* You'll find more details in the [Internet Routing Security](https://www.ipspace.net/Internet_Routing_Security) webinar.

### Revision History

2023-04-13
: Added a summary by Jeff Tantsura, removed mention of AS Cones,  and a link to Fastly response to FCC inquiry
