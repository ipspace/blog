---
title: "On Routing Protocol Metrics"
date: 2024-01-08 07:38:00+0100
tags: [ IP routing, networking fundamentals ]
---
This LinkedIn snippet just came in from the _someone is not exactly right on the Internet_ department:

> Unlike IGP protocols, BGP is not dependent on a single type of metric to choose the best path.

EIGRP is an immediate counterexample that brought the above quote to my attention, but it's worth exploring the topic in more detail.
<!--more-->
All routing protocols have the same (generic) job:

* Find the set of potential destinations
* Find one or more of the best paths to each destination
* Insert the destinations and some next hops (direct or indirect) toward them in the forwarding table.

In this blog post, we'll focus on the second bullet. To decide what a _best path_ might be, the paths must be _comparable_. To implement a sorting algorithm[^BPS], something must tell that algorithm whether A is better than B. Routing protocols usually use _metrics_ to get the job done.

[^BPS]: Best path selection is conceptually a large number of sorting operations of all potential paths toward a single destination, where all but the top results are discarded.

The routing protocol metrics could be _scalars_ (a single value) or _vectors_ (a set of values). RIP, OSPF, and IS-IS use scalar metrics (cost); EIGRP and BGP use vector metrics.

Comparing scalar metrics is trivial[^LEFR]; comparing vector metrics could be interesting:

[^LEFR]: Proving that is left as an exercise for the reader ;)

* BGP metrics have strict precedence order -- for example, local preference is stronger than AS-path length.
* EIGRP calculates a scalar value (composite metric) out of the vector metric and uses the composite metric to select the best path to a destination.

One might wonder why EIGRP goes through the convoluted two-stage process. It has to do that because every component of the vector metric is adjusted differently as the end-to-end metric is accumulated through consecutive routing updates.

Sounds like Latin? Let's unroll it a bit:

* To get started, a routing protocol has to know the local (interface) metrics to local destinations.
* Those local metrics are advertised together with the local destinations to whomever the routing protocol perceives to be its neighbors.
* As a routing protocol receives an update from its peer, it has to adjust the metrics advertised by the peer to account for the transit cost to get to its peer.

RIP has a trivial "adjust the metric" algorithm: increase the hop count by one. OSPF and IS-IS are adding positive interface metric (cost) to the reported metric[^SPF]. EIGRP is already a bit more complex:

[^SPF]: When OSPF and IS-IS were designed, the most efficient SPF algorithm (Dijkstra's algorithm) required positive scalar metrics. While I know the SPF problem has been solved for graphs with negative costs, I don't know how efficient the solutions are (not that we would care that much in the world of 4GHz CPUs with megabytes of cache).

* *Delay* and *hop count* are accumulated across hops[^PBR]
* *Bandwidth*, *MTU* and *reliability* are minimized hops.

[^PBR]: That's why you should tweak the EIGRP delay (not bandwidth) if you want to push traffic onto alternate paths.

It looks like the link-state routing protocol community thought an additive scalar metric wasn't hip enough for the 21st millennium. [IGP Flexible Algorithm](https://www.rfc-editor.org/rfc/rfc9350.html) (RFC 9350) specifies OSPF and IS-IS TLVs that allow you to create your own vector metric comparison algorithm and a bunch of other RFCs specify all sorts of vector metric components those algorithms can use.

Finally, BGP is (as always) a nutcase of complexity:

* Weight has local significance and is not even part of the vector metric
* Local preference is lost across EBGP sessions
* AS path is (usually) increased across EBGP sessions.
* MED is sent over EBGP sessions but not propagated beyond the adjacent autonomous system.
* Next hops are there to fill the slots in the forwarding table but then used together with IGP costs as tiebreakers.

To make matters ~~worse~~ even more interesting, BGP allows you to attach post-it notes[^BC] to routing updates to tell someone down the road to adjust their vector metric. What's not to like there; you have infinitely many ways to make your network as complex as you like.

[^BC]: Called _BGP communities_ just to confuse everyone

### Want to Know More?

* Watch the *[Routing Protocols](https://my.ipspace.net/bin/list?id=Net101#ROUTING)* part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar (no registration required)
* Figure out how BGP works through a [set of lab exercises](https://bgplabs.net/) you can run on your laptop or a (public cloud) Ubuntu VM instance.
