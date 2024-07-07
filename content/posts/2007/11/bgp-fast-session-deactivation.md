---
date: 2007-11-29 07:37:00+01:00
tags:
- BGP
title: BGP Fast Session Deactivation
url: /2007/11/bgp-fast-session-deactivation/
---
We all know that BGP is meant to converge slowly... well, the MPLS/VPN service providers tend to disagree, as their users are not used to minute-long convergence times. One of the major components of slow BGP convergence is the time it takes a router to discover that a neighbor has disappeared. Traditionally, the BGP keepalive packets were sent every minute and it took up to three minutes to discover that a neighbor is down.

Of course you could fine-tune those times with the **neighbor timers** configuration command, but the reduced timers resulted in increased TCP traffic and consequently increased CPU load, which could reach tens of percents if the timers were set to a few seconds and the router had lots of BGP neighbors.
<!--more-->
{{<note update>}}Update 2021-01-01: You should look at BFD before considering any of the tricks discussed in the rest of this blog post. Just saying...{{</note>}}

The neighbor loss detection has improved dramatically in 12.3T and 12.0S with the introduction of the *fast session deactivation*, where a BGP session is dropped as soon as the route to the BGP neighbor is lost. You can configure this feature with the ominous-sounding **neighbor fall-over** configuration command. Obviously, this feature does not work well if you use default routing (or summaries), since the path to the BGP neighbor is never completely lost. In that case, you can use a **route-map** option of the **neighbor fall-over** command (introduced in 12.4(4)T) to select which less specific route is still a valid route to the BGP neighbor.

Here are the logging and debugging printouts from a router that lost a BGP neighbor and discovered it after the BGP hold time has expired:

```
00:00:48: %BGP-5-ADJCHANGE: neighbor 10.0.3.3 Up
00:01:23: RT: del 10.0.3.3/32 via 10.0.1.2, ospf metric [110/129]
00:01:23: RT: delete subnet route to 10.0.3.3/32
00:03:49: %BGP-3-NOTIFICATION: received from neighbor 10.0.3.3 4/0 
  (hold time expired) 0 bytes
00:03:49: %BGP-5-ADJCHANGE: neighbor 10.0.3.3 Down BGP Notification received
```

As you can see, there is more than a two minute gap between the time the OSPF route to the BGP neighbor was lost and the time the BGP session went down (and the BGP routes were recalculated). When the **neighbor 10.0.3.3 fall-over** is configured, the BGP session is disconnected as soon as the OSPF route to the neighbor is gone:

```
00:08:12: RT: del 10.0.3.3/32 via 10.2.0.2, ospf metric [110/75]
00:08:12: RT: delete subnet route to 10.0.3.3/32
00:08:12: RT: NET-RED 10.0.3.3/32
00:08:12: RT: Try lookup less specific 10.0.3.3/32, default 1
00:08:12: RT: Failed found subnet on less specific
00:08:12: RT: return NULL
00:08:12: %BGP-5-ADJCHANGE: neighbor 10.0.3.3 Down Route to peer lost
```