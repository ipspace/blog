---
date: 2008-07-02 07:07:00+02:00
eigrp_tag: deploy
lastmod: 2023-05-20 09:51:00
tags:
- EIGRP
- BGP
- MPLS VPN
title: Multihomed EIGRP Sites in MPLS VPN Network
url: /2008/07/multihomed-eigrp-sites-in-mpls-vpn.html
---
Deploying EIGRP as the PE-CE routing protocol in MPLS VPN networks is easy if [all sites have a single PE-CE link and there are no backdoor links between the sites](/2008/06/simple-eigrp-in-mpls-vpn-networks.html). Real life is never as simple as that; you have to cope with various (sometimes undocumented) network topologies. Even that would be manageable if the customer networks would have a clean addressing scheme that would allow good summarization (that happens once in a blue moon) or if the MPLS VPN core could announce the default route into the EIGRP sites (wishful thinking; the customer probably has one or more Internet exit points).
<!--more-->
In the end, you're left with two-way route redistribution between core MP-BGP and edge EIGRP, resulting in nightmarish scenarios (probably a good half of the blog posts of the CCIE candidates talk about redistribution horrors). Fortunately, Cisco implemented two extra features supporting EIGRP-to-MP-BGP redistribution: BGP cost community and BGP Site-of-Origin.

{{<ct3_rescue>}}

In most EIGRP networks migrated to MPLS VPN environments, two-way redistribution between EIGRP and core MP-BGP is required due to haphazard addressing of the original EIGRP network. Two-way redistribution can easily introduce hard-to-diagnose routing loops in topologies with multiple redistribution points between the routing protocols; for example in a topology with multiple PE-routers connected to the same customer site:

{{<figure src="/2008/07/MH_EIGRP_Diagram.png" caption="Test network diagram">}}

## Route Redistribution Issues

Two-way routing protocol redistributions can cause three common loop symptoms.

**Suboptimal route selection:** one of the redistributing routers selects suboptimal route. For example, if the PE-C2 router receives EIGRP update before the original BGP update, it installs the redistributed EIGRP route in its BGP table and ignores the incoming BGP update (redistributed EIGRP route has weight set to 32768; weight of incoming BGP update is zero).

{{<figure src="/2008/07/MH_EIGRP_Redistribute_Route_Best.png" caption="Two-way redistribution between EIGRP and BGP">}}

**Count-to-infinity loop on route removal:** once the original EIGRP route disappears, resulting in MP-BGP update, the EIGRP-to-BGP redistribution keeps the bogus route active until the EIGRP hop count component of the metric exceeds maximum value.

{{<figure src="/2008/07/MH_EIGRP_Count_To_Infinity.png">}}

{{<note info>}}You might need additional CE-routers configured with EIGRP summaries to experience this behavior.{{</note>}}

**Temporary loop on route insertion:** in Inter-AS MPLS VPN deployments, the route redistributed back into BGP from EIGRP has shorter AS-path and is thus preferred over the original route.

{{<figure src="/2008/07/MH_EIGRP_InterAS_Loop.png">}}

Cisco IOS has two features that help you prevent routing protocol loops when using EIGRP in MPLS VPN environments:

-   BGP cost community, introduced in 12.0(24)S, 12.2(18)S, 12.3(2)T and 12.4.
-   EIGRP site-of-origin (SoO) introduced in 12.0(27)S, 12.1(18)SXE, 12.3(8)T and 12.4.

## BGP Cost Community

