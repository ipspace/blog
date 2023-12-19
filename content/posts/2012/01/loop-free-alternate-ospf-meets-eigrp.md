---
date: 2012-01-26 06:18:00+01:00
eigrp_tag: deploy
ospf_tag: mp
series_title: OSPF Meets EIGRP
tags:
- IS-IS
- OSPF
- EIGRP
title: 'Loop-Free Alternate: OSPF Meets EIGRP'
url: /2012/01/loop-free-alternate-ospf-meets-eigrp.html
---
Assume we have a simple triangular network:

{{<figure src="/2012/01/s400-LFA_Topology.png">}}

Now imagine the A-to-C link fails. How will OSPF react to the link failure as compared to EIGRP? Which one will converge faster? Try to answer the questions before pressing the *Read more* link ;)
<!--more-->
### EIGRP: Feasible Successors

EIGRP tries to use *feasible successors* to speed up the convergence process. Whenever B reports its distance to X to A, A compares B's *reported distance* to its current *feasibility distance*. Lower *reported distance* means that B doesn't use A to get to X (A is not B\'s successor). B is also not A\'s successor for X (that's C as long as the A-to-C link is operational), but it's a *feasible successor*. Using B to get traffic to X will not result in a routing loop.

A *feasible successor* is evaluated for individual destinations. From A's perspective, B is a feasible successor for X and C is a feasible successor for Y.

Faced with A-to-C link loss, A can switch immediately to the *feasible successor* (B) for destination X. Convergence is immediate.

{{<figure src="/2012/01/s400-LFA_Failure.png" caption="EIGRP convergence after a link failure">}}

### OSPF: Let's Make Sure We're in Sync

OSPF is way more lackadaisical:

-   It changes the LSAs affected by the updates and floods them unless there's been a recent topology change, in which case it goes and sits quietly in a corner until the **timers throttle lsa** *hold-interval* expires.
-   It waits a bit more, silently lamenting its misery, until the **timers throttle spf** *spf-start* timer expires.
-   It runs SPF algorithm, computes the new OSPF shortest-path tree, and copies the results in the IP routing table.

Total convergence time: 5+ seconds (unless you've done some serious tweaking).

### Loop-Free Alternate: Feasible Successor for OSPF

There's no reason OSPF couldn't have reacted faster -- every single router knows the whole topology of all attached areas and can thus easily calculate which of its neighbors could be feasible successors. That's exactly what LFA is doing:

-   OSPF (or IS-IS) routing process runs SPF, computes its own best paths, and installs them in the IP routing table (RIB).
-   After the network has converged, OSPF runs SPF algorithm from the perspective of its neighbors. If a neighbor's SPF tree doesn't use current router as the next hop for a specific destination, it's safe to use that neighbor as a feasible successor.
-   The feasible successor information calculated by OSPF is downloaded in RIB and FIB, where it can be used immediately after the link failure.

### Can I use it?

Loop Free Alternate Fast Reroute is available in Cisco IOS ([OSPF](http://www.cisco.com/en/US/docs/ios-xml/ios/iproute_ospf/configuration/xe-3s/iro-lfa-frr-xe.html), [IS-IS](http://www.cisco.com/en/US/docs/ios/iproute_isis/configuration/guide/irs_ipv4_lfafrr.pdf)), Junos ([OSPF](http://www.juniper.net/techpubs/en_US/junos10.0/information-products/topic-collections/config-guide-routing/ospf-loop-free-alternate-routes-overview.html), [IS-IS](https://www.juniper.net/techpubs/software/junos/junos95/swconfig-routing/jd0e44501.html)), IOS XR  ([OSPF](http://www.cisco.com/en/US/docs/routers/crs/software/crs_r4.2/routing/configuration/guide/b_routing_cg42crs_chapter_0100.html), [IS-IS](http://www.cisco.com/en/US/docs/routers/crs/software/crs_r4.2/routing/configuration/guide/b_routing_cg42crs_chapter_011.html)) and other network operating systems.


### More information

- [Fast Failover](https://my.ipspace.net/bin/list?id=Net101#FRR) section in [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar
- [Basic Specification for IP Fast Reroute: Loop-Free Alternates](http://tools.ietf.org/html/rfc5286) (RFC 5286)
- [Understanding and Deploying Loop-Free Alternate Feature](http://kb.juniper.net/library/CUSTOMERSERVICE/GLOBAL_JTAC/technotes/8010056-001-EN.pdf) (Junos Implementation Guide)
- [Nice introductory article by Tony Brown](http://etherealmind.com/loop-free-alternate-routes/)
- [IP Fast Reroute Applicability](http://www.data.proidea.org.pl/euronog/1edycja/materialy/prezentacje/Pierre_Francois_IP_Fast_Reroute_Applicability.pdf) -- EuroNOG presentation by Pierre Francois (with lots and lots of details and topology analysis).

