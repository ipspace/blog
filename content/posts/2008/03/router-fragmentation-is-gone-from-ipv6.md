---
date: 2008-03-05 07:53:00.001000+01:00
tags:
- IPv6
title: Router Fragmentation Is Gone from IPv6
url: /2008/03/router-fragmentation-is-gone-from-ipv6/
---
In response to my [*Never-Ending Story of IP Fragmentation*](/kb/Internet/PMTUD/), Stojanco Cavdarov made an interesting observation: routers are not allowed to fragment IPv6 packets, they have to respond back with ICMP unreachable (effectively, routers behave as if IPv6 packets would have an implicit *don\'t fragment* bit).

To make life easier for non-TCP IPv6 applications (TCP is supposed to use Path MTU Discovery), the minimum IPv6 packet size that has to be supported on all links was increased to 1280 bytes (which, incidentally, fits very nicely into GRE+IPSec envelope transported across links with 1500-byte MTU).
