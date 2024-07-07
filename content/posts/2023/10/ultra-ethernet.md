---
title: "What Is Ultra Ethernet All About?"
date: 2023-10-03 05:47:00
tags: [ switching ]
---
If you're monitoring the industry press (or other usual hype factories), you might have heard about Ultra Ethernet, a dazzling new technology that will be developed by the Ultra Ethernet Consortium[^ITS]. What is it, and does it matter to you (TL&DR: probably not[^WHS])?

[^ITS]: Because they're sick and tired of the glacial speed at which IEEE moves

[^WHS]: Unless you work for a hyperscaler or train ML models on GPU clusters with tens of thousands of nodes, in which case I hope you're not reading this blog for anything else but its entertainment value.

As always, let's start with *What Problem Are We Solving?*
<!--more-->
For decades, we've known how to divide numerous computational problems into smaller parallel computations. Weather forecast is among those, as are multiple physics, chemistry, or astronomy simulations. The whole field of High-Performance Computing is built around the ability to split a large problem into smaller parts and combine their results. Big data is no different (remember *map-reduce* algorithms?), and neither is machine learning, whether training an ML model or trying to get usable answers from the trained model.

However, AI/ML is hot, and all the other stuff is boring[^BDH], so let's claim we need Ultra Ethernet for AI/ML workloads to generate attention, sell more stuff, and attract VC funding.

[^BDH]: After the big data hype dispersed, we realized we were sugarcoating applied statistics.

OK, it looks like the problem we're trying to solve is building a fabric to support distributed computations running in large clusters. Why do we need a new Ethernet technology to do that? What's wrong with the existing Ethernet?

As it turns out, for whatever weird reason, the programmers writing the software solving real-life problems want to focus on those problems, not on exchanging data between parts of the distributed computation. It's easiest for them to assume their algorithms run in multiple threads that can share memory. That approach works beautifully as long as the nodes running the computation share actual memory, be it many CPU cores in a server or multiple GPUs in a single chassis, but what happens when you have to grow beyond that? We knew the answer decades ago: [Remote Direct Memory Access](https://en.wikipedia.org/wiki/Remote_direct_memory_access) (RDMA). This solution allows a program to write directly into another program's memory even when the other program runs on a different host.
  
RDMA was designed to run over Infiniband. As expected, someone inevitably said[^RH], "*Hold my beer, I can make this work over Ethernet,*" so RoCE (RDMA over Converged Ethernet) was born. There are just a few tiny little problems with RoCE:

[^RH]: Around 2010, almost a decade and a half ago

-   Like FCoE, RoCE works best over lossless transport -- that's why it's running over *Converged Ethernet* that supports [Priority Flow Control](/2010/09/introduction-to-8021qbb-priority-flow/)[^PFC].
-   RoCE cannot deal gracefully with packet reordering.
-   RoCE's performance catastrophically degrades when faced with packet drops or out-of-order packets.

[^PFC]: Did you notice I wrote the "What is PFC" blog post around the same time RoCE was launched? I promise that's pure coincidence.

Running RoCE across a single switch is a piece of cake, and if you buy one of the newest data center switches[^CANGET], you'll get over 50 Tbps of bandwidth in a single box -- enough to build a cluster of 128 high-end GPUs with 400 GbE uplinks. You won't need more than that in most environments, so you probably don't have to care about Ultra Ethernet. Congratulations, you can stop reading.

[^CANGET]: Assuming you can get them anytime soon

Still here? I have a fun fact for you: some people need GPU clusters with tens of thousands of nodes, and the only (sane) way to connect them is to build a vast leaf-and-spine fabric, and that's where RoCE rears its ugly head:

-   Data exchange between a pair of nodes is a single UDP flow. Goodbye, efficient per-flow load balancing.
-   Lossless transport across a fabric inevitably has to deal with congestion avoidance, and trying to get fabric-wide congestion avoidance to work is usually an exciting resume-enhancing challenge[^NN].

[^NN]: It's not that we wouldn't have been aware of these challenges in the past. We encountered them with FCoE and iSCSI, but we never tried to run those protocols at such a scale.

