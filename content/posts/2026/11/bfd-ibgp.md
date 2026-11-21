---
title: "BFD on IBGP Sessions? Why Exactly?"
date: 2026-11-25 07:14:00+0200
tags: [ BGP ]
---
A friend of mine sent me an email with a weird observation:

> In the last year, I've seen a number of networks configure BFD on their iBGP sessions with very aggressive timers, including a network with 300 msec BFD timers (900 msec holddown).

There might be (marginally sane) reasons to run BFD on iBGP sessions instead of relying on other failure detection mechanisms, but using such short timers seems like a Really Bad Idea&trade;
<!--more-->
Let's start with what anyone touching BGP should always keep in mind: IBGP is an endpoint reachability propagation mechanism[^DKVS], not a routing protocol for figuring out the best immediate next hop toward a destination. It SHOULD[^CVI] always be used together with an IGP that calculates the best path to internal (intra-AS) IP prefixes, which IBGP can then use for next hops.

[^DKVS]: You can also call it *distributed key-value store* if you want to sound really cool.

[^CVI]: Don't get me started on crazy vendor ideas, sometimes even documented in their _validated designs_. I [ranted about them in the past](/series/dcbgp/#rant); if you haven't read those blog posts, grab a bag of popcorn and start exploring ;)

However, an IBGP peer advertising the best BGP route could go down due to a router reload or any other node failure. BGP convergence relying solely on BGP timers could take a while, and BFD might seem like a great answer.

Ever since Henk Smit implemented the first version of fast *BGP next-hop tracking*, we have had a better solution (that was quickly "picked up" by many other vendors[^SV]). When a BGP next -hop disappears from the routing table[^NHTD], all BGP routes using it are revoked from the BGP table, allowing the BGP routing process to select alternate routes (either those already in the BGP table or advertised by its neighbors during the BGP convergence process). 

[^SV]: I'm really sorry if your box doesn't implement that functionality; someone was obviously sloppy when buying your network equipment. Maybe it's time to switch vendors?

[^NHTD]: Some implementations include a configurable delay to prevent route flushing during IGP convergence.

A failed IBGP neighbor should thus be detected via a change in the IP routing table caused by IGP convergence. Using BFD as a workaround is like applying a thick layer of lipstick to an ugly pig (= a ~~broken~~ suboptimal design or a bad BGP implementation). Also, don't even try to argue that you have to use BFD to detect forwarding-path failures between IBGP peers; that just proves your network is broken beyond hope[^KC].

[^KC]: Or maybe you're running BGP over controller-installed static routes and NAT in a Kubernetes cluster 🤔 Anyway, I don't want to hear about it.

Speaking of suboptimal designs, there is one where BFD between IBGP endpoints might be useful: summarization of address ranges (including loopback prefixes)[^SRv6]. If you have BGP next-hops within a summary prefix, the next-hop tracking becomes a waste of CPU cycles.

[^SRv6]: The concept recently peddled by some SRv6 evangelists, proving the eternal wisdom of RFC 1925 Rule 11.

One might wonder why someone would introduce summarization of loopbacks when we have an order of magnitude larger forwarding tables than we had in the past, and the modern CPUs are at least 1000x faster than what we had when we were first building large OSPF or IS-IS networks, but there's no accounting for taste[^PPD]. But no worries, even if you believed you had to introduce loopback summarization for whatever reason, vendors already have a solution[^SHW]: IGP Unreachable Prefix Announcement, described in [RFC 9929](https://www.rfc-editor.org/info/rfc9929/)[^NM].

[^PPD]: Or exciting PowerPoint designs picked up by people with too little real-life experience

[^SHW]: And if you feel like a wall being hit by spaghetti in the *let's see what sticks* game, you're not wrong. Randy Bush [nailed it](https://dl.acm.org/doi/pdf/10.1145/1096536.1096544) ages ago, and nothing has changed since.

[^NM]: I was introduced to this masterpiece of a Rube Goldberg-style workaround by [Nicola Modena](https://www.linkedin.com/in/nmodena/), and when the RFC mentioned BGP PIC, everything just clicked.

However, if you're so far from a sane network design or implementation that BFD between IBGP peers is your only hope, PRETTY PLEASE don't use aggressive timers. The BFD timers SHOULD be longer than your worst-case IGP convergence, or you might lose IBGP sessions (and IBGP routes) during a normal IGP convergence event, potentially resulting in a pretty spectacular network meltdown[^RGE].

[^RGE]: In some cases, also known as a Resume Generating Event

Finally, multihop BFD (needed for IBGP sessions) might be implemented in the control-plane CPU, making it even more vulnerable to CPU overloads. See also [How Fast Can We Detect a Network Failure?](/2020/11/detecting-network-failure/), [To BFD or Not to BFD?](/2017/10/to-bfd-or-not-to-bfd/), and [Know Thy Environment Before Redesigning It](/2019/06/know-thy-environment-before-redesigning/).
