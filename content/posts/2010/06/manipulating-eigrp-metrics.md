---
date: 2010-06-22 06:55:00.005000+02:00
eigrp_tag: deploy
tags:
- EIGRP
title: Manipulating EIGRP Metrics
url: /2010/06/manipulating-eigrp-metrics.html
---
If you want to influence traffic flow in a network, you might want to tweak routing protocol metrics to shift the traffic between paths of almost-equal cost (I would always prefer MPLS Traffic Engineering as it's so much better, but sometimes changing a metric is faster than rebuilding your network). OSPF and IS-IS are easy: change the interface metric or interface bandwidth. EIGRP and its composite metric are trickier.

As you know, EIGRP vector metric has five components; [two of which are usually ignored](https://blog.ipspace.net/2009/06/eigrp-load-and-reliability-metrics.html) and [MTU serves only as tie breaker](https://blog.ipspace.net/2010/06/eigrp-mtu-metric.html). This leaves us with bandwidth and delay. Every EIGRP reference tells you to adjust interface delay, not bandwidth, and the simplistic explanation is that "bandwidth is used for QoS features, so it's better left unchanged". While that's true, there are other more important reasons to focus on delay:
<!--more-->
-   EIGRP vector metric (which is the only information exchanged between the routers) carries *minimum* of bandwidth and *sum* of delays between the originating router and the current router. Changing delay will (usually) directly influence RD/FD and thus route selection, while changing bandwidth might not.
-   EIGRP composite metric (RD/FD) is *proportional* to delay and *inversely proportional* to bandwidth (see this [pretty precise EIGRP composite metric formula](http://www.lastkrell.com/2006/09/13/cisco%E2%80%99s-eigrp-metric-calculations/)). Even if you manage to change the bandwidth in the composite metric (which assumes that there is now lower bandwidth link on the whole path to the originating router), its influence on RD/FD is slightly harder to grasp.
-   EIGRP **offset-list** changes delay (admittedly primarily due to our first reason).
