---
date: 2014-09-08 18:19:00+02:00
distributed-systems_tag: sdn
ha-cluster_tag: overview
high-availability_tag: ignore
series:
- ha-cluster
- distributed-systems
series_weight: 1600
tags:
- SDN
- high availability
title: Controller Cluster Is a Single Failure Domain
url: /2014/09/controller-cluster-is-single-failure.html
---
Some OpenFlow-focused startups are [desperately trying to tell you how redundant their architecture is](http://www.bigswitch.com/blog/2014/06/02/modern-openflow-and-sdn-part-ii). Unfortunately all the whitepapers (and the prancing unicorns) cannot change a simple fact: an SDN controller (OpenFlow-based or otherwise) is in some aspects a single failure domain.
<!--more-->
### But the Controller Cluster Will Save the Day

No, it won't. A controller cluster will protect you against hardware failures, which are probably the last 1% of all failures you'll encounter (if that's not the case, change the hardware). A cluster will not protect you against software failures (= bugs) or operator mistakes (= fat fingers).

An active/standby controller cluster might be less sensitive than an active/active one. If the active controller crashes, the standby controller takes over (similar to supervisor failover in most high-end switches) and starts with a fresh copy of the data structures. Controllers in an active-active cluster might share the data structures and thus be affected by the same bug at the same time.

A controller crash might also be triggered by a malformed packet, or even a perfectly valid one -- decades ago one of my hosts generated a legitimate ARP packet that consistently crashed next-hop Cisco router. In this case, it's reasonable to expect the backup controller to crash as soon as it takes over and receives the same packet from the same host.

Finally there's the complexity of the clustering software. I haven't heard of a clustering solution that would provably work under all possible weird conditions (and it's pretty hard to test all of them); [failovers between supervisor modules](http://blog.ipspace.net/2014/04/should-we-use-redundant-supervisors.html) are no exceptions.

{{<note>}}Obviously, if there's a perfect clustering solution out there, I'd love to hear about it. Please write a comment.{{</note>}}

### What Can We Do?

The solutions to this challenge are well known:

-   Distributed systems are more resilient than centralized ones;
-   Loosely coupled systems (example: [BGP SDN](http://blog.ipspace.net/2013/10/exception-routing-with-bgp-sdn-done.html)) are more resilient than tightly coupled ones (example: [OpenFlow controller](http://blog.ipspace.net/2013/09/openflow-fabric-controllers-are-light.html));
-   [Network infrastructure *enhanced* by a controller](http://demo.ipspace.net/get/5.20%20-%20Plexxi%20Affinity%20Networking.mp4) is more resilient than one that relies on a controller to operate;
-   [Complexity at the edge of the network](http://blog.ipspace.net/2011/05/complexity-belongs-to-network-edge.html) scales better than centralized complexity.

Not surprisingly, scalable SDN solutions from [Google](http://blog.ipspace.net/2012/05/openflow-google-brilliant-but-not.html), [Microsoft](https://www.nanog.org/sites/default/files/wed.general.brainslug.lapukhov.20.pdf) and (supposedly) Facebook, as well as some network virtualization solutions use most or all of these principles.

### Need a Bigger Picture?

Check out [SDN](http://www.ipspace.net/SDN) and [cloud networking](http://www.ipspace.net/Cloud) resources on ipSpace.net.
