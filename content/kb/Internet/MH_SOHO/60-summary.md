---
kb_section: MH_SOHO
minimal_sidebar: true
title: Summary
alt_section: posts
---
With the ever faster replacement of traditional WAN networks with MPLS VPN- or Internet-based solutions, it’s increasingly important to have a good design and implementation strategy for small multi-homed sites. While it’s easy to implement multi-homed sites whenever you are able to run a routing protocol between the customer edge (CE) and provider edge (PE) router, as is the case with most MPLS VPN implementations, the static default routing imposed on most Internet customers by their ISPs make reliable multi-homing almost impossible in modern networks that are not able to signal loss of layer-2 connectivity reliably.

The *Reliable Static Routing Using Object Tracking* feature available in Cisco IOS release 12.4 allows you to tie static route viability to a tracked object (interface, another route …). If you track the state of the next-hop router, it’s possible to detect layer-3 failures reliably, triggering a reroute to the backup ISP. You can improve this design, track the end-to-end availability of the central site and reroute to the backup ISP whenever you cannot reach the central site through the primary ISP. Even more, you don’t have to rely on ICMP echo packets; IP SLA feature of Cisco IOS can track availability of a large number of applications (for example, your company’s central web server).
