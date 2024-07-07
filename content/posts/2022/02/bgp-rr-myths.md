---
date: 2022-02-01 07:54:00+00:00
dcbgp_tag: relevant
series:
- dcbgp
tags:
- BGP
title: BGP Route Reflector Myths
---
New networking myths are continuously popping up. Here's a BGP one I encountered a few days ago:

> You don't need IBGP sessions between BGP route reflectors

In general, that's clearly wrong, as illustrated by this setup:
<!--more-->
{{<figure src="/2022/02/rr-ibgp.png" caption="BGP session (arrows indicate RR clients)">}}

* RR1 and RR2 are route reflectors
* PE1 and PE2 are route reflector clients
* RR1 has an external BGP session

Without the IBGP session between RR1 and RR2, X1 and RR2 could not communicate. Maybe you don't consider that a big deal, in which case add X2 connected to PE2.

Next question: where did that myth come from? Imagine a data center fabric running IBGP (for EVPN) on top of an IGP. You could have dedicated out-of-band route reflectors, or you could use spine switches as route reflectors. Spine switches shouldn't have external connections (more about that in _[Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)_ webinar), and a typical leaf-and-spine fabric wouldn't have spine-to-spine links anyway. IBGP sessions between spine switches do seem like an overkill.

The idea of not having a full mesh of IBGP sessions between spine switches still sounds a bit off. Without that full mesh you're losing redundancy. For example, in our network PE1 receives routes from X1 via RR1 and RR2; if the BGP session between RR1 and PE1 is lost for any reason, PE1 still has a route toward X1. Remove the IBGP session between RR1 and RR2 and you've lost that backup update propagation path.

{{<cc>}}BGP prefix advertised from X1 as observed on PE1{{</cc>}}
```
pe1# sh ip bgp 10.0.0.5
BGP routing table entry for 10.0.0.5/32
Paths: (2 available, best #1, table default)
  Not advertised to any peer
  65001
    10.0.0.1(rr1) (metric 20) from rr1(10.0.0.1) (10.0.0.1)
      Origin IGP, metric 0, localpref 100, valid, internal, best (Cluser length)
  65001
    10.0.0.1(rr2) (metric 20) from rr2(10.0.0.2) (10.0.0.1)
      Origin IGP, metric 0, localpref 100, valid, internal
      Originator: 10.0.0.1, Cluster list: 10.0.0.1
```

In theory, the need for the IBGP sessions between spine switches diminishes if as the number of spine switches grows (unless someone "wisely" decided to use only two of the spines as route reflectors). In practice, I prefer not to over-optimize my designs; I've been bitten too many times by what seemed like an awesome idea at the time I implemented it.

### Lesson Learned

You can't beat the laws of physics (or networking). A BGP router in an autonomous system should either participate in the IBGP full mesh or be a client of at least two route reflectors. For more details, please read _[BGP Route Reflector Details](/2008/08/bgp-route-reflector-details/)_.

Does the above rule cover all possible scenarios? The answer is left as an exercise for the careful reader.
