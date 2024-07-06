---
date: 2009-12-09 06:39:00+01:00
tags:
- load balancing
title: Load Sharing 101 (with References)
url: /2009/12/load-sharing-101-with-references.html
---
It looks like my [load sharing posts](/tag/load-balancing.html) did not paint the whole picture; I'm always assuming the readers have a basic level of IP routing knowledge (somewhere around BSCI/CCNP) and jump into juicy details. Let's try to fix this error and start from the beginning. For more details, watch the [How Networks Really Work webinar](https://www.ipspace.net/How_Networks_Really_Work).

A router receives its routing information (reachability of IP prefixes) from various sources: connected IP prefixes, static routes and dynamic routing protocols. For every IP prefix, the best source (= one with the lowest administrative distance) is selected and only the route(s) from that source are included in the IP routing table.
<!--more-->
If the best source offers multiple equal-cost routes, more than one (up to the value of **maximum-paths** router configuration command) can be installed in the IP routing table and used for *load sharing*.

{{<note>}}Things can get tricky when you use BGP, the *How Networks Really Work* webinar explains those details in *[Advanced Routing Protocol Topics](https://my.ipspace.net/bin/list?id=Net101)* section.{{</note>}}
<!--more-->
What happens next depends on the forwarding (switching) mechanism used by the router. All switching mechanisms perform best-prefix match: they use the entry (or entries) that are the closest match for the destination IP address. If the best prefix has multiple entries in the IP routing table (traffic toward it can be load-shared), the action varies by switching mechanism:

{{<note warn>}}Keep in mind this blog post was written in 2009, and covers only software switching implementations in Cisco IOS. For updated information watch the *Multipath Forwarding* part of *[Advanced Routing Protocol Topics](https://my.ipspace.net/bin/list?id=Net101)* section I mentioned above.{{</note>}}

**Process switching:** The router performs an IP routing table lookup for every forwarded packet and selects one out of several possible entries in a round-robin fashion, resulting in per-packet load balancing.

**Fast switching:** Initial packet is process-switched (see above) and a cache entry is created based on the results of the IP routing table lookup. Further packets use the cached entry and thus always use only one of the possible routes.

There rules are somewhat crazy; sometimes fast switching would create per-host entries (resulting in better spread of the load), but in most cases (including the worst one: two default routes) it behaves as described.

**CEF switching:** information from IP routing table is evaluated (including recursive lookups) and transferred into CEF FIB (forwarding information base). For every IP prefix with multiple entries in the IP routing table, CEF creates a table of 16 slots and [populates them with alternate routes to the IP prefix](/2006/10/cef-load-sharing-details.html) ([in unequal-cost load sharing some routes are used more often than the others](/2007/02/unequal-cost-load-sharing.html)).

CEF supports [per-destination](/2006/10/cef-per-destination-load-sharing.html), [per-packet](/2006/12/per-destination-or-per-packet-cef-load.html) and [per-session](/2006/12/per-port-cef-load-sharing.html) load sharing. Per-packet load sharing is obvious: the 16 slots are used in a round-robin fashion. Per-destination load sharing takes the source and destination IP address from the forwarded packet, scrambles (the correct term is hashes) them together to get a 4-bit number (between 0 and 15) and selects the route from the corresponding slot in the 16-slot table to forward the packet. Per-session load sharing uses [source and destination UDP/TCP ports together with the source and destination IP address in the hashing function](/2006/12/per-port-cef-load-sharing.html).
