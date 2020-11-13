---
title: "Fast Failover: Hardware and Software Implementations"
date: 2020-11-12 09:23:00
tags: [ IP routing ]
series: fast-failover
draft: true
---
**Hardware-based failover** changes the hardware forwarding tables after a hardware-detectable link failure (most likely loss-of-light). Forwarding hardware is usually pretty limited and cannot do extensive calculations; the alternate paths are thus usually pre-programmed (more details in an upcoming blog post).

**Software-based failover** can act on link or node failures, including byzantine failures on a path between two forwarding engines as detected by BFD or similar protocols. It can involve extensive reprogramming of forwarding tables, but do keep in mind that on modern CPUs the reprogramming of forwarding tables might take longer than the time routing protocol needs to do its job, so it might not make sense to make software-based failover too complex.
