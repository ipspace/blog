---
kb_section: MH_SOHO
minimal_sidebar: true
title: Small-Site Multihoming
toc_title: Introduction
url: /kb/Internet/MH_SOHO/
tags: [ Internet ]
date: 2025-03-21 07:30:00+0100
alt_section: posts
index: true
summary: |
  In 2007, I wrote a series of articles describing an implementation of small-site (BGP-less) multihoming in the IPv4 world. It seems that this topic is still interesting, as I recently received requests to republish them, and it may (sadly enough) apply equally well to the IPv6 world.
  
  This is the first article in the series. It describes a design with a single router using two uplinks to two upstream ISPs.
---
Unless your network operates under extreme security considerations or in places without Internet access, your management has probably already asked you to lower your Wide Area Network (WAN) costs by migrating from a traditional leased line or frame-relay-based network to an Internet or MPLS VPN-based transport while retaining or even increasing network reliability. These conflicting requirements might force you to make all your sites multi-homed (connected to more than one Internet Service Provider, or ISP).
<!--more-->
{{<note migrated>}}
This article was written in 2007 and has been updated and republished on ipSpace.net in March 2025. The printouts were taken on an old release of Cisco IOS that still used serial interfaces, but I don't expect much change in the recent IOS/XE releases.
{{</note>}}

Multi-homing requirements aren’t new; for example, every decent e-commerce solution should be multi-homed. However, most solutions you’ll find with extensive help from Google require:

* a provider-independent (PI) public IP prefix,
* an autonomous system number (ASN)
* Border Gateway Protocol (BGP) running between your router and ISP edge routers. 

While getting a BGP AS number or an IPv6 prefix is easy, you can only buy IPv4 prefixes on the secondary market after the exhaustion of the IPv4 address space. Furthermore, it's hard to find ISPs that will run BGP over a low-cost Internet connectivity service. The above requirements are unrealistic if you want to multi-home a small remote office; we need a more creative solution.

In this article, you’ll learn how to:

* connect a small remote site to more than one ISP;
* detect failures in the ISP networks and adjust the outbound routing accordingly;
* increase overall availability of your sites with Service Level Agreement (SLA) monitoring;
* log all relevant changes in the remote site connectivity.
