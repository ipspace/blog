---
date: 2009-10-12 06:25:00.005000+02:00
tags:
- ARP
- IP routing
title: 'Follow-up: Interface Default Route'
url: /2009/10/follow-up-interface-default-route.html
---
Judging by your comments, some of you have already faced a stupidity [similar to the one I've described on Friday](/2009/10/my-stupid-moments-interface-default.html). The symptoms are well described in the comments: the CPU utilization of the ARP process increases, packet forwarding becomes sluggish and the router runs out of memory, potentially resulting in a router crash. Now let's analyze what's going on.
<!--more-->
**What's wrong:** A static default route (without an IP next hop) pointing to an interface indicates that the rest of the Internet is directly connected to that interface as a single flat network. Every destination address is reachable directly through that interface.

**Why does the problem occur on an Ethernet interface and not on a point-to-point link:** The router does not need to know the layer-2 address of its neighbor on a point-to-point link; it has a single neighbor and the layer-2 encapsulation is static.

On a multi-access interface, the router has to match the destination IP address with a layer-2 address of the next-hop router or host. A static route pointing to an interface is an equivalent of telling the router that all the addresses covered by the static route's IP prefix are directly connected.

**How does the router react:** Since every IP address on the Internet is supposedly directly connected, the router needs the MAC address of every destination host if it wants to forward the IP traffic to it. For every new destination IP address the router sends an ARP request and drops all IP packets until the ARP request is resolved. This also explains the high CPU utilization caused by the ARP process.

**Why is the packet forwarding so sluggish:** If you're not using CEF switching, the router falls back to process switching for every next-hop address that is not yet available in the ARP cache. The first few packets toward any new destination address on the Internet are therefore process switched.

**Why is the router running out of memory:** The ARP cache is not supposed to grow indefinitely. Cisco IOS has no mechanism that would limit its size, it's flushing the ARP cache only when its entries age out (and even that is [never going to happen if you use CEF](/2007/06/ar.html)).
