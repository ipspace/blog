---
date: 2010-10-26 06:57:00.001000+02:00
dmvpn_tag: routing
eigrp_tag: deploy
tags:
- DMVPN
- EIGRP
title: 'Solution: EIGRP Summarization Breaks Phase 2 DMVPN'
url: /2010/10/solution-eigrp-summarization-breaks.html
---
Last week I posted an interesting challenge: [what happens if you configure route summarization in a Phase 2 DMVPN network](/2010/10/eigrp-summarization-in-dmvpn-phase-2.html)? The only response came from an anonymous contributor strongly suspected to be a routing/DMVPN expert working for a CCIE-related training company.

The anonymous responder was somewhat cryptic, so let's do a step-by-step explanation. We'll use a simple 3-router network; C1 is hub, R2 and R3 are spokes.
<!--more-->
{{<figure src="/2010/10/s1600-EIGRP_DMVPN.png">}}

Routing updates in DMVPN networks (usually) flow only between the hub and the spokes as dictated by static and dynamic NHRP multicast maps. In our scenario, C1 and R2 (as well as C1 and R3) are EIGRP neighbors, but R2 and R3 cannot exchange routing updates. This behavior makes DMVPN way more scalable than VPLS.

Without any special configuration on C1, R2 and R3 would never see each other's routes. EIGRP uses split horizon filters; updates received from R2 are thus never sent to R3, which receives only EIGRP routes originated by C1 (and any other routes behind C1). R2 and R3 cannot communicate at all.

``` code
R3#show ip route eigrp | begin 10.0
      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
D        10.0.1.1/32 [90/27008000] via 192.168.0.1, 00:01:27, Tunnel0
D        10.0.10.0/24 [90/26882560] via 192.168.0.1, 00:01:27, Tunnel0
```

When we disable EIGRP split horizon on the DMVPN tunnel interface of the hub router with **no ip split-horizon eigrp 1** command, the spokes start receiving routes from other spokes, but the next-hop address is still the hub router. All traffic still flows through the hub (as dictated by the IP routing table).

``` code
R3#show ip route eigrp | begin 10.0
      10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
D        10.0.1.1/32 [90/27008000] via 192.168.0.1, 00:03:32, Tunnel0
D        10.0.1.5/32 [90/28288000] via 192.168.0.1, 00:00:07, Tunnel0
D        10.0.10.0/24 [90/26882560] via 192.168.0.1, 00:03:32, Tunnel0
D        10.0.15.0/24 [90/28162560] via 192.168.0.1, 00:00:07, Tunnel0
```

We have to disable EIGRP next-hop processing on the hub router to enable spoke-to-spoke traffic flow (**no ip next-hop-self eigrp 1** command entered on the DMVPN tunnel interface). IP next hops for the spoke routes are now the other spoke routers.

``` code
R3#show ip route eigrp | begin 10.0
      10.0.0.0/8 is variably subnetted, 7 subnets, 2 masks
D        10.0.1.1/32 [90/27008000] via 192.168.0.1, 00:01:29, Tunnel0
D        10.0.1.5/32 [90/28288000] via 192.168.0.5, 00:01:24, Tunnel0
D        10.0.10.0/24 [90/26882560] via 192.168.0.1, 00:01:29, Tunnel0
D        10.0.15.0/24 [90/28162560] via 192.168.0.5, 00:01:24, Tunnel0
```

If we configure summarization on the hub router with the **ip summary-address eigrp 1 10.0.0.0 255.0.0.0** command, the individual routes are suppressed (the spokes no longer receive /32s and /24s) and the summary prefix is advertised with the hub router as the next hop. Traffic between spokes yet again flows through the hub router -- we've managed to destroy the most important property of Phase 2 DMVPN.

``` code
R3#show ip route eigrp | begin 10.0
      10.0.0.0/8 is variably subnetted, 4 subnets, 3 masks
D        10.0.0.0/8 [90/26882560] via 192.168.0.1, 00:00:02, Tunnel0
```

{{<note info>}}As *bmigette* pointed out in the comments, summarizing spoke routes on the tunnel interface of the spoke router is OK as is summarizing any non-spoke routes on the hub router. You break spoke-to-spoke traffic flow only if the hub router summarizes routes from multiple spoke sites into a single IP prefix.{{</note>}}

### Lesson Learned

Careless route summarization at the hub router stops spoke-to-spoke traffic flow in Phase 2 DMVPN networks using EIGRP.

If you have to reduce the amount of routing information sent to the spoke routers (which only makes sense if DMVPN is a small part of your network), use static route-generated summaries and route filters (distribute lists).
