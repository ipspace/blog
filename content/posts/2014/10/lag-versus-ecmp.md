---
date: 2014-10-06T07:20:00.000+02:00
tags: [ link aggregation, IP routing ]
title: LAG versus ECMP
url: /2014/10/lag-versus-ecmp.html
---

[Bryan](https://www.linkedin.com/in/bryanbartik) sent me an interesting question:

> When you have the opportunity to use LAG or ECMP, what are some things you should consider?

He already gathered some ideas (thank you!), and I expanded his list and added a few comments.

**Purpose**: resiliency or more bandwidth? For resiliency you want fast failure detection and the ability to connect to multiple uplink devices, for more bandwidth, you want better hashing.
<!--more-->
**Failure detection**: LAG uses LACP to detect link failures, and assuming your LAG implementation supports fast LACP timers, you can [detect link failures in three seconds](https://blog.ipspace.net/2012/09/do-we-need-lacp-and-udld.html). ECMP uses routing protocol hello mechanisms (which you can tune to sub-second convergence) or BFD.

**Scalability**: Adding more IP links might increase the size of the OSPF link state database (or not, if you use IPv6 link local addresses or OSPF knobs that don’t propagate transit subnets in router LSAs).

ECMP usually increases the size of the IP routing table and forwarding tables, which might cause problems in some data center switches with pretty low IPv4 and [IPv6 forwarding tables](https://blog.ipspace.net/2014/09/ipv6-neighbor-discovery-nd-and.html). Some vendors might be smart enough to use next-hop groups (available in most switching silicon these days) for ECMP purposes; not sure whether anyone does – please do write a comment if you know more.

On the other hand, you might get multiple ARP entries for a single IP adjacency (toward a router or a host) over a LAG in forwarding architectures that include outgoing physical interface in the ARP entry. In these scenarios you might run out of ARP/ND entries.

**Load balancing** **algorithm**: usually not an issue. Platforms that support [5-tuple load balancing](https://blog.ipspace.net/2006/12/per-port-cef-load-sharing.html) across a LAG usually support it over ECMP and vice versa. There might be exceptions that drove you mad – write a comment and list the offenders.

**Redundant** **designs**: It’s trivial to implement a design connecting an edge (leaf) switch to two core (spine) switches with ECMP. Doing the same thing with LAG involves MLAG, which is always proprietary (because there’s no MLAG standard) and somewhat clumsy.

Using more than two spine switches in a layer-2-only fabric forces you to use TRILL/SPB or any number of proprietary layer-2 fabric solutions (example: FabricPath, VCS Fabric…). I'd rather stay with ECMP; it's been working for the last 20 years.

Anything else? Write a comment!

#### More information

Speaking of leafs and spines -- you’ll find numerous L2/L3 designs in my [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar. Worried about forwarding table sizes of popular data center switches? Check out the [Data Center Fabric Architectures](http://www.ipspace.net/Data_Center_Fabrics) webinar (or get access to both of them and [dozens more](http://www.ipspace.net/Webinars) with the [subscription](http://www.ipspace.net/Subscription)). We can also discuss your design and implementation challenges in an [ExpertExpress session](http://www.ipspace.net/ExpertExpress).

