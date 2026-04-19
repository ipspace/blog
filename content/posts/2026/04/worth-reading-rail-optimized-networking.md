---
title: "Hmmm: Rail-Optimized Networking for AI Workloads"
date: 2026-04-21 07:44:00+0200
tags: [ worth reading, data center, fabric ]
---
Phil Gervasi wrote an interesting article describing [Rail-Optimized Networking for AI Training Workloads](https://networkphil.com/2026/04/15/rail-optimized-data-center-networking-for-ai-training-workloads/). Go read it first; I'll wait.

Does it sound interesting? Were you able to see behind the curtain and figure out what it's really about?
<!--more-->
The way I read it, he described a regular leaf-and-spine fabric in which the workload is placed in such a way that most traffic stays within leaf switches. That has nothing to do with networking; it's just smart workload placement. Straight from Phil's article:

> A rail isn’t a separate topology or a bypass of the leaf-spine fabric. Instead, it’s a consistent mapping of endpoints to a specific network plane within a shared Clos-based fabric.

I don't know enough about intra-server forwarding to figure out whether the "_stay within the leaf switch and use the server bus to send traffic to the other GPU_" idea has anything to do with networking, or is it just using RDMA to write into another part of memory (= application-level solution).

In any case, the idea is not new. This is a slide I had in my *Designing a Private Cloud* presentation from 2014, and the idea was already pretty old and well known by then.

{{<figure src="/2026/04/load-splitting.png">}}

What about the other idea Phil described: use disconnected leaf switches (rail-only networks)? Back to his article:

> Each rail acts as an independent failure domain, which also provides a bounded congestion domain. 

Remember the SAN-A/SAN-B networks from the 1990s, using either Fibre Channel or iSCSI?

**Long story short:** When in doubt, read RFC 1925 ;))
