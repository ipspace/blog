---
comment: 'In early 2020 I created the _[Comparing IP and CLNP Addressing](https://my.ipspace.net/bin/get/Net101/NA3.2%20-%20Comparing%20IP%20and%20CLNP%20Addressing.mp4?doccode=Net101)_
  video as part of the _[How Networks Really Work webinar](https://www.ipspace.net/How_Networks_Really_Work)_.
  This blog post is an edited transcript of the third part of that video.

  '
date: 2025-03-19 07:59:00+01:00
networking-fundamentals_tag: osi
series_title: Network State Summarization
tags:
- networking fundamentals
title: 'Comparing IP and CLNP: Network State Summarization'
---
In the previous blog posts, we discussed how [TCP/IP and CLNP reach adjacent nodes and build ARP/ND/ES caches](/2024/10/comparing-ip-clnp-addressing/) and how they [reach off-subnet nodes](/2025/03/comparing-ip-clnp-off-subnet-nodes/). Now, let's move from the network edge into the network core and explore how the two protocol stacks reduce the amount of information they have to propagate in routing protocols.

While I'm not exactly an OSI fan, I must admit they got many things right (and IPv6 copied those ideas), but TCP/IP is a clear winner in this aspect.
<!--more-->
{{<figure src="/2025/03/addr-reducing-network-state.png">}}

In the IPv4/IPv6 world, prefixes (subnets) are assigned to data link layer segments, hiding their internal structure from anyone not attached to the segment. Thus, the routers advertise the prefixes (for example, /64 IPv6 prefixes), and from the forwarding perspective, no one outside the subnet cares about the node addresses because a node address always belongs to a subnet prefix.

Every IPv4 routing protocol has at least one additional summarization boundary beyond subnet-level summarization. Some routing protocols, like EIGRP or BGP, provide multiple summarization boundaries. For example, in EIGRP, there could be a different summarization boundary on every interface. 

{{<note info>}}Interestingly, decades after IS-IS was invented, some vendors decided to try to retrofit IS-IS with multiple summarization boundaries ([IS-IS Extended Hierarchy](https://www.ietf.org/archive/id/draft-ietf-lsr-isis-extended-hierarchy-06.html)).{{</note>}}

The CLNP world has no intrinsic subnets, and [addresses are assigned to nodes](/2024/02/interface-node-addresses/) (not interfaces). IS-IS areas are somewhat equivalent to IP prefixes, but entries for every node had to be known by every router within an OSI area (not just on a single segment). Beyond that, you only had the second level of summarization, exchanging areas between level-two routers in IS-IS.

{{<note>}}It's worth noting that it is perfectly possible to have many levels of summarization with NSAPs (OSI addresses). For example, many summarization levels were defined for PNNI, the routing protocol for ATM networks {{</note>}}

From the technology perspective, IP and CLNP could implement many levels of summarization hierarchy. However, from the implementation perspective, most CLNP networks had only two levels of summarization: intra-area routing based on node addresses and inter-area routing based on area addresses (prefixes). In contrast, most TCP/IP routing protocols had at least three levels: subnets, intra-area prefixes, and inter-area summary prefixes.

In both cases, you could always combine an IGP with BGP and have many additional summarization levels in BGP. 

{{<note info>}}It is possible to use BGP with CLNP, with at least [Cisco IOS having a working implementation](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/command/irg-cr-book/bgp-a1.html#wp6463189810). [IANA AF registry](https://www.iana.org/assignments/address-family-numbers/address-family-numbers.xhtml) defines an AF value for NSAPs (OSI addresses), and you can use that AF value with [multiprotocol extensions for BGP-4](https://datatracker.ietf.org/doc/html/rfc4760).{{</note>}}
