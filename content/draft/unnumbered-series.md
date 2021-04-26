---
title: "Unnumbered Interfaces: Series"
# date: 2021-04-06 07:28:00
tags: [ IP routing, networking fundamentals ]
draft: True
series: unnumbered-interfaces
---
# Basics: Do We Need Interface Addresses?

TL&DR: Not on point-to-point links

# Basics: The History of IP Interface Addresses

* IP had interface addresses because the original IP hosts had a single interface, and routers didn't use IP

# Basics: What Are Unnumbered IP Interfaces?

Why do we need unnumbered interfaces

# Basics: Routing over Unnumbered Interfaces

* Route points to an interface

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