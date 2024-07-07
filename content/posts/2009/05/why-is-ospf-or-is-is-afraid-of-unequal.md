---
date: 2009-05-02 22:33:00+02:00
ospf_tag: ucmp
tags:
- IS-IS
- OSPF
title: Why Is OSPF (Or IS-IS) Afraid of Unequal-Cost Load Balancing
url: /2009/05/why-is-ospf-or-is-is-afraid-of-unequal/
---
You might have wondered why no link-state routing protocols support unequal-cost load balancing (UCLB). Petr Lapukhov provides part of the answer in his [Understanding Unequal-Cost Load-Balancing](http://blog.internetworkexpert.com/2009/05/01/understanding-unequal-cost-load-balancing/) article: EIGRP is one of those few protocols that can ensure a neighbor is not using the current router as its next-hop.

However, one has to wonder: with OSPF and IS-IS having the entire network topology (or at least the intra-area part of it) in the SPF tree, how hard would it be to detect that sending a packet to a device that is not on the shortest path results in a forwarding loop? Is the lack of OSPF or IS-IS UCLB in Cisco IOS the result of lip service to the standards (at least the OSPF one is way too prescriptive) or a shoddy implementation? What are your thoughts?