Cisco IOS implementation of MP-BGP has been augmented with yet another extended community: the _pre-**bestpath** cost_ community defined in [draft-retana-bgp-custom-decision](https://datatracker.ietf.org/doc/html/draft-retana-bgp-custom-decision). This community allows the originator of a BGP route to tweak the route selection process within the recipient router. The community’s value is a structured 6-byte field (see the draft document for details). The first byte (*Point of Insertion*) indicates the position within the BGP route selection algorithm where the cost community should be considered.

EIGRP routes are redistributed into MP-BGP with the *Point of Insertion* (POI) set to 128 and the *Cost* set to EIGRP composite metric, indicating that the cost community’s value should be considered before any other BGP attribute (including locally set weights). This behavior effectively disables BGP route selection mechanism; EIGRP routes redistributed into MP-BGP are compared solely based on their EIGRP composite metric as calculated at the original EIGRP-to-MP-BGP redistribution point.

{{<figure src="/2008/07/MH_EIGRP_BGPCost.png">}}

BGP routes without the *cost* community are evaluated as having the *cost* community set to half the maximum value (2147483647). Routes with the *cost* community with POI set to 128 are thus almost always preferred over routes without this community, regardless of the values of other BGP attributes. This also implies that the EIGRP routes will be preferred over almost any other route type.

You can inspect the *cost* community with the **show ip bgp vpnv4 \[all|vrf *name*\] *prefix*** command. For example, to inspect the MP-BGP routes toward the core LAN subnet on the PE-R1 router, use the following command:

```
PE-R1#show ip bgp vpnv4 all 10.2.5.0
BGP routing table entry for 65000:1:10.2.5.0/24, version 138
Paths: (2 available, best #2, table Cust)
  Not advertised to any peer
  Local
    10.0.1.2 (metric 65) from 10.0.1.2 (10.0.1.2)
      Origin incomplete, metric 0, localpref 100, valid, internal
      Extended Community: RT:65001:1 Cost:pre-bestpath:128:28160
        0x8800:32768:0 0x8801:11:2560 0x8802:65280:25600 0x8803:65281:1500
      mpls labels in/out nolabel/22
  Local
    10.0.1.1 (metric 65) from 10.0.1.1 (10.0.1.1)
      Origin incomplete, metric 0, localpref 100, valid, internal, best
      Extended Community: RT:65001:1 Cost:pre-bestpath:128:28160
        0x8800:32768:0 0x8801:11:2560 0x8802:65280:25600 0x8803:65281:1500
      mpls labels in/out nolabel/26
```

The BGP cost community effectively stops the suboptimal route insertion. For example, if one of the core routers receives EIGRP update before the original MP-BGP update, it will redistribute the EIGRP route into MP-BGP, but this route will soon be replaced by the remote MP-BGP route with lower *cost* community value.

{{<note warn>}}The BGP cost community is not propagated on EBGP sessions. Inter-AS MPLS VPN networks are still vulnerable to redistribution loops.{{</note>}}

## EIGRP Site-of-Origin

The Site-of-Origin is an extended BGP community attached to routes redistributed into MP-BGP from a PE-CE routing protocol. The routes marked with a SoO are not advertised over PE-CE interfaces having the same SoO, effectively breaking redistribution and count-to-infinity loops for multihomed customer sites. The Site-of-Origin attribute is configured in a slightly convoluted manner:

-   You have to configure a **route-map** that sets the SoO community with the **set** **extcommunity** **soo** ***value*** statement.
-   The route map is applied to the PE-CE interface with the **ip** **vrf** **sitemap** ***name*** interface configuration command.

{{<note warn>}}Configuring the VRF sitemap on a PE-CE interface clears all EIGRP adjacencies on that interface.{{</note>}}

To stop the EIGRP-to-BGP routing loops between the PE-C1 and PE-C2 in the sample network, you should configure the SoO on both PE routers:

```
route-map Cust_Central_SoO permit 10
 set extcommunity soo 65001:100
!
interface FastEthernet0/0
 description Core customer LAN
 ip vrf forwarding Cust
 ip vrf sitemap Cust_Central_SoO
```

{{<note info>}}The PE-CE routing protocol must be reset (preferably by disabling/enabling the PE-CE interface) if you change the SoO value in the route map.{{</note>}}

After the SoO is configured on the core site, all routes received from the CE-routers (as well as directly connected routes) and redistributed into MP-BGP carry the SoO extended community, which can be inspected similarly to the *cost* community:

```
PE-R1#show ip bgp vpnv4 all 10.2.5.0
BGP routing table entry for 65000:1:10.2.5.0/24, version 1254
Paths: (2 available, best #2, table Cust)
  Not advertised to any peer
  Local
    10.0.1.2 (metric 65) from 10.0.1.2 (10.0.1.2)
      Origin incomplete, metric 0, localpref 100, valid, internal
      Extended Community: SoO:65001:100 RT:65001:1
        Cost:pre-bestpath:128:28160 0x8800:32768:0 0x8801:11:2560
        0x8802:65280:25600 0x8803:65281:1500
      mpls labels in/out nolabel/38
  Local
    10.0.1.1 (metric 65) from 10.0.1.1 (10.0.1.1)
      Origin incomplete, metric 0, localpref 100, valid, internal, best
      Extended Community: SoO:65001:100 RT:65001:1
        Cost:pre-bestpath:128:28160 0x8800:32768:0 0x8801:11:2560
        0x8802:65280:25600 0x8803:65281:1500
      mpls labels in/out nolabel/26 
```
