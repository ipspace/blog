---
title: "Unnumbered Interfaces: Series"
# date: 2021-04-06 07:28:00
tags: [ IP routing, networking fundamentals ]
draft: True
series: unnumbered-interfaces
---
# Basics: Do We Need Interface Addresses?

TL&DR: Not on point-to-point links

* Explain the differences between device- and link addresses
* Why we don't need link addresses on P2P links
* Why we don't need layer-3 addresses on inter-router links

# Basics: The History of IP Interface Addresses

* SNA and DECnet had node addresses because they were focused on large routed networks. CLNP is really DECnet done right.
* IPX, AppleTalk... had interface addresses because they were designed to run on a single LAN segment
* IP had interface addresses because the original IP hosts had a single interface, and routers didn't use IP

# Basics: What Are Unnumbered IP Interfaces?

Why do we need unnumbered interfaces

* Reduced address utilization
* No need to allocate small address blocks and keep track of them
* Simplified configuration
* Reduced network state (including routing tables)
* Simplified automation

How does routing work?
* Route points to an interface
* There is no next hop
* Assumption: layer-2 header has no device-specific address

IPv4 versus IPv6

# Basics: Unnumbered Ethernet Interfaces

Question: How do we get L2 header when sending a packet across an unnumbered interface?

We need:
* A bogus next hop
* A bogus ARP entry

How do we get those? RFC 5549 or what?

# Running OSPF over Unnumbered Ethernet Interfaces

Describe the OSPF quirks 

# Running Routing Protocols over Unnumbered Interfaces

* IS-IS has no problems
* OSPF has been adjusted
* What about BGP?

RFC xxxx to the rescue