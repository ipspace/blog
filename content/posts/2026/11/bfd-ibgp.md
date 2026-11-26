---
title: "BFD on IBGP Sessions? Why Exactly?"
date: 2026-11-25 07:14:00+0200
tags: [ BGP ]
---
A friend of mine sent me an email with a weird observation:

> In the last year, I've seen a number of networks configure BFD on their iBGP sessions with very aggressive timers, including a network with 300 msec BFD timers (900 msec holddown).

There might be reasons to run BFD on iBGP sessions instead of relying on other failure detection mechanisms, but using such short timers seems like a Really Bad Idea&trade; unless your AS has only two directly-connected routers (a few details in the final section of the blog post).

You might also want to keep reading until you hit the **Recap** and **What Others are Saying** sections at the end of the blog post.
<!--more-->
### Why Would You Consider BFD with IBGP?

Let's start with what anyone touching BGP should always keep in mind: with a few exceptions, IBGP is an endpoint reachability propagation mechanism[^DKVS], not a routing protocol for figuring out the best immediate next hop toward a destination. It SHOULD[^CVI] always be used together with an IGP that calculates the best path to internal (intra-AS) IP prefixes, which IBGP can then use for next hops.

[^DKVS]: You can also call it *distributed key-value store* if you want to sound really cool.

[^CVI]: Don't get me started on crazy vendor ideas, sometimes even documented in their _validated designs_. I [ranted about them in the past](/series/dcbgp/#rant); if you haven't read those blog posts, grab a bag of popcorn and start exploring ;)

However, an IBGP peer advertising the best BGP route could go down due to a router reload or any other node failure. BGP convergence relying solely on BGP timers could take a while, and BFD might seem like a great answer.

### Do You Really Need It?

Ever since Henk Smit implemented the first version of fast *BGP next-hop tracking*, we have had a better solution (that was quickly "picked up" by many other vendors[^SV]). When a BGP next -hop disappears from the routing table[^NHTD], all BGP routes using it are revoked from the BGP table, allowing the BGP routing process to select alternate routes (either those already in the BGP table or advertised by its neighbors during the BGP convergence process). 

[^SV]: I'm really sorry if your box doesn't implement that functionality; someone was obviously sloppy when buying your network equipment. Maybe it's time to switch vendors?

[^NHTD]: Some implementations include a configurable delay to prevent route flushing during IGP convergence.

A failed IBGP neighbor should thus be detected via a change in the IP routing table caused by IGP convergence. Using BFD as a workaround is like applying a thick layer of lipstick to an ugly pig (= a ~~broken~~ suboptimal design or a bad BGP implementation). Also, don't even try to argue that you have to use BFD to detect forwarding-path failures between IBGP peers; that just proves your network is broken beyond hope[^KC].

[^KC]: Or maybe you're running BGP over controller-installed static routes and NAT in a Kubernetes cluster 🤔 Anyway, I don't want to hear about it.

### There Are Always Exceptions

Speaking of suboptimal designs, there is one where BFD between IBGP endpoints might be useful: summarization of address ranges (including loopback prefixes)[^SRv6]. If you have BGP next-hops within a summary prefix, the next-hop tracking becomes a waste of CPU cycles.

[^SRv6]: The concept recently peddled by some SRv6 evangelists, proving the eternal wisdom of RFC 1925 Rule 11.

One might wonder why someone would introduce summarization of loopbacks when we have an order of magnitude larger forwarding tables than we had in the past, and the modern CPUs are at least 1000x faster than what we had when we were first building large OSPF or IS-IS networks, but there's no accounting for taste[^PPD]. But no worries, even if you believed you had to introduce loopback summarization for whatever reason, vendors already have a solution[^SHW]: IGP Unreachable Prefix Announcement, described in [RFC 9929](https://www.rfc-editor.org/info/rfc9929/)[^NM].

[^PPD]: Or exciting PowerPoint designs picked up by people with too little real-life experience

