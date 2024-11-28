---
title: "IPv6 Support for Multiple Routers and Multiple Interfaces"
date: 2024-11-28 11:57:00+0100
tags: [ IPv6 ]
---
Fernando Gont published an *Individual Internet Draft* (meaning it hasn't been adopted by any IETF WG yet) describing the [Problem Statement about IPv6 Support for Multiple Routers and Multiple Interfaces](https://datatracker.ietf.org/doc/html/draft-gont-v6ops-multi-ipv6). It's so nice to see someone finally acknowledging the full scope of the problem and describing it succinctly. However, I cannot help but point out that:

* I was [ranting about that problem in 2009](https://blog.ipspace.net/2009/05/lack-of-ipv6-multihoming-elephant-in/) (15 years ago) and did a [summary of older rants in 2015](https://blog.ipspace.net/2015/11/theres-problem-with-ipv6-multihoming/).
* It was evident to everyone but the religious zealots that the only solution we have at the moment is either [NAT](https://blog.ipspace.net/2011/12/we-just-might-need-nat66/) (because [stuff simply does not work otherwise](https://blog.ipspace.net/2011/12/ipv6-multihoming-without-nat-problem/)) or host-based solutions that never got implemented (apart from a few rare cases of [multipath TCP](https://blog.ipspace.net/2019/03/multipath-tcp-on-software-gone-wild/)).

Anyway, Fernando wraps up his draft with:
<!--more-->
> As a result, this document concludes that protocol improvements that accommodate these deployment scenarios are warranted.

I wouldn't be surprised if no IPv6-related working group adopts the draft -- the number of vocal people with severe cognitive dissonance firmly believing in their interpretation of IPv6 is simply too large. You might enjoy the comments to my old rants saying, "*we solved the problem with PI prefixes*" ([really?](https://blog.ipspace.net/2018/04/why-cant-we-all-use-provider/)). There's also the never-ending "*[we don't need no DHCPv6](https://blog.ipspace.net/2021/10/dhcpv6-matters/)*" saga that [hurts everyone](https://blog.ipspace.net/2024/04/ipv6-slaac-unintended-consequences/) trying to deploy certain IPv6 mobile devices into somewhat-controlled enterprise IPv6 networks.

No wonder we're still [yammering about the adoption ratio](https://blog.apnic.net/2024/10/22/the-ipv6-transition/) of a [29-year-old protocol](https://datatracker.ietf.org/doc/html/rfc1883).
