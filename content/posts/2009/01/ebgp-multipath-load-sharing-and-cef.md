---
date: 2009-01-21 06:48:00+01:00
tags:
- CEF
- BGP
- load balancing
title: EBGP Multipath Load Sharing and CEF
url: /2009/01/ebgp-multipath-load-sharing-and-cef.html
---
When I was discussing the details of the BGP troubleshooting video with one of my readers, he pointed out that I should mention the need for CEF switching in EBGP multipath scenario. My initial response was "*Why would you need CEF? EBGP multipath is older than CEF*" and his answer told me I should turn on my gray cells before responding to emails: "*Your video as well as Cisco's web site recommends CEF for EBGP multipath design... but interestingly, it does work without CEF*".

The real reason we need CEF in EBGP load sharing designs is the efficacy of load distribution. Without CEF, the router will send all traffic toward a single BGP prefix over one of the links (fast switching performs per-destination-prefix load sharing). With CEF, the [load is distributed based on the source-destination IP address pair combinations](/2006/10/cef-load-sharing-details.html). Even if multiple clients send the traffic toward the same server, the load is spread across available links.
