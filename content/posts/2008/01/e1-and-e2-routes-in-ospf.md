---
date: 2011-04-16 07:32:00+02:00
ospf_tag: details
tags:
- OSPF
title: OSPF Route Selection Rules
url: /2008/01/e1-and-e2-routes-in-ospf/
---
OSPF implementation in Cisco IOS deviates slightly from OSPF/NSSA standards ([RFC 2328](http://tools.ietf.org/html/rfc2328) and [RFC 3101](http://tools.ietf.org/html/rfc3101)). These are the OSPF route selection rules as implemented by Cisco IOS release 12.2(33)SRE1 (all recent releases probably behave identically):

<!--more-->
-   Intra-area routes are preferred over inter-area or external routes *regardless of their cost*; see [Section 16.2 paragraph (6) of the OSPF RFC](http://tools.ietf.org/html/rfc2328#page-170).
-   Inter-area routes are preferred over external routes; see [Section 16.2 paragraph (5) of the OSPF RFC](http://tools.ietf.org/html/rfc2328#page-169).
-   E1 routes are preferred over E2 routes; see [Section 16.4 paragraph (6) of the OSPF RFC](http://tools.ietf.org/html/rfc2328#page-174).
-   External routes received from an intra-area ASBR should be preferred over external routes received from ASBRs in other areas. [Cisco IOS ignores this rule](/2008/02/common-sense-prevails-over-rfc-2328/) even after configuring **no compatible rfc1583** ([Section 16.4.1](http://tools.ietf.org/html/rfc2328#page-175) of the OSPF RFC)
-   When comparing E1 routes, the route metric is the external cost added to the internal cost; see [Section 16.4 paragraph (6.d) of the OSPF RFC](http://tools.ietf.org/html/rfc2328#page-175).
-   The internal cost of an E1/E2 route is the cost between the current router and the forwarding address specified in the Type-5 LSA (or originating ASBR if the forwarding address is set to 0.0.0.0); see [Section 16.4 paragraph (3) of the OSPF RFC](http://tools.ietf.org/html/rfc2328#page-173).
-   When comparing E2 routes, only the external costs are compared; see [Section 16.4 paragraph (6.b) of the OSPF RFC](http://tools.ietf.org/html/rfc2328#page-174).
-   If multiple E2 routes have the same external cost, the internal cost (as above) is compared; see [Section 16.4 paragraph (6.d) of the OSPF RFC](http://tools.ietf.org/html/rfc2328#page-175).
-   NSSA (type-7 LSA) routes should be preferred over external (type-5 LSA) routes ([paragraphs (6.c) and (6.e) of Section 2.5](http://tools.ietf.org/html/rfc3101#page-13) of RFC 3101). Cisco IOS prefers external routes over NSSA routes; even if they have the same cost as the external routes (and **maximum-path** is configured), NSSA routes are not entered in the IP routing table.
-   It seems the final tie-breaker is the LSA stability (or its position in the topology database/SPF tree?). For example, if the router cannot enter all equal-cost external routes into the IP routing table (based on **maximum-path** value), it appears to select the more stable ones (described by LSAs that have been longer in the OSPF topology database).

### Revision History

2008-01-17
: The original version of this post

2011-03-30
: Updated and renamed the blog post after a lengthy (and very productive) discussion with one of my readers.

2011-04-16
: Fixed the final tie-breaker part.

2016-02-19
: Fixed a typo - early OSPF RFC was RFC 1583, not RFC 1683
