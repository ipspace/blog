---
date: 2020-11-10 07:14:00+00:00
series:
- fast-failover
tags:
- IP routing
title: 'Fast Failover: The Challenge'
---
Sometimes you're asked to design a network that will reroute around a failure in milliseconds. Is that feasible? Maybe. Is it simple? Absolutely not. 

In this series of blog posts we'll start with the basics, explore the technologies that you can use to reach that goal, and discover one or two unexpected rabbit holes.

{{<note info>}}Fast failover is just one of the topics we'll discuss in *Advanced Routing Protocol Features* part of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.{{</note>}}
<!--more-->
### The Basics

Adapting network forwarding behavior following a link- or node failure includes at least these steps:

1. Detecting the failure;
2. Adjusting forwarding behavior near the failure point (when possible);
3. Disseminating changed topology information;
4. Recomputing network topology graph (link-state protocols) or adjusting routing tables (distance vector protocols)
5. Adjusting forwarding tables based on new routing table information.

The moment you start relying on distributed computation (steps 3-4) it's neigh impossible to reroute around a failure in a few milliseconds; the only way to reach that goal is to have localized redundancy that can be utilized without consulting anyone else.

Please note that you need localized redundancy **per destination** (Forwarding Equivalence Class in MPLS terms), be it IP prefix, IP address, or MAC address. It's also perfectly possible to design fast failover for some (critical) destinations but not for others.

There are at least three options to get local redundancy:

* **Redundant equal-cost links**, connected to the same downstream node, or to a set of downstream nodes.
* **A link to a feasible successor** - an adjacent node that is guaranteed not to use local node for traffic forwarding toward the destination.
* **A tunnel to a distant feasible successor** - when all adjacent nodes use local node to reach a destination, you could rely on a tunnel leading to a far-enough node which is guaranteed to use a different path toward the destination.

We'll cover the details of all three options and the potential implementation mechanisms in a series of blog posts, but before embarking on this journey it makes sense to ask a few simple questions:

* Do you need fast failover?
* How fast is good enough?
* Can you make it work?
* Is the added complexity worth the effort?

### Do You Need Fast Failover?

Unless you're carrying critical traffic where a temporary disruption might cause loss of life or billions of dollars in damages, the answer is most probably "*not really*". 

However, if you're implementing a control system for a nuclear power plant, a video network to support long-distance heart surgeries, or a voice network for 112 (Europe)/911 (US) service please stop reading right now and get expert help.

### How Fast Is Good Enough?

Years ago when I was still young and enthusiastic I considered 50 msec failover a holy grail everyone tries to reach... until I attended a [presentation by Ian Farrer](/2013/11/deutsche-telekom-terastream-designed/), who pointed out an oft-overlooked fact: maybe you should read your Service Level Agreement first, and design your network to support what you promised instead of chasing the grail. Maybe you could reach what you have to deliver with a  decently-implemented routing protocol.

### Can You Make It Work?

Remember the first step in the _Basics_ section: detect the failure? The failover process can't start until someone realizes there's been a failure.

Most network designs promising extremely fast failover times rely on some external magic to provide instantaneous failure detection. Most commonly used magic in modern networks is _loss of light_: the optical cable will be cleanly cut in a microsecond, and the transceiver will report the failure in less than a millisecond.

Really? Sometimes you're lucky and things do work that way. Sometimes you get [gray failures](/2017/10/to-bfd-or-not-to-bfd/). Sometimes an intermediate box that you have no control over (repeater, media converter) doesn't propagate loss-of-light condition.

"_No problem_", a seasoned networking engineer says, "_we'll detect the failure with BFD_". Of course he's right... but how fast could BFD detect a failure? It depends on how low you can tweak the BFD timers before getting an unstable network, and that depends on the specifics of BFD implementation. 

Regardless of what the actual value is, pondering a failover solution faster than BFD failure detection time is a colossal waste of time.

### Is the Added Complexity Worth the Effort?

In most cases, the answer is NO, in particular if the [failures are rare](/2019/06/know-thy-environment-before-redesigning/).