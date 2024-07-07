---
date: 2022-06-02 06:01:00+00:00
series:
- ASIC
tags:
- data center
- switching
title: Data Center Switching ASICs Tradeoffs
---
A brief mention of Broadcom ASIC families in the _[Networking Hardware/Software Disaggregation in 2022](/2022/05/network-hardware-disaggregation-2022/)_ blog post triggered an interesting discussion of ASIC features and where one should use different ASIC families.

Like so many things in life, ASIC design is all about tradeoffs. Usually you're faced with a decision to either implement X (whatever X happens to be), or have high-performance product, or have a reasonably-priced product. It's very hard to get two out of three, and getting all three is beyond Mission Impossible.
<!--more-->
{{<note info>}}I might have known a few things about switching ASICs years ago, but I most probably became a victim of [Clarke's First Law](https://en.wikipedia.org/wiki/Clarke%27s_three_laws). Feedback and corrections are most welcome!{{</note>}}

### Tradeoffs

Here are just a few things you have to trade against performance and cost:

**Buffer space**. An ASIC with megabytes of internal buffer storage is using very high speed on-chip static RAM. The only way to get gigabyte-sized buffers is to use crazily-complex (and expensive) technology like [Hybrid Memory Cube](https://en.wikipedia.org/wiki/Hybrid_Memory_Cube) or [High Bandwidth Memory](https://en.wikipedia.org/wiki/High_Bandwidth_Memory). Conventional dynamic RAM used in your laptop is way too slow.

**Forwarding table size**. Small forwarding tables can be implemented with on-chip TCAM. Larger forwarding tables that use simple matching (MAC address table) can use fast on-chip static RAM and get the results in a single lookup ([more details](/2022/02/packet-forwarding-header-lookup/)).

Longest-prefix matching is already more complex and might require more than one lookup to get the end result. Whenever you need more than one lookup to get the result, you have to settle for lower forwarding performance, or use higher-speed memory.

I don't want to know how complex the longest-prefix matching can get at terabit speeds when faced with a routing table containing millions of entries.

**Forwarding features**. The more an ASIC can do, the more silicon it needs, so it tends to be more expensive to make. It might also need more steps in a forwarding pipeline which increases latency.

Worst case, a forwarding operation needs to search in the same forwarding table multiple times (example: routing out of VXLAN tunnel), in which case we're back to the tradeoff between forwarding performance and memory speed.

**Programmable forwarding pipeline**. Having a forwarding pipeline in which every step can do anything you wish sounds wonderful... until you realize how much complexity you have to add to the switching silicon to make it happen.

More complex silicon is either slower, or more expensive because you have to use better manufacturing process, but the difference might not be huge. In a [paper published in 2013](https://dl.acm.org/doi/pdf/10.1145/2486001.2486011) (pointer to the paper provided by [Aaron Glenn](https://www.linkedin.com/in/aaglenn/)), the authors estimated that programmable pipeline increased the area of their ASIC by ~15% (see section 5.5).

Oh, and there's the tiny little detail of multiple steps in the pipeline using the same lookup tables (see above).

### Real-Life Examples

It's hard to imagine how fast switching ASICs have to work -- a modern data center switching ASIC can forward billions of packets per second. For example, the throughput of Broadcom Tomahawk 3[^T4] is 12.8 Tbps[^MM], and it can switch 8 billion packets per second, or 8 packets every nanosecond.

If you want to forward eight packets per nanosecond, you have to search (at least) the MAC table eight times each nanosecond, giving you 125 picoseconds per lookup -- that's eight times faster than the level-1 cache in modern CPUs. I have absolutely no clue how they got it done, and I can't square it with 700 nanosecond forwarding latency (that would mean 5600 packets in transit within the ASIC at any given time), but it's probably just me showing off my ignorance.

[^T4]: Tomahawk 4 is approximately twice as fast
[^MM]: Or 25.6 Tbps if you believe in marketing math. Tomahawk 3 has 32 400 GE ports, and thus can't receive (and forward) more than 12.8 Tbps of traffic. Counting every packet twice is called cheating.

Tomahawk 3 is thus all about performance:

* 12.8 Tbps throughput, 8 Bpps
* Small table sizes (example: 8K MAC table)
* Small system buffers (64 MB)
* Limited functionality (L2 and L3 forwarding)

[Results of a quick Google search](https://itprice.com/arista-price-list/dcs-7060.html) claim an Arista switch with this ASIC and 32 400 GE ports costs around $55.000[^P].

[^P]: Please don't tell me you can get Arista switches way cheaper, or that they cost more in your geography. All I'm interested in are the approximate price ratios, and I hope the switches I chose have been in the market long enough I haven't stumbled into some desperate "_we need to push new boxes to meet our quota_" promotion. Even so, this is a very rough approximation -- there's only a vague correlation between what a switch vendor is paying for an ASIC and the final switch price.

What could you do if you sacrifice performance? Welcome to Trident 3[^T3]:

* A quarter of the Tomahawk 3 performance (3.2 Tbps throughput, 2 Bpps)
* Twice as much buffer space (per terabit)
* Larger forwarding tables (example: 128K MAC table)
* Complex features like routing out of VXLAN tunnels.

[^T3]: To stay within the same generation of ASICs

The [same web page claims](https://itprice.com/arista-price-list/7050cx3-32s.html) an Arista switch with Trident 3 ASIC and 32 100 GE ports costs around $30.000 -- more than half the price for a quarter of forwarding performance.

What if the ASIC could be more expensive? Let's look at Jericho2:

* Performance somewhere between Trident 3 and Tomahawk 3 (9.6 Tbps throughput, but still 2 Bpps)
* Cell-based fabric
* Complex packet processing
* Large forwarding tables (1M IPv4/IPv6 table without a sweat)
* 8 GB buffers implemented with [HBM2 cube](https://en.wikipedia.org/wiki/High_Bandwidth_Memory)

It also has a "slightly" higher price tag. [Arista 7280R3 with 24 400GE ports](https://itprice.com/arista-price-list/7280r3.html) using two Jericho2 ASICs[^2J] costs between $129.000 and $209.000 depending on the forwarding table sizes and amount of buffer memory[^HSR]. The single-ASIC models with 32 100 GE ports and four 400 GE ports (an equivalent of 12 400 GE ports) cost around $75.000, or approximately 50% more than a Tomahawk-based switch with 32 400 GE ports.

{{<next-in-series page="/posts/2022/06/select-data-center-switching-asic.md" />}}

### Revision History

2022-03-06
: Fixed the footnote explaining how to use two back-to-back Jericho2 ASICs

[^2J]: According to the [data sheet](https://www.broadcom.com/products/ethernet-connectivity/switching/stratadnx/bcm88690) Jericho2 ASIC has 12 400GE (96 x 50GE) lanes and 112 x 50GE fabric lanes. To get 24 400 GE ports you have to connect the fabric lanes of two ASICs back-to-back.

[^HSR]: High-speed RAM is obviously still a bit on the expensive side.