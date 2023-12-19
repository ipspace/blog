---
date: 2008-09-10 07:09:00+02:00
ospf_tag: default
tags:
- OSPF
title: Default Routing in NSSA Area
url: /2008/09/default-routing-in-nssa-area.html
---
The [RFC 3101](http://tools.ietf.org/html/rfc3101#page-6) (OSPF NSSA Option) states:

> In addition, an NSSA border router should originate a default LSA (IP network is 0.0.0.0/0) into the NSSA. Default routes are necessary because NSSAs do not receive full routing information and must have a default route in order to route to AS-external destinations.

I am pretty sure IOS inserted the type-7 default route into an NSSA area when the NSSA feature was introduced.
<!--more-->
However, at least in some Cisco IOS releases, you have to configure the type-7 default route origination explicitly with the **area nssa default-information-originate** router configuration command, in which you can also specify the route metric and metric type (N1 or N2). Entering the **area *xx* nssa** without the **default-information-originate** keyword will result in an NSSA area with no connectivity to external destinations redistributed into OSPF in other areas.
