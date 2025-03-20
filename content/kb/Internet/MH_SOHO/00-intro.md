---
kb_section: MH_SOHO
minimal_sidebar: true
title: Small-Site Multihoming
toc_title: Introduction
url: /kb/Internet/MH_SOHO/
tags: [ Internet ]
date: 2025-03-21 07:52:00+0100
alt_section: posts
index: true
summary: |
  In 2007, I wrote a series of articles describing how one could implement small-site (BGP-less) multihoming in IPv4 world. It looks like that's still an interesting topic, as I recently got requests to resurrect those articles.
  
  This is the first article in the series, describing a setup in which a single site router connects to two upstream ISPs.
---
Unless your network operates under extreme security considerations or in places where the is no Internet access, your management has probably already asked you to lower the wide area network (WAN) costs by migrating from a traditional leased line or frame-relay-based network to an Internet- or MPLS VPN-based transport, while at the same time retaining or even increasing network reliability. This conflicting set of requirements might force you to make all your sites multi-homed (connected to more than one Internet Service Provider – ISP).
<!--more-->
{{<note migrated>}}This article was written in 2007 and has been updated and republished on ipSpace.net in March/April 2025. The printouts were taken on an old release of Cisco IOS that still used serial interfaces, but I don't expect to see much change in the recent IOS/XE releases.{{</note>}}

Multi-homing requirements aren’t new; for example, every decent e-commerce solution should be multi-homed. However, most solutions you’ll find with extensive help from Google require that you possess your own public IP prefix and an autonomous system number (both of them are scarce resources) and run Border Gateway Protocol (BGP) with all ISPs. Clearly, these requirements are completely unrealistic if you want to multi-home a small remote office.

In this article, you’ll learn how to:

* connect a small remote site to more than one ISP;
* detect failures in the ISP networks and adjust your routing accordingly;
* increase overall availability of your sites with Service Level Agreement (SLA) monitoring;
* log all relevant changes in the remote site connectivity.
