---
date: 2011-07-25T10:08:00.000+02:00
tags:
- firewall
- MPLS
- workshop
title: Asymmetric MPLS MTU problem
url: /2011/07/asymmetric-mpls-mtu-problem.html
---

Russell Heilling made a highly interesting observation in a comment to my [*MPLS MTU challenges*](https://blog.ipspace.net/2011/07/mpls-mtu-challenges.html) post: you could get asymmetric MTUs in MPLS networks due to penultimate hop popping. 

Imagine our network has the following topology ([drawn](http://en.wikipedia.org/wiki/Vi) with the [fantastic tools](http://en.wikipedia.org/wiki/Monospaced_font) used by the RFC authors):

```
S---CE---R1===R2---FW---C
```
<!--more-->
The only link using MPLS is between R1 and R2. FW is a misconfigured firewall blocking all ICMP packets. Furthermore, FW uses NAT making the client C appear to be directly connected to R2. Layer-2 payload size ([known as MTU on Cisco IOS](https://blog.ipspace.net/2011/07/all-mtus-are-not-same.html)) on all links is 1500 bytes. Unlabeled IP packets can be up to 1500 byte long; labeled IP packets cannot exceed 1496 bytes (depending on the size of the MPLS label stack).

R1 and R2 advertise labels for all known prefixes to each other using LDP. R1 advertises a “real” label for S (because it’s reachable through a next-hop router); R2 advertises *implicit null* label for FW/C to R1 to enable [penultimate hop popping](/kb/tag/MPLS/Implicit_Explicit_NULL.html).

{{<note info>}}Routers [advertise *implicit null* labels for directly connected prefixes and summary routes pointing to *null0*](/2011/07/penultimate-hop-popping-php-demystified.html). You can change that behavior with the **mpls ldp explicit-null** global configuration command that also allows you to limit the use of *explicit null* to specific IP prefixes or LDP peers.{{</note>}}

When the server S sends a packet to client C, R1 should send a labeled packet to R2, but due to *implicit null* advertised by R2, the MPLS label stack is empty; IP MTU from S to C is 1500 bytes.

When C sends a packet to S, R2 inserts a single MPLS label in front of the IP payload (remember: R1 advertised a non-null label for S to R2); IP MTU from C to S is 1496 bytes.

In properly configured networks, asymmetric MTUs wouldn’t matter; combined with misconfigured firewalls they can be fatal and extremely hard to troubleshoot. In our scenario, client would be able to download any content from the server (unless the HTTP request header or its equivalent grows beyond 1456 bytes), but would fail to upload anything longer than ~1400 bytes.

#### More information

To learn more about MTU path discovery and related problems, read the [Never-Ending Story of IP Fragmentation](/kb/Internet/PMTUD/).

You’ll find in-depth description of MPLS/VPN technology and enterprise network deployment hints in our [Enterprise MPLS/VPN Deployment](https://www.ipspace.net/EntMPLS). For more VPN webinars, check our [VPN webinar roadmap](https://www.ipspace.net/Roadmap/VPN_webinars). You get access to all those webinars when you buy the [yearly subscription](https://www.ipspace.net/Subscription).
