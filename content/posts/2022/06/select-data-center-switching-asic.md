---
date: 2022-06-08 06:16:00+00:00
series:
- ASIC
tags:
- data center
- switching
title: Select the Best Switching ASIC For the Job
---
Last week I described some of the [data center switching ASIC design tradeoffs](/2022/06/data-center-switching-asic-tradeoffs.html) and the ASIC families Broadcom created to fit somewhere in that multi-dimensional space. 

Next step: how could you design your data center fabric to make the most out of them? To keep things simple, we'll build a typical leaf-and-spine fabric with a WAN edge layer (sometimes called *border leaf* switches).
<!--more-->
**Spine switches** should be significantly faster than the leaf switches -- in a typical leaf-and-spine fabric, you'd use two or four spine switches to connect up to 32 (or 64) leaf switches. You probably don't want to spend an arm and a leg for a spine switch; high-performance switches should therefore have:

* Small buffers
* Small forwarding tables
* Minimum forwarding complexity -- nothing else but rudimentary L2 and L3 forwarding with a sprinkle of course-grained QoS

Not surprisingly, the Broadcom Tomahawk series fits the bill perfectly, but you have to be careful in your design:

* You might experience scaling challenges when using this ASIC in a traditional layer-2 fabric due to its small MAC/ARP forwarding tables[^THFW]. Build a routed data center fabric, and implement stretched VLANs with VXLAN transport between edge switches or hypervisors.
* The same ASIC supports relatively large IPv4/IPv6 forwarding tables[^THIP], making it a perfect fit for a core switch in a routed fabric.
* We chose spine switches with small buffers to reduce cost. Don't even think about connecting anything else but leaf switches to them unless you want to live in a world of eternal drop-caused pain.

[^THFW]: 8K MAC table and 16K ARP table according to an [Arista datasheet](https://www.arista.com/assets/data/pdf/Datasheets/7060X4-Datasheet.pdf)

[^THIP]: 640K IPv4 longest-prefix-match (LPM) routes or 160K IPv6 LPM routes according to the same datasheet

**Leaf switches** might need slightly larger buffers, larger MAC/ARP forwarding tables[^CTR], and more complex packet forwarding functionality (example: VXLAN routing). A data center switch using a Broadcom Trident-series ASIC is usually a perfect fit.

Leaf switches dealing with a significant amount of incast traffic[^INC] might need [significantly larger buffers](/2021/05/packet-bursts-data-center-networks.html). Typical scenarios include:

* WAN edge
* Applications with scatter-gather behavior (example: Map/Reduce)
* Many hosts writing to the same iSCSI target

Use a deep buffer switch in those few scenarios -- they tend to be horrendously expensive but still cheaper (per gigabit) than WAN edge routers.

Please note that you usually DO NOT need a deep buffer leaf switch (or deep buffers on spine switches) outside of these few scenarios. For more details explore:

* [Networks, Buffers and Drops](https://my.ipspace.net/bin/list?id=xBuffers) webinar and all the [related reference material](https://my.ipspace.net/bin/list?id=xBuffers#REF).
* [Switch Buffer Sizes and Fermi Estimates](/2019/06/switch-buffer-sizes-and-fermi-estimates.html)
* [Packet Bursts in Data Center Fabrics](/2021/05/packet-bursts-data-center-networks.html)
* [Do Packet Drops Matter for TCP Performance?](/2019/06/do-packet-drops-matter-for-tcp.html)
* [Fundamentals: Is Switching Latency Relevant?](/2021/04/switching-latency-relevant.html) (focus on the discussion about buffering-induced latency)

[^CTR]: In particular, when you plan to connect containers straight to the data center fabric.

[^INC]: Traffic sent from many sources to one or more destinations connected to the same link

{{<next-in-series page="/posts/2022/06/beware-vendors-bringing-whitepapers.md" />}}
