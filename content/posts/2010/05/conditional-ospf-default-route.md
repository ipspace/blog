---
date: 2010-05-28 20:06:00.003000+02:00
tags:
- OSPF
title: Conditional OSPF Default Route Origination Based on Classless IP Prefixes
url: /2010/05/conditional-ospf-default-route.html
---
Almost two years ago I wrote the *OSPF default mysteries* article (you'll find it somewhere in [this list](https://www.ipspace.net/kb/Internet/)) in which I've described the caveats of conditional OSPF default route origination, claiming that it requires an IP access list that can only match classful networks.

Later someone sent me a message stating that you can match classless IP prefixes with an **ip prefix-list** \... and it took me well over a year to find the time (and mental energy) to lab the scenario and document the results.
<!--more-->
The sender was correct: you can originate OSPF default route based on presence of a classless IP prefix in the IP routing table; you'll find details in the [*Conditional OSPF default route origination based on classless IP prefixes*](http://wiki.nil.com/Conditional_OSPF_default_route_origination_based_on_classless_IP_prefixes) article in the [CT3 wiki](http://wiki.nil.com/).

I've also fixed the [*OSPF default routes*](http://wiki.nil.com/OSPF_default_routes) article in the wiki to include the summaries of all relevant articles in the CT3 wiki (previously it only contained a link to the IP corner article).
