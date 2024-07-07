---
date: 2011-08-29 06:43:00+02:00
lastmod: 2022-05-05 07:47:00
series:
- bgp-essentials
tags:
- design
- BGP
title: BGP Next Hop Processing
url: /2011/08/bgp-next-hop-processing/
---
Following my [*IBGP or EBGP in an enterprise network*](/2011/08/ibgp-or-ebgp-in-enterprise-network/) post a few people have asked for a more graphical explanation of IBGP/EBGP differences. Apart from the obvious ones (AS path does not change inside an AS) and more arcane ones (local preference is only propagated on IBGP sessions, MED of an EBGP route is not propagated to other EBGP neighbors), the most important difference between IBGP and EBGP is BGP next hop processing.
<!--more-->
It's best to explain BGP next hop processing through a set of examples; mine will be based on the following small network:

{{<figure src="/2011/08/s1600-BGP_Next_Hop_Sample_Network.png" caption="Sample network diagram">}}

And since this post became way too long, here's a rough table of content:

-   [Originating BGP routes](#bgp-next-hop-of-a-locally-originated-route)
-   [Route reflectors](#route-reflector-cannot-change-bgp-next-hop-of-reflected-routes)
-   [EBGP rules](#bgp-next-hop-is-set-to-routers-own-address-on-ebgp-sessions) and [forwarding optimization](#next-hop-optimization-on-ebgp-sessions)
-   [IBGP rules](#bgp-next-hop-is-not-changed-on-ibgp-sessions) and [design guidelines](#ibgp-next-hop-design-rules)

### BGP Next Hop of a Locally Originated Route

When a router originates a BGP route configured with a **network** router configuration command or through route redistribution (**redistribute** router configuration command), it sets the BGP next hop to the IGP next hop (the same value you'd find in the IP routing table). BGP next hop is set to 0.0.0.0 for routes with unknown next hops -- connected interfaces, static routes to *null 0* or summary routes configured with **aggregate-address** router configuration command.

You can set the BGP next hop of a locally originated BGP route to any value you like with a **route-map** applied to **network, redistribute** or **aggregate-address** router configuration command. But remember: just because you could doesn't mean that you should.

#### Changing Missing Next Hop in BGP Updates

When a BGP route with missing next hop (next-hop = 0.0.0.0) is sent to BGP neighbors, the BGP next hop is set to the source IP address of the BGP session.

**Example**: PE-A originates BGP prefix 10.0.1.0/24 based on a static route to *null 0*. When it sends this BGP prefix to X1 and X2, BGP next hop is set to 192.168.0.3. BGP next hop in update sent to RR is 10.0.0.1.

If you use common BGP design recipes (IBGP sessions configured between loopback addresses and EBGP sessions configured across directly-connected subnets), and the BGP next hop is unknown, the BGP router advertises its loopback address as BGP next hop on IBGP sessions, making BGP table resilient to topology changes inside your network.

For routes with known next hops, the router applies standard IBGP/EBGP next hop processing rules (see below) when sending the BGP updates to its neighbors.

### Route Reflector Cannot Change BGP Next Hop of Reflected Routes

Large autonomous systems use BGP route reflectors. [With a few exceptions](/2014/04/changes-in-ibgp-next-hop-processing/), BGP route reflectors [cannot change any attribute of the routes they reflect](/2008/08/bgp-route-reflector-details/). The BGP next hop advertised by an edge router is thus propagated unchanged across the whole AS.

**Exceptions**:

* Cisco IOS allows setting next-hop to **self** on reflected routes with the **neighbor next-hop-self all** configuration command. See [Changes in IBGP Next Hop Processing](/2014/04/changes-in-ibgp-next-hop-processing/) blog post for more details.
* You can change BGP next hop on a route reflector with an *inbound* route-map. Don't do this outside of a CCIE lab.

**Example**: Prefix 10.0.1.0/24 originated by PE-A is propagated by RR to PE-B. BGP next hop is still 10.0.0.1.

### BGP Next Hop Is Set to Router's Own Address on EBGP Sessions

The internal details of an AS should not influence packet forwarding between autonomous systems (and we cannot assume that a router external to our AS would know our internal details). The BGP next hop is thus changed to router's own IP address (source address of the EBGP session) in outgoing EBGP updates.

**Example**: When PE-B sends BGP prefix 10.0.1.0/24 (with next-hop 10.0.0.1) to X3, it sets BGP next hop to 192.168.2.1.

{{<note warn>}}You can always set the BGP next hop to any value you like with an outbound route-map. Risky (because it's hard to check whether the next hop you advertise is actually reachable), but ensures pretty decent good job security.{{</note>}}

### Next Hop Optimization on EBGP sessions

EBGP next hop is not changed if the BGP next hop in the BGP table belongs to the same IP subnet as the EBGP neighbor to which the update is sent. This rule ensures optimum packet forwarding in partially meshed EBGP deployments (example: internet exchange points).

**Example**: X1 sends BGP prefix 172.16.0.0/16 to PE-A. Next hop is set to the source address of the EBGP session between X1 and PE-A (192.168.0.1). When PE-A propagates the BGP prefix to X2, it does not change the next hop (X1, PE-A and X2 are in the same subnet).

You can disable the EBGP next hop optimization with **neighbor next-hop-self** router configuration command. This command is particularly useful in partially meshed multi-access networks (Frame Relay, ATM, Phase 1 DMVPN, private VLANs), see [*Using BGP in Phase 1 DMVPN Networks*](/2011/01/using-bgp-in-phase-1-dmvpn-network/) post for more details.

**Example**: Assuming **neighbor 192.168.0.2 next-hop-self** is configured on PE-A, the BGP next hop of all BGP routes sent to X2 from PE-A will be 192.168.0.3 and the traffic between X1 and X2 will flow through PE-A.

### BGP Next Hop Is not Changed on IBGP Sessions

All routers within an autonomous system are assumed to be able to reach the same set of subnets (advertised through IGP). Consequently, when an AS edge router propagates external BGP prefixes to internal BGP peers, it does not change the BGP next hop.

The only exception to this rule is a router doing load balancing across multiple EBGP paths (as configured with **maximum-paths** configuration command). In that case, the BGP next hop is set to router\'s IP address on IBGP updates so the IBGP peers send the traffic to the originating router which can then do EBGP load balancing (added on 2019-09-19 based on input from Denis).

**Example**: X1 sends BGP prefix 172.16.0.0/16 with next hop 192.168.0.1 to PE-A. When PE-A propagates that prefix to RR, the BGP next hop is still 192.168.0.1. When the same prefix is reflected to PE-B, the next hop is still unchanged. PE-B therefore needs IGP path toward 192.168.0.0/24 or it cannot forward the traffic toward 172.16.0.0/16.

{{<note warn>}}You could make BGP next hops reachable via BGP paths. While it might work, don't do this at home (or in your production network).{{</note>}}

As with EBGP sessions, you can force the AS edge router to advertise its own IP address as the BGP next hop in IBGP updates with **neighbor next-hop-self** router configuration command applied to all IBGP sessions (I would usually use an [IBGP peer session and peer policy template](/2008/01/bgp-essentials-peer-session-templates/) to simplify my configuration).

**Example**: X1 sends BGP prefix 172.16.0.0/16 with next hop 192.168.0.1 to PE-A. Assuming **neighbor 10.0.0.2 next-hop-self** has been configured on PE-A, the BGP next hop of the BGP route sent to RR will be 10.0.0.1.

### IBGP Next Hop Design Rules

You can design IBGP in your autonomous system in two fundamentally different ways:

-   IBGP routes point to external BGP next hops (default behavior)
-   IGBP routes point to loopback interfaces of AS edge routers (**next-hop-self** is configured on IBGP sessions on AS edge routers).

If you don't change the BGP next hop on AS edge routers, you have to propagate external subnets with your IGP. You can either configure external subnets as passive interfaces or redistribute them into your IGP. The two methods are almost identical if you use IS-IS; OSPF is a slightly different story. [Flap of a passive OSPF interface causes full SPF run](/2009/04/spf-events-in-ospf-and-is-is/), whereas addition or removal of an external route (type-5 or type-7 LSA) results in partial SPF run. Redistribution of external subnets is thus preferred if you use OSPF.

However, it's never a good idea to allow external events (like link flaps in your access network) to [influence the stability of your core IGP](/2011/08/bgpigp-network-design-principles/). Using **next-hop-self** on AS edge routers (and changing the external next hops into edge router's loopback address) is thus almost always the preferred design.

### Summary

Saravanan posted an excellent table summarizing the BGP next hop  behavior in a comment that got thoroughly mangled. Here it is (slightly edited):

|Scenario|Typical use case|Next hop in BGP table|Next hop sent to peers|Comments|
|--|--|--|--|--
|**Locally originated** routes to both IBGP and EBGP peers|Connected interfaces or static routes with null0 next hop (blackholing)|0.0.0.0|Source address of the BGP session (source address of BGP packets sent by this BGP speaker)|Outgoing interface address if *update-source* is not used, else the value specified in update-source configuration.|
|Received routes **sent to IBGP peers**|Redistributed IGP routes, EBGP routes, or Static routes with valid/non-null next hop|Next-hop advertised by IGP or EBGP|Next-hop value from BGP table is advertised to IBGP peers.|You can override BGP next hop with **next-hop-self** or **set next-hop** (route map) configuration.|
|Received routes **sent to EBGP peers** where the EBGP peer IP address _is not in the same subnet_ as the BGP next hop|Redistributed IGP routes, IBGP routes, EBGP routes, static routes with valid/non-null next hop|Next-hop advertised by IGP, IBGP or EBGP|Source address of the EBGP session|Outgoing interface address if *update-source* is not used, otherwise the value specified in update-source configuration.|
|Received routes **sent to EBGP peers** where the EBGP peer IP address _is in the same subnet_ as the BGP next hop|Redistributed IGP routes, IBGP routes, EBGP routes, static routes with valid/non-null next hop|Next-hop advertised by IGP, IBGP or EBGP|BGP next hop is not modified -- this is called EBGP next hop optimization or third-party next hop.|Next-hop value in BGP table is advertised as-is unless you configured **next-hop-self** or used **set next-hop** in a route map.|
|Route-reflector **reflecting IBGP routes**|IBGP routes only|Next-hop advertised by IBGP|BGP next hop is not modified|While it's discouraged in BGP RFC, some implementations allow you to change next hop on reflected routes|
{.fmtTable}

### Further Reading

* [Can We Trust BGP Next Hops (Part 1)?](/2020/04/can-we-trust-bgp-next-hops-part-1/)
* [Can We Trust BGP Next Hops (Part 2)?](/2020/04/can-we-trust-bgp-next-hops-part-2/)
* [Real Life BGP Route Origination and BGP Next Hop Intricacies](/2014/04/real-life-bgp-route-origination-and-bgp/)
* [What is a BGP RIB failure](/2007/12/what-is-bgp-rib-failure/)
* [Can BGP Route Reflectors Really Generate Forwarding Loops?](/2013/10/can-bgp-route-reflectors-really/)

### Revision History

2022-05-05
: Added a summary table

