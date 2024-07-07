---
title: "A Quick Look at AWS Scalable Reliable Datagram Protocol"
date: 2022-12-14 07:17:00
tags: [ AWS, switching ]
---
One of the most exciting announcements from the last AWS re:Invent was the [Elastic Network Adapter (ENA) Express](https://aws.amazon.com/about-aws/whats-new/2022/11/elastic-network-adapter-ena-express-amazon-ec2-instances/) functionality that uses the [Scalable Reliable Datagram (SRD)](https://ieeexplore.ieee.org/document/9167399) protocol as the transport protocol for the overlay virtual networks. AWS claims ENA Express can push 25 Gbps over a single TCP flow and that SRD improves the tail latency (99.9 percentile) for high-throughput workloads by 85%.

Ignoring the "_[DPUs could change the network forever](/2023/01/dpu-change-network-forever/)_" blogosphere reactions (hint: they won't), let's see what could be happening behind the scenes and why SRD improves TCP throughput and tail latency.
<!--more-->
AWS developed SRD as a transport protocol for Elastic Fabric Adapters (the networking part of their HPC implementation). There's no magic behind SRD; it's just another data point in the transport protocol solution space:

* Like UDP, it provides a datagram transport.
* Unlike UDP, the datagram delivery is reliable.
* Unlike TCP (another reliable delivery protocol), SRD can reorder packets in transit and deliver them out-of-order.

SRD consumers are [supposed to deal with packet reordering](https://aws.amazon.com/blogs/hpc/in-the-search-for-performance-theres-more-than-one-way-to-build-a-network/) (unlike some UDP consumers that drop reordered packets).

Dropping the "in-order delivery" requirement allows AWS to send SRD packets in parallel over all alternate paths. That approach also reduces link congestion -- instead of a long burst of packets landing on a single link, the packet burst is spread across many parallel links.

Next step: [ENA Express uses SRD instead of GRE](https://aws.amazon.com/about-aws/whats-new/2022/11/elastic-network-adapter-ena-express-amazon-ec2-instances/) (or VXLAN or GENEVE) to transport Ethernet frames between hypervisor hosts, resulting in faster, reliable delivery. According to [AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ena-express.html), they even reorder incoming SRD packets into the proper sequence before passing them to the VM TCP/IP stack:

> Handles some tasks directly in the network layer, such as packet reordering on the receiving end, and most retransmits that are needed. This frees up the application layer for other work.

It's obvious why SRD increases the throughput of a single TCP session -- packets from a single session can be sent over multiple links[^BRC] -- but why does it decrease the tail latency?

[^BRC]: Brocade did [something similar ages ago in the VCS Fabric](/2011/04/brocade-vcs-fabric-has-almost-perfect/).

I know just enough about TCP to have incorrect opinions, but ([based on what people who should know better told me](/2019/06/do-packet-drops-matter-for-tcp/)) there are several reasons for variability in TCP throughput and latency:

* Packet drops could be a Really Bad Thing if your TCP stack uses [drop-sensitive congestion avoidance algorithm](https://en.wikipedia.org/wiki/TCP_congestion_control#Algorithms). Having reliable underlay transport solves this one.
* Early TCP implementations could interpret reordered packets as a packet drop of the intermediate packets (see above). I was told this was a solved problem and should have disappeared in recent TCP implementations after the TCP Selective ACK was implemented.
* Packet reordering also kills hardware-based Receive Side Coalescing, but it looks like AWS was more than willing to sacrifice the CPU cycles needed to sort the packets in software to get better performance.
* [Losing the last packet of a packet burst is a killer](/2019/06/do-packet-drops-matter-for-tcp/#3111488803170449903), even if your TCP stack uses Selective ACK. The receiver can't acknowledge the lost packet or send Selective ACK because there's no subsequent packet, forcing the sender to wait for the timeout. The real SNAFU:  the minimum TCP timeout on most operating systems is a few milliseconds, while the fabric transit times are measured in microseconds. No wonder the tail latency is through the roof and can be fixed with reliable transport of IP datagrams.

Now that you understand some of the reasons why ENA Express improves performance and tail latency, let's quickly deal with the inevitable hype:

* Is this a new idea? Of course not. We've used reliable frame transport for ages on media that were too noisy (or drop-prone) for TCP, starting with X.25 and analog modems using V.42 error correction and continuing with radio networks.
* Do you need a DPU to implement something like ENA Express? Absolutely not; you could implement it in the virtual switch like GRE, VXLAN, or GENEVE. It's just the question of which CPU cycles you like to burn.
* Could someone else do something similar? Of course, but it would require a focus on customer performance, a deep understanding of transport protocols, and engineering prowess. Charging the customers for services they consume also helps to focus your thinking. Is it fair to expect any of that from a company that needed years to add LACP to its virtual switch?

Want to know more about networking in AWS? Watch the [Amazon Web Services Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) webinar ;)

## Revision History

2023-01-26
: One of my readers politely pointed out that ENA Express reorders incoming SRD packets if needed. Fixed the relevant bits in the blog post.
