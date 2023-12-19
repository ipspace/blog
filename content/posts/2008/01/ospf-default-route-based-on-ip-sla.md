---
date: 2008-01-24 07:32:00+01:00
ospf_tag: default
tags:
- OSPF
- IP routing
title: OSPF Default Route Based on IP SLA
url: /2008/01/ospf-default-route-based-on-ip-sla.html
---
Olivier Guillemain has asked an interesting question: "*how could I originate a default route into OSPF based on IP SLA (for example, based on pinging a remote IP address)?*"

This is very easy to do when the router originating the default route into OSPF needs an SLA-based default route itself:

1.  Configure IP SLA and a corresponding **track** object;
2.  Configure a default route using [reliable static routing](https://blog.ipspace.net/2007/02/reliable-static-routing.html)
3.  [Advertise the default route into OSPF](https://blog.ipspace.net/2007/06/ospf-default-route-design-scenarios.html) with the **default-information originate** router configuration command

The solution is a bit more complex when the router originating the default route into OSPF should not have a default route. In this case, you could use a routing trick:

1.  Configure IP SLA and a corresponding **track** object as before;
2.  Use [reliable static routing](https://blog.ipspace.net/2007/02/reliable-static-routing.html) to configure a static host route for a bogus IP address (for example, *10.0.0.1/32*) pointing to *null0* (for example, **ip route 10.0.0.1 255.255.255.255 null 0 track 100**). Obviously, this host route should not be redistributed into any routing protocol.
3.  [Conditionally advertise default route into OSPF](https://blog.ipspace.net/2007/08/conditional-ospf-default-route-tested.html) based on presence of the static host route.
