---
date: 2013-03-14 07:03:00+01:00
ospf_tag: details
tags:
- OSPF
title: Inter-Process OSPF Route Selection Rules
url: /2013/03/inter-process-ospf-route-selection-rules.html
---
[Nicolas Michel](https://plus.google.com/103779506789076415201/posts) left an interesting comment (quoting [Cisco's documentation](http://www.cisco.com/en/US/tech/tk365/technologies_white_paper09186a0080531fd2.shtml#routepref)) on my [OSPF Route Selection Rules](/2008/01/e1-and-e2-routes-in-ospf.html) blog post:

> ... The OSPF route selection rule is that intra-area routes are preferred over inter-area routes, which are preferred over external routes. However, this rule should apply to routes learned via the same process ...

Let's see what's going on behind the scenes.
<!--more-->
As you know, OSPF goes through the following process to select the best (candidate) routes:

-   Run intra-area SPF for every area to which the router is connected;
-   Run inter-area and external route selection process (actually a distance-vector calculation, because only the costs are compared);
-   Offer the best routes (according to [OSPF route selection rules as implemented by Cisco IOS](/2008/01/e1-and-e2-routes-in-ospf.html)) to the routing table.

While the information about OSPF cost and route type gets copied to the routing table (but not the forwarding table -- the [RIBs and FIBs](/2010/09/ribs-and-fibs.html) blog post explains the difference) or you wouldn't be able to see it with **show ip route** command, that information is not used when the router compares routes arriving into the IP routing table from multiple sources (routing protocols, static routes...).

If multiple routing protocols offer the same IP prefix (with potentially different next hops) to the IP routing table, *the entry with the lowest administrative distance* *(AD)* *always wins*, regardless of its other attributes.

What happens when two entries have the same AD (for example, they're coming from two OSPF routing protocols using default AD values) is under-documented. Based on [information from a Cisco Live presentation](http://d2zmdbbm9feqrf.cloudfront.net/2010/usa/pdf/BRKARC-2350.pdf), the routing protocol that provided the currently-installed route decides what to do with the new route. It seems EIGRP yields to an EIGRP route with better metric, and OSPF prefers older (more stable) route regardless of its OSPF cost.

You might easily reverse-engineer the behavior of your current IOS release, but there's no guarantee the behavior won't change in the future. In short -- *don't rely on whatever happens when two routing protocols have the same AD value*.

Each routing protocol used on your router must have a different set of AD values if you want to have deterministic behavior (assuming they try to insert the same information into the routing table -- you don't have to worry if there's no overlap between the routing protocols). Fortunately, Cisco IOS supports different AD values for different OSPF route types since IOS release 11.1(14). You can set values for intra-area, inter-area and external routes with **distance ospf** router configuration command (for historical reasons, the Cisco IOS uses 110 as the default value for all OSPF route types).

### How To Use It?

If you want to prefer intra-area OSPF routes from any OSPF routing process over inter-area or external OSPF routes from any other routing process, use something like **distance ospf intra-area 110 inter-area 112 external 114** (ensuring that OSPF routes remain more preferred than IS-IS, RIP or external EIGRP routes) -- but keep in mind that it's somewhat unpredictable what happens if two OSPF routing protocols have the same intra-area route; Cisco IOS most probably won't use OSPF cost as the tie-breaker.

If you want to prefer one OSPF routing protocol over another, use **distance 110** in one of them (applies the same distance to all route types) and **distance 112** (or higher) in the other.

Finally, if you want to have fine-grained control, preferring OSPF intra-area routes over inter-area routes across OSPF routing protocols, while at the same time preferring one OSPF routing process over another, use **distance ospf intra-area 110 inter-area 112 external 114** in one of them and **distance ospf intra-area 111 inter-area 113 external 115** in the other (I'm assuming you won't run multiple OSPF processes *and* IS-IS at the same time -- if you do, adjust the values accordingly).
