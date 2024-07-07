---
date: 2008-08-08 06:38:00+02:00
tags:
- BGP
title: BGP Route Reflector Details
url: /2008/08/bgp-route-reflector-details/
lastmod: 2020-11-20 09:24:00
series: bgp-essentials
---
BGP route reflectors have been supported in Cisco IOS well before I started to develop the first BGP course for Cisco in mid 1990s. It's a very simple feature, so I was pleasantly surprised when I started digging into it and discovered a few rarely known details.

### The Basics

Route reflector is an IBGP feature that allows you to build scalable IBGP networks. The original BGP protocol (RFC 1771) contained no intra-AS loop prevention mechanism; routers were therefore prohibited from sending routes received from an IBGP peer to another IBGP peer, requiring a full-mesh of IBGP sessions between all BGP routers within an AS.

<!--more-->
The next revision of the BGP standard ([RFC 4271](https://tools.ietf.org/html/rfc4271)) already included references to the BGP Route Reflector functionality defined in [RFC4456](https://tools.ietf.org/html/rfc4271) and augmented in [RFC7606](https://tools.ietf.org/html/rfc7606). RFC 4271 defines a new attribute (*cluster list*) which can detect route propagation loops within an AS, allowing us to build any IBGP topology we wish as long as we follow a few simple rules.

### Route Reflector Rules

A BGP router implementing route reflector functionality propagates BGP routes according to these rules:

-   Locally originated routes and routes received from EBGP neighbors and selected as best routes are propagated to all BGP peers (internal and external).
-   Routes received from an IGBP peer that is not a route-reflector client and selected as best routes are propagated to all EBGP peers and all IGBP peers configured as route-reflector clients.
-   Routes received from a route-reflector client and selected as best routes are propagated to all BGP peers (internal and external).

{{<note info>}}An IBGP route received from a route-reflector client is sent to all IBGP peers, **including the client from which it was received**.{{</note>}}

Whenever an IBGP route is reflected (propagated to another IBGP peer), the route reflector appends two optional, non-transitive attributes to the BGP route:

-   If the route does not have the *Originator ID* attribute (it has not been reflected before), the *router ID* of the IBGP peer from which the route has been received is copied into the *Originator ID* attribute.
-   If the route does not have the *Cluster list* attribute, it’s added to the route.
-   The value configured with the **bgp cluster-id** router configuration command (or the *router ID* of the route reflector if the **cluster-id** is not configured) is prepended to the *Cluster list* attribute.

Route reflector does not change or remove any other attributes of the reflected routes (even non-transitive attributes), ensuring that the IBGP routes are not changed within the autonomous system. The **next-hop-self** neighbor configuration parameter or (most of the) **set** options of outbound **route-map** configured on route-reflector clients are ignored for reflected routes. 

Exceptions:

* BGP next-hop can be changed **set ip next-hop** route map command or with **neighbor next-hop-self all** feature introduced to [support large-scale DMVPN networks using IBGP](/2014/04/changes-in-ibgp-next-hop-processing/).
* Standard and extended BGP communities are removed from the reflected routes unless the **neighbor send-community \[both\]** is configured on the route reflector.
* The *link bandwidth* community is removed from reflected route if the route-reflector performs IBGP multipath load-sharing for that route.

### Monitoring Route Reflection

The route reflector-related BGP attributes attached to a BGP route (_Originator_ and _Cluster list_) can be inspected with the **show ip bgp _prefix_** command:

```
Edge#show ip bgp 10.2.2.0
BGP routing table entry for 10.2.2.0/24, version 12
Paths: (1 available, best #1, table default)
Flag: 0xA20
  Not advertised to any peer
  65001
    10.0.1.1 (metric 129) from 10.0.1.3 (10.0.1.3)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      Originator: 10.0.1.1, Cluster list: 10.0.1.3
```

The same command executed on a route reflector will also indicate whether a route was received from a route-reflector client (and will thus be reflected to all IBGP peers):

```
RR#show ip bgp 10.2.2.0
BGP routing table entry for 10.2.2.0/24, version 18
Paths: (2 available, best #2, table default)
Multipath: eBGP iBGP
Flag: 0x1A20
  Advertised to update-groups:
     1
  65001, (Received from a RR-client)
    10.0.1.2 (metric 65) from 10.0.1.2 (10.0.1.2)
      Origin IGP, metric 0, localpref 100, valid, internal, multipath
  65001, (Received from a RR-client)
    10.0.1.1 (metric 65) from 10.0.1.1 (10.0.1.1)
      Origin IGP, metric 0, localpref 100, valid, internal, multipath, best
```

The route propagation policy of a route reflector is also displayed in the **show ip bgp update-group** printout:

```
RR#show ip bgp update-group
BGP version 4 update-group 1, internal, Address Family: IPv4 Unicast
  BGP Update version : 22/0, messages 0
  Route-Reflector Client
  Community attribute sent to this neighbor
  Extended-community attribute sent to this neighbor
  Update messages formatted 59, replicated 47
  Number of NLRIs in the update sent: max 1, min 0
  Minimum time between advertisement runs is 0 seconds
  Has 2 members (* indicates the members currently being sent updates):
   10.0.1.2         10.0.1.4

BGP version 4 update-group 2, internal, Address Family: IPv4 Unicast
  BGP Update version : 22/0, messages 0
  Community attribute sent to this neighbor
  Extended-community attribute sent to this neighbor
  Update messages formatted 5, replicated 0
  Number of NLRIs in the update sent: max 1, min 1
  Minimum time between advertisement runs is 0 seconds
  Has 1 member (* indicates the members currently being sent updates):
   10.0.1.1
```

<span id="Loop_Detection_and_Avoidance"></span>

### Loop Detection and Avoidance

The BGP routers implementing RFC 1966 (original route reflector RFC) use the following mechanisms to detect route-reflector-related loops:

-   If the *Originator ID* in an incoming IBGP route update is equal to the BGP router ID, the update is ignored (reflected route was propagated back to its originator).
-   If the *Cluster ID* of a route-reflector appears in the *Cluster list* attribute of an incoming IBGP update, the update is ignored (route reflector loop).

{{<note>}}The route reflector functionality was introduced in IOS release 11.1. It’s therefore relatively safe to assume that every Cisco router encountered in a production network supports it. Ancient routers that do not support RFC 1966 would usually ignore IBGP routes with their own *Originator ID*, as they would have a better EBGP or locally originated route.{{</note>}}

Although the mechanisms specified in RFC 1966 ensure loop-free IBGP operation regardless of the actual topology of the IBGP sessions, [RFC 4456](https://tools.ietf.org/html/rfc4456) added new route selection rules that improve the actual convergence within an AS and reduce the amount of BGP updates propagated across the AS:

-   Routes with shorter *Cluster list* attribute are preferred. This rule ensures that all routers select routes with minimum number of reflections, significantly reducing the amount of unnecessary BGP updates (remember: only best routes selected by a route reflector are reflected to its clients).
-   The *Originator ID* attribute of a reflected route should be used as the *Router ID* attribute when comparing otherwise identical IBGP routes, ensuring the stability of route selection across AS regardless of the route reflectors.

### Route Reflector Design Rules

Traditional design rules recommended an IBGP full mesh of route reflectors or other core routers, combined with route reflector clients at the network edge:

{{<figure src="/2008/08/BGP_RR_IBGP_Mesh.png" caption="BGP route reflectors combined with IBGP full mesh between core routers">}}

Alternatively you could build a hierarchy of route reflectors with mid-range route reflectors being clients of core route reflectors:

{{<figure src="/2008/08/BGP_RR_Hierarchy.png" caption="A hierarchy of BGP route reflectors">}}

With the improved IBGP loop avoidance, you could use more relaxed designs, ranging from **route-reflector-client** being configured on every IBGP neighbor to designs where the edge routers act as route reflector clients and all other BGP routers in the AS act as route reflectors.

{{<figure src="/2008/08/BGP_RR_Hierarchy.png" caption="IBGP session topology with bidirectional route-reflector-client configuration">}}

### Cluster-ID is Obsolete

Cisco IOS implementation of route reflector functionality supports the **bgp** **cluster-id** parameter, which is used in the *Cluster list* attribute instead of the *Router ID*. The **cluster-id** parameter is useful in redundant route reflector scenarios where multiple route reflectors serve the same set of clients, but can lead to partial connectivity when multiple IBGP sessions are disrupted ([more details](/2022/02/bgp-rr-cluster-myths/)).

{{<figure src="/2008/08/BGP_RR_Cluster.png" caption="Cluster of redundant BGP route reflectors">}}

The revised BGP route selection rules ensure that a route reflector in a cluster always prefers route from a client (with shorter *Cluster list*) over a reflected route, thus making the **bgp** **cluster-id** parameter obsolete. You should not use the **bgp** **cluster-id** in new designs to increase the resilience of your network.

### Further Reading

* [Can BGP Route Reflectors Really Generate Forwarding Loops?](/2013/10/can-bgp-route-reflectors-really/)
* [Mixed Feelings about BGP Route Reflector Cluster ID](/2022/02/bgp-rr-cluster-myths/)
* [BGP Route Reflector update groups (technical details)](/2009/04/bgp-route-reflector-update-groups/)
* [BGP next hop processing](/2011/08/bgp-next-hop-processing/)
* [Can We Trust BGP Next Hops (Part 2)?](/2020/04/can-we-trust-bgp-next-hops-part-2/)
* [Running BGP Route Reflector in a Virtual Machine](/2016/05/running-bgp-route-reflector-in-virtual/)
* [Building BGP Route Reflector Configuration with Ansible/Jinja2](/2020/04/building-bgp-rr-configuration-ansible-jinja2/)

