---
date: 2022-02-14 07:40:00+00:00
series:
- forwarding
tags:
- networking fundamentals
- switching
- LISP
title: 'Packet Forwarding 101: Header Lookups'
---
Whenever someone asks me about LISP, I answer, "_it's a nice idea, but cache-based forwarding never worked well._" Oldtimers familiar with the spectacular failures of fast switching and various incarnations of flow switching usually need no further explanation. Unfortunately, that lore is quickly dying out, so let's start with the fundamentals: how does packet forwarding work?

Packet forwarding used by bridges and routers (or [Layer-2/3 switches](/2011/02/how-did-we-ever-get-into-this-switching/) if you believe in [marketing terminology](/2009/12/lies-damned-lies-and-product-marketing/)) is just a particular case of [statistical multiplexing](https://en.wikipedia.org/wiki/Statistical_time-division_multiplexing) -- a mechanism where many communication streams share the network resources by slicing the data into packets that are sent across the network. The packets are usually forwarded independently; every one of them must contain enough information to be propagated by each intermediate device it encounters on its way across the network.
<!--more-->
Packet forwarding in an intermediate device is always composed of these steps:

* Receive a packet;
* Extract forwarding information from the received packet;
* Find the next hop or outgoing interface from a lookup table;
* Enqueue the forwarded packet into an output queue where it waits to be sent to the next device.

The lookup step is often the most complex part of packet processing:

* Exact matches of a small set of values (VLANs, MPLS labels) are straightforward: allocate a large enough table to accommodate all possible values and populate it with forwarding information.
* Exact matches of a large set of values (MAC addresses, IP addresses, IPv4 /32 prefixes...) usually use hash tables. A data-munging function produces a unique small number out of the (too large) value and uses that as an entry into the forwarding table. Sounds easy until you realize that the function could produce the same result for multiple input values. Welcome to the wonderful world of [hash collisions](https://en.wikipedia.org/wiki/Hash_collision) and hacks like [Cuckoo hashing](https://en.wikipedia.org/wiki/Cuckoo_hashing).
* Lookups of network prefixes (using longest-prefix matching) traditionally used a tree-like data structure (example: [trie](https://en.wikipedia.org/wiki/Trie)) that requires several accesses to get the answer, significantly reducing the packet forwarding performance. Alternate solutions include hash tables for prefixes with known length (example: /24 IPv4 prefixes) or [Bloom filters](https://en.wikipedia.org/wiki/Bloom_filter) (see [Longest-Prefix Matching Using Bloom Filters](https://cial.csie.ncku.edu.tw:8081/presentation/group_pdf/[Y2006]Longest%20Prefix%20Matching%20Using%20Bloom%20Filters.pdf)  for details).
* More complex lookups use [TCAM](https://en.wikipedia.org/wiki/Content-addressable_memory#Ternary_CAMs) -- an extraordinarily versatile but also power-hungry and expensive bit of hardware -- or dirty hacks like "_let's walk down an access control list and compare every line with the header of the packet we're trying to forward._"

Compared to the awkwardly slow way we were taught access control lists work, TCAM works almost like magic:

* The network operating system stores matching values and corresponding bit masks into TCAM
* When presented with an input value, the best match (considering the match values, bitmasks, and matching priorities) pops up in a single lookup.

While we usually associate TCAM with hardware-based packet forwarding, I've seen what seems to be an efficient software implementation of TCAM in Open vSwitch. It was elegant but so complex that I don't want to look at it again ;)

Ready to deal with even more complexity? How about recursive lookups, from BGP prefixes to BGP next-hops (which can be BGP prefixes themselves, adding another layer of indirection) to IGP next-hops or static routes. Modern hardware can accept most of that complexity through a hierarchical forwarding table[^FW]. In the good old days, complex hardware was too expensive, so the routers had to do the recursive walk through the routing table for every packet until someone got a bright idea: what if we would cache the results of the recursive lookup?

[^FW]: As expected it's hard to get the actual details. Minh Ha pointed me to [ASR9K documentation](https://community.cisco.com/t5/service-providers-documents/asr9000-xr-load-balancing-architecture-and-characteristics/ta-p/3124809); if you're aware of a similar document describing other hardware platforms please write a comment.

Coming up next: cache-based forwarding

### More Details

* You'll find an extensive discussion of various packet forwarding mechanisms in the [Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH) part of _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.
* Hierarchical FIB and its use in prefix-independent convergence is covered in the Fast Failover part of the same webinar.
