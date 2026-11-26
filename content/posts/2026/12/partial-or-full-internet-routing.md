---
title: "Default Routes or Full BGP Table for Internet Access?"
date: 2026-12-03 08:32:00+0100
tags: [ BGP, Internet ]
---
_**TL&DR:** Searching for information has never been easier; LLMs made the Internet search usable again. What they'll find in search results and who'll write the new content is a more interesting question, though 🤷🏻‍♂️_

I got the following question from one of my readers (edited and shortened for clarity):

> We are consolidating two independently managed Internet environments. One uses dual Internet connections from the same ISP and relies on a default route via BGP. The other one uses two independent ISPs and receives the full Internet routing table from both providers via BGP. Would you recommend maintaining full Internet routing tables from both providers, or adopting a model based on partial routes combined with a default route?

I replied with a brief summary of what I'd usually recommend (prefaced by the obligatory It Depends&trade;)
<!--more-->
{{<long-quote>}}
As always, the correct answer is "it depends". For two links to the same upstream provider, it usually doesn't matter.

However, if you have two providers, you don't want a problem with your primary upstream to bring down everything, so taking the full routing table is the usual solution. You could trim that down in various ways (along with a default route); for example, drop stuff that has many distinct AS numbers in the AS path. In this case, it's also not a good idea to trust the default route advertised by the upstream; use several destinations that should never fail at the same time (for example, Google DNS, Cloudflare DNS, and maybe something locally relevant) as the next hops of a static default route.

I think I've written several blog posts on the topic and might have discussed this in a design clinic. It was definitely part of David Barroso's "SDN Router" idea.
{{</long-quote>}}

But then I started wondering what an AI agent would reply when asked the same question with the instructions to focus on ipSpace.net content (after all, the reader asked me for a reason). Here's the "focus on ipSpace.net" part of the prompt I used:

> Please scan blog.ipspace.net and ipSpace.net webinars/videos as well as https://designclinic.ipspace.net/ to find relevant blog posts and other materials that would answer this question.

Not surprisingly (for late 2026 ;), Claude AI generated a long, nuanced response with all the right pointers (warning: I wrote the above intro; what follows is AI-generated).

---

### Question and short answer

An enterprise is consolidating two Internet edges. Environment A has two links to the same ISP and gets a BGP default route. Environment B has two independent ISPs and takes full tables from both. Should the merged design keep full tables or move to partial routes plus a default?

**Short answer:** an enterprise that sells no transit doesn't need the full table. A bare default route from each ISP isn't enough either. The designs ipSpace.net recommends sit in between.

### Core ipSpace.net blog posts

Three posts answer the question almost directly: the 768K post for the design, the single-ISP post for Environment A, and the default-route posts for why a plain default is risky.

