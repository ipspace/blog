---
date: 2014-10-09 07:31:00+02:00
tags:
- bridging
- data center
- overlay networks
- WAN
- LISP
title: 'VXLAN and OTV: The Saga Continues'
url: /2014/10/vxlan-and-otv-saga-continues.html
---
Randall Greer [left a comment](https://blog.ipspace.net/2014/08/revisited-layer-2-dci-over-vxlan.html?showComment=1408458333877#c3225945583309424804) on my [*Revisited: Layer-2 DCI over VXLAN*](http://blog.ipspace.net/2014/08/revisited-layer-2-dci-over-vxlan.html) post saying:

> Could you please elaborate on how VXLAN is a better option than OTV? As far as I can see, OTV doesn\'t suffer from the traffic tromboning you get from VXLAN. Sure you have to stretch your VLANs, but you\'re protected from bridging failures going over your DCI. OTV is also able to have multiple edge devices per site, so there\'s no single failure domain. It\'s even integrated with LISP to mitigate any sub-optimal traffic flows.

Before going through the individual points, let's focus on the big picture: the failure domains.
<!--more-->
### The Big Picture

**Fact**: [layer-2 network (VLAN) is a single failure domain](https://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html). You might not believe it... until you experience your first [STP-induced loop](http://blog.ipspace.net/2014/07/is-stp-really-evil.html) or a [broadcast storm](http://blog.ipspace.net/2012/05/transparent-bridging-aka-l2-switching.html) (but then, there are people who believe in [bandwidth fairy](http://blog.ipspace.net/2012/02/bandwidth-on-demand-is-openflow-silver.html) and [flat earth](http://blog.ipspace.net/2011/09/large-scale-bridging-nuked-earth.html)).

Now let's compare the bridging domains in three scenarios:

-   VXLAN VTEP on the hypervisor
-   VXLAN VTEP on the first ToR switch
-   VXLAN VTEP or OTV at the WAN edge router.

{{<figure src="/2014/10/s1600-VXLAN+versus+OTV.jpg">}}

When you place the tunnel encapsulation endpoint on the WAN edge router, you turn at least one data center into a single failure domain. With the VXLAN on the hypervisor, the failure domain is limited to all hypervisors participating in the same VLAN, and if the hypervisor uses packet replication to emulate BUM flooding, a VM-triggered broadcast storm cannot do too much damage. The proof is left as an exercise for the reader.

{{<note>}}I will not go into the horror stories of multi-DC meltdowns, [you might not believe them](https://blog.ipspace.net/2012/08/layer-2-dci-and-infinite-wisdom-of.html); I know [people who have experienced them](http://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html)... and then started listening to my advice.{{</note>}}

### The Details

Now let's go through Randall's points:

**OTV doesn't suffer from** [**traffic tromboning**](https://blog.ipspace.net/2011/02/traffic-trombone-what-it-is-and-how-you.html). You might solve northbound (DC-to-WAN) traffic flow in OTV scenario with first-hop gateway localization (which is a kludge that shouldn't have existed). You won't even start solving southbound traffic flow problems until you introduce LISP, and the solution will be suboptimal until you deploy LISP at remote sites.

You cannot solve east-west tromboning (traffic between VMs in different data centers), and all your glorious ideas kick the dust the moment someone inserts a stateful appliance (firewall or load balancer) in the forwarding path... unless you plan to deploy [stretched firewall cluster](https://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html), in which case I'll wish you luck and walk away in disgust.

**TL&DR:** [Stop being a MacGyver](https://blog.ipspace.net/2013/08/temper-your-macgyver-streak.html) and get a life. You might also want to [watch this video](http://blog.ipspace.net/2013/01/redundant-data-center-internet.html).

**You're protected from bridging failures going over your DCI**. This assumes that I'm OK with bridging failures bringing down one of my data centers. I don't have a dozen data centers, so I don't want to risk even one of them.

Also, if a VM goes broadcast-crazy and pumps 10Gbps of BUM traffic into your data center core, the OTV solution will either (A) saturate the WAN link or (B) saturate the server links in the other data center.

Before telling me that I don't know what *storm control* is, please do read how it actually works. A single BUM-crazy VM will kill almost all BUM traffic on your OTV link, effectively breaking ARP (and a few other things) across stretched VLANs.

**OTV is also able to have multiple edge devices per site, so there\'s no single failure domain**. *Single point of failure* is not the same thing as *single failure domain*.

**OTV is even integrated with LISP**... and you get optimal southbound traffic flow only when you deploy LISP on all remote sites, which is still a stretch BHAG for the global Internet.
