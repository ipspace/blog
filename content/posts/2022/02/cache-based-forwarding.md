---
title: "Cache-Based Packet Forwarding"
date: 2022-02-24 08:57:00
tags: [ networking fundamentals, switching ]
series: forwarding
---
In the previous blog post in this series I described [how convoluted routing table lookups could become](/2022/02/packet-forwarding-header-lookup.html) when you have to deal with numerous layers of indirection (BGP prefix ⇨ BGP next hop ⇨ IGP next hop ⇨ link bundle ⇨ outgoing interface). Modern high-end hardware can deal with the resulting complexity; decades ago we had to use router CPU to walk through the multilayer data structures.

Network devices were always pushed to the bleeding edge of performance, and smart programmers always tried to optimize the CPU-intensive processes. One of the obvious packet forwarding optimizations relied on the fact that within a short timeframe most packets have to be forwarded to a small set of destinations. Welcome to the wonderful world of cache-based forwarding.
<!--more-->
The first cache-based packet forwarding mechanism I've encountered was Cisco's venerable *fast switching* (now long dead). The first packet toward an unknown destination would be *process switched*. The results of the lookups needed to forward the packet (IP routing table + ARP/ND table) would be stored in a *fast switching cache* to be used by subsequent packets. The following information was stored in the fast switching cache:

* IP prefix (using a calculated subnet mask based on an "interesting" algorithm[^PFX])
* IP next hop (used only for cache invalidation)
* Outgoing interface
* Complete layer-2 header

[^PFX]: Fast switching did not use the usual tree-based data structure that would allow it to deal with variable-length subnet masks. The details are best forgotten; a few of them are documented in Inside Cisco IOS Software Architecture book.

The performance difference between *process switching* and *fast switching* was significant. Fast switching was performed within the interrupt processing (packet forwarding could interrupt whatever else the router was doing), whereas process switching (as the name implies) was done within the *IP Input* process that had to compete for CPU cycles with control-plane processes. To make matters worse, Cisco IOS used non-preemptive scheduling leading to hilarious results: transit packets had to wait for things like OSPF SPF run or BGP table scan to complete before they could be processed.

Fast switching implementations had to deal with the usual caching headaches:

* **Incomplete cached information** -- in an ECMP scenario, only a single path toward a destination would be cached, resulting in suboptimal load balancing[^LB].
* **Cache invalidation** -- it was pretty easy to invalidate fast switching entries whenever a directly-connected next hop disappeared, or whenever a prefix in the routing table changed. Figuring out what entries one needs to invalidate when one of the interim steps in a recursive routing table lookup changes must have been an interesting challenge[^FLUSH]
* **Cache trashing** -- when the number of active destinations exceeded the size of the cache, most packets became *process switched*, resulting in significant performance drop.

[^LB]: I could write a whole blog post on the intricacies of load balancing with fast switching, but it makes no sense to waste everyone's time on the details of an obsolete implementation.

[^FLUSH]: I have a weird feeling that they simply flushed the whole cache when they couldn't decide what to do, but have zero evidence for that claim.

To make matters worse, Cisco implemented *fast switching* in hardware (*autonomous switching*), resulting in orders-of-magnitude performance drop when cache trashing forced a router to fall back to *process switching*.

*Fast switching* worked pretty well on low-end edge routers and failed miserably in high-end (Internet) core routers, the last nail in its coffin being the ubiquitous port scans. A single hacker scanning the Internet at a reasonably low scan rate could bring a high-end router to its knees by polluting its *fast switching* cache.

Internet core experienced numerous regional brownouts in those days until Cisco managed to get its act together and roll out Cisco Express Forwarding (CEF) -- a packet forwarding mechanism that relies on fully evaluated forwarding table[^MEM] instead of a forwarding cache.

The laws of physics haven't changed in the interim[^MAGIC] -- whenever you encounter a cache-based forwarding scheme (conversation learning, LISP, Cisco SDA...) you can kill its performance with a simple address scanning tool, or as I said in the past "*cache-based forwarding never scaled.*"

There's an obvious exception to that rule: the forwarding cache might be large enough to hold all potential destinations... but then any cache-based forwarding scheme becomes nothing else but a steaming pile of unnecessary complexity.

But wait, it gets worse. Every few years someone gets the awesome idea of caching individual TCP/UDP flows. What could possibly go wrong?

### More Details

* *Inside Cisco IOS Software Architecture* book has an excellent overview of *process switching*, *fast switching*, *optimum switching* and *autonomous switching*. It was published in 2000 and hasn't been updated since, but you could still browse it for a few days with a trial Safari subscription.
* You'll find an extensive discussion of various packet forwarding mechanisms in the [Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH) part of _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.

[^MEM]: Limited amount of router memory was only reason Cisco went down the cache-based forwarding rabbit trail. Many routers didn't have enough memory to store two or three copies of routing information from the Internet default-free zone (BGP table, IP routing table, CEF table).

[^MAGIC]: That might surprise believers in the magical powers of unicorn dust and PowerPoint slides. I'm pretty sure the regular readers of this blog are immune against that hallucination.
