---
url: /2012/01/bgp-free-service-provider-core-in.html
title: "BGP-Free Service Provider Core in Pictures"
date: "2012-01-11T07:04:00.000+01:00"
tags: [ MPLS,IPv6,BGP ]
---
I got a follow-up question to the [*Should I use 6PE or native IPv6*](https://blog.ipspace.net/2012/01/should-i-use-6pe-or-native-ipv6.html) post: 

> Am I remembering correctly that if you run IPv6 native throughout the network you need to enable BGP on all routers, even P routers? Why is that?

I [wrote about BGP-free core before](https://blog.ipspace.net/2008/03/use-mpls-to-scale-your-internet.html), but evidently wasn’t clear enough, so I’ll try to fix that error.

Imagine a small ISP with a customer-facing PE-router (A), two PE-routers providing upstream connectivity (B and D), a core router (C), and a route reflector (R). The ISP is running IPv4 and IPv6 natively (no MPLS).
<!--more-->
![](s400-BGP_FC_1.png)

When an end-customer sends a packet toward an Internet destination (a Facebook server, for example), each router in the ISP network has to examine the packet, perform destination address lookup in its [forwarding table](https://blog.ipspace.net/2010/09/ribs-and-fibs.html) (FIB), and forward the packet toward the next hop.

Assuming the ISP is not running BGP on the core router, the core router is not aware of any destination outside of its own AS, and thus drops the packet sent toward Facebook.

![](s400-BGP_FC_2.png)

You can use default routing as a problem-solving kludge (B and D advertise default routes into the ISP’s network), or deploy BGP on the core router (C).

After a BGP session between C and R is configured, C receives all global BGP routes, and is able to forward packets toward external destinations:

![](s400-BGP_FC_3.png)

There is another solution: if you deploy MPLS in the network, LDP automatically builds virtual circuits (Label Switched Paths – LSP) between any two routers.

{{<note info>}}Cisco IOS builds LSPs for all IGP destinations, Junos only for the loopback interfaces. More details in [*Junos and Cisco IOS: MPLS and LDP*](https://blog.ipspace.net/2011/11/junos-versus-cisco-ios-mpls-and-ldp.html), and [*Junos Day One: MPLS behind the scenes*](https://blog.ipspace.net/2011/12/junos-day-one-mpls-behind-scenes.html).{{</note>}}

Ingress PE-routers use LSPs toward BGP next hops to send packets toward external destinations learned through BGP. The core router (C) thus receives labeled packet that it can switch toward the next hop without inspecting the destination IPv4 or IPv6 address, and thus there is no need to run BGP on C.

![](s400-BGP_FC_4.png)

The last core router might send labeled or unlabeled IP packet (due to [penultimate hop popping](https://blog.ipspace.net/2011/07/penultimate-hop-popping-php-demystified.html)) to the egress PE-router. You can [influence this behavior with **mpls ldp explicit- null**](https://www.ipspace.net/kb/tag/MPLS/Implicit_Explicit_NULL.html) configuration command.

#### Need help?

If you need a second opinion or a review of your MPLS or BGP design, check out the [ExpertExpress service](http://www.ipspace.net/ExpertExpress).