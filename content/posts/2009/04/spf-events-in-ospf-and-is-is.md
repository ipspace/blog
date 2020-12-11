---
date: 2009-04-27 06:43:00+02:00
tags:
- IS-IS
- OSPF
title: SPF Events in OSPF and IS-IS
url: /2009/04/spf-events-in-ospf-and-is-is.html
needs_fix: true
---
The Shortest Path First (SPF) algorithm used by all (read: both) popular link-state routing protocols should be well-known to all network engineers, but the fact that the IP routing table gets populated by a distance-vector-like second phase of the algorithm is oft forgotten.

{{<note info>}}I wrote about the distance vector aspects of OSPF   in 2008. You'll find the article somewhere in [this list](https://www.ipspace.net/kb/Internet/){{</note>}} 

The second phase of the link state route selection algorithm is called *Partial SPF* in OSPF and *Partial Route Calculation (PRC)* in IS-IS. Obviously it's beneficial if the router can react to a change in the network topology by running PRC, not the full SPF, and there are [significant differences in the way OSPF and IS-IS respond to various topology change events](http://wiki.nil.com/SPF_events_in_OSPF_and_IS-IS). The differences are not architectural; you could make OSPF behave as well as IS-IS. They just prove that the old wisdom is still true: very large IOS-based networks use IS-IS because it's better implemented than OSPF.

{{<jump>}}[Keep reading](http://wiki.nil.com/SPF_events_in_OSPF_and_IS-IS){{</jump>}}
