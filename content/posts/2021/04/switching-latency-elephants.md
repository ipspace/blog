---
title: "Switching Latency Elephants: Congestion"
date: 2021-04-17 09:02:00
tags: [ switching, networking fundamentals ]
draft: True
---
My *[Is Switching Latency Relevant](/2021/04/switching-latency-relevant.html)* blog post mentioned *an elephant in the room* and asked the readers to identify it.

Many of them correctly identified congestion or queuing latency (more about that one in a minute), or pointed to endpoint latency. The endpoint latency is probably a pod of blue whales compared to everything else we've been discussing, and worthy of another blog post... but it's well worth measuring and understanding.

It doesn't make sense to optimize microseconds when the nodes connected to the network need milliseconds to respond. In other words: figure out what problem you're trying to solve, and focus on the lowest-hanging fruits first.
<!--more-->
Someone also mentioned that *QoS can lower the latency even further*. Unfortunately, that's a red herring. QoS can lower the latency of high-priority traffic during periods of congestion by placing them at the front of the queue, but it cannot beat the laws of physics. No QoS tricks can reduce whatever the serialization or switching latency happen to be under idle conditions. Also, keep in mind that QoS tends to be a zero-sum game -- you give someone more resources at the expense of someone else. The only exception I'm aware of is link compression, but I haven't seen anyone doing that since the days of sub-Mbps Frame Relay or ISDN circuits.
