---
date: 2019-02-19 08:31:00+01:00
tags:
- switching
- data center
- ACI
title: Cross-Data-Center L4-7 Services With Cisco ACI
url: /2019/02/cross-data-center-l4-7-services-with/
---
[Craig Weinhold](https://www.linkedin.com/in/craig-weinhold-0230236/) sent me his thoughts on using Cisco ACI to implement cross-data-center L4-7 services. While we both believe this is not the way to do things (because you should start with proper application architecture), you might find his insights useful if you have to deal with legacy environments that believe in Santa Claus and solving application problems with networking infrastructure.

---

An "easy button" for multi-DC is like the quest for the holy grail. I explain to my clients that the answer is right in front of them -- local IP addressing, L3 routing, and DNS. But they refuse to accept that, draw their swords, and engage in a fruitless war against common sense. Asymmetry, stateful inspection, ingress routing, split-brain, quorums, host mobility, cache coherency, non-RFC complaint ARP, etc.  
<!--more-->
Shamefully, I've stretched firewall clusters and MLAGs, OTV and LISP, NSX UDLR's and F5 EtherIPs. I've done ingress route optimization with host routing, LISP, mobile ARP, Python scripts, and F5 VIP advertisements. I've dealt with storage metroclusters, geoclusters, and clusterf\*\*\*'s. I even wrote my own GSLB back in the 90's to handle mainframe TN3270 VIP redundancy.   

That said, Cisco ACI has been slowly delivering a serious "easy button".

-   ACI's internally uses an [endpoint table](https://www.cisco.com/c/en/us/solutions/collateral/data-center-virtualization/application-centric-infrastructure/white-paper-c11-739989.html) and host routing rather than relying on decoupled MAC, ARP, and IP forwarding tables. For better or worse, this normalizes endpoint behavior, killing off non-RFC compliant crap, old IP stacks, "adaptive" NIC teaming, bad software load-balancing, and other monstrosities. With ACI, all endpoints are clean endpoints.
-   ACI multi-pod and multi-site both normalize how the fabric stretches L2/L3/VRF for up to a dozen remote sites. No more cobbling a DIY solution out of disparate technologies.
-   ACI can advertise each DC's host routes to the upstream network in that DC, where they can be summarized or propagated at will. This provides a normalized way of optimizing ingress routing compatible with any routing protocol and WAN technology.
-   ACI's most recent 4.0 release from November 2018 has normalized the multi-site behavior of a service chain containing a firewall and/or a load-balancer (with or without source NAT) that may live in different DC's. The firewall & SLB can be of any vendor, physical or virtual, and are deployed in a simple active/standby configurations (i.e., no need for complicated stretched clusters or active/active, although those are also supported). As you can imagine, this is a very complex area, so make sure you understand the details before rushing in.

I'm a cynic and a skeptic, but it's clear that Cisco ACI is making strong progress in delivering an "easy button" multi-tenant, multi-DC architecture that effortlessly supports clean L3, stretched L2, and stretched L4-7.
