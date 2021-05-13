---
title: "Local TCP Anycast Is Really Hard"
date: 2021-06-03 06:55:00
tags: [ load balancing, data center ]
---
[Pete Lumbis](https://blog.ipspace.net/2021/02/does-ucmp-make-sense.html#421) and [Network Ninja](https://blog.ipspace.net/2021/04/ucmp-leaf-spine-fabrics.html#540) mentioned an interesting Unequal-Cost Multipathing (UCMP) data center use case in their comments to my [UCMP-related blog posts](https://blog.ipspace.net/series/ucmp.html): anycast servers.

Here's a typical scenario they mentioned: a bunch of servers, randomly connected to multiple leaf switches, is offering a service on the *same IP address* (that's where *anycast* comes from).

{{<figure src="/2021/06/Anycast-TCP.png" caption="Typical Data Center Anycast Deployment">}}
<!--more-->
Before going into the details, let's ask a simple question: *Does that work outside of PowerPoint?* Absolutely. It's a perfect design for a scale-out UDP service like DNS, and large DNS server farms are usually built that way.

The really interesting question: *Does it work for TCP services?* Now we're coming to the *really hard* part -- as the spine and leaf switches do ECMP or UCMP toward the anycast IP address, someone must keep track of session-to-server assignments, or all hell would break loose.

{{<note>}}Please note that what we're discussing here is totally different from the WAN (Internet) anycast, which works really well and is widely used. It's almost impossible to get into the situation where you'd have equal-cost paths to two different sites anywhere in the Internet.{{</note>}}

It's easy to figure out that the design works in a steady-state situation. Data center switches do 5-tuple load balancing; every session is thus consistently forwarded to one of the servers. Problem solved... until you get a link or node failure. 

Most production-grade hardware ECMP implementations use *hash buckets* ([more details](https://blog.ipspace.net/2020/11/fast-failover-implementation.html)), and if the number of next hops changes due to a topology change, the hash buckets are reassigned, sending most of the traffic to a server that has no idea what to do with it. Modern ECMP implementations avoid that with *consistent hashing*. Consistent hashing tries to avoids recomputing the hash buckets after a topology change[^1]:

* Hash buckets for valid next hops are not touched.
* Invalid hash buckets (due to invalid next hop) are reassigned to valid next hops.

[^1]: Please note that this is a control-plane functionality where you can take all the time in the world to get it done, even more so if you're able to [precompute the backup next hops](https://blog.ipspace.net/2020/12/fast-failover-techniques.html).

Obviously we'll get some misdirected traffic, but those sessions are hopelessly lost anyway -- they were connected to a server that is no longer reachable.

The really fun part starts when you try to *add a server*. To do that, the last-hop switch has to take a few buckets from every valid next hop, and assign them to the new server. That's really hard to do (and even harder if you want to solve it in hardware at terabit speeds) without disrupting something. Even waiting for a bucket to get idle (the *[flowlet load balancing](https://blog.ipspace.net/2015/01/improving-ecmp-load-balancing-with.html)* approach) doesn't help -- an idle bucket does not mean there's no active TCP session using it.

Oh, and finally there's ICMP: ICMP replies include the original TCP/UDP port numbers, but no hardware switch is able to dig that far into the packet, so the ICMP reply is usually sent to some random server that has no idea what to do with it. Welcome to [PMTUD](https://www.ipspace.net/kb/Internet/PMTUD/20-mtu-discovery.html) hell.

Does that mean that it's impossible to do local TCP anycast load balancing? Of course not -- every hyperscaler uses that trick to implement scale-out network load balancing. Microsoft engineers [wrote about their solution in 2013](https://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p207.pdf), Fastly [documented their solution](https://www.fastly.com/blog/building-and-scaling-fastly-network-part-2-balancing-requests) in 2016[^2], I know Google published something a while ago (links welcome), and we learned not to expect anything tangible from AWS anyway[^3]. 

[^2]: Take your time and read the whole article. They went into intricate details I briefly touched upon in this blog post.

[^3]: We know they call their magic _Hyperplane_, but that's about it.

You could do something similar at a much smaller scale with a cluster of firewalls or load balancers (assuming your vendor manages to count beyond two active nodes), but the performance of network services clusters is usually far from linear -- the more boxes you add to the cluster, the less performance you gain with each additional box -- due to cluster-wide state maintenance.

Is there an easy-to-deploy software solution out there that would allow you to build large-scale anycast TCP services? I'd love to hear about it -- please write a comment.

### More to Explore

* [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers) webinar has a long [load balancing section](https://my.ipspace.net/bin/list?id=DC30#LOAD_BALANCING).
* I described Microsoft's approach to scale-out load balancing and its implications in [SDN Use Cases](https://www.ipspace.net/SDN_Use_Cases) and in [load balancing](https://my.ipspace.net/bin/list?id=AzureNet#LB) part of [Microsoft Azure Networking](https://www.ipspace.net/Microsoft_Azure_Networking) webinar.
* The user-facing part of AWS load balancing is described in [Amazon Web Services Networking](https://www.ipspace.net/Amazon_Web_Services_Networking) webinar.



