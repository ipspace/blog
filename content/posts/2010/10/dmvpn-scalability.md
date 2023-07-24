---
date: 2010-10-28 09:17:00+02:00
dmvpn_tag: basics
series_weight: 100
tags:
- DMVPN
title: DMVPN Scalability
url: /2010/10/dmvpn-scalability.html
---
Alexander sent me a very valid question: "*Do you cover scalability problems in your [DMVPN webinar](https://www.ipspace.net/DMVPN)?*". Of course I do, more than half of the webinar is devoted to them.

As you know, DMVPN is a combination of multiple technologies, including ISAKMP (key exchange), IPsec (encryption), GRE (tunneling), NHRP (tunnel endpoint resolution) and a routing protocol. Any one of these can be a limiting factor:
<!--more-->
-   ISAKMP is CPU-consuming, more so if you use certificates. Large number of concurrent key exchanges can overload a low-end spoke router in Phase 2/3 DMVPN networks. Use ISAKMP call admission control;
-   The limiting factor of IPsec encryption is usually the throughput. Use hardware encryption modules;
-   Multicast/broadcast packets sent over an mGRE tunnel (for example, routing protocol hello messages or updates) are transformed into numerous unicast GRE packets, potentially overloading the output interface on the hub router. Change the routing protocol;
-   Low NHRP registration timeout on the spoke routers can overload the hub router in networks with very high hub-to-spoke ratios. Increase the NHRP registration timeout;

Most common limiting factor is the routing protocol. OSPF is the worst possible choice, as the weakest spoke router limits the scalability (unless you use flooding filters). EIGRP with stub routers is pretty good (although it's hard to push it above 350 peers on a 7200) as is RIP and ODR, but they all suffer from the multicast replication issues. For larger networks you should use unidirectional RIP, BGP or static routes.
