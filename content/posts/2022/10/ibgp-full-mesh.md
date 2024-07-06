---
title: "Why Do We Need IBGP Full Mesh?"
date: 2022-10-19 07:45:00
tags: [ BGP ]
---
Here's another question from the [excellent list posted by Daniel Dib on Twitter](https://twitter.com/danieldibswe/status/1579674196833366017):

> BGP Split Horizon rule says "_Don't advertise IBGP-learned routes to another IBGP peer._" The purpose is to avoid loops because it's assumed that all of IBGP peers will be on full mesh connectivity. What is the reason the BGP protocol designers made this assumption?

Time for another history lesson. BGP was designed in late 1980s ([RFC 1105](https://datatracker.ietf.org/doc/html/rfc1105) was published in 1989) as a replacement for the original Exterior Gateway Protocol (EGP). In those days, the original hub-and-spoke Internet topology with [NSFNET core](https://en.wikipedia.org/wiki/National_Science_Foundation_Network) was gradually replaced with a mesh of interconnections, and EGP couldn't cope with that.
<!--more-->
At that time, [Yakov Rekhter](https://en.wikipedia.org/wiki/Yakov_Rekhter) and [Kirk Lougheed](https://www.linkedin.com/in/kirk-lougheed-7556748/) designed the famous three-napkins protocol that became BGP version 1 (RFC 1105). Its goal was to replace EGP and all it needed to get that job done was to advertise networks with AS paths. There were no other attributes in BGP version 1 (and thus absolutely no way to detect intra-AS routing loops).

BGP was designed in days when networking engineers still focused on solving point challenges instead of trying to boil the ocean, and it was clearly understood that while routing within an autonomous system was needed, it was not what BGP was trying to do. From RFC 1105:

> If a particular AS has more than one BGP gateway, then all these gateways should have a consistent view of routing. A consistent view of the interior routes of the autonomous system is provided by the intra-AS routing protocol. A consistent view of the routes exterior to the AS may be provided in a variety of ways.

One of the ways to provide a consistent view of exterior routes was to redistribute exterior routes into IGP. Early BGP implementations required BGP prefixes to be present in an IGP, or they wouldn't advertise them to other autonomous systems -- the famous `bgp synchronization` nerd knob that persisted in Cisco IOS (and CCIE lab exams) for decades.

Even more, when redistributing a BGP route into OSPF, the redistributing router copies the first AS in the AS-path into the OSPF tag together with a few extra bits that help the egress router recreate a short AS-path from OSPF tag when redistributing OSPF back into BGP[^IOSF] -- in those days, if you were a regional ISP, you didn't need IBGP at all.

[^IOSF]: See [RFC 1403](https://datatracker.ietf.org/doc/html/rfc1403) and [OSPF-to-BGP redistribution](/2009/05/ios-fossils-ospf-to-bgp-redistribution.html) for details.

The designers of BGP version 1 understood that some networks might prefer to exchange BGP information directly between AS-edge routers while still [redistributing BGP into IGP to get external routes into forwarding tables of intermediate devices](/2022/10/ospf-external-routes.html). They could have made the protocol more complex (and harder to implement) but decided to go down the long-forgotten path of "_we'll keep protocols simple and assume that the engineers using them know what they're doing_." Quoting RFC 1105 again:

> One way is to use the BGP protocol to exchange routing information between the BGP gateways within a single AS. In this case, in order to maintain consist routing information, these gateways MUST have direct BGP sessions with each other (the BGP sessions should form a complete graph).

BGP didn't remain a simple protocol solving a simple problem for long:

* Version 2 ([RFC 1163](https://datatracker.ietf.org/doc/html/rfc1163), June 1990) added (well-known and optional) path attributes and defined ORIGIN, AS_PATH, NEXT_HOP, and INTER-AS (now known as MED) attributes.
* Version 3 ([RFC 1267](https://datatracker.ietf.org/doc/html/rfc1267), October 1991) added hold timers, notifications, and formal finite-state machine
* Version 4 (RFC 1771, March 1995) added local preference, CIDR support, and route aggregation.

At approximately the same time, IBGP full mesh became a scalability bottleneck in large service provider networks, resulting in route reflectors ([RFC 1966](https://datatracker.ietf.org/doc/html/rfc1966), June 1996) and confederations ([RFC 1965](https://datatracker.ietf.org/doc/html/rfc1965), June 1996). I still remember getting a new Cisco software release, looking at BGP route reflectors, saying "_now, that's a cool new thing_," and rushing to burn the software into EPROMs to test it[^NR].

[^NR]: That last bit is a "[we were living in a shoebox](https://www.youtube.com/watch?v=ue7wM0QC5LE)" fairy tale. BGP route reflectors were implemented in software release 11.1, and most Cisco routers had programmable Flash EPROMs at that time. You could also boot new software images via TFTP if you had enough memory in your router -- IIRC, the early Cisco 2500-series routers shipped with 2MB of RAM.
