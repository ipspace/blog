---
title: "Data Center Switching ASICs Tradeoffs"
date: 2022-06-01 06:01:00
draft: True
tags: [ data center, switching ]
---
A brief mention of Broadcom ASIC families in the _[Networking Hardware/Software Disaggregation in 2022](https://blog.ipspace.net/2022/05/network-hardware-disaggregation-2022.html)_ blog post triggered an interesting discussion of ASIC features and where one should use different ASIC families.

Like so many things in life, ASIC design is all about tradeoffs. Usually you're faced with a decision to either implement X (for whatever value of X), or have high-performance product, or have a low-price product. It's very hard to get two out of three, and getting all three is usually Mission Impossible.
<!--more-->
{{<note info>}}I thought I knew a few things about switching ASICs, but I'm probably totally lost in the woods. Feedback and corrections are most welcome!{{</note>}}

A bit of a perspective first: a high-speed ASIC can switch billions of packets per second. For example, the throughput of Broadcom Tomahawk 3[^T4] is 12.8 Tbps, and it can switch 8 billion packets per second, or 8 packets every nanosecond. I have absolutely no clue how they got it done, and I can't square it with 700 nanosecond forwarding latency (that would mean 5600 packets in transit within the ASIC at any given time), but it's probably just me showing off my ignorance.

[^T4]: Tomahawk 4 is approximately twice as fast

To get there, Broadcom had to focus on performance. Forwarding table sizes are small, system buffers are small, and the ASIC can do little else but L2 and L3 forwarding.

What could you do if you sacrifice performance? Welcome to Trident 3[^T3]: 3.2 Tbps throughput, 2 Bpps (= four times lower performance), but twice as much buffer space (per terabit), larger forwarding tables, and complex features like VXLAN routing.

[^T3]: To stay within the same generation of ASICs

What about creating a more expensive ASIC? Let's look at Jericho2: 4.8 Tbps throughput, 2 Bpps, cell-based fabric, complex packet processing, large forwarding tables, 8 GB buffers implemented with [HBM2 cube](https://en.wikipedia.org/wiki/High_Bandwidth_Memory)... and a "slightly" higher price tag (Jericho2-based switches tend to be 3-4 times more expensive than similar Trident3-based switches).
