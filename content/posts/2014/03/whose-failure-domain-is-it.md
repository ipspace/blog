---
date: 2014-03-05 07:13:00+01:00
dr_tag: fail_fix
high-availability_tag: dr
series:
- dr
tags:
- bridging
- Internet
- high availability
title: Whose Failure Domain Is It?
url: /2014/03/whose-failure-domain-is-it.html
---
*Draco* made a [valid comment](http://blog.ipspace.net/2014/02/keep-your-failure-domains-small.html?showComment=1392697415285#c8785876830767953728) to my [*Keep Your Failure Domain Small*](http://blog.ipspace.net/2014/02/keep-your-failure-domains-small.html?showComment=1392697415285) post:

> What could a small ISP do to limit failure domains? Metro Ethernet and MPLS Virtual Private LAN service are all the rage, and offers customers the promise of being able to connect all their branch offices together, and use the same set of VLANs with free Layer 2 connectivity between their sites. It\'s either: extend the failure domains, or lose out in selling the service, b/c the customer will buy from another ISP.

Well, [your customer's failure domain doesn't have to be yours](http://blog.ipspace.net/2012/07/the-difference-between-metro-ethernet.html).
<!--more-->
### Protect Yourself

The first thing you should do as an ISP is to limit the amount of damage a customer could do to your edge (PE) routers:

-   Rate-limit the BUM frames entering your network (Cisco's *storm control* is such a mechanism, although a pretty rudimentary one);
-   Configure BPDU guard (if appropriate), or root guard on customer-facing links;
-   Protect the PE router control plane.

{{<note warn>}}Years ago, I met an ISP running RIPv1 with their customers (no, they were not offering MPLS/VPN services). Go figure ;){{</note>}}

### Decouple Customer Networks from Your Core

If you implement a Metro Ethernet service with an end-to-end bridged network using 802.1Q or 802.1ad (QinQ) encapsulation, don't act surprised when it collapses due to a [L2 forwarding loop](http://blog.ipspace.net/2009/02/connecting-switch-to-itself-does-it.html), or when you get uncontrollable amount of unicast flooding due to TCAM overflows -- you've tightly coupled the fate of your core network to the (mis)behavior of your customers.

802.1ah (PBB) is slightly better -- at the very least the core switches don't see the customer MAC addresses any longer.

Layer-2 VPN running over a layer-3 infrastructure is the best solution. You would get total decoupling of the [layer-2 forwarding behavior](http://blog.ipspace.net/2010/07/bridging-and-routing-is-there.html) of your services from stable layer-3 forwarding behavior of your transport core. A problem within a customer's network can no longer trash the ISP core (assuming the customer cannot generate enough traffic to overload the core links).

In the old days we used pseudowires (EoMPLS, L2TPv3, VPLS) to implement L2VPN over L3 code. Today I'd recommend considering VXLAN -- most high-speed switches have linerate VXLAN VTEPs.

For more details, watch the [Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service) and [Data Center Interconnects](https://www.ipspace.net/Data_Center_Interconnects) webinars.
