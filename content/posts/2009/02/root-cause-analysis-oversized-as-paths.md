---
date: 2009-02-20 15:09:00.001000+01:00
tags:
- BGP
title: 'Root Cause Analysis: Oversized AS Paths'
url: /2009/02/root-cause-analysis-oversized-as-paths/
---
The "BGP experiment" a small European ISP performed in February 2009 has generated quite a splash: [Cisco has discovered a new BGP bug](http://mailman.nanog.org/pipermail/nanog/2009-February/008195.html) that can be triggered only if you have a long enough AS-path and do outbound AS-path prepending (and a few of us learned more BGP intricacies we never wanted to know), lots of people have (hopefully) discovered the [importance of the **bgp maxas-limit** configuration command](/2009/02/protect-your-network-with-bgp-maxas/) and at least [some ISPs](http://mailman.nanog.org/pipermail/nanog/2009-February/008213.html) have implemented [inbound prepending filters](/2008/02/as-path-based-filter-of-customer-bgp/) that I wrote about almost a year ago. However, most of us thought that the original problem arose due to inexperienced operators of a leaf AS.

Mikael Abrahamsson was the first to notice that the [number of prepends matches the low-order 8 bits of the offending AS number](http://mailman.nanog.org/pipermail/nanog/2009-February/008202.html). Further contributors to NANOG mailing list confirmed that two autonomous systems with very long prepends are using BGP routers from [Mikrotik](http://www.mikrotik.com/software.html). You configure those boxes with commands that have syntax deceptively close to Cisco\'s, but [expect the number of AS numbers to prepend, not the AS-path](http://www.mikrotik.com/testdocs/ros/2.9/routing/filter.php). Obviously no range checking is done on the configuration parameter and the high-order 8 bits are ignored.

So it looks like the incident started with a box that accepts invalid configuration parameter used in an AS with very high value in low-order 8 bits (quite improbable, but obviously not impossible). Numerous ISPs that did not limit the BGP updates they were propagating and an IOS bug did the rest.