Want to know more? Read *[Datacenter Ethernet And RDMA: Issues At Hyperscale](https://arxiv.org/pdf/2302.03337.pdf)*[^NOTCP]. 

[^NOTCP]: Another article that seems to hint it's [time to replace TCP in the data center](/2023/01/data-center-tcp-replacement/) ;)

As always, you can fix the problem in three ways:

-   Fix the application software or middleware (fat chance)
-   Develop a new networking technology and sell tons of new ASICs (the Ultra Ethernet way)
-   Insert a smart NIC between the application and the network, and let it handle the hard stuff[^R6], like pretending the out-of-order packet delivery didn't happen.

[^R6]: Proving yet again RFC 1925 rule 6a

Broadcom figured out they already have *the new technology*[^NFD]. Many chassis switches use internal cell-based transport and cell spraying across all (intra-switch) fabric links with the egress linecard handling packet reordering before forwarding the reassembled packet to the egress Ethernet port. That solves the optimal load balancing part of the challenge.

[^NFD]: For more details, watch the [Networking Field Day 32](https://techfieldday.com/appearance/broadcom-presents-at-networking-field-day-32/) videos.

These switches also use *Virtual Output Queues* -- the output port queues are on the ingress linecards, and the ingress linecard transmits data over the fabric only when the egress port can accept it. Virtual output queues move the congestion closer to the ingress port, preventing fabric-wide congestion from spreading when an output port becomes congested. That solves the "*congestion avoidance in large fabrics is a hard problem*" part of the challenge.

Now imagine you disaggregate[^DG] a chassis switch, repackage linecards and fabric modules into standalone boxes, and replace internal copper[^CP] links with transceivers and fibers. Congratulations, you built a virtual switch that can supposedly have up to 32.000 ports. BTW, do you remember those *virtual output queues* from the previous paragraph? Each ingress switch should have an output queue for each output port[^VOQ], so you need at least 32.000 fabric-facing queues per ASIC. All that complexity is bound to result in an expensive ASIC. Lovely, but what else did you expect?

[^DG]: Isn't that a great word when you want to sound smart?

[^CP]: Or whatever it is these days

[^VOQ]: Or bad things start to happen, like a congested port slowing down adjacent ports. How do you think we know that? ;)

There's just one tiny problem with Broadcom's approach: while it (probably) works, it's proprietary and will likely stay that way forever[^BCM]. That might upset other vendors (more so if they don't have a comparable ASIC), so they're trying hard to hammer the square peg (RoCE) into the round hole (Ethernet with minimal modifications). [Ultra Ethernet position paper](https://ultraethernet.org/wp-content/uploads/sites/20/2023/07/23.07.12-UEC-1.0-Overview-FINAL-WITH-LOGO.pdf) claims they plan to:

[^BCM]: At least considering the [history of Broadcom's openness](/2016/05/what-are-problems-with-broadcom/).

-   Add multipathing and packet spraying to Ethernet.
-   Get rid of the "Ethernet is not IP and does not reorder packets" constraint.
-   Invent new magic[^NM] that will finally solve fabric-wide congestion challenges because "*None of the current algorithms meet all the needs of a transport protocol optimized for AI.[^WAI]"*

[^NM]: For ages, people claimed they solved Internet-wide QoS or implemented a centralized control plane for WAN networks. Unfortunately, most of those solutions had an unexpected glitch or two. I don't expect this one to be any different.

[^WAI]: Not "optimized for long-lived high-volume flows" or "low number of high-volume flows," it has to be "optimized for AI" because that hype sells unicorn farts.

Now for the final bit of the puzzle: how can you run a protocol that does not tolerate packet reordering across a network that reorders packets due to packet spraying? It turns out you could do some heavy handwaving in the existing RoCE NICs; for more details see the *‌[To spray or not to spray: Solving the low entropy problem of the AI/ML training workloads in the Ethernet Fabrics](https://web.archive.org/web/20230917162058/https://www.linkedin.com/pulse/spray-solving-low-entropy-problem-aiml-training-fabrics-shokarev/)* article by Dmitry Shokarev.

### Behind the Scenes

J Metz described some of the reasons the Ultra Ethernet Consortium was created in a [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7140339582054612992/):

{{<long-quote>}}
We didn't create UEC because "IEEE was too slow." We created UEC because in order to ensure that the network fabric was tuned for the workloads correctly, there were too many touchpoints for IEEE (or IETF or NVMe or SNIA or DMTF or OCP or... or... or..) to cope with.

We entertained the notion that we could attempt to insert our ideas into each and every standards or specification body as needed, but that was a fool's errand. Instead, we have opted to create our own SDO (Standards Development Organization) and, instead, partner or align with these other organizations to ensure industry-wide compatibility.

So far, with working relationships with IEEE 802.3, OCP, and many more in the works, this strategy appears to be succeeding. UEC has tapped into a much bigger need than even we anticipated at the onset.
{{</long-quote>}}

### Revision History

2023-12-13
: Added the *Behind the Scenes* section
