---
title: "On MPLS Forwarding Performance Myths"
date: 2026-02-05 08:20:00+0100
tags: [ MPLS ]
---
Whenever I [claim](/2026/01/mpls-paths-tunnels-interfaces/) that the initial use case for MPLS was improved forwarding performance (using the [RFC](https://datatracker.ietf.org/doc/html/rfc2105) that matches the [IETF MPLS BoF slides](https://www.ietf.org/proceedings/37/rtg/tagsw-slides/index.htm) as supporting evidence), someone inevitably comes up with a source claiming something along these lines:

> The idea of speeding up the lookup operation on an IP datagram turned out to have little practical impact.

That might be true[^SDN], although I do remember how hard it was for Cisco to build the first IP forwarding hardware in the AGS+ CBUS controller. Switching labels would be much faster (or at least cheaper), but the time it takes to do a forwarding table lookup was never the main consideration. It was all about the aggregate forwarding performance of core devices.

Anyhow, [Duty Calls](https://xkcd.com/386/). It's time for another archeology dig. Unfortunately, most of the primary sources irrecoverably went to `/dev/null`, and personal memories are never reliable; comments are most welcome.
<!--more-->
[^SDN]: Although that same source once claimed SDN was a success 🤷‍♂️. A grain of salt might be advised.

It was the mid-1990s, the Internet was taking off, and a few large US ISPs had a bit of a problem. They had too much traffic to use routers as core network devices; ATM switches were the only alternative.

To qualify that, you have to understand how "fast" routers were in those days:

* AGS+ had a 533 Mbps backplane (Cbus, [source](https://designated-router.com/ciscos-first-router-revisiting-the-venerable-ags-in-2021/))
* Cisco 7000 was just a better implementation of the same concepts, and it looks like the CxBus had the same speed as the original Cbus (based on [this source](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y1995/m08/cisco-7500-series-boosts-routing-muscle-for-large-evolving-corporate-networks.html)).
* Cisco 7500, launched in 1995, had CyBus providing 1.067 Gbps. The entry-level model (7505) had a single bus; higher-end models (7507/7513) had dual-CyBus backplanes, yielding 2.1 Gbps of forwarding performance [^CY].
* Line cards were laughable (by today's standards). The fastest linecard had two Fast Ethernet ports (200 Mbps or 400 Mbps of marketing bandwidth).

On the other hand, Cisco's LightStream 1010 ATM switch (also launched in 1995) had 5 Gbps of bandwidth ([source](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y1995/m11/cisco-lightstream-1010-next-generation-workgroup-campus-atm-switch-first-to-offer-standard-atm-routing-and-traffic-management.html)). Keep in mind that although LS1010 was an excellent product, it was a late-to-market me-too entry-level switch. Other ATM switches had even higher performance.

The service providers were thus forced to combine routers at the network edge (because they needed IP forwarding) with ATM switches at the network core (to get sufficient aggregate forwarding bandwidth). There were "just" two problems with that approach:

* The only (working) way to interconnect routers and ATM switches was to build point-to-point ATM virtual circuits (VC) between routers (using a network management system) and then run routing protocols on the full mesh of ATM VCs. In a word, a spaghetti-mess nightmare.

* The customers were spending money (that Cisco wanted to get) buying ATM switches from other vendors.

Now, imagine you had a technology that would:

1. Allow a seamless integration of all devices in the network
2. Have a unified control plane running IP routing protocols
3. Use labels in the core (reusing ATM VPI/VCI header) to retain the benefits of high-speed ATM forwarding while mapping IP packets into those labels at the slower network edge
4. Be available from a single vendor[^GSV]

[^GSV]: And, even better, only work on gear from that single vendor. Why do you think everyone else was so interested in standardizing something that was notably *different* from Cisco's initial implementation?

And that's (according to how this was explained to me when I asked, "Who would ever need this?") why we got Tag Switching. Read the early Tag Switching information (or even the [LDP RFC](https://datatracker.ietf.org/doc/html/rfc3036)), and you'll see how heavily biased toward ATM (cell-mode MPLS) it was[^ACH]. Most of the TDP/LDP complexity comes from dealing with hardware that:

* Could not do IP lookups
* Could not preallocate labels to every prefix in the network because the VPI/VCI forwarding table was limited
* Could not even merge two data streams into a single one. Streams from two ingress routers had to be kept separate until they reached the egress router[^VCM].

[^ACH]: My MPLS/VPN book had two chapters on MPLS-over-ATM describing cell-mode MPLS (the "real" ATM MPLS) and the frame-mode MPLS over ATM VCs (router-to-router MPLS over ATM). If you don't have the book on your dusty bookshelf, I'm sure you'll find a stolen PDF in a dark corner of the Internet.

[^VCM]: Unless your ATM switch supported the VC Merge feature, which requires heavy buffering in transit switches. Yeah, we're back to the *shallow*/*deep* buffer discussion. Some things never change.

Not surprisingly, someone quickly figured out that one could use the same concepts on Frame Relay[^FR] and point-to-point links (merging multiple layer-2 transport technologies into a single label space). When the labels were no longer limited to ATM headers, it wasn't too hard to think of the label *stack*[^YR], and then get really creative and use the label stack to implement services on top of the transport label-switched paths. 

MPLS/VPN was the first such service (and the first time most people heard of MPLS), and the rest is history. ATM is long gone, cell-mode MPLS died even before that, and we're still using frame-mode MPLS transport and MPLS/VPN technologies.

[^FR]: Of course there's an [RFC](https://datatracker.ietf.org/doc/html/rfc3034) for that crazy idea

[^YR]: ChatGPT claims the idea is usually credited to Yakov Rekhter. That sounds about right.

### Revision History

2026-02-06
: Fixed the CyBus section based on a comment by Emanuele and LinkedIn comments.
