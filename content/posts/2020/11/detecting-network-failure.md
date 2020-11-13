---
title: "How Fast Can We Detect a Network Failure?"
date: 2020-11-17 07:46:00
tags: [ IP routing, networking fundamentals ]
series: fast-failover
---
In the [introductory fast failover blog post](https://blog.ipspace.net/2020/11/fast-failover-challenge.html) I mentioned the challenge of fast link- and node failure detection, and how it makes little sense to waste your efforts on fast failover tricks if the routing protocol convergence time has the same order of magnitude as failure detection time.

Now let's focus on realistic failure detection mechanisms and detection times. Imagine a system connecting a hardware switching platform (example: data center switch or a high-end router) with a software switching platform (midrange router):
<!--more-->
{{<figure src="FRR_Failure_Detection.jpg" caption="Sample 2-node network with a hardware- and software switching platform">}}

Hardware switching platform has a CPU (control plane), switching hardware (data plane), and a number of transceivers (PHY modules). Software switching platform has a CPU (that runs control- and data planes), interface cards, and transceivers.

The fastest link failure detection mechanism is the _physical link failure detection_ sometimes called (for historical reasons) _loss of carrier_ (or light in optical networks). That mechanism kicks in as soon as you get a clean cable cut, but cannot detect unidirectional problems, or somewhat-faulty cables introducing spurious transmission errors.

Some physical layers -- including Gigabit Ethernet -- provide end-to-end fault detection (_link fault signaling_ in the above diagram). While that might seem like a perfect solution, do keep in mind that LFS works between transceivers, and thus cannot detect faulty transceivers or faults deeper inside the network node.

Many data link layer (layer-2) technologies provide link fault detection mechanisms - LACP timers, [UDLD](https://blog.ipspace.net/2012/09/do-we-need-lacp-and-udld.html), Ethernet Connectivity and Fault Management (CFM)... These protocols are often run by the control plane, and are thus correspondingly slow. Example: LACP packets are sent once per second when using _fast LACP timers_, and it takes three seconds to detect LAG failure.

{{<note>}}Some people argue that you don't need UDLD (on layer-2) or BFD (on layer-3) in a Gigabit Ethernet network due to built-in Link Fault Signaling (LFS). Looking at the above diagram, it becomes painfully obvious that LFS tests PHY-to-PHY path, whereas UDLD and BFD provide more comprehensive tests... but if you think the only failure that could ever happen is a cable cut, go ahead.{{</note>}}

[Bidirectional Forwarding Detection](https://blog.ipspace.net/2014/10/micro-bfd-bfd-over-lag-port-channel.html) (BFD) seems like an [ideal solution](https://blog.ipspace.net/2017/10/to-bfd-or-not-to-bfd.html), at least while looking at vendor PowerPoint decks. The reality is a bit different, although it's still [much better to use BFD than to tweak BGP or OSPF timers](https://blog.ipspace.net/2017/09/improving-bgp-convergence-without.html).

High-end platforms running BFD in hardware can provide very short failure detection times, but also tend to be reassuringly expensive. Most other devices run BFD in software and can provide somewhat-stable failure detection in hundreds of milliseconds.

{{<note warn>}}You don't want to tweak BFD timers too much when running BFD on the control plane CPU. The CPU might get too busy, drop a few BFD packets, and the resulting routing protocol adjacency loss did bring down a few networks.{{</note>}}

So far we focused on detecting failures on point-to-point links. Multi-access networks and paths containing invisible third-party devices (media converters, Ethernet switches...) add a new layer of complexity that we'll discuss in *Advanced Routing Protocol Topics* part of [*How Networks Really Work*](https://www.ipspace.net/How_Networks_Really_Work) webinar.

Long story short:

* Total interface loss (cable cut) can be detected in milliseconds;
* Detecting any other failure requires data link- or network-layer protocols, and usually requires hundreds of milliseconds.

Keep these facts in mind when evaluating whether it makes sense to spend time designing a perfect fast failover solution.