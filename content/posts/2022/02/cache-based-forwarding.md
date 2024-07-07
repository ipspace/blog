---
date: 2022-02-24 08:57:00+00:00
lastmod: 2022-02-28 16:07:00
series:
- forwarding
tags:
- networking fundamentals
- switching
- LISP
title: Cache-Based Packet Forwarding
---
In the previous blog post in this series I described [how convoluted routing table lookups could become](/2022/02/packet-forwarding-header-lookup/) when you have to deal with numerous layers of indirection (BGP prefix ⇨ BGP next hop ⇨ IGP next hop ⇨ link bundle ⇨ outgoing interface). Modern high-end hardware can deal with the resulting complexity; decades ago we had to use router CPU to do multiple (potentially recursive) lookups in the IP routing table (there was no FIB at that time).

Network devices were always pushed to the bleeding edge of performance, and smart programmers always tried to optimize the CPU-intensive processes. One of the obvious packet forwarding optimizations relied on the fact that within a short timeframe most packets have to be forwarded to a small set of destinations. Welcome to the wonderful world of cache-based forwarding.
<!--more-->
{{<note info>}}The blog post has been updated based on extensive feedback by Henk Smit (see comments){{</note>}}

The first cache-based packet forwarding mechanism I've encountered was Cisco's venerable *fast switching* (now long dead). The first packet toward an unknown destination would be *process switched*. The results of the lookups needed to forward the packet (IP routing table + ARP/ND[^ND] table) would be stored in a *fast switching cache* to be used by subsequent packets. The following information was stored in the fast switching cache:

[^ND]: Contrary to Henk's comment, it seems IPv6 had a fast switching implementation. I even found a document explaining [IPv6 multicast process- and fast switching on Catalyst switches](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960xr/software/15-0_2_EX1/ipv6/configuration_guide/b_ipv6_152ex1_2960-xr_cg/b_ipv6_152ex1_2960-xr_cg_chapter_0100.html#concept_E52E96CD726B4C019A188FEB96C99A1C). That must have been ultra-fast ;)

* IP prefix (using a calculated subnet mask based on an "interesting" algorithm[^PFX])
* IP next hop (used only for cache invalidation)
* Outgoing interface
* Complete layer-2 header

[^PFX]: Fast switching did not use the usual tree-based data structure that would allow it to deal with variable-length subnet masks. The details are best forgotten; a few of them are documented in Inside Cisco IOS Software Architecture book. It might even be that the early versions of fast switching created host entries (not prefixes) in the fast switching cache. Will try to find someone whose memory is better than mine.

The performance difference between *process switching* and *fast switching* was significant. Fast switching was performed within the interrupt processing (packet forwarding could interrupt whatever else the router was doing), whereas process switching (as the name implies) was done within the *IP Input* process that had to compete for CPU cycles with control-plane processes. To make matters worse, Cisco IOS used non-preemptive scheduling leading to hilarious results: transit packets had to wait for goodwill of other processes like OSPF SPF run or BGP table scan to release CPU before they could be processed[^HOG].

[^HOG]: A failure to release CPU in a timely manner would result in much-beloved CPUHOG syslog messages. Not that you could do anything if one kept popping up; they were just an indication of suboptimal code.

Fast switching implementations had to deal with the usual caching headaches:

* **Incomplete cached information** -- in an ECMP scenario, only a single path toward a destination would be cached, resulting in suboptimal load balancing[^LB].
* **Cache invalidation** -- it was pretty easy to invalidate fast switching entries whenever a directly-connected next hop disappeared, or whenever a prefix in the routing table changed. Figuring out what entries one needs to invalidate when one of the interim steps in a recursive routing table lookup changes must have been an interesting challenge[^FLUSH]
* **Cache trashing** -- when the number of active destinations exceeded the size of the cache, most packets became *process switched*, resulting in significant performance drop.

[^LB]: I could write a whole blog post on the intricacies of load balancing with fast switching, but it makes no sense to waste everyone's time on the details of an obsolete implementation.

[^FLUSH]: I have a weird feeling that they simply flushed the whole cache when they couldn't decide what to do, but have zero evidence for that claim. See also comments by Henk Smit.

