---
title: "Is It Time to Replace TCP in Data Centers?"
date: 2023-01-10 07:41:00
tags: [ TCP, data center ]
---
One of my readers asked for my opinion about the provocative "_[It's Time to Replace TCP in the Datacenter](https://arxiv.org/abs/2210.00714)_" article by prof. [John Ousterhout](https://en.wikipedia.org/wiki/John_Ousterhout). I started reading it, found too many things that didn't make sense, and decided to ignore it as another attempt of a [proverbial physicist solving hard problems in someone else's field](https://xkcd.com/793/).

However, pointers to that article kept popping up, and I eventually realized it was a _position paper_ in a long-term process that included [conference talks](https://www.usenix.org/conference/atc21/presentation/ousterhout), [interviews](https://www.theregister.com/2022/07/27/replace_tcp_datacenter/) and [keynote speeches](https://netdevconf.info/0x16/session.html?keynote-ousterhout), so I decided to take another look at the technical details.
<!--more-->

Let's start with the abstract:

> Every significant element of TCP, from its stream orientation to its expectation of in-order packet delivery, is wrong for the data center. It is time to recognize that TCP's problems are too fundamental and interrelated to be fixed; the only way to harness the full performance potential of modern networks is to introduce a new transport protocol into the data center. 

If that doesn't sound like a manifesto rallying point, I don't know what does. Everyone is [fed up with TCP in one way or another](/2019/10/saved-tcp-is-most-expensive-part-of.html) (quite often because TCP gets blamed for unrelated problems like the [lack of a session layer](/2009/08/what-went-wrong-tcpip-lacks-session.html)), so it's not hard to react to that message with a "hear, hear!!!" TCP specifications are also full of arcane nerd knobs resulting in [bizarre behavior](https://withinboredom.info/blog/2022/12/29/golang-is-evil-on-shitty-networks/) due to [incompatible features](https://en.wikipedia.org/wiki/TCP_delayed_acknowledgment) being [enabled by default](https://news.ycombinator.com/item?id=34180239) in different TCP/IP protocol stacks. 

However, most attempts to persuade networking engineers to ignore the laws of physics inevitably fail when marketing encounters reality. Let's see how well the _It's Time to Replace TCP in the Datacenter_ article fares in that respect.

Prof. Ousterhout compares TCP with Homa, a new message-based connectionless transport protocol. The claims in the _position paper_ seem to be based on measurements described in [_A Linux Kernel Implementation of the Homa Transport Protocol_](https://www.usenix.org/conference/atc21/presentation/ousterhout) article, which used the following setup:

* Majority of the results was produced in a cluster of 40 nodes with a full mesh of bidirectional client-server traffic.
* It looks like the setup used a small number of parallel TCP sessions between a pair of nodes and tried to send multiple independent messages across a single TCP session resulting in transport-layer head-of-line blocking (more about that later).

As a starter, it's worth pointing out that the above scenario does not correspond to how TCP is used in most application stacks or production environments and is heavily biased toward connectionless alternatives to TCP, making the measurement results potentially inapplicable to real life.

### Transport Protocol Requirements

Ignoring the biased abstract, let's dig into the technical details, starting with the transport protocol requirements (section 2):

* Reliable delivery
* Low latency
* High throughput (including high message throughput)
* Congestion control
* Efficient load balancing *across server cores*
* NIC offload

So far so good, but there's a conspicuously missing requirement in that list: the recipient must know when it's safe to start working on a message, and it might not be safe to handle incoming messages out-of-order. While the order of execution might not matter for read-only transactions with no side effects, it's crucial if the messages cause a state change in the recipient application.

While the read-only transactions are usually more common than the read-write ones, the latter ones tend to impact data consistency, and raise the interesting challenge of providing consistent data to read-after-write transactions. Someone has to reshuffle incoming out-of-order messages into the sequence in which they were sent, and if the transport protocol is not doing that, everyone else has to reinvent the wheel. Look at the [socket API](/2009/08/what-went-wrong-socket-api.html) or [happy eyeballs](/2013/03/happy-eyeballs-happiness-defined-by.html) if you want to know how well that ends.

The *efficient load balancing across server cores* (as opposed to *across the network*) is also worrying -- it implies the CPU cores are the bottleneck, and might indicate unfamiliarity with the state-of-the-art high-speed packet processing. The focus on CPU cores and hotspots described in the deep-dive article might be an artifact of using small number of TCP sessions, which is an unnecessary artificial restriction -- _[systems running Nginx or NodeJS have been scaled to 1-million connections per server](https://blog.erratasec.com/2012/10/scalability-is-systemic-anomaly.html#.Y59TJewo_lw)_ a decade ago. Statistical distribution of TCP sessions to cores would also be much better with a larger number of TCP sessions.

Speaking of high-speed networking: most optimized implementations use CPU cores dedicated to packet processing, sometimes reaching a throughput of tens of Gbps per CPU core -- see for example [Snap: a Microkernel Approach to Host Networking](https://research.google/pubs/pub48630/), or what [fd.io](https://fd.io/) is doing. I have no idea where the author got "_Driving a 100 Gbps network at 80% utilization in both directions consumes 10–20 cores just in the networking stack_" -- the Snap paper quoted as a reference definitely does not support that claim.

### Everything about TCP Is Wrong

The next section of the article identifies everything that's wrong with TCP:

* Stream orientation (as opposed to messages)
* Connection-oriented protocol
* Bandwidth sharing
* Sender-driven congestion control
* In-order packet delivery

The first two points are valid -- TCP was designed to be a connection-oriented protocol transporting a stream of bytes[^SD]. The article goes into long lamentations of why that's bad and why a message-oriented transport protocol would be so much better but never asks even one of these simple questions (let alone tries to answer them):

[^SD]: Also, complaining about a screwdriver being bad at hammering nails just tells everyone you're misusing the tools.

* **What's wrong with Infiniband?** Environments focused on low latency often use Infiniband. Why should we use Homa to solve the challenges it is supposed to solve if we have a ready-to-use proven technology?
* **What's wrong with RoCE?** Maybe you dislike Infiniband and prefer Ethernet as the transport fabric. In that case, you could use RDMA over Converged Ethernet (RoCE) as a low-latency high-throughput mechanism.
* **What's wrong with existing alternatives?** Even if you don't like RDMA, you could choose between several existing message-oriented transport protocols. [SCTP](/2009/08/what-went-wrong-sctp.html) and [QUIC](/2022/10/worth-reading-quic-tcp.html) immediately come to mind. There's also [SRD](/2022/12/quick-look-aws-srd.html) used by AWS.
* **What happened to other RPC frameworks?** We had solutions implementing Remote Procedure Calls (RPC) on top of UDP, including Sun RPC, DNS and NFS. Some of them faded away; others started using TCP as an alternate transport mechanism instead of improving UDP. gRPC (the new cool RPC kid) uses HTTP/2[^gRPC] which rides on top of TCP. Why should that be the case, considering how bad TCP supposedly is? 
* **Why is everyone still using TCP?** There's no regulatory requirement to use TCP, and everyone is unhappy with it. Why are we still using it? Why is nobody using alternatives like SCTP? Why is there no QUIC-like protocol but without encryption (which is often not needed within data centers)? Why is nobody (apart from giants like Google and AWS) investing significant resources in developing an alternative protocol? Are we all lazy, or incompetent, or is TCP just good enough to shrug and move on?

[^gRPC]: Which totally surprised me as it kills some really cool ideas you implement with streaming telemetry. It's quite possible I'm missing something fundamental.

Anyway, not mentioning any of the alternative transport protocols seems biased and a significant omission, and misses the opportunity to discuss their potential shortcomings and how Homa might address them.

But wait, it gets better when we get to the networking details.

Starting with *bandwidth sharing*, the article claims that:

> In TCP, when a host's link is overloaded (either for incoming or outgoing traffic), TCP attempts to share the available bandwidth equally among the active connections. This approach is also referred to as "fair scheduling." 

That claim ignores a few minor details:

* It's really hard to influence incoming traffic.
* Bandwidth sharing is just a side-effect of running many independent TCP sessions across a network using FIFO queueing, but even then it's [far from ideal](/2022/11/worth-reading-congestion-control-not-fair.html).
* While a TCP/IP stack might try to provide fair scheduling of outbound traffic (but often does not), all bets are off once the traffic enters the network.
* Obviously, one could use QoS mechanisms (including priority queuing and weighted round-robin queuing) to change that behavior should one wish to do so.

The next claim is even worse (the *sender-driven congestion control* section makes similar claims):

> TCP's approach discriminates heavily against short messages. Figure 1 shows how round-trip latencies for messages of different sizes slow down when running on a heavily loaded network compared to messages of the same size on an unloaded network.

I checked the _Figure 1_, and it uses workload "_based on message size distribution measured on a Hadoop cluster at Facebook_" -- not exactly the most common data center scenario, but one that might exacerbate TCP shortcomings due to heavy incast. Even worse, the [deep dive article](https://www.usenix.org/conference/atc21/presentation/ousterhout) (the source for _Figure 1_) compares Homa (a connectionless messaging protocol) with a scenario in which a single TCP session seems to carry numerous messages generated in parallel:

> Streams also have the disadvantage of enforcing FIFO ordering on their messages. As a result, long messages can severely delay short ones that follow them. This head-of-line blocking is one of the primary sources of tail latency measured for TCP in Section 5.

Sending independent messages over a single TCP session obviously results in head-of-line blocking -- behavior that has been well-understood since the early days of HTTP. The solutions to head-of-line blocking are also well-known, from parallel sessions to QUIC.

Let me also reiterate that this is not how TCP is commonly used. Environments in which a single application client would send multiple independent competing messages to a single server tend to be rare.

Anyway, ignoring the "apples to mushroom soup" comparison, which skews the results so far that they become meaningless, let's focus on incast-generated congestion. Yet again, the countermeasures have been known for decades, from flow-based queuing to priority queuing or data center TCP (DCTCP) that reduces the average queue length. 

In any case, once we accept that it doesn't make sense to use a single high-volume TCP session between two nodes, what's stopping an optimized TCP implementation from setting a higher priority on traffic belonging to low-bandwidth conversations[^OC], similar to a [proof-of-concept implemented in Open vSwitch years ago](/2014/06/mice-elephants-and-virtual-switches.html)[^HP].

[^HP]: Reality might intervene: the network devices often ignore those signals as most networks don't trust host QoS marking, usually for an excellent reason -- everyone thinks whatever they're doing must be high priority.

[^OC]: At this point I'm almost expecting a comment from prof. Olivier Bonaventure saying "_we implemented this a decade ago, and here's the link to the corresponding paper._"

Finally, there's the *in-order packet delivery* -- the article claims that:

> TCP assumes that packets will arrive at a receiver in the same order they were transmitted by the sender, and it assumes that out-of-order arrivals indicate packet drops. 

IP never guaranteed in-order delivery[^RSRB], so TCP never assumed in-order packet arrival. The second part of the claim might have been valid in certain TCP implementations decades ago but is no longer true[^OOI].

[^RSRB]: That's why it was so cumbersome to implement Token Ring bridging on top of IP networks.

[^OOI]: Or so I was told by people who worked on TCP/IP implementations for ages. Please feel free to correct my ignorance.

But wait, it gets worse. When AWS [introduced SRD as the transport protocol for overlay virtual networks](/2022/12/quick-look-aws-srd.html), they claimed they observed a significant TCP performance improvements due to SRD packet spraying. At the same time, the Homa _position paper_ claims that:

> However, packet spraying cannot be used with TCP since it could change the order in which packets arrive at their destination. 

One of them must be wrong.

The ultimate gem in this section is the following handwaving argument:

> I hypothesize that flow-consistent routing is responsible for virtually all of the congestion that occurs in the core of data center networks.

As the server-to-network links tend to be an order of magnitude slower than the core links, I hypothesize that it takes a significant amount of bad luck to get core congestion solely based on flow-consistent routing. The statistical details are left as an exercise for the reader.

Regardless of the validity of that claim, flow-consistent routing might result in imbalance in edge or core link utilization, but even there we have numerous well-known solutions. I [wrote about flowlets in 2015](/2015/01/improving-ecmp-load-balancing-with.html) when there were already several production-grade implementations, while the [FlowBender paper](http://conferences2.sigcomm.org/co-next/2014/CoNEXT_papers/p149.pdf) was published in 2014. There's also the [Conga paper](https://people.csail.mit.edu/alizadeh/papers/conga-sigcomm14.pdf) implemented in Cisco ACI, and a [number of other well-known mechanisms](/2021/03/topology-congestion-driven-load-balancing.html) that can be used to alleviate the imbalance.

### Is It Time to Replace TCP in Data Centers?

I would love to see a reliable (as opposed to UDP) message-based transport protocol between components of an application stack and have absolutely no problem admitting that TCP is not the best tool for that job.

Also, based on the *[A Linux Kernel Implementation of the Homa Transport Protocol](https://www.usenix.org/conference/atc21/presentation/ousterhout)* article, in which the author described the proposed solution, it looks like they spent a lot of time implementing Homa as a Linux kernel module. I wish them all the best, but unfortunately I can't take Homa seriously based on the arguments made in this _position paper_ -- why should I trust the claimed benefits of a proposed solution if the _position paper_ favoring it misidentified the problems and ignored all prior art? 

Anyway, is this a problem worth solving? In many cases, the answer is a resounding **no**. Application stacks often include components that generate much higher latency than what TCP could cause. From that perspective, Homa looks a lot like another entry in the long list of solutions in desperate search of a problem.

Finally, the _It's Time to Replace TCP in the Datacenter_ article focuses solely on application-to-application messaging, which might be relevant for the "niche" applications like large microservices-based web properties, high-performance computing, or map-reduce clusters that use in-memory data structures or local storage. At the same time, it completely ignores long-lived high-volume connections that represent the majority of traffic in most data centers: storage traffic, be it access to remote disk volumes or data synchronization between nodes participating in a distributed file system or distributed database.

### LinkedIn Feedback

The blog post triggered [numerous interesting comments on LinkedIn](https://www.linkedin.com/posts/ivanpepelnjak_is-it-time-to-replace-tcp-in-data-centers-activity-7018586453815271425-IhGQ); this section contains an edited summary.

Jeff Tantsura and Jitendra Padhye on TCP in the data center:

{{<long-quote>}}
Networking in ML/AI clusters (in a some form of DC) are rarely using TCP today, they are most definitely won’t be using TCP going forward.

RoCEv2 (RDMA over IP/UDP) is often used, DCQCN is the most common CC implementation (with PFC as last resort). There’s quite some work on better CC and drop avoidance technologies, spray (with all the implications to be addressed) is an almost MUST.

You might take a look at work we have been doing in IETF: https://datatracker.ietf.org/doc/draft-miao-tsv-hpcc/ - looks very promising, with wide ecosystem and already significant deployment at Alibaba.

Over 65% of Azure traffic (bytes and packets) uses RoCEv2, not TCP. TCP is a distant second.
{{</long-quote>}}

Jeff Tantsura on congestion mechanisms:

{{<long-quote>}}
RFC3168 (published in early 2000) -- The Addition of Explicit Congestion Notification (ECN) to IP -- takes care of anything that runs over IP (more details in RFC8087). DCQCN (and many other technologies) make use of ECN marking to signal queue occupancy growth and allows sender to react accordingly (not necessary stop).
{{</long-quote>}}