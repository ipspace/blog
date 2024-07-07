---
date: 2012-01-05 10:01:00.001000+01:00
tags:
- IPv6
- design
- MPLS
title: Should I Use 6PE or Native IPv6 Transport?
url: /2012/01/should-i-use-6pe-or-native-ipv6/
---
One of my students was watching the [*Building IPv6 Service Provider Core*](http://www.ipspace.net/Building_IPv6_Service_Provider_Core) webinar and wondered whether he should use 6PE or native IPv6 transport:

> Could you explain further why it is better to choose 6PE over running IPv6 in the core? I have to implement IPv6 where I work (a small ISP) and need to fully understand why I should choose a certain implementation.

Here's a short decision tree that should help you make that decision:
<!--more-->
{{<note>}}The decision tree should help you answer the question: "should I use native IPv6 transport or IPv6-over-MPLS for the global IPv6 connectivity?" L2/L3 VPN services are out of scope.{{</note>}}

---
**Do you already have MPLS in your network?**

* *Yes*: Do you use features like MPLS TE or FRR?
    * *Yes*: you must use 6PE.
    * *No*: you could run IPv6 natively. Do you run BGP (for Internet services) on all core routers?

        - *No:* Don't change the network design, use 6PE.
        - *Yes:* You could run either native IPv6 or 6PE. Native IPv6 requires IPv6 deployment on all core routers. 6PE needs IPv6 only on PE routers and route reflectors.

* *No*: Are you willing to deploy MPLS?
    * *No*: Forget 6PE, use native IPv6.
    * *Yes*: Will you deploy IPv6 gradually (only on a few PE-routers)?

        -   *Yes*: Introduction of MPLS and 6PE might make sense.
        -   *No*: Forget it, doesn\'t make sense to introduce MPLS just for IPv6

---

## More information

* To get an initial overview of what's needed to deploy IPv6 in your network, watch the [*Service Provider IPv6 Introduction*](http://www.ipspace.net/Service_Provider_IPv6_Introduction) or [*Enterprise IPv6 -- the first steps*](http://www.ipspace.net/Enterprise_IPv6_-_the_First_Steps) webinar. 
* You'll find IPv6 network design and deployment guidelines in the [*Building Large IPv6 Service Provider Networks*](https://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks) webinar.
* All three webinars are included in the [yearly subscription](http://www.ipspace.net/Subscription).
