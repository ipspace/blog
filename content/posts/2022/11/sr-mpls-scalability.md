---
title: "Scalability Aspects of SR-MPLS"
date: 2022-11-02 07:37:00
tags: [ segment routing, MPLS ]
---
Henk Smit left a [wonderful comment discussing various scalability aspects of SR-MPLS](https://blog.ipspace.net/2022/09/greenfield-sr-mpls-srv6.html#1397). Let's go through the points he made:

> When you have a thousand routers in your networks, you can put all of them in one (IS-IS) area. Maybe with 2k routers as well. But when you have several thousand routers, you want to use areas, if only to limit the blast-radius.

Absolutely agree, and as RFC 3439 explained in more eloquent terms than I ever could:
<!--more-->
> In particular, the largest networks exhibit, both in theory and in practice, architecture, design, and engineering non-linearities which are not exhibited at smaller scale.

Unfortunately, vendors always focus on creating solutions for their largest customers, and then try to shove them down the market with glitzy PowerPoints to _leverage the investment_. Bonus points if those solutions require new hardware[^HW]. Well, when I need to trim the trees in my backyard, I don't care much about that beautiful robotic chainsaw used by people who cut down acres of forest per day.

[^HW]: Mentioning new hardware in a blog post talking about segment routing is pure coincidence.

Anyway, although most of us could probably live another day with a soft limit of about a thousand routers in a network, let's throw some ignorant ideas around. I'm sure Jeff Tantsura will quickly post a comment saying "_and that is addressed in this particular IETF draft_," and someone else will tell me what I've missed... and that's why I like blogging so much ;)
 
> But there are several technologies where you need to know the SID of the router at the endpoint where you want to send traffic. That means in SR-MPLS you need to advertise the /32 (or /128) of every router in your network. Plus their SID. If you do flex-algo, multiple SIDs even. 

There are two aspects to this challenge:

* You need to know the IP-to-SID mappings (example: BGP-free core or VPN services). You can solve this in a variety of ways (more below)
* You need to know the network topology to calculate alternate paths (example: TI-LFA).

If we need alternate path calculation, we could either:

* Limit ourselves to a single area, in which case our discussion is moot
* Use manual configuration similar to Multi-area MPLS Traffic Engineering (a delight to manage and an awesome source of job security ;)
* Use an SDN controller to collect topology from multiple areas, calculate alternate paths, and install them into your boxes. It might cost an arm and a leg, require the latest software update[^BS], and take forever to fine-tune, but it might be a huge resume booster ;)

[^BS]: That would break tons of unrelated things because you can't upgrade just one package in a network operating system.

Anyway, back to the more interesting _we just need IP-to-SID mapping_ use case. That's no different from the ancient _we can't summarize loopbacks if we need to build a label-switched path with LSP_ challenge. Either you can fit all the information into the inter-area (or inter-level) part of your topology database or you use a protocol that's been used forever to distribute mappings between _whatever_ and next-hop addresses (hint: BGP). Obviously there's a way to use BGP-LU to distribute SR SIDs (see [RFC 8669](https://www.rfc-editor.org/rfc/rfc8669.html) for details).

However, at least IS-IS has an interesting problem: the amount of information any router could generate (including inter-level information leakage) is limited[^SO]. Still not sure whether that's a good or a bad thing :)

[^SO]: Score one for OSPF where a router can redistribute the whole BGP routing table as a million type-5 LSAs. Hint: [don't do that at home](https://blog.ipspace.net/2020/10/redistributing-bgp-into-ospf.html), it might [cause a short-term outage](https://twitter.com/stubarea51/status/1582931047796604928).

> That starts to add up to a lot of info in your LSPDB. Your L1L2 routers might need to advertise several thousands of prefixes down. This is a practical concern. You can do things like increase lsp-mtu. Or implement RFC5311. I don't find that an elegant solution.

Well, you want to have _simple_, _cheap_, _efficient_, _elegant_, _fast_, _stable_ and _infinitely scalable_? You could have two (maybe three) out of those ;)

> The best thing would be to have summarizable SIDs. SR-MPLS doesn't have that. SRv6 does. So there SRv6 has an advantage, imho. But even when you have summarizable SIDs, you still need to know the mapping between /32 (or /128) and the SID. I don't think there's a good way to do that yet, besides advertising each individual /32 and SID combination.

Well, if you want to stay within a single routing protocol, then summarization might be the only option. If you're OK with whatever solution scales, then you can avoid summarization until you hit the next limit: the LFIB size on your core routers (which have to know how to get to all edge routers).

You could get around that with some sort of hierarchical MPLS or (yet again) with an SDN controller, or you could give up and go for SRv6.

Do keep in mind that regardless of what evangelists would like you to believe, SRv6 is really a tunneling protocol like VXLAN, GENEVE, or LISP, and all tunneling protocols that are OK with sending their payload toward a summarized underlay prefix suffer the _path liveliness_ problem[^MD].

[^MD]: I wonder why this [interesting draft](https://datatracker.ietf.org/doc/html/draft-meyer-loc-id-implications-01) never became endorsed by the working group or turned into an RFC. Must be a pure coincidence.

Back to Henk...

> I've been told a few times that "routing is a solved problem". I don't agree. Routing is maybe a solved problem for networks with <= 1000 routers. For larger networks, you still need to use a bunch of trick and kludges to make it work. We could use a better solution.

Anyone claiming that _routing is a solved problem_ has as much in-depth experience with routing as people claiming that _quantum physics is a solved problem_ have with calculating the expected results of Feynman diagrams, but ignorance has never stopped _thought leaders_ from having opinions. Then there are people like [SD-WAN marketers](https://blog.ipspace.net/2015/07/some-ridiculous-sd-wan-claims.html) who consider routing a solved problem because [they "solved" the problem by offloading it to someone else](https://blog.ipspace.net/2015/07/routing-protocols-and-sd-wan-apples-and.html).

However, I don't think it's realistic to expect a single unified solution to a complex challenge[^UTE]. Solving a complex-enough task usually requires multiple tools and the knowledge and experience to select the best tool for the next step in the process. I do a bit of woodworking when I get tired of networking, and I have a garage full of tools. Obviously I could replace most of them with either a brutally expensive CNC machine, or with a Swiss Army knife. Neither of them would be optimal for my needs ;)

[^UTE]: It looks like most physicists would agree (at least in private) with the exception of those still searching the for the Great Unified Theory of Everything. And yeah, I've spent way too much time reading [Sabine Hossenfelder's juicy blog posts](http://backreaction.blogspot.com/) lately.