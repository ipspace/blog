---
date: 2017-10-10 09:10:00+02:00
dcbgp_tag: abstract
ospf_tag: rant
series:
- dcbgp
tags:
- OSPF
- BGP
- IP routing
title: 'Routing Protocols: Perfect Example of RFC 1925 Rule 5'
url: /2017/10/routing-protocols-perfect-example-of.html
---
In case you're not familiar with RFC 1925, Rule 5 states:

> It is always possible to agglutinate multiple separate problems into a single complex interdependent solution. In most cases, this is a bad idea.

Most routing protocols are a perfect demonstration of this rule.
<!--more-->
A typical routing protocol tries to handle:

-   Neighbor discovery (which nodes can I see on the link)
-   Failure detection (is the path to my neighbor working)
-   Health check and byzantine neighbor failure detection (is the neighbor sane)
-   Dissemination of information (aka flooding)
-   Collecting and distributing topology information (who is connected to whom)
-   Collecting and distributing endpoint reachability information (what endpoints are connected to the network)

Most routing protocols reinvent every single wheel listed above and also try to bundle several features with sometimes conflicting requirements into a single protocol. For example, OSPF, EIGRP, and IS-IS use *hello* or *keepalive* messages to discover neighbors, detect link failure, and verify neighbor's health. BGP uses *keepalive* messages to detect link and neighbor failure.

Is there anything wrong with that approach? Of course -- links usually fail more often than nodes or routing protocols. It's crucial to detect link failure relatively quickly, but we don't have to be aggressive with the node health check.

Not surprisingly, we got BFD a while back -- a lightweight protocol with a single mission: detect path loss between two adjacent unicast IP addresses. Nonetheless, years later, we're still discussing BGP keepalives.

While more and more network deployments use BFD, we still haven't even touched the *dissemination of information* problem. Why does every single routing protocol have to reinvent flooding when we have so many production-tested message queue or eventually-consistent database products?

Finally, agglutinating routing and reachability information led to bloated LSPs in IS-IS and a zillion tiny LSAs in OSPF.

As always, it's possible to get a more stable and scalable network (even though the tools are suboptimal) with sensible architecture. A typical large-scale network design would use the right tool for each job:

-   OSPF or IS-IS to discover network topology and shortest paths;
-   BGP to collect endpoint information and map it to egress next-hop.

However, while we knew how to design scalable networks for ages, many engineers deploying large enterprise networks consistently ignored that insight, resulting in way too many OSPF Band-Aids.
