---
date: 2015-10-12 08:27:00+02:00
dmvpn_tag: routing
tags:
- DMVPN
- IP routing
title: DMVPN Split Default Routing
url: /2015/10/dmvpn-split-default-routing.html
---
[SD-WAN](/2015/06/software-defined-wanwell-orchestrated.html) is [all the rage](/2015/07/some-ridiculous-sd-wan-claims.html) these days (at least according to software-defined pundits), but networking engineers still build DMVPN networks, even though they are supposedly impossibly-hard-to-configure [Rube Goldberg](https://en.wikipedia.org/wiki/Rube_Goldberg_machine) machinery.

To be honest, DMVPN is not the easiest technology Cisco ever developed, and there are plenty of gotchas, including the problem of default routing in Phase 2/3 DMVPN networks.
<!--more-->
### The Problem

In DMVPN [Phase 2](/2011/01/dmvpn-phase-2-fundamentals.html) or [Phase 3](/2014/03/the-fundamental-difference-between.html) designs a spoke site exchanges encrypted traffic directly with another spoke site. As we usually don't know the IP addresses of other remote sites in advance, we solve the remote spoke site reachability problem with a default route on the spoke routers pointing to the Internet uplink.

On the other hand, we might want to use a default route throughout the corporate WAN network, be it to simplify routing or to attract all user-generated Internet traffic to the central site for inspection.

{{<figure src="/2015/10/s520-DMVPN_Split_Default_Problem.png">}}

The above picture clearly illustrates the problem we're dealing with -- different types of traffic (user traffic versus DMVPN-encapsulated WAN traffic) use different default routes. While you could use PBR to meet this requirement, I'd strongly discourage that -- who knows how PBR applied to GRE/IPsec traffic works on platforms that implement IPsec encryption and/or DMVPN encapsulation in hardware.

### The Solution

There's a much cleaner solution: create a transport VRF with its own routing table and its own default route, and assign the Internet uplink to the transport VRF. The default route used in the transport (Internet) VRF is totally independent from the default route used by the user (or other router-generated) traffic. Problem solved.

{{<figure src="/2015/10/s520-DMVPN_Split_Default_Solution.png">}}

Well, there are (as always) a few other bits-and-pieces you have to configure. You have to associate the new VRF with the transport functionality of the DMVPN tunnel, and move the IKE/IPsec functionality to the VRF (Cisco's IPsec documentation calls this *front door VRF -- FVRF*). You'll find the necessary details in Cisco's online documentation or in [my DMVPN webinars](http://www.ipspace.net/DMVPN_trilogy) (which include [fully-tested router configurations](/2010/09/advanced-dmvpn-webinar-router.html)).

{{<note warn>}}
SD-WAN solutions use exactly the same tricks (we don\'t know whether they use multiple routing tables or PBR because they hide the details), the only difference is a [nice orchestration UI](/2015/07/routing-protocols-and-sd-wan-apples-and.html) used by most SDN solutions as opposed to CLI syntax that has grown organically over the last 30 years.
{{</note>}}
