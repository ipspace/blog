---
anycast_tag: ecmp
date: 2021-06-01 06:35:00+00:00
ospf_tag: ucmp
series:
- UCMP
- anycast
tags:
- IP routing
- OSPF
title: Single-Metric Unequal-Cost Multipathing Is Hard
---
A while ago, we discussed whether [unequal-cost multipathing (UCMP) makes sense](/2021/02/does-ucmp-make-sense/) (TL&DR: rarely), and whether we could implement it in [link-state routing protocols](/2021/03/ucmp-link-state-protocols/) (TL&DR: yes). Even though we could modify OSPF or IS-IS to support UCMP, and Cisco IOS XR even implemented those changes ([they are not exactly widely used](/2021/03/ucmp-link-state-protocols/#496)), the results are... suboptimal.

Imagine a simple network with four nodes, three equal-bandwidth links, and a link that has half the bandwidth of the other three:

{{<figure src="/2021/06/UCMP-Square.png">}}
<!--more-->
It obviously makes sense to spread the load between E1 and E2 in a 2:1 ratio (⅔ of the traffic going over C2 and ⅓ of the traffic going over C1). That's not what you'd get if you add the link costs together. The cost of E1-C1-E2 is 30, the cost of E1-C2-E2 is 20, and thus the load balancing ratio will be 2:3 (or something similar).

There's absolutely no way that you would get the load balancing ratios right in a single-metric routing protocol without getting insane trying to tweak the link metrics. You _could_ get the metrics just right with some interesting math, using a tool like Cariden MATE, or using MPLS-TE tunnels (where the load balancing ratio is determined by relative tunnel bandwidth)... but it's not trivial.

How about the data center anycast use case I [mentioned the last time](/2021/06/tcp-anycast-hard/)?

{{<figure src="/2021/06/Anycast-TCP.png">}}

What we'd like to have is 75% of the traffic going from L4 toward L1 (where it's spread between A, B, and C) and 25% of the traffic going toward L2. 

A simplistic approach could assign humongous costs to the server links (so that the intra-fabric cost would be negligible compared to the total cost), but you'd still be stuck with 50:50 ratio between L1 and L2 -- no implementation of a link-state protocol I've seen so far is reducing the link cost based on availability of parallel links. S1 would see 10.42.0.1/32 prefix being available through L1 with exactly the same cost as through L2.

Yet again, you could tweak the metrics and change them automatically every time you add or remove a server (congratulations, you implemented a self-driving software-defined network), but I wish you luck trying to troubleshoot that Rube Goldberg invention.

The only way to make anycast UCMP work well is to realize the problem has two components:

* **Network topology component** -- find the end-to-end paths from ingress to egress devices
* **Endpoint reachability component** -- find how many endpoints are connected to every egress device and change the load balancing ratios accordingly.

Do we have a set of routing protocols that could do all that? Of course, one of them is called BGP 😉... and in the next blog post in this series, we'll use BGP to solve the problem.

### More to Explore

Interested in challenging networking fundamentals like what we discussed in this blog post? You might find the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar interesting (and parts of it are available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free)).
