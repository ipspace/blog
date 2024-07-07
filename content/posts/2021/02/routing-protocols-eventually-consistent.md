---
date: 2021-02-17 06:38:00+00:00
ospf_tag: rant
series:
- consistent-state
tags:
- networking fundamentals
- OSPF
- IS-IS
title: Link-State Routing Protocols Are Eventually Consistent
---
One of my readers sent me this interesting question:

> Assuming we are running a very large OSPF area with a few thousand nodes. If we follow the chain reaction of OSPF LSA flooding while the network is converging at the same time, how  would all routers come to know that they all now have same view of area link states and there are no further updates or convergence?

I have bad news: the design requirements for link state protocols effectively prevent that idea from ever working well. 
<!--more-->
Big picture first: as I explained in the [Routing Protocols](https://my.ipspace.net/bin/list?id=Net101#ROUTING) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar, link state protocols use a distributed database (OSPF or IS-IS topology database) with numerous instances of the same application (SPF algorithm) using the data from that database. 

Next step: a few design requirements. Routing protocols have to be resilient against all sorts of network failures including link loss, node loss, or network partitioning. Combine that with the idea of using a distributed database, consider the impact of CAP theorem, and you'll quickly realize that the only way forward is to use [*eventually consistent database* with *last-writer-wins* edit conflict resolution](/2021/02/state-consistency-distributed-controllers.html#consistency-requirements). 

{{<note info>}}If the previous sentence sounded like Latin, start with [State Consistency in Distributed SDN Controller Clusters](/2021/02/state-consistency-distributed-controllers/) blog post.{{</note>}} 

Even worse, a node might be lost forever. Every node running a link-state routing protocol inserts its own local topology data into the distributed database, and no-one else can touch that data. Link state protocols thus need a garbage collection mechanism to purge the irrelevant data from the distributed database. Welcome to LSA/LSP aging concept.

Back to the original question... considering the environment a routing protocol has to survive, it's clear we cannot expect any sort of network-wide reliable transport or signaling mechanism. Asking the question "*how would all routers know they have all the data they need*" is therefore equivalent to solving *[Byzantine agreement problem](https://en.wikipedia.org/wiki/Byzantine_fault)*. That problem has been solved (example: [Byzantine Paxos](https://en.wikipedia.org/wiki/Paxos_(computer_science)#Byzantine_Paxos)), but it's questionable whether the significant added complexity is worth the minimal gain considering the myriad ways in which a packet might be lost in the network anyway.

The "*is it worth it?*" and "*what problem are we solving?*" considerations also answer the second question from my reader:

> Why can't we use a global timer to prevent routers using a link-state algorithm from forwarding traffic (that can potentially cause traffic black holes or transit loops) as in theory this entire large area can take significant amount of time to converge besides having dependency on physical resources, topology etc.

Link state routing protocols were introduced to provide fast reaction to network topology changes, not a provably consistent network-wide forwarding state. Sometimes it's better to provide a fast good-enough answer than to spend a long time looking for the absolutely correct answer.

{{<note info>}}For an interesting take on this deliberation, read *[Thinking, Fast and Slow](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow)* by Daniel Kahnemann{{</note>}}

## Stories Are Not Data, but Here We Go

When IEEE started designing Shortest-Path Bridging (SPB -- 802.1aq) they realized they needed a routing protocol to get the job done (surprise, surprise...). They decided to use IS-IS as the underlying routing protocol, but wanted to stick to the *no loops ever* Ethernet bridging mantra... effectively trying to hammer a round peg into a square hole.

They got it done (in a way). 802.1aq introduced the concepts of *loop mitigation* and *loop prevention* to Ethernet bridging. Loop mitigation is effectively an RPF check, while loop prevention modified IS-IS to "*exchange information between neighboring bridges to ensure either that their topology calculations are consistent and each frame is consistently allocated to the same active topology, or that frames are not relayed.*" The standard is also pretty clear about the tradeoffs: "*‌Allowing temporary loops to form for unicast traffic and using loop mitigation provides for faster response to topology changes.*" (what have I just told you 🤷‍♂️).

I tried really hard to understand how the IS-IS modifications would work, but the whole thing was so complex I gave up after a while... and I was not the only one. Now we're coming to the *story* part.

When SPB was still the new kid on the block I met a distinguished engineer very active in the SPB community and working for one of the few vendors that decided to implement SPB. I congratulated him on the way they solved IS-IS consistent topology challenges and while I don't remember his exact reply (it must have been a decade ago), it was along the lines of "*We never implemented that part. It was too complex. It turns out loop mitigation is good enough even for Ethernet bridging*". Some bright ideas are obviously not worth implementing.


