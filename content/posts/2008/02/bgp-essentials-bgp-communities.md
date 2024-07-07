---
date: 2008-02-04 07:19:00+01:00
tags:
- BGP
title: 'BGP Essentials: BGP Communities'
url: /2008/02/bgp-essentials-bgp-communities/
---
BGP communities are extra attributes you can attach to an IP route carried by BGP. You can use communities to indicate which routes should be propagated or filtered (for example, the well-known *NO_EXPORT* community signifies that the route it's attached to shall not be sent outside of the local AS), to influence route selection on remote routers or to trigger other BGP-dependent IOS features (for example, quality-of-service marking based on BGP).

Each BGP community is a 32-bit value. The best practice dictates that the top 16 bits should be the AS number of the network defining the community meaning and the bottom 16 bits are defined by the network administrator.
<!--more-->
For example, if you use BGP communities to control QoS marking within your network, the top 16 bits should be your AS number. If you're using a BGP community to mark backup BGP routes before they are sent to your ISP, you should use the BGP community defined by your ISP (and thus the top 16 bits are the ISP's AS number).

The only mechanism to set BGP community in Cisco IOS is the **set community** command in a **route-map**.

{{<note warn>}}Important: The **set community** command erases existing communities attached to a route and replaces them with the new set of communities unless you specify the **additive** option.{{</note>}}

You can set BGP communities in any point where you can use a **route-map** within BGP:

-   on routes you're receiving from a neighbor with the **neighbor route-map in** router configuration command;
-   on routes you're sending to a neighbor with the **neighbor route-map out** router configuration command;
-   on routes originated into BGP with the **network route-map** router configuration command;
-   on routes redistributed into BGP with the **redistribute route-map** router configuration command.

The BGP communities are transitive BGP attribute, meaning that they should be propagated to all BGP neighbors.

{{<note warn>}}Cisco IOS does not propagate BGP communities unless you manually configure community propagation for each neighbor with the **neighbor send-community** configuration command. BGP peer groups or peer templates are an excellent way to configure BGP community propagation for a large number of peers.{{</note>}}