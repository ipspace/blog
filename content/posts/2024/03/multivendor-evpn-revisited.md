---
date: 2024-03-05 08:36:00+01:00
evpn_tag: rant
series_title: Multi-Vendor EVPN Fabrics
tags:
- EVPN
title: 'Rant: Multi-Vendor EVPN Fabrics'
---
[Daniel Dib](https://twitter.com/danieldibswe) tweeted about an [old comment of mine](https://blog.ipspace.net/2022/09/mlag-bridging-evpn.html#1420) a few days ago, adding[^TIC]:

[^TIC]: As I stopped believing in the long-term viability of the site formerly known as Twitter, I'm taking screenshots of what people were saying to have them preserved in a place where I can control their durability ;)

{{<figure src="/2024/03/tweet-ddib-evpn.jpg">}}

Not surprisingly, that was bound to upset a few people, and [Roman Dodin](https://twitter.com/ntdvps) quickly pointed out the EVPN interoperability tests:
<!--more-->
{{<figure src="/2024/03/tweet-ntdvps-evpn.jpg">}}

Roman is absolutely correct. Vendors have been running EVPN interoperability tests for years, and recent results showed surprising levels of interoperability. Considering Daniel's original scenario, you could also build a fabric where the spine switches run just an IGP, so you'd get almost guaranteed interoperability, but I'm digressing.

{{<long-quote>}}Before going any further, you might want to read my [more nuanced take on the topic](https://blog.ipspace.net/2023/04/multi-vendor-evpn-fabric.html). Rant starting in 3...2...1...now ;){{</long-quote>}}

Looking back, vendors had been running OSPF or SIP interoperability tests for years[^OI], and still, it took a long time for the technology to stabilize enough for people who love not being on a frantic conference call with a network-down situation to start building multi-vendor solutions with those technologies[^O32].

[^OI]: How do you think The Interop started? It [evolved](https://en.wikipedia.org/wiki/Interop#History) from the 1986 *TCP/IP Vendors Workshop*.

[^O32]: Remember the good old days when OSPF stopped working after a few weeks due to whatever counter overflow? I tried to find something describing that behavior (and failed) and uncovered tons of recent reports of weird OSPF behavior. Do I have to point out that OSPF is almost 30 years old and relatively trivial compared to EVPN?

You see, there's a fundamental difference in perspective if you consider multi-vendor interoperability as a runner-up box builder or a network builder using other people's boxes. I understand that vendors get upset when people like Daniel or myself say, "_I see no reason why I would make my life harder building a multi-vendor EVPN data center fabric_," however, it's hard enough being the QA department for a single vendor[^QT], let alone being an interoperability test bed and QA department for multiple vendors. It took some vendors years to get the VXLAN/EVPN gear they were selling to the point where it could be safely used in production networks. Why should we believe they're doing a better job with multi-vendor interoperability?

[^QT]: Let's be realistic and admit it's impossible to test every single deployment scenario of a complex distributed system. It's also impossible to predict the crazy ways in which MacGyvers of the networking world will use your boxes. On the other hand, it's inexcusable to [ship a virtual appliance with a broken DHCP client](https://blog.ipspace.net/2023/10/vjunos-declines-dhcp-address.html) and then take over three months to release a fixed image. Nonetheless, I want to avoid being unpaid vendors' QA department as much as possible.

{{<long-quote>}}
A recent LinkedIn comment is a perfect illustration of what I'm talking about:

> One thing that is really hard to simulate in a lab, which gives me serious heartburn with VXLAN implementation, is what happens when you get a bad- or stale state in the table. So far, I've been unable to find a better solution than **clear bgp all**, which is somewhat acceptable when services are partition tolerant and a complete nightmare when they are not.

Vendors have been "shipping" EVPN/VXLAN for years, and we're still dealing with *BGP tables or forwarding tables are messed up* scenarios. Do I need to say more?
{{</long-quote>}}

Now for a slightly more nuanced perspective. Roman also argued that there's a difference between *EVPN services* and *MC-LAG* and he's absolutely correct.

{{<figure src="/2024/03/tweet-ntdvps-mclag.jpg">}}

However, due to the influence of PowerPoint creators and EVPN gospel spreaders on people who prefer believing vendors instead of doing their own research, every time someone mentions [MC-LAG](https://blog.ipspace.net/series/mlag.html), a LinkedIn ~~Engagement Farmer~~ [Thought Leader](https://blog.ipspace.net/2023/08/engagement-farming.html) inevitably writes a comment saying "_[you should use EVPN ESI](https://blog.ipspace.net/2022/11/mlag-vxlan-evpn.html), that's a standard_" without realizing it [takes more than the engine](https://blog.ipspace.net/2022/11/mlag-vxlan-evpn.html) (EVPN ESI) to build a car (a solution in which [two boxes pretend to be one](https://blog.ipspace.net/2010/10/multi-chassis-link-aggregation-basics.html)). Some other parts of MC-LAG solutions are standardized (ICCP), while others are not. Yet you need all of those building blocks if you want to build a link aggregation group with member links connected to different devices. *Stick to MC-LAG* movement[^SMC] is not *slowing progress* but pointing out the inevitable reality[^EC] to people who think a sprinkle of unicorn dust (EVPN ESI) solves a complex technology challenge.

[^SMC]: Of which I'm not a member. I've been recommending to get as far away from MC-LAG as possible [at the network edge](https://blog.ipspace.net/2014/01/vsphere-does-not-need-lag-bandaids.html) or in the [fabric core](https://blog.ipspace.net/2019/05/dont-base-your-design-on-vendor.html) for a decade.

[^EC]: And I completely understand that some people prefer not to discuss the [state of their wardrobe](https://en.wikipedia.org/wiki/The_Emperor%27s_New_Clothes).

I don't care if some vendors believe they should implement MC-LAG with EVPN ESI technology while others think they should use anycast IP. It's the vendors' job to ensure the two types of solutions are interoperable in large fabrics, but that still wouldn't persuade me to build a data center layer-2 domain[^SVL] with boxes from two vendors. Carrier Ethernet networks are a different story[^OG], but even there, one should keep all endpoints of a link aggregation group connected to the same type of boxes for consistency reasons.

[^SVL]: ... or VLANs stretching across continents or reaching into a public cloud.

[^OG]: Data center pods are often built and deployed as a single project, whereas Carrier Ethernet networks usually grow organically over decades.

Last but not least, this saga proves vendors learned nothing from the OSPF debacle of the mid-1990s:

* The development of the EVPN RFCs was mostly vendor-driven (because nobody else would pay top-notch engineers to ~~waste~~ dedicate their time to arguing about the number of angels dancing on virtual pins).
* As usual, most parts of the EVPN standards were made optional because nobody in their right mind would agree to have something they haven't implemented yet be MANDATORY.
* Vendors decided to implement different subsets of the EVPN standards and used standards in different creative ways, creating the whole interoperability mess in the first place.
* Don't get me started on the crazy ideas of running IBGP over EBGP because (A) EVPN was [designed to be used with IBGP and IGP](https://blog.ipspace.net/2019/04/dont-sugarcoat-challenges-you-have.html), and (B) [EBGP-as-IGP craze took over](https://blog.ipspace.net/2019/11/the-evpn-dilemma.html) in the meantime.
* Rushing to market with broken implementations didn't help build the end-user confidence either.

So, if you're working for a vendor, don't complain when old-timers like Daniel and myself say, "_I love quiet evenings and would try to avoid multi-vendor fabrics as much as possible._" I know most of you weren't there when this particular [complexity sausage](https://blog.ipspace.net/2012/07/virtualized-squashed-complexity-sausage.html) was being made. Still, your company might have helped create that sentiment in the first place (probably not starting with EVPN), and unfortunately, you have to share the consequences. However, I agree that (A) EVPN is probably the way to go if one wants to build layer-2+3 VPNs, and (B) interoperability matters, so please keep up the good fight!
