---
title: "Do We Need LFA or FRR for Fast Failover in ECMP Designs?"
date: 2020-11-04 06:02:00
tags: [ ip routing, design ]
---
One of my readers sent me a question along these lines:

> Imagine you have a router with four equal-cost paths to prefix  X, two toward _upstream-1_ and two toward _upstream-2_. Now let's suppose that one of those links goes down and you want to have link protection. Do I really need Loop-Free Alternate (LFA) or MPLS Fast Reroute (FRR) to get fast (= immediate) failover or could I rely on multiple equal-cost paths to get the job done? I'm getting different answers from different vendors...

This is how I always understood things should work:
<!--more-->
* Equal-cost paths are installed in routing and forwarding tables. They might be implemented as independent forwarding entries, or as a single forwarding entry pointing to a next-hop group (I [discussed next-hop groups](https://my.ipspace.net/bin/list?id=OpenFlow#OpenFlow%20Forwarding%20Model) in [OpenFlow Deep Dive](https://www.ipspace.net/OpenFlow_Deep_Dive) webinar).
* Once a link to a next hop fails, the corresponding entry is removed from routing and forwarding table (or the next-hop group is adjusted).
* If you have LFA or Fast Reroute in place, the failed next hop could be replaced with another next hop without involving a routing protocol.
* Without LFA or Fast Reroute, you just have fewer equal-cost next hops and life goes on.

After a while, the routing protocol wakes up, does its job, and adjusts the routing and forwarding table.

Obviously that’s how things _should_ work. I’m positive there are tons of implementation details involved, some of them ASIC-related, and the only way to get reliable results is to set everything up in a lab, connect a Spirent-like tester to it, and pull a cable… and then you’ll know how things work on (A) the platform you tested (B) using a specific software release with (C) specific ASICs.

However, it looks like some vendors decided LFA or FRR is the only way to go... This is what someone told my reader:

> What the $vendor is telling me is that ECMP cannot provide fast-protection because the hash-buckets are reallocated by the control plane when a ECMP link fails

Wait... WTF??? The hardware can be programmed to replace an entry in a next-hop group with a standby LFA/FRR entry, but it cannot remove an entry from a next-hop group? And even if that's true, nobody thought about using a dummy replacement entry that would point to one of the other valid next hops until the control plane wakes up... which is what LFA would end up doing anyway?

Here's what seems to be going on in some of the platforms out there (according to my reader):

---

It looks that amongst some of the high-end router vendors (Juniper MX960, Cisco ASR9922, Nokia 7950 XRS), IOS-XR ECMP implementation does not provide fast-protection while Nokia and Junos do. Cisco in fact needs LFA to provide fast-protection for ECMP'ed prefixes while Junos and Nokia don't run LFA for ECMP'ed prefixes as they don't need to. 

LFA over ECMP'ed prefixes seems to provide (during protection and while the IGP converges), a lower grade of flows spraying when compared to pure ECMP  with the difference in flows number amongst destinations being an additional risk factor towards link saturation and/or QoS threshold crossing. 

Junos seems to require the forwarding policy knob ECMP-FRR (why is it in the BGP section?) for some of the platforms while Nokia has a fast implementation of ECMP by default on any platform with its uniform-failover. It's not always clear though what kind of fast-protections (if any) hold for all forms of ECMP hashing: 

* ECMP amongst (multipath) BGP next hops;
* ECMP amongst L3 single-links;
* L3 LAGs and/or amongst L2 links (e.g. LAG's individual links). 

It's not always clear what their relation to LFA is either since they could be alternatives or coexist. I have no info from Huawei as do not have any of their boxes but they look promising as they seem to provide the best of both worlds where the fast IP/LDP ECMP implementation coexists with LFA and with the latter kicking in only when ECMP is not considered available anymore. 

To me, this area of networking needs to be polished/clarified before even thinking of moving over to SR and TI-LFA designs.

---

Any other real-life experience would be highly appreciated. If you KNOW the answer for any specific platform (as opposed to _this is how it SHOULD be_), please write a comment... and if you have a juicy dirty secret to share, send me an email and I'll add it to this blog post as another anonymous contribution.