---
title: "Repost: LISP Is a False Economy"
date: 2022-03-01 07:13:00
tags: [ LISP ]
---
_Minh Ha left this comment on the *[Packet Forwarding 101](/2022/02/packet-forwarding-header-lookup/)* blog post. As is usually the case, it's fun reading and it would be a shame not to repost it as a standalone blog post (even though I don't necessarily agree with all his conclusions)._

---

I always enjoy Bela's great insights, esp. on hardware and transport networks, but this time I beg to differ. LISP, is a false economy. It was twisted from the start, unscalable right from the get-go. In Networking and OS, to name (ID) something is to locate it, and vice versa. So the name LISP itself reflects a false distinction. Due to this misconception, LISP proponents are unable to establish the right boundary conditions, leading to the size of xTRs' RIB diverging (going unbounded). In a word, it has come full circle back to BGP, an exemplary manifestation of RFC 1925 rule 6.
<!--more-->
As always, misunderstanding the fundamentals leads to exploding complexity and dead ends, so LISP has [problems with path liveness check and state synchronization as well](https://datatracker.ietf.org/doc/html/draft-meyer-loc-id-implications-01#section-4)[^DM]

[^DM]: Dave Meyer identified numerous shortcomings of Locator/ID separation in early 2009. As is usually the case, nobody listened.

All 3 problems severely limit scalability, so LISP essentially fails in its original goal. One can argue that LISP works fine for small networks, but small networks need no design. There, a brute-force sequential search (flat) method for routing is good enough, in a word, anything goes. It's the big networks that need hierarchy, and LISP can't enforce this hierarchy essential for scaling, because it can't impose the right boundary conditions.

LISP is in a pretty similar situation to TCP congestion control, wherein people, due to a lack of understanding, naively think it can be solved by "careful tuning" of parameters. It cannot, because end-to-end CC is a dead end. So as long as you keep clinging to it, all you do is putting lipstick on a pig.

Just as the key with CC is understanding that end-to-end CC attempts to solve problem on the wrong layer, and so all end-to-end transport protocols, try as they may, are fundamentally incapable of resolving it, and what has to be done, is a renormalization of the CC's length scale and layering, the key to understanding why LISP is unworkable on large scale, is realizing that people have been asking the wrong question. Routing explosion is an addressing problem; it has to be solved based on an understanding of how addressing should be structured.

As it stands, IP is missing more than half the structure, with IP and MAC redundantly naming the same thing (the interface). This, coupled with provider-based addressing, plus one global address space for the entire Internet, will always lead to unbounded RIB sizes, and routing update explosion. Topological addressing can deal with that, and when we think in terms of topology, new structures start to emerge, including the understanding that provider-independent address assignment, is the right way to go. Topological PI addressing will help set up the proper boundary conditions, and RIB size can go down by several times and potentially be bounded too.

[Tony P's comments on valley-free routing](/2018/09/repost-tony-przygienda-on-valley-free/)  is essentially a description of topology-based (resilient) addressing, where distortion on the network graph has no impact on underlying addressing structure -- it's topologically protected.

Since this scaling metric is universal enough, the same solution applies equally to DC networks, which essentially are just one type of SP network. It can lead to better simplification and less pain.