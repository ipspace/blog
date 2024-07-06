---
date: 2015-01-19 07:42:00+01:00
tags:
- data center
- fabric
- load balancing
title: Improving ECMP Load Balancing with Flowlets
url: /2015/01/improving-ecmp-load-balancing-with.html
---
Every time I write about [unequal traffic distribution across a link aggregation group](/2015/01/load-balancing-elephant-storage-flows.html) (LAG, aka Etherchannel or Port Channel) or ECMP fabric, someone asks a simple question "*is there no way to reshuffle the traffic to make it more balanced?*"

**TL&DR summary**: there are ways to do it, and some vendors already implemented them.
<!--more-->

### The Problem

The algorithm that spreads the traffic across a group of outbound links (LAG or set of ECMP next hops) has to satisfy a few requirements:

-   It has to work reasonably well in typical environments;
-   It should not reorder packets of the same flow ([here's why](/2014/03/per-packet-load-balancing-interferes.html));
-   It has to be simple enough to be implementable in reasonably cheap ASICs;

The second and third requirement result in what the chipset manufacturers (and subsequently the hardware vendors) are offering today: hash-based distribution of packets. In case you need a step-by-step overview of this process, here's how it works:

-   **Create an array of buckets** and assign each outgoing link to one or more buckets. The bucket size is the number you see in marketing papers as "*we support N-way ECMP*" or "*we have N-way LAG*".
-   **Take N fields from the outgoing packet header**. The fields could be MAC addresses (source and/or destination), IP addresses (source and/or destination), IP port numbers, or even some other fixed-position fields in the packet header. Some vendors -- for example Arista -- allow you to configure which fields you want to use (assuming the platform chipset supports this functionality).
-   **Hash the fields from the packet header** to get an integer between 0 and *bucket size -- 1*. Example: for bucket sizes that are power of two take the low-order N bits of the hash.
-   **Enqueue the packet into the output queue** of the interface that is associated with the bucket selected by the packet hash.

Have you noticed that the algorithm never checks the size of the output queue? If the hashing algorithm decides to send the packet through Interface\#1, the switch will send the packet through Interface\#1 even though that interface might be dropping packets like crazy due to continuous congestion, and all the other interfaces sit idle.

The reason the load-balancing algorithm never checks the load on the outbound interface is simple: the **typical environment** mentioned above is usually assumed to be a healthy mix of [numerous independent mice flows](/2014/06/mice-elephants-and-virtual-switches.html). Throw a few elephants in the mix and the [assumptions start breaking down](http://packetpushers.net/the-scaling-limitations-of-etherchannel-or-why-11-does-not-equal-2/).

The only vendor that was [always able to cope with the elephants in the mix](/2011/04/brocade-vcs-fabric-has-almost-perfect.html) is Brocade due to the fact that their traditional typical environment (storage networks) consists mainly of elephants.

### Can We Solve the Problem?

Here's an intriguingly simple question: *Why can't we change the mix of outgoing interfaces in the N-way ECMP table to reflect the actual interface load? Wouldn't that allow us to push the mice flows away from elephants crowding some of the interfaces?*

In principle, the answer is "*Sure, we could do that*", but we have to solve three challenges:

-   **Coarse-grained reshuffling** could make matters worse. If your hardware supports 8-way ECMP and you have four uplinks, you might shift a large proportion of the traffic when you reassign the buckets to less-loaded interfaces, resulting in a nasty oscillation. Modern chipsets support at least 256-way ECMP, so that shouldn't be a problem.
-   The hardware you use has to support **per-bucket counters.** All hardware supports per-interface counters, but while they help you identify the congested interfaces, the won't help you reshuffle the traffic -- if the control-plane software cannot see how much traffic goes through each bucket, it makes no sense to randomly reshuffle the buckets hoping for the best.
-   **We shall not reorder the packets** (at least within the data center), which means that we cannot reshuffle *active* buckets, but it's relatively safe to change the outgoing interface of a currently inactive bucket. You could still reorder packets within a TCP session under an unlikely set of circumstances (figuring out what those circumstances are is left as an exercise for the reader), but we just might have to accept that slight risk of temporary performance degradation if we want to get better link utilization.

Would the *reshuffle inactive buckets* idea work in practice? Are there inactive buckets in a typical high-volume data center environment? Welcome to the weird world of *flowlets*.

### What Are Flowlets?

It seems the idea of flowlets first appeared in the [Harnessing TCP's Burstiness with Flowlet Switching](http://groups.csail.mit.edu/netmit/wordpress/wp-content/themes/netmit/papers/texcp-hotnets04.pdf) paper (see also [corresponding PPT](http://nms.lcs.mit.edu/~kandula/data/FLARE_HotNets04_web.ppt)) -- due to the bursty nature of TCP, you might be able to do pretty reliable bucket reshuffling with 256 or more buckets, as some buckets always tend to be empty.

Microsoft started using flowlets in [Windows Server 2012 R2](http://insidevirtualization.com/windows-server-2012-r2/windows-server-2012-r2-nic-teaming-options/), and recently Cisco implemented [flowlet-based dynamic load balancing](http://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/1-x/aci-fundamentals/b_ACI-Fundamentals/b_ACI_Fundamentals_BigBook_chapter_0100.html#concept_F280C079790A451ABA76BC5C6427D746) in the ACI leaf-and-spine fabrics. Juniper is doing something similar ([adaptive load balancing](http://www.juniper.net/techpubs/en_US/junos14.1/topics/concept/load-balance-technique-overview.html)) on MX routers in Junos 14.1, and did Adaptive Flowlet Splicing within a Virtual Chassis Fabric ([a nice rehash of the topic](https://cloudnets.wordpress.com/2014/09/08/mice-and-elephants-in-my-data-center/)).

### Need more information?

-   [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) webinar describes data center solutions from leading networking vendors;
-   [ipSpace.net webinar subscription](https://www.ipspace.net/Subscription) also gives you access to further [data center topics](https://www.ipspace.net/Roadmap/Data_center_webinars), including [leaf-and-spine fabric architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) and [design scenarios](http://www.ipspace.net/Data_Center_Design_Case_Studies);
