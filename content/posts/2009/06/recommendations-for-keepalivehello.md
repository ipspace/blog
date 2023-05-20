---
date: 2009-06-17 07:09:00.008000+02:00
eigrp_tag: deploy
tags:
- EIGRP
- GRE
title: Recommendations for Keepalive/Hello Timers
url: /2009/06/recommendations-for-keepalivehello.html
---
The "[GRE keepalives or EIGRP hellos](https://blog.ipspace.net/2009/06/gre-keepalives-or-eigrp-hellos.html)" discussion has triggered another interesting question:

> Is there a good rule-of-thumb for setting hold-down timers in respect to the bandwidth/delay of a given link? Perhaps something based off of the SRTT?

Routing protocol hello packets or GRE keepalive packets are small compared to the bandwidths we have today and common RTT values are measured in milliseconds while the timers' granularity is usually in seconds.
<!--more-->
{{<note>}}
[OSPF](http://www.cisco.com/en/US/docs/ios/12_0s/feature/guide/fasthelo.html) and IS-IS support for fast hellos is an exception, but you wouldn't want to use this feature on a hub router with tens or hundreds of small remote sites.{{</note>}}

You should answer the above question by asking yourself: what are my business needs for a fast switchover and how can I get there? If you're satisfied with a switchover that takes a few (up to ten) seconds, you can achieve it with keepalive/hello packets. If you need a faster switchover, you will have to do serious routing protocol tuning. Even better, use BFD, or deploy LFA/TI-LFA if you care about sub-second rerouting.

For more details, watch the _convergence_ part of _[Advanced Routing Protocols](https://my.ipspace.net/bin/list?id=Net101#ADV_ROUTING)_ section in _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.
