---
date: 2012-01-03 06:32:00+01:00
tags:
- IPv6
- workshop
title: Are Provider-Independent IPv6 Prefixes Really Global?
url: /2012/01/are-provider-independent-ipv6-prefixes/
---
Aleksej sent me an intriguing question: "*Can the /48 PI block that a global company is assigned be attached to any region, or it is region-specific?*", or, more specifically:

> Imagine a company with major DC with public services in EMEA. Centralized internet break-out in Europe fails and this DC must be reachable from Asia or America - but with the same IPv6 address? That would require Asia or America\'s ISPs to accept injection of this same subnet in their region. Do they do that?

In theory, the answer is *yes*. In practice, some global organizations are hedging their bets.
<!--more-->
A PI IPv6 prefix should be just that -- a range of globally unique IPv6 address space that could be advertised from anywhere and should be accepted (and routed to) everywhere. A minimum globally routable IPv6 prefix length is a /48 and that's how much PI address space you get if you don't ask for more.

Hint: If you have more than one location, you need more than a /48. If you have more than a few locations, always ask for ~~at least /32~~ the largest prefix you can get (see the comment by nosx).

Today, a PI IPv6 prefix is (usually) globally routable (but nobody could guarantee you that). Even more, PA prefixes not longer than /48 *should* be globally routable, but they're not -- at least the [latest measurements from RIPE labs](https://labs.ripe.net/Members/dbayer/visibility-of-prefix-lengths) indicate some providers still use PA-specific route advertisement filters.

However, once mid-size organizations start migrating to IPv6, they'll [start asking for PI address space](http://etherealmind.com/importance-provider-independent-ipv6-addresses/) (because it's too much hassle to renumber the internal network \... and because everyone is telling them NAT stinks). Likewise, at least some customers [using poor man's multihoming](/2009/05/small-site-multihoming-tutorial/) will start applying for PI prefixes (unless we admit [we need NPT66](/2011/12/we-just-might-need-nat66/) and someone actually implements it). End result: explosion in global BGP tables and forwarding tables (unless LISP gets implemented everywhere), that just might force some ISPs to implement geo-aggregation or region-based filters.

**Summary:** if you're a global organization with data centers spread across multiple RIR regions, apply for PI address space in every region where you need mission-critical connectivity.

### More Information

IPv6 addressing is just part of the bigger picture (you\'ll find a good overview of what\'s needed in the *[Enterprise IPv6 - the first steps](https://www.ipspace.net/IPv6E101)* webinar). If you need more information on IPv6 access network design and deployment, check out my [*Building Large IPv6 Access Networks*](https://www.ipspace.net/IPv6SPCore) webinar.
