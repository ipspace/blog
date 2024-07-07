---
date: 2020-11-24 08:23:00+00:00
series:
- fast-failover
tags:
- IP routing
title: 'Fast Failover: Hardware and Software Implementations'
---
In previous blog posts in this series we discussed whether it [makes sense to invest into fast failover network designs](/2020/11/fast-failover-challenge/), the [topologies you can use in such designs](/2020/11/fast-failover-topologies/), and the [fault detection techniques](/2020/11/detecting-network-failure/). I also hinted at different fast failover implementations; this blog post focuses on some of them.

**Hardware-based failover** changes the hardware forwarding tables after a hardware-detectable link failure, most likely loss-of-light or transceiver-reported link fault. Forwarding hardware cannot do extensive calculations; the alternate paths are thus usually pre-programmed (more details below).
<!--more-->
{{<note warn>}}Investing in complex hardware-based failover makes sense only when the hardware autonomously detects link failures. Relying on BFD running on the control-plane CPU to detect failures, and then extolling the beauties of hardware failover makes little sense.{{</note>}}

**Software-based failover** can act on link or node failures, including byzantine failures on a path between two forwarding engines as detected by BFD or similar protocols. It can involve selecting alternate routes provided by another routing protocol -- including floating static routes -- and extensive reprogramming of forwarding tables. 

However, keep in mind that on modern CPUs the reprogramming of forwarding tables might take longer than the time a routing protocol needs to do its job, so it might not make sense to make software-based failover too complex... unless of course your hardware supports _Prefix Independent Convergence_ (the ability to update next hops for a set of prefixes).

Hardware details are extremely hard to come by. Most high-speed switching silicon is either designed in-house by networking vendors or covered by [impenetrable NDAs](/2016/05/what-are-problems-with-broadcom/) (an [astonishing state of affairs](https://packetpushers.net/industry-needs-open-source-framework-switching-silicon/) considering how everyone loves to praise the virtues of _open-everything_).

Sometimes a vendor using third-party merchant silicon decides to spill some of the beans like Cisco did [describing ASR 9000 behavior](https://community.cisco.com/t5/service-providers-documents/asr9000-xr-load-balancing-architecture-and-characteristics/ta-p/3124809). While those documents are fun to read, to understand the fundamentals we often don't need more than a high-level overview like what [Lukas Krattiger](https://www.ipspace.net/Author:Lukas_Krattiger) sent me. As always, all the good stuff is his, and all the errors are mine.

---

_Equal Cost Multi-Path_ (ECMP) is a function available in routing protocols that is supported natively in most routing platforms. It results in having multiple next-hops for a prefix (IP prefix or MAC address). 

Routing protocol ECMP is driving the _Routing Information Base_ (RIB, routing table), generally based in control-plane/CPU. Forwarding Information Base (FIB), the data-plane/ASIC-based part, is a different part of the story. If you support ECMP in the control plane doesn't necessarily mean that you have ECMP programmed in the data plane.

{{<note info>}}Explore *[Control and Data Plane](/2013/08/management-control-and-data-planes-in/)* and *[RIB and FIB](/2010/09/ribs-and-fibs/)* blog posts for more details, or watch *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.{{</note>}}

We need to understand that _Equal Cost Multipath_ (ECMP), _Unequal Cost Multipath_ (UCMP), _Loop Free Alternate_ (LFA) or _Fast Reroute_ (FRR) are ways to influence the RIB and, if supported, tell the FIB what to program for forwarding. In order to make this happen, FIB needs functionality to support this, most commonly ECMP groups, _Recursive Next Hops_ (RNH) used by protocols like BGP, and directly-connected next hops (CNH) aka adjacencies.

{{<figure src="/2020/11/FIB_ECMP_Groups.png" caption="Typical FIB implementation supporting prefix-independent convergence with next-hop groups and ECMP buckets">}}

Our expectation is that ECMP fast failover is always fast and consistent, but in fact, it's usually _Prefix Independent Convergence_ (PIC) which delivers this. To make matters even more complex, we have _PIC Core_ (recursive next-hop resolution in a ECMP network) and _PIC Edge_ (backup routes)

So three points become important when evaluating a solution:

* Routing protocol functionality;
* Programming RIB and FIB
* Forwarding hierarchies available and used in the FIB itself (ECMP, PIC, RNH, CNH).

If you rely only on routing protocols and techniques like FRR, LFA. routing protocol ECMP, you will not achieve faster convergence as the hardware must be re-programmed after every change has been evaluated. If you move groupings, hierarchies, and resolution checks into the hardware, you can achieve this much, much faster.

In simple terms, if you are using ECMP in the FIB, and a link to a next hop fails, there is no change to the prefix. A member of the ECMP group (directly connected or recursive) will be removed as it is not reachable anymore. Once a routing protocols learns about the topology change, most likely much later than the FIB can react, then it will start recalculating your routing topology and this can take time.

If you use indirection in the FIB and in the network, you can use things like MPLS labels, as used in Topology-Independent LFA (TI-LFA) or FRR. While this is a great approach, you might end up in using a lot more ECMP groups as your hardware might lack an additional level of indirection (labels in next hop groups).

Most scalable approach is still classic ECMP with PIC Core. If you can’t do that because of a complicated set of WAN links, choose wisely what method to use. In that particular case Segment Routing (SR) could be an option, as it has less complexity than the traditional MPLS-based solutions.

---

Let me add my own set of warnings to the end of this story:

* Different ASICs from the same manufacturer have different FIB structure and thus different fast failover capabilities;
* We don't know what most ASICs can do, and can only hope to glean some details from vendor presentations;
* Even when an ASIC contains specific hardware functionality, that feature might not be supported in software running on the device;
* Until things settle down, expect every software release to behave a bit differently;
* If the fast failover behavior really matters, get all vendor promises in writing, make them part of purchase agreement, and do thorough lab testing way beyond pulling cables and measuring **ping** packet loss.
