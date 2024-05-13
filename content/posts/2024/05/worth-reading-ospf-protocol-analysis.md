---
title: "Must Read: OSPF Protocol Analysis (RFC 1245)"
date: 2024-05-16 08:40:00+0200
tags: [ OSPF ]
---
Daniel Dib [found](https://twitter.com/danieldibswe/status/1789894892769931265) the ancient [OSPF Protocol Analysis (RFC 1245)](https://www.rfc-editor.org/rfc/rfc1245) that includes the *Router CPU* section. Please keep in mind the RFC was published in 1991 (35 years ago):

> Steve Deering presented results for the Dijkstra calculation in the "MOSPF meeting report" in [3]. Steve's calculation was done on a DEC 5000 (10 mips processor), using the Stanford internet as a model. His graphs are based on numbers of networks, not number of routers. However, if we extrapolate that the ratio of routers to networks remains the same, the time to run Dijkstra for 200 routers in Steve's implementation was around 15 milliseconds.
<!--more-->
Talking about [Millions of Instructions per Second](https://en.wikipedia.org/wiki/Instructions_per_second#Millions_of_instructions_per_second_(MIPS)) (MIPS) makes as much sense as measuring outside temperature with a wet finger because the amount of work you can do in an instruction depends on the CPU architecture, and memory access quickly becomes the bottleneck anyway. However, while [Cisco 2500 router](https://en.wikipedia.org/wiki/Cisco_2500_series) had a CPU comparable to the one mentioned in RFC 1245, the then-recommendation was "30 routers per area", giving more credence to the rumors about suboptimal OSPF implementation (as opposed to IS-IS) in Cisco routers.

Anyhow, modern CPUs are a bit faster than their 1991 counterparts. Ten-year-old Intel CPUs have ~1000 times higher CPU frequency and ~8000 times the CPU performance of the machine described in RFC 1245. The claims that one *needs* to replace OSPF (or IS-IS) with EBGP to make a data center fabric scale (as opposed to *wants to play with a new toy* or *would like to boost his resume*) are obviously total BS, unless you bought networking software from a vendor who decided to implement OSPF in JavaScript or Prolog 😜
