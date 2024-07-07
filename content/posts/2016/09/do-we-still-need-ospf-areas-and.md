---
date: 2016-09-05 12:48:00+02:00
ospf_tag: areas
tags:
- design
- OSPF
- WAN
title: Do We Still Need OSPF Areas and Summarization?
url: /2016/09/do-we-still-need-ospf-areas-and/
---
One of my [ExpertExpress design discussions](http://www.ipspace.net/ExpertExpress) focused on WAN network design and the need for OSPF areas and summarization (the customer had random addressing and the engineers wondered whether it makes sense to renumber the network to get better summarization).

I was struggling with the question of whether we still need OSPF areas and summarization in 2016 for a long time. Here are my thoughts on the topic; please share yours in the comments.
<!--more-->
### Do We Need OSPF Areas?

When OSPF was created, it used areas to minimize the size of the topology graph and the time it took to run the Dijkstra algorithm. In the meantime, the CPU speeds increased by orders of magnitude, and graph computation algorithms got a few optimization boosts (*incremental SPF*, for example).

{{<note>}}IIRC, we were told decades ago the computational complexity of the Dijkstra algorithm is O(V\^3), where V is the number of vertices (routers). However, its [real computational complexity](http://stackoverflow.com/questions/26547816/understanding-time-complexity-calculation-for-dijkstra-algorithm) (when implemented correctly) is O(E log V) where E is the total number of edges (links), or way less than what we were told.{{</note>}}

There are obviously still limits to what CPUs can handle, but anecdata suggests having a few hundred routers in an OSPF area is no big deal (unless, of course, that includes nodes with $0.02 CPUs).

Based on this reasoning, one would say that:

-   It doesn't make sense to worry about OSPF areas if you have tens of routers;
-   You definitely have a problem if you have thousands of routers, and BGP is probably your friend;
-   In between, there's an *It Depends* area.

However, even if you feel you have to split your network into multiple areas to cut down the size of the topology graph, you might not need route summarization.

### Do We Need Inter-Area Route Summarization?

Let's be frank: route summarization is a royal pain. You need a hierarchical addressing plan (which means you need an addressing plan in the first place), and even when you do it right, things start moving around (or get connected to the wrong place), ruining your wonderful design.

Even worse than that are area splits. Announcing the same summarized prefix from two points that are not in a contiguous area is a perfect blackhole recipe (just ask anyone who advertised the same prefix from two data centers and lost the DCI link).

{{<note>}}To be more precise, the routers advertising a summarized prefix should be connected by a path going exclusively through the part of the network with more specific prefixes. GRE tunnel also satisfies that criteria; the proof is left as an exercise for the reader.{{</note>}}

With the route summarization being such a pain, one has to wonder why they introduced it in the first place. There were at least three good reasons for that decision:

-   Reducing the size of the routing tables;
-   Reducing the CPU load across areas;
-   Preventing a change within an area from impacting other areas.

The first reason is mostly bogus in 2016 unless you have a huge network.

If you feel you might have a problem with the CPU load, you SHOULD change the vendor. Changes in inter-area LSAs trigger partial SPF, which is relatively cheap compared to full SPF.

However, there's the *failure domain separation* aspect of route summarization.

### Areas and Route Summarization Split Network in Isolated Failure Domains

If you implement OSPF areas and route summarization correctly, you get excellent separation of failure domains:

-   Failures in the core network don't impact nodes in the access network (particularly if you use totally stubby areas);
-   Failures in the access network don't impact the core network (particularly if you include border router loopback IP address in the summarized prefix);

Are the pains of using OSPF areas and getting the route summarization just right worth it? As always, it depends, and maybe we're yet again using the wrong tool to solve the problem. Here are a few alternatives:

-   Using BGP for customer routes and OSPF for core routes. I know this sounds like "*BGP is the answer, what was the question?"*, but this is the design used successfully in hundreds of large-scale networks, so maybe it isn't that bad.
-   Reducing the number of changes in the access network (where most of the flaky links are) using functionality like [IP event dampening](http://www.cisco.com/c/en/us/td/docs/ios/12_0s/feature/guide/s_ipevdp.html) or network automation scripts (EEM is good enough) to kick flapping interfaces offline.

However, using one of these alternatives requires:

-   An approximate understanding of the network behavior (= how often do you get link flaps and how bad could they be);
-   An estimate of the actual business requirements (= can I keep a remote site down for five minutes because the link is flapping) as opposed to "*everything has to converge in 50 msec because voice*"

Meh, maybe it's easier to rely on the magic properties of OSPF route summarization and blame protocol designs or vendor implementations when things go wrong than dealing with other people within your organization.

### More Information

* I explained the routing protocol fundamentals in the *[Routing Protocols](https://my.ipspace.net/bin/list?id=Net101#ROUTING)* part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.
* Russ White wrote two articles about *slicing and dicing flooding domains*: [part 1](https://rule11.tech/flooding-domains-1/), [part 2](https://rule11.tech/flooding-domains-2/).
