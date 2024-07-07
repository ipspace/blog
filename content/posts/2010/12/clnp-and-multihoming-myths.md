---
date: 2010-12-07 06:08:00+01:00
multihoming_tag: server
series:
- multihoming
tags:
- IPv6
- Internet
- CLNP
title: CLNP and the Multihoming Myths
url: /2010/12/clnp-and-multihoming-myths/
---
When IESG decided to adopt SIP, not TUBA (TCP/UDP over CLNP) as IPv6, a lot of people were mightily disappointed and some of them still propagate the myths how CLNP with its per-node addresses would fare better than IPv6 with its per-interface addresses (you might find the [writings of John Day on this topic](http://pouzin.pnanetworks.com/images/LocIDSplit090309.pdf) interesting and [Petr Lapukhov is also advocating this view in his comments](#comments)).

These views are correct when considering small-scale (intra-network) multihoming, but unfortunately wrong when it comes to Internet-scale multihoming, [where CLNP with TCP on top of it would be as bad as IPv4 or IPv6 is](/2022/11/multihoming-within-network/) (routing table explosion due to multihoming is also one of the topics of my *Upcoming Internet Challenges* webinar).
<!--more-->
{{<note>}}Before anyone accuses me of being IP-centric ignoramus: my first encounter with networking was DECnet phase IV and I was totally shocked (and dismayed) when discovering the IP subnet-focused architecture. I was also beta-testing TUBA implementation in Cisco IOS and thus firmly belonged to the disappointed "how-could-they-had-chosen-SIP" camp.{{</note>}}

### CLNP Background

CLNP addresses are assigned to nodes, not interfaces. In IPv4 terms, all interfaces (even multi-access interfaces like LAN) are unnumbered and each node has a "loopback" interface with a single address (/32 prefix in IPv4). While the concept was highly interesting and marginally more useful than subnet-based IP architecture, it also imposed additional burden on hosts and routers:

-   Hosts and routers had to run ES-IS protocol which enabled routers to find adjacent hosts and helped hosts to find the nearest router (similar to what we do with RA in IPv6).
-   Routers had to propagate host reachability information (host routes in IP terminology) throughout the area.
-   Each router in the area had to know the location of all hosts within the same area.

CLNP intra-area forwarding has some elements superficially similar to bridging (packets are forwarded based on host ID) but works as true routing (layer-2 encapsulation is changed and TTL is decreased whenever a packet is forwarded by a CLNP router). The number of hosts within an area is obviously limited by the routers' capabilities (and can be quite limited in some actual CLNP implementations); to scale, CLNP introduced a concept of areas, which are almost identical to IP summary routes.

IP undoubtedly scales much better, as its IP subnets present the first layer of summarization: even if the directly connected router has to know the location of every host in the subnet (its MAC address learned through ARP), that information is not propagated to any other router.

### CLNP and Multihoming

Per-node addresses nicely solve intra-area multihoming. A host is always reachable through a single address, even if it has more than one interface. When an interface fails, the existing sessions are not disrupted (as they originate from an address that belongs to the box, not the failed interface).

CLNP behavior might have been marginally more useful for multihomed workstations, in particular to mission-critical applications that cannot afford to lose TCP sessions, but I doubt that most users have serious problems with the current IP-subnet-based approach.

Multihomed CLNP servers are undoubtedly easier to implement than their IP cousins (there is nothing to implement in the CLNP case), but the current tools (from NIC bonding to multi-chassis port channel) provide reasonably-good solution.

In any case, if you truly want to have CLNP-like behavior, you can always deploy loopback interfaces and RIP or OSPF on the servers (IBM used that approach to implement IP multihoming for the mainframes).

### Larger-scale Multihoming

CLNP hosts could not be attached to more than one area or they'd have to use two CLNP addresses, one in each area (or become inter-area routers), so CLNP is no different from IP when you want to have a host attached to two widely separate subnets or areas.

The claims that node-based addresses could solve global routing table explosion are still [misguided science fiction](/2022/11/multihoming-within-network/).
