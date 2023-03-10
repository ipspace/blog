---
date: 2021-03-17 06:59:00+00:00
multihoming_tag: session
series:
- UCMP
- multihoming
tags:
- TCP
- QoS
title: 'Repost: Using MP-TCP to Utilize Unequal Links'
---
In the *[Does Unequal-Cost Multipathing Make Sense](https://blog.ipspace.net/2021/02/does-ucmp-make-sense.html)* blog post I wrote (paraphrased):

> The trick to successful utilization of unequal uplinks is to use them wisely [...] It's how multipath TCP (MP-TCP) could be used for latency-critical applications like Siri.

Minh Ha quickly [pointed out (some) limitations of MP-TCP](https://blog.ipspace.net/2021/02/does-ucmp-make-sense.html#428) and as is usually the case, his comment was too valuable to be left as a small print at the bottom of a blog post.

{{<note>}}Intuitively I don't necessarily agree with all of his conclusions, but don't know enough to have a qualified opinion.{{</note>}}
<!--more-->
---
While MPCTP indeed has its use, in mobile networks where the RTT can vary big time between Wifi and 4G, MPTCP can suffer from head-of-line blocking on both sender and receiver side, when one sub-flow has to wait for another carrying earlier packets to arrive, basically out-of-order problem. Also, when the flow size is small and bandwidth is high, MPTCP might not have time to utilize the sub-flows or use them effectively, resulting in similar or even worse latency than vanilla TCP.

In data center (DC) scenarios, again results vary. For workloads that make use of long-lived elephant flows, MPTCP can provide throughput benefits. For mice flows, which also account for a lot of traffic in DCs, MPTCP's setup and scheduling overhead outweighs its benefit, so latency performance can be lower than that of single-flow TCP. Also, for disk-bound workloads, since the network is much faster than the disk access time, using MPTCP again provides no benefit, as the bottleneck lies with the disk system.

OTOH, MPTCP can cause starvation/fairness issues in partition/aggregate workload, like MapReduce, or any kind of many-to-one traffic. This kind of traffic can result in Incast scenarios, and TCP Incast can result in [TCP Outcast](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/prakash) problem for small flows destined to the same host as big flows. MPTCP makes Outcast worse because of its multi-flow nature, adding to the total number of competing flows.

I think wrt to DCs, DC-TCP provides a much better solution than MPTCP. It works well; it mitigates Incast and Outcast problems, and it does away with big buffer, improving latency. Practically speaking, DCs already have much smaller RTT latencies than WAN/Internet, so solutions that are not viable on the later can be applied here. I'm referring specifically to per-packet ECMP. Per-packet ECMP provides close to ideal network capacity utilization, at the expense of potential reordering. But since DC links have plenty of capacity, DC networks also have much lower latencies, reordering is less likely (due to lots of bandwidth) and can be tolerable (due to much lower RTTs). Coupling that with DC-TCP which deals efficiently with congestion, and we can have a network that makes the best use of traffic load balancing, all without the need for MPTCP, which can be complex to implement.
