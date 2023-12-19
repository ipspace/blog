---
date: 2007-08-28 07:31:00+02:00
ospf_tag: mp
tags:
- MPLS
- OSPF
- LDP
title: MPLS LDP Autoconfiguration
url: /2007/08/mpls-ldp-autoconfiguration.html
---
Most MPLS books (mine included) and courses tell you that you have to manually enable MPLS on each interface where you want to run it with the **mpls ip** interface configuration command. However, this task was significantly simplified in IOS release 12.3(14)T with the introduction of MPLS LDP autoconfiguration. If you use OSPF as the routing protocol in your network, you can use the **mpls autoconfig ldp [area *number*]** router configuration command to enable LDP on all interfaces running OSPF (optionally limited to an OSPF area).

As the careful readers of my MPLS books know, it's dangerous to run LDP with your customers; the moment you run LDP with them (Carrier's carrier model is an exception), they can insert any labeled packet into your network, bypassing inbound access lists and sending traffic where it's not supposed to go (even into another VPN). It's vital that you consider security implications before deploying MPLS LDP autoconfiguration.

Using this feature on P routers is absolutely safe, as they have no customer links. You have to be more careful on the PE routers, more so if you run routing protocols with your customers. The safest configuration method would be to configure LDP autoconfiguration inside a single OSPF area, but even then, a configuration error (placing a PE-CE interface in a wrong area) could open your network to MPLS-based attacks.
