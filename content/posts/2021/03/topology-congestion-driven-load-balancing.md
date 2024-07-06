---
title: "Topology- and Congestion-Driven Load Balancing"
date: 2021-03-11 07:28:00
tags: [ load balancing, SD-WAN ]
sd-wan_tag: details
---
When preparing an answer to an interesting idea left as a comment to my unequal-cost load balancing blog post, I realized I never described the difference between *topology-based* and *congestion-driven* load balancing.

To keep things simple, let's start with an easy leaf-and-spine fabric:
<!--more-->
{{<figure src="leaf-spine-fabric.png">}}

### Topology-Based Load Balancing

Looking at the network diagram, it's easy to realize there are two paths from L1 to L2, and modern routing protocols have absolutely no problem identifying the two paths and entering them in the forwarding table.

Now imagine the link S1-L2 is slower than the link S2-L2. A routing protocol capable of *unequal-cost multipathing* (EIGRP or properly designed BGP) would be able to identify the opportunity to use both paths in unequal ratio.

In both cases, the decision to use multiple paths (and the traffic ratio) was made based on *network topology*.

Going back to the first scenario: L1 has two equal-cost paths to L2, and can balance outgoing traffic across both of them. The usual implementation would use ECMP hash buckets ([high-level overview](/2020/11/fast-failover-implementation.html), [more details](/2015/01/improving-ecmp-load-balancing-with.html)). Assuming the forwarding hardware supports 128 hash buckets per next-hop group, 64 of those would point to L1-S1 and the other 64 would point to L1-S2.

### Congestion-Based Load Balancing

Let's add some heavy hitters to the mix: a few backup jobs are started and for whatever crazy reason the all land on L1-S1 link. That link becomes congested, and when another session gets assigned to that link, it will experience lower throughput and higher latency. Wouldn't it be possible to avoid the congested link even though it has equal cost as the uncongested one? Welcome to the dynamic world of *congestion-driven load balancing* (or whatever it's properly called).

Modern forwarding hardware supports dynamic reassignment of output interfaces to hash buckets in a next-hop group. With per-bucket traffic counters and proper software support, L1 could rearrange the hash buckets so that the traffic across both uplinks becomes more balanced (fewer hash buckets pointing to S1 than to S2). In a best-case scenario the reshuffling could be done without reordering in-transit packets (hint: move a bucket when it's empty -- see also [flowlets](/2015/01/improving-ecmp-load-balancing-with.html)).

{{<note info>}}Recent Broadcom data center switching silicon [includes the hardware support for the *Dynamic Load Balancing*](https://www.broadcom.com/blog/broadcom-s-trident-3-enhances-ecmp-with-dynamic-load-balancing) (HT: Jeroen van Bemmel) or *Adaptive Load Balancing* (choose your marketing lingo), it's just a question of whether it's implemented in the operating system. Arista EOS has it since at least 4.24.2F release.{{</note>}}

### Mission Impossible

Now for a really interesting scenario: imagine someone runs a bunch of backup jobs between L3 and L2, and they all land on S1-L2 link. The path L1-S1-L2 becomes congested (on the S1-L2 leg). Could L1 do anything about that? Most often, the answer is **no** and the only exception I'm aware of is Cisco ACI (at least they claim so -- see also [CONGA paper](https://people.csail.mit.edu/alizadeh/papers/conga-sigcomm14.pdf) / HT: Minh Ha). Juniper claims [they do something similar in Virtual Chassis Fabric](https://www.juniper.net/documentation/en_US/junos/topics/concept/virtual-chassis-fabric-traffic-flow-understanding.html) (HT: Alexander Grigorenko)

To change the forwarding behavior on L1 based on downstream congestion, there would have to be a mechanism telling L1 to reduce its utilization of one of the end-to-end paths. While that could be done with a routing protocol, no major vendor ever implemented anything along those lines for a good reason -- the positive feedback loop introduced by load-aware routing and resulting oscillations would be fun to troubleshoot. 

Ignoring the early IGRP implementations from early 1980s, I heard of [one implementation of QoS-aware routing protocol](/2015/09/dlsp-qos-aware-routing-protocol-on.html), and I've never seen it used in real life. Please also note that SD-WAN [uses a different mechanism to get the job done](/2015/07/routing-protocols-and-sd-wan-apples-and.html): it's not using a routing protocol but end-to-end path measurement. That approach works because SD-WAN solutions ignore the complexities of the transport network; they assume the transport network is a single-hop cloud full of magic beans.

### Could We Fix It?

Ignoring the crazy ideas of SDN controller dynamically reprogramming edge switches, the best way to solve the problem is ([yet again](/2011/05/complexity-belongs-to-network-edge.html)) an end-host implementation:

* Connect hosts to the network with multiple IP interfaces, not MLAG kludges.
* Use MP-TCP or similar to establish parallel TCP sessions across multiple paths using different pairs of source-destination IP addresses.
* When multiple TCP sessions between a pair of hosts land on the same path due to load balancing hashing algorithms, use an irrelevant field in the packet header (TTL, flow label...) to change the hash values -- see [FlowBender paper](https://conferences2.sigcomm.org/co-next/2014/CoNEXT_papers/p149.pdf) for details.

### Release Notes

2021-03-13
: * Link to Juniper VCF documentation
  * Information on Broadcom supporting Dynamic Load Balancing
  * Link to CONGA research paper
