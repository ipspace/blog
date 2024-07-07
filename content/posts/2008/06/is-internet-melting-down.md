---
date: 2008-06-29 07:28:00+02:00
tags:
- BGP
- IP routing
title: Is Internet Melting Down?
url: /2008/06/is-internet-melting-down/
---
A while ago I've read a [post about the potential Internet meltdown by Michael Morris](http://www.networkworld.com/community/node/27191). He provided an amazingly accurate analysis of the facts ... and ended with a wrong conclusion. To understand the whole issue, please [thoroughly read his text in its entirety](http://www.networkworld.com/community/node/27191) before proceeding.

Back? OK. As I said, his analysis was great, but the conclusions were wrong. Regardless of whether we use IPv4 (and advertise smaller and smaller prefixes) or IPv6, the problem is the same: everyone wants to have chunks of non-aggregatable provider-independent public address space (so you can freely move between Service Providers) and everyone advertises these PI prefixes to multiple service providers (because multihoming is so cheap these days). Even networks that are not multihomed today use their own PI address space and private AS numbers to connect to a single ISP, so they could get multi-homed in a second if they feel like it.

The growth of the Internet routing tables thus has nothing to do with the prefix sizes and version of IP, but with the requirements of the end-customers to have immediate capability to switch service providers at will. As long as this trend persists (and I cannot see it stopping, as Internet is considered a commodity these days), the routing tables will grow, regardless of whether we use IPv4 or IPv6 or CLNS or something not invented yet.

For more details watch ‌[*Upcoming Internet Challenges*](https://www.ipspace.net/Upcoming_Internet_Challenges) and *[Surviving the Internet Default Free Zone](https://www.ipspace.net/Surviving_the_Internet_Default_Free_Zone)* webinars.