**[If You Worry About 768K Day, You're Probably Doing Something Wrong](https://blog.ipspace.net/2019/05/if-you-worry-about-768k-day-youre/)** (2019)

The best single answer to the question.

- You need the full table only inside the Default Free Zone (DFZ). If you buy transit, a default toward the upstream is simpler.
- Most autonomous systems don't need the full table, but they shouldn't blindly follow a default route either.
- Minimum: accept each upstream's customer prefixes from that upstream, and make the default depend on reaching a third-party prefix (for example a public DNS resolver).
- Alternative 1: default toward the primary upstream; install only prefixes learned from other upstreams or peers.
- Alternative 2: take the full table, use NetFlow to find the autonomous systems that matter, install those, and default the rest (the Spotify / David Barroso approach).

**[Multihoming to a Single ISP](https://blog.ipspace.net/2008/05/multihoming-to-single-isp/)** (2008)

Covers Environment A. A BGP default from the ISP is enough for correct upstream routing; the ISP's own and customer prefixes can be added to optimize local routing. A full table from one ISP offers no real choice of path.

**[Coping with Byzantine Routing Failures](https://blog.ipspace.net/2014/11/coping-with-byzantine-routing-failures/)** (2014) and **[Responsible Generation of BGP Default](https://blog.ipspace.net/2011/09/responsible-generation-of-bgp-default/)** (2011)

Why a plain default is risky.

- If the provider originates the default on its PE router without checking the rest of its network, BGP's shared-fate property breaks and BGP alone can't fix the failure.
- Fix: originate the default locally, based on IP SLA reachability checks (for example Google DNS or root name servers).
- Health signals suggested for a conditional default: BGP table size, long AS paths, anycast root DNS servers.

### Supporting material

These back up the core posts with the "full table in BGP, small table in hardware" option and background on BGP defaults.

| Source | Why it matters |
| --- | --- |
| [Living with Small Forwarding Tables](https://blog.ipspace.net/2022/05/living-small-forwarding-tables/) (2022) | A few thousand prefixes carry over 90% of traffic: filter what reaches the hardware FIB, keep a reliable default. Costs: slower convergence, risk of FIB overflow in some failures. |
| [Do You Really Need to See All 512K Internet Routes?](https://blog.ipspace.net/2014/08/do-you-really-need-to-see-all-512k/) (2014) | Most edge networks don't need the full table; covers BGP Selective Route Download and virtual aggregation. |
| [Use BGP Default Route to Replace Static Routing](https://blog.ipspace.net/2007/11/bgp-default-route/) | Get the default via BGP rather than a static route, so it goes away when the neighbor does. |
| [Default Routes in BGP](https://blog.ipspace.net/kb/tag/BGP/Default_Route/) | Knowledge base background on BGP default origination. |
| [SDN Router @ Spotify](https://blog.ipspace.net/2015/01/sdn-router-spotify-on-software-gone-wild/) and [SDN Internet Router Is in Production](https://blog.ipspace.net/2015/10/sdn-internet-router-is-in-production-on/) | Software Gone Wild episodes: the real-world "hot prefixes" design. |
{.fmtTable}

### Design Clinic and webinars

The September 2022 Design Clinic session is the closest match, but its videos are subscriber-only and I couldn't check what they say.

- **[Redundant BGP-Based Internet Access](https://designclinic.ipspace.net/topic/redundant-internet-access/)** (September 2022): compares full tables from both ISPs on both routers against one router with a default and one with a full table. Videos: Overview of Design Options and Challenges (10:20), Egress Traffic Engineering (16:49), Ingress Traffic Engineering (9:59). The public page has no written conclusion.
- Related sessions: [Improving BGP WAN Edge Convergence](https://designclinic.ipspace.net/topic/bgp-customer-convergence/), [Secure BGP Configuration on Customer Routers](https://designclinic.ipspace.net/topic/securing-customer-bgp-setup/), [BGP Routing with a DC Edge Firewall](https://designclinic.ipspace.net/topic/dc-edge-firewall-bgp/) (relevant if the edge devices are firewalls with small forwarding tables).
- Webinar[^CS]: **[BGP Convergence Optimization](https://www.ipspace.net/BGP_Convergence_Optimization)**, which the blog points to for reducing table size.

[^CS]: A blunder: it's a case study

### Counter-argument: partitions

The strongest case for full tables is a partition: one ISP has lost the route to a destination while the other still has it.

In the [2015 NANOG thread on this exact question](https://mailman.nanog.org/pipermail/nanog/2015-June/075653.html), William Herrin pointed out that a default route sends such packets to an ISP that will drop them, and you don't get to choose which ISP lacks the route. He also said that defaults from two ISPs are still more reliable than a single ISP.

Accepting each ISP's customer prefixes, as the 768K post recommends, covers part of this gap but not all of it.

### Suggested answer framing

Default to partial routes plus a conditional default; take full tables only for a specific reason.

1. **Environment A (one ISP):** default route plus the ISP's customer prefixes. A full table adds nothing.
2. **Merged two-ISP design:** partial routes from both ISPs (their own and their customers' prefixes) plus a default. The default must depend on reaching something beyond the ISP, not just on the BGP session: ask for a conditional default or generate one from reachability checks.
3. **Full tables** only for fine-grained outbound traffic engineering or partition protection, and only if the edge hardware holds two full tables. Otherwise, take the full table but install only selected prefixes in hardware.
4. **Questions for the reader:** do they actually do outbound traffic engineering, how big is the edge devices' forwarding table, and how much BGP policy can they run day to day?

No single ipSpace.net post compares partial-plus-default with full tables for a two-ISP enterprise. The 768K post comes closest, so the question could make a good follow-up post.
