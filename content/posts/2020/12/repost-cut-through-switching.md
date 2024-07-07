---
title: "Repost: Drawbacks and Pitfalls of Cut-Through Switching"
date: 2020-12-14 07:44:00
tags: [ switching ]
---
Minh Ha left a great comment describing additional pitfalls of cut-through switching on my [Chasing CRC Errors](/2020/12/chasing-crc-errors-data-center-fabric/) blog post. Here it is (lightly edited).

---

Ivan, I don't know about you, but I think cut-through and deep buffer are nothing but scams, and it's subtle problems like this  [*fabric-wide crc errors*] that open one's eyes to the difference between reality and academy. Cut-through switching might improve nominal device latency a little bit compared to store-and-forward (SAF), but when one puts it into the bigger end-to-end context, it's mostly useless.
<!--more-->
Take the topology in the post, say if the spine switch operates in cut-thru mode, then it can forward the frames a bit faster, only to be blocked up at the slower device(s) down the chain, as they're lower-end devices and so, can't handle the higher rate -- asynchronous speeds -- and being at the lower end, they might be SAF devices themselves. The downstream devices then become the bottlenecks, so end-to-end latency is hardly any better. Also, as cut-thru switches can't check CRC, they will just cause retransmission of bad packets, and along with it, an increase in end-to-end latency.

Even within the cut-thru switch itself, cut-thru mode is not always viable. Let's use Nexus 5k as an example. It uses single-stage crossbar fabric with Virtual Output Queue (VOQ). If you have output contention, which you always do if your network is highly utilized, then the packets need to be buffered at the input waiting for the output to be available. In that case, cut-thru behavior is essentially as good as SAF; both have to buffer the packets and wait for their turns to transmit.

Also, Nexus 5k (and other crossbar switches) uses cell-based fabric + VOQ to deal with Head-of-Line (HOL) blocking. So basically the crossbar has to provide speed-up/overspeed to both compensate for cell tax and evade the HOL blocking problem. Since the crossbar is therefore faster than the input interfaces, the asynchronous-speeds situation once again surface, and cells will have to be buffered before being sent across the crossbar. Plus, in each cell time, there're arbitration decisions made by the crossbar schedulers in regard to which cells get to enter the fabric, so buffering and waiting are inevitable.

All in all, the (dubious) benefit of cut-thru switching seems to be almost totally nullified. Not to mention cut-thru switches have more complicated ASICs and wiring than simple SAF switches, making it more expensive for no tangible gains.

I think cut-thru switching only makes sense if the whole network fabric runs the same model of switches, with simple protocol stack. So the place where it makes sense is niche markets like HPC cluster running low-overhead infiniband, or HFT trading, but the latter are mostly criminals trying to front-run each other anyway, so not sure if it's ethical to provide a tools for them to do damage to society.

In day-to-day networks that deal with a mixture of traffic types and aggressive traffic patterns, cut-thru switching, like deep buffer, is just a diversion, and provides yet another opportunity for vendors to sell their overpriced boxes.

I must admit, I did find Cisco very admirable for having the guts to come out and say it like it is, that these days Cut-thru and SAF are very similar performance-wise.