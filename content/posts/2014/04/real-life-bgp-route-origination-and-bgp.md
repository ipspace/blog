---
date: 2014-04-07 07:21:00+02:00
dmvpn_tag: deploy
tags:
- design
- DMVPN
- BGP
title: Real Life BGP Route Origination and BGP Next Hop Intricacies
url: /2014/04/real-life-bgp-route-origination-and-bgp.html
---
During one of the [ExpertExpress engagements](http://www.ipspace.net/ExpertExpress) I helped a company implement the [BGP Everywhere](http://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN) concept, significantly simplifying their routing by replacing unstable route redistribution between BGP and IGP with a single BGP domain running across MPLS/VPN and [DMVPN](http://www.ipspace.net/DMVPN_trilogy) networks.

They had a pretty simple core site network, so we decided to establish an IBGP session between DMVPH hub router and MPLS/VPN CE router (managed by the SP).
<!--more-->
{{<figure src="/2014/04/s500-BGP_NH_1.jpg">}}

Unfortunately, things are never as easy as they seem during the initial discussion -- inevitably a few skeletons everyone forgot about fall out of a dusty closet. In this case, it was a VPN concentrator connecting remote users to the core network.

In the past, the customer used static routes on MPLS/VPN CE router and DMVPN hub router to reach the prefixes behind the VPN concentrator.

{{<figure src="/2014/04/s500-BGP_NH_2.jpg">}}

As they have a single VPN concentrator, static routes proved to be sufficient... but the customer had to open a ticket with the ISP (and wait a few days for a maintenance window) every time they wanted to change the static routes on the provider-controller CE router.

With the IBGP session between DMVPN hub router and MPLS/VPN CE router, the customer started wondering: "*Would it be possible to originate the prefixes reachable through the VPN concentrator on the DMVPN hub router?*"

After warning them that their idea creates a single point of failure (which they accepted, looks like there's nothing mission-critical behind the VPN box), we started discussing the technical details, in particular what the BGP next hop of the route originating from the DMVPN hub router would be and how the traffic would flow.

### A Slight Digression into Layer-3 World

If the customer had a layer-3 core network, there would be no discussion. The layer-3 switch (replacing the layer-2 network drawn as an Ethernet segment in my pictures) would advertise the prefixes behind the VPN concentrator and we could easily set the BGP next hop to the IP address of the layer-3 switch with **neighbor next-hop-self** command. Alas, we were facing a slightly more interesting challenge.

{{<figure src="/2014/04/s500-BGP_NH_3.jpg">}}

### BGP Route Origination Details

The question we had to answer before deploying the proposed solution was "*What would the BGP next hop of a static route redistributed into BGP be?*"

{{<figure src="/2014/04/s500-BGP_NH_4.jpg">}}

If the DMVPN hub router advertises a static route pointing to the VPN concentrator with the BGP next hop set to the IP address of the VPN concentrator, traffic between sites in MPLS/VPN network and sites behind VPN concentrator flows directly. If the DMVPN hub router sets itself as the BGP next hop, the traffic takes an undesired detour. Time for a lab test.

{{<figure src="/2014/04/s500-BGP_NH_5.jpg">}}

### Virtual Lab to the Rescue

Having access to cloud-based beta version of [Cisco Modeling Lab](/2013/10/cisco-modeling-lab-virl-behind-scenes.html) turned out to be one of the best things I got from a vendor in the last few months.

{{<note info>}}The blog post was written in 2014. A decade later I'd use Tailscale VPN to access the Intel NUC sitting in my office and build the test topology in _[netlab](https://netlab.tools/)_.{{</note>}}

Even though I was presenting at a conference in Germany, I managed to create a simple lab during one of the breaks and verify my understand of how BGP route origination works (on second thought, it might have been faster to read what [I wrote in 2011](/2011/08/bgp-next-hop-processing.html)):

-   Directly connected networks are inserted into the BGP table with BGP next hop set to all zeroes (= self);
-   When a BGP routing process inserts a route from IP routing table (static- or IGP-derived route) into BGP table, [it copies the IP next hop from the IP routing table into the *BGP next hop* attribute](/2011/08/bgp-next-hop-processing.html#NHLocal).
-   When a BGP router advertises the BGP route it originated to its BGP neighbors, it uses the [standard BGP next hop processing rules](/2011/08/bgp-next-hop-processing.html).

In our case, DMVPN hub router shouldn't change the BGP next hop of the static routes -- the BGP next hop should point to the VPN concentrator, resulting in optimal traffic flow.

### A Few Printouts

I was using this configuration on DMVPN hub router to generate the desired BGP route:

``` code
router bgp 65000
 network 192.168.4.0
!
ip route 192.168.4.0 255.255.255.0 10.0.0.42
```

As you can see, BGP next hop in BGP table matches IP next hop in IP table:

``` code
DMVPN#show ip route 192.168.4.0
Routing entry for 192.168.4.0/24
  Known via "static", distance 1, metric 0
  Advertised by bgp 65000
  Routing Descriptor Blocks:
  * 10.0.0.42
      Route metric is 0, traffic share count is 1
DMVPN#show ip bgp 192.168.4.0
BGP routing table entry for 192.168.4.0/24, version 11
Paths: (1 available, best #1, table default)
  Advertised to update-groups:
     1         
  Refresh Epoch 1
  Local
    10.0.0.42 from 0.0.0.0 (192.168.0.1)
      Origin IGP, metric 0, localpref 100, weight 32768, valid, sourced, local, best
```

BGP next hop is not modified on IBGP sessions; the managed CE router thus receives the correct value for the BGP next hop:

``` code
CE#show ip bgp 192.168.4.0
BGP routing table entry for 192.168.4.0/24, version 11
Paths: (1 available, best #1, table default)
  Not advertised to any peer
  Refresh Epoch 1
  Local
    10.0.0.42 from 10.0.0.1 (192.168.0.1)
      Origin IGP, metric 0, localpref 100, valid, internal, best
```

### Meanwhile on Planet Earth

Unfortunately, the reality quickly diverged from the optimistic theoretical results -- the BGP next hop on the MPLS/VPN CE router pointed to the DMVPN hub router.

A few minutes of troubleshooting identified the culprit: **neighbor next-hop-self** that we had to configure on the IBGP session between DMVPN hub router and MPLS/VPN CE router to circumvent lack of IGP between the two BGP routers ([IBGP is supposed to be run in combination with an IGP that resolves BGP next hops](/2011/08/ibgp-or-ebgp-in-enterprise-network.html)).

We could have solved the problem with a **route-map** that would set BGP next hop for non-local routes and keep it unchanged for locally originated routes, but decided that the extra complexity simply isn't worth it (sometimes you [have to know when to give up](/2013/08/temper-your-macgyver-streak.html)).
