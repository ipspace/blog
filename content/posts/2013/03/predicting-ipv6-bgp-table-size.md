---
date: 2013-03-05 07:21:00+01:00
tags:
- IPv6
- Internet
- BGP
title: Predicting the IPv6 BGP Table Size
url: /2013/03/predicting-ipv6-bgp-table-size/
---
One of my readers sent me an interesting question:

> Are you aware of any studies looking at the effectiveness of IPv6 address allocation policies? I\'m specifically interested in the affects of allocation policy on RIB/FIB sizes.

Well, we haven't solved a single BGP-inflating problem with IPv6, so expect the IPv6 BGP table to be similar to IPv4 BGP table once IPv6 is widely deployed.
<!--more-->
There are three main reasons the global Internet table contains over 450K entries:

-   Ignorance and sloppiness. The [CIDR report](http://www.cidr-report.org/as2.0/#Gains) claims we could aggregate exiting 450K entries into just over 250K entries ... but why would the top offenders do that if it costs them nothing to advertise their prefixes (and who cares that everyone else is paying stupidity tax by buying more high-speed RAM).
-   Multihoming. [Session-level multihoming](/2009/08/what-went-wrong-tcpip-lacks-session/) was [never implemented](/2009/05/lack-of-ipv6-multihoming-elephant-in/) in the TCP stack (LISP or MP-TCP could help assuming they ever get deployed).
-   Traffic engineering. If you're multihomed and want to control the use of your uplinks for inbound traffic, you [have to advertise smaller chunks of your address space](/2012/10/is-layer-3-dci-safe/) to individual ISPs.

IPv6 doesn't change a thing (widespread deployment of LISP might), so even if all the prefix hogs start advertising optimized IPv6 prefixes, the absolute minimum we need to describe the current Internet topology (and routing policies expressed by its participants) is around 250K routes.

Things might actually get worse -- we might see more prefixes in the IPv6 table because a lot of organizations that used PA (example: a /24 allocated by their ISP) and NAT44 today [might consider PI address space](/2011/02/ipv6-provider-independent-addresses/) to avoid the royal pain of renumbering.

Finally, there's the noble and worthy push toward NAT-less IPv6 world. That sounds great, until you realize small organizations that use NAT-based IPv4 multihoming today might [opt for provider independent IPv6 prefix](/2010/12/small-site-multihoming-in-ipv6-mission/) (which costs around 50 EUR a year in RIPEland) ... or [use NPT66](/2011/12/we-just-might-need-nat66/).

Does the IPv6 BGP table explosion matter? You might believe in the universal safety of Moore's law, but let me point out that Cisco 7600 with RSP 720-3CXL that you bought yesterday (and won't be able to depreciate for the next 4-5 years) supports up to 1M IPv4 routes *or* 512K IPv6 routes (or a mix of both) ... and we're pretty close to that limit already assuming IPv6 prefixes would match maximally-aggregated IPv4 prefix.

ASR 1000 with maximum memory fares a bit better (1M IPv4 routes *or* 1M IPv6 routes), and MX-80 seems to be in the same range (although I couldn't find the exact figures anywhere in the data sheets). It might be [time to leave the default-free zone](http://www.ipspace.net/BGP_Convergence_Optimization) if you're not a Tier-1/2 ISP (or maybe one of the vendors will [actually implement virtual aggregation](/2010/09/virtual-aggregation-quick-fix-for/)).

### More IPv6 Goodies

-   Introduction to IPv6 for [Enterprise](http://www.ipspace.net/Enterprise_IPv6_-_the_First_Steps) and [Service Provider](http://www.ipspace.net/Service_Provider_IPv6_Introduction) engineers;
-   [IPv6 core and access network design guidelines and configuration examples](http://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks);
-   [IPv6 security](http://www.ipspace.net/IPv6_security);
-   [IPv6 transition mechanisms](http://www.ipspace.net/IPv6_Transition_Mechanisms);
-   [More IPv6 presentations](http://www.ipspace.net/Presentations#IPv6).
