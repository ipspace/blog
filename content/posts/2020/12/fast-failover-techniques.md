---
date: 2020-12-03 06:59:00+00:00
series:
- fast-failover
tags:
- IP routing
title: 'Fast Failover: Techniques and Technologies'
---
Continuing our [Fast Failover saga](/series/fast-failover.html), let's focus on techniques and technologies available to implement it (assuming you [still think it's worth the effort](/2020/11/fast-failover-challenge.html)).

{{<note info>}}The following text is heavily based on comments [Jeff Tantsura](https://www.linkedin.com/in/jeff-tantsura/) wrote on one of my LinkedIn posts as well as the original blog post. Thank you!{{</note>}}

There are numerous technologies you can use to implement fast reroute, from the most complex to the easiest one:
<!--more-->

* Original MPLS Fast Reroute (FRR) which requires a full-blown MPLS network running RSVP-TE
* IP Fast Reroute (IP FRR) which relies on Loop Free Alternates (LFA)
* Fast rehash of ECMP paths. This is a non-standardized local implementation technique based on common implementations in forwarding silicon.

These technologies can provide various levels of failure detection and protection:

**MPLS FRR** based on RSVP-TE signaling (which builds an end-to-end virtual circuit) can provide link, node, and path protection.

{{<note info>}}Traffic engineering based MPLS FRR is the only fast failover mechanism that works with *virtual circuits* and can therefore provide *path protection*. LFA, rLFA and TI-LFA just redirect the traffic to a far-enough node. For more details on differences between circuit-based and hop-by-hop switching watch the *[Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH)* part of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.{{</note>}}

**IP FRR** requires link-state routing protocol and LFA computation and can provide various levels of protection:

* LFA and Remote LFA (rLFA) provide link and node protection and are topology dependent;
* Topology-Independent LFA (TI-LFA) provides link and node protection and is topology independent as it uses Segment Routing (SR) tunnel to push traffic to a far-enough (PQ) node.

{{<note info>}}More details about LFA/rLFA/TI-LFA coming in another blog post{{</note>}}

**Fast-rehash** requires alternate active paths toward the destination prefix and provides link protection in (E|U)CMP topologies.

### Comparing IP FRR and Fast Rehash

Both IP FRR and Fast Rehash rely on IP forwarding, so they can be implemented in hardware with no MPLS support.

IP FRR is a control plane function (xLFA) that relies on a pre-computed backup next-hop (it is more complex in rLFA/TI-LFA) that is loop-free (could be ECMP). The backup next-hop computation could take into consideration some additional data like Shared Risk Link Groups (SRLG) or interface load. Eventually, the end-result of the computation is downloaded as backup paths into the forwarding hardware. 

{{<note>}}Fast failover based on LFA computation is usually implemented in hardware. It doesn't make much sense to invest into complexities of LFA when it takes approximately as long to recalculate paths with SPF algorithm as it takes to install changes in the forwarding table.{{</note>}}

Usually you’d see LFA implemented on a high end router. It is much more intelligent that fast rehash and provides non connected bypass to reach PQ node (rLFA/TI-LFA).

Fast Rehash is a forwarding construct, where the next-hop (could be called differently) is not a single entry but an array of entries (ECMP bundle) downloaded in the forwarding hardware by the control plane. If one of them becomes unavailable (BFD DOWN, carrier loss, or interface down events) it is simply removed from the array and the hashing is updated accordingly, hence the name.

Fast-rehash protects only connected links and doesn’t require any additional computation (ECMP alternatives are per definition loop-free). It is usually implemented in data center fabrics.

Regardless of the technology used, the failover from lost active path(s) to a backup path could be [implemented in hardware or software](/2020/11/fast-failover-implementation.html). Hardware failover usually takes less than a millisecond, while software failover (example: rehashing of ECMP next hops in software, and downloading new ECMP buckets into hardware) takes ~50-100 milliseconds.
