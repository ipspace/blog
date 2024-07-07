---
date: 2021-10-14 06:23:00+00:00
dcbgp_tag: relevant
series:
- dcbgp
tags:
- BGP
title: BGP Optimal Route Reflection 101
---
Almost a decade ago I described a scenario in which a [perfectly valid IBGP topology could result in a permanent routing loop](/2013/10/can-bgp-route-reflectors-really/). While one wouldn't expect to see such a scenario in a well designed network, it's been known for ages[^ORR-1] that using BGP route reflectors could result in suboptimal forwarding.

[^ORR-1]: A [handwaving](https://wiki.c2.com/?HandWaving) catch-all phrase used when there's no data to support the claim, or when the writer is too lazy to go into the details.

Here's a simple description of how that could happen:
<!--more-->
* Multiple edge routers advertise the same prefix (IPv4, IPv6, or VPNv4).
* BGP route reflector (RR) receives all alternate BGP paths to that prefix, and selects one of them as the best one. When the BGP paths are too similar, it uses IGP cost to the BGP next hop[^ORR-2] as the tie breaker.
* The best path selected by the BGP RR is advertised to its clients.

**The challenge**: RR clients might be better served using a different prefix (due to a different position in IGP topology), or could use multiple prefixes with identical IGP cost for IBGP multipathing.

[^ORR-2]: Figuring out what happens if the BGP next hop is reachable through another BGP route is left as an exercise for the reader.

We had a solution to that challenge for years: *[Advertisement of Multiple Paths in BGP](https://datatracker.ietf.org/doc/html/rfc7911)* (RFC 7911) aka *BGP AddPath*[^1], and it's available in most modern BGP implementations... but the remaining flies in the ointment still bother some people:

[^1]: Or you could use [PE-specific route distinguishers in MPLS/VPN](/2012/07/bgp-route-replication-in-mplsvpn-pe/). EVPN is using the same approach.

* BGP RR clients receive more information than needed, resulting in memory- and CPU overhead.
* With most *BGP AddPath* implementations the operator can limit the number of alternate routes sent to the BGP RR clients... but what is the minimum number of alternate paths you need to get optimal end-to-end packet forwarding?

As you might have expected: whenever there's a niche challenge to be solved, there's an IETF draft or RFC solving it (sometimes in five different ways). This time, it's *[BGP Optimal Route Reflection (BGP ORR)](https://datatracker.ietf.org/doc/html/rfc9107)* (RFC 9107). 

Here's the CliffsNotes version of that idea: the BGP route reflector imagines how it must feel to be its client, selects the best BGP paths *from its client perspective* and sends them to the client.

Hope you got two questions while reading the previous sentence:

* **Are the best BGP paths calculated _for every client_** (and how much overhead would that generate)? Fortunately, the BGP ORR implementations are smarter than that, and allow you to configure *groups of clients*. Also, you need to run the client-specific calculations only for otherwise-identical paths where IGP cost is the tie breaker *unless you want to support client-specific route selection policies* -- a morass into which we won't look.
* **How does the BGP RR know what it feels like to be a client?** BGP RR and its clients could be part of the same link-state IGP area, or the RR clients could sent their topology information to the reflector via [BGP-LS](/2021/06/ospf-bgp-ls/)[^ORR-LS]

[^ORR-LS]: What else did you expect? IETF has a hammer for every nail.

**Has anyone implemented BGP ORR?** I found IOS XR and Junos implementations, and [someone has been promising to implement it in FRR for a year](https://github.com/FRRouting/frr/issues/2236), so it might happen in not-too-distant future. 

**Is it useful?** In theory, you could use it whenever a BGP RR is far enough outside of the optimal ingress-to-egress forwarding path[^ORR-WP]. In practice, I prefer structured network designs that can work without extra magic. 

[^ORR-WP]: Cisco has also published a [pretty good technical note](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/212881-border-gateway-protocol-bgp-optimal-ro.html) explaining BGP ORR details and the alternatives (in-path BGP RR).

### Further Reading

You might want to explore what these RFCs have to say on the subject:

* [Border Gateway Protocol (BGP) Persistent Route Oscillation Condition](https://datatracker.ietf.org/doc/html/rfc3345) (RFC  3345)
* [Distribution of Diverse BGP Paths](https://datatracker.ietf.org/doc/html/rfc6774) (RFC 6774)
* [BGP Wedgies](https://datatracker.ietf.org/doc/html/rfc4264) (RFC 4264)

I also covered the need for *BGP AddPath* in the *[BGP Multipath Basics](https://my.ipspace.net/bin/get/Net101/AR4.3%20-%20BGP%20Multipath%20Basics.mp4?doccode=Net101)* video (part of *[Advanced Routing Protocol Topics](https://my.ipspace.net/bin/list?id=Net101#ADV_ROUTING)* section of _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar).