[^SHW]: And if you feel like a wall being hit by spaghetti in the *let's see what sticks* game, you're not wrong. Randy Bush [nailed it](https://dl.acm.org/doi/pdf/10.1145/1096536.1096544) ages ago, and nothing has changed since.

[^NM]: I was introduced to this masterpiece of a Rube Goldberg-style workaround by [Nicola Modena](https://www.linkedin.com/in/nmodena/), and when the RFC mentioned BGP PIC, everything just clicked.

However, if you're so far from a sane network design or implementation that BFD between distant IBGP peers is your only hope, PRETTY PLEASE don't use aggressive timers. The BFD timers SHOULD be longer than your worst-case IGP convergence, or you might lose IBGP sessions (and IBGP routes) during a normal IGP convergence event, potentially resulting in a pretty spectacular network meltdown[^RGE].

[^RGE]: In some cases, also known as a Resume Generating Event

### Recap

* BFD is the best mechanism to detect link or path failure between adjacent L3 nodes (see also the [Fast Failover](/series/fast-failover/) series), be it IGP neighbors or EBGP neighbors.
* Using BFD between nodes separated by multiple L3 devices ([traditionally](https://blog.ipspace.net/2009/12/lies-damned-lies-and-product-marketing/) called *routers*) is already questionable, unless you're checking the reachability of indirect next hops of static routes.
* When you're running IBGP between nodes separated by intermediate routers, let IGP do its job, and use BFD to help IGP do a better job.
* Whatever you do, use very conservative timers when using BFD between IGBP endpoints that are not directly connected. You don't want to lose a BGP session due to a convergence event.

And as always: before getting stuck on technology, figure out what problem you're trying to solve, and whether it's worth solving. In this particular case:

* What failure are you trying to detect?
* Which protocol should be responsible for failure detection and recovery?
* How long will the recovery take, and what mechanism could make it faster without introducing too much complexity or making the network unstable?

The last one is particularly tricky, as the answers rely on [hard-to-get](https://blog.ipspace.net/2016/05/what-are-problems-with-broadcom/) implementation details. For example, how fast BGP detects next-hop failure, and whether it can trigger PIC to avoid a FIB rewrite. Or will the BGP churn on my router impact the IGP convergence speed?

Finally:

* This is a generic discussion. YMMV. You might have very specific requirements, in which case you SHOULD NEVER rely solely on information gathered from blog posts.
* Multihop BFD (needed for IBGP sessions) might be implemented in the control-plane CPU, making it even more vulnerable to CPU overloads. See also [How Fast Can We Detect a Network Failure?](/2020/11/detecting-network-failure/), [To BFD or Not to BFD?](/2017/10/to-bfd-or-not-to-bfd/), and [Know Thy Environment Before Redesigning It](/2019/06/know-thy-environment-before-redesigning/).

### What Others Are Saying

The [LinkedIn post](https://www.linkedin.com/posts/ivanpepelnjak_does-it-make-sense-to-run-bfd-on-ibgp-sessions-share-7531247834520514560-tVXe/) generated tons of responses. You might want to read them all; here are a few useful pointers I collected from them:

* The [BGP RR Deployment Considerations](https://www.ietf.org/archive/id/draft-smith-idr-rr-deployment-considerations-02.html) draft effectively says "Don't do it" in [section 11.8](https://www.ietf.org/archive/id/draft-smith-idr-rr-deployment-considerations-02.html#name-multi-hop-bfd-for-ibgp). Who knows whether that sage advice will survive the IETF process (or maybe the draft will stay in limbo for years, like our [BGP Operations and Security](/2015/02/rfc-7454-bgp-operations-and-security/) draft did).
* OTOH, Cisco's [Agile Services Networking Metro Implementation](https://xrdocs.io/design/blogs/2026-01-01-agile-service-networking-metro-1_0-ig) uses BFD on Services Route Reflector (VPN routes) but not on Transport Route Reflector (global IPv4/IPv6 routes), with the minimum timer set to three milliseconds. I would love to see how that survives an IGP glitch that is not immediately recovered by TI-LFA.
* Juniper (oops, HPE) is also recommending BFD with a 300 msec detection timer in their [Metro Ethernet Business Services Juniper Validated Design](https://networkingdocs.hpe.com/documentation/us/en/software/jvd/jvd-metro-ebs-03-03/jvd-metro-ebs-03-03.pdf).

OTOH, [Tyler Leeds](https://www.linkedin.com/in/tylercleeds/) made an extremely valid point in a LinkedIn comment: running BFD in hardware between directly connected IP addresses would usually trigger Prefix Independent Convergence (PIC), rewriting next-hop groups in hardware and resulting in extremely fast failover, way faster than anything you could hope to achieve with IBGP/IGP/next-hop-tracking combo. You'd need a pretty specific design for that, though.

### The One Design That Needs BFD

I have to admit I was too focused on the generic "large network with multi-hop IBGP sessions" scenario. There's a niche case (OK, a pretty large *niche*):

* Layer-2 network (a small site or a layer-2-only DMZ) -- like IXP, but within your network.
* Only a few edge routers are involved in BGP. Unlike an IXP, they are all in the same AS, so you run IBGP between them.
* Sometimes you don't even need an IGP (think firewalls using the shared VRRP IP address on the routers as the next hop for a static default route)

In that case, it makes perfect sense to run IBGP as your sole routing protocol between the edge routers. You'd obviously do that between directly connected IP addresses (as there's no IGP to propagate loopbacks) and use BFD for fast failure detection. I even [wrote about that](/2011/08/road-to-complex-designs-is-paved-with/) in the past ;), but as I [mentioned a decade later](/2023/05/small-site-ebgp-only-design/), the IBGP-only design might get too unusual as the network grows beyond that one single layer-2 segment.

### Revision History

2026-11-26
: Slightly reworded the intro, split the growing wall of text into sections, and added the three sections at the end of the blog post based on readers' feedback. Thanks a million for your perspectives, all the extra information, and pointers!