To make matters worse, Cisco implemented *fast switching* in hardware (*autonomous switching*), resulting in orders-of-magnitude performance drop when cache trashing forced a router to fall back to *process switching*.

*Fast switching* worked pretty well on low-end edge routers and failed miserably in high-end (Internet) core routers, the last nail in its coffin being the ubiquitous port scans. A single hacker scanning the Internet at a reasonably low scan rate could bring a high-end router to its knees by polluting its *fast switching* cache.

Internet core experienced numerous regional brownouts in those days until Cisco changed the packet forwarding paradigm and rolled out Cisco Express Forwarding (CEF) -- a packet forwarding mechanism that relies on fully evaluated forwarding table[^MEM] instead of a forwarding cache.

The laws of physics haven't changed in the interim[^MAGIC] -- whenever you encounter a cache-based forwarding scheme (conversation learning, original LISP, Cisco SDA...) you can kill its performance with a simple address scanning tool, or as I said in the past "*cache-based forwarding never scaled.*"

There's an obvious exception to that rule: the forwarding cache might be large enough to hold all potential destinations, and the number of changes is so small that the cache maintenance doesn't overload the CPU... but then any cache-based forwarding scheme becomes nothing else but a steaming pile of unnecessary complexity.

But wait, it gets worse. Every few years someone gets the awesome idea of caching individual TCP/UDP flows. What could possibly go wrong?

### Another Data Point for RFC 1925 Rule 11

When I was updating this blog post to ensure everyone understands I'm referring to the _original_ LISP ideas, I remembered an [extensive comment Victor Moreno wrote](/2017/09/why-is-cisco-pushing-lisp-in-enterprise/#5200837098827991481) in 2017 on my _[Why Is Cisco Pushing LISP in Enterprise Campus?](/2017/09/why-is-cisco-pushing-lisp-in-enterprise/)_ blog post.

> The impact of mobility events in a LISP network (as you know from past reviews published in your blog) is limited to signaling amongst the network elements involved in active connections between the devices. However, the impact of mobility events in a BGP network is unbound. Even if you have conditional FIB programming, all changes are pushed to all participants. 

And also...

> I happened to be in the process of posting a document that describes a wealth of other functionality that is possible by the simple principle of the demand based control plane and a discussion on why this is best realized with a demand protocol. 

Please note that the _demand-based control plane_ is a nice euphemism for _cache-based forwarding_. Now compare what Victor wrote in 2017 to what Bela wrote in 2021:

> LISP is a more complex animal nowadays. Nowadays it is used with reliable transport and full PubSub. There is no caching behavior at all. Each xTR has a full routing table.

I would say that the evolution of LISP proves (A) the point of this blog post as well as (B) RFC 1925 rule 11.

### More Details

* *Inside Cisco IOS Software Architecture* book has an excellent overview of *process switching*, *fast switching*, *optimum switching* and *autonomous switching*. It was published in 2000 and hasn't been updated since, but you could still browse it for a few days with a trial Safari subscription.
* You'll find an extensive discussion of various packet forwarding mechanisms in the [Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH) part of _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.

[^MEM]: Limited amount of router memory is the only reason I can think of that made Cisco go down the cache-based forwarding rabbit trail. Many routers didn't have enough memory to store two or three copies of routing information from the Internet default-free zone (BGP table, IP routing table, CEF table). Henk Smit disagrees with me (see comments), but I still remember routers that would get kicked out of CEF switching due to memory shortage and subsequently blackhole all MPLS services which relied on CEF switching.

[^MAGIC]: That might surprise believers in the magical powers of unicorn dust and PowerPoint slides. I'm pretty sure the regular readers of this blog are immune against that hallucination.

### Revision History

2022-02-28:
: Reworded a number of things and fixed the inaccuracies based on extensive feedback by Henk Smit, including:
:
: * Changed "walking the routing table" into "multiple lookups in the IP routing table"
: * Fixed the "packets waiting for SPF run" part
: * Didn't touch the fast switching details -- checked with Henk, and we agreed that our memories are too hazy for a definitive answer. Have to find someone who remembers how things were done.

2022-02-25
: Clarified that I had the _original_ LISP ideas in mind, and added a paragraph about evolution of LISP proving RFC 1925 Rule 11.