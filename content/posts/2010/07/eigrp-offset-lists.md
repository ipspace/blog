---
date: 2010-07-06 06:57:00.001000+02:00
eigrp_tag: details
tags:
- EIGRP
title: EIGRP Offset Lists
url: /2010/07/eigrp-offset-lists/
---
A simplistic explanation of EIGRP **offset-list** configuration command you might see every now and then is "it adjusts the RD/FD to influence route selection". If that would be the case, the adjustment would not be propagated to upstream routers (remember: only the EIGRP vector metric is sent in the routing updates, not RD or FD) resulting in potential routing loops (it's never a good idea to use one set of metrics and propagate another set of metrics to your neighbors).

In reality, the EIGRP offset lists adjust the *delay* portion of the EIGRP vector metric (which [linearly influences the RD/FD value](/2010/06/manipulating-eigrp-metrics/)). You can increase the value of the *delay* metric for EIGRP updates received or sent through a specific interface (or all interfaces). You can also use an access list in the **offset-list** command, applying changes only to specific IP prefixes. For more details, please read [this technology note on Cisco's web site](http://www.cisco.com/en/US/tech/tk365/technologies_tech_note09186a00800c2d96.shtml).
