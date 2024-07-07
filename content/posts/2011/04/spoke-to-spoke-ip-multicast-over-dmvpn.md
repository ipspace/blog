---
date: 2011-04-20 07:35:00+02:00
dmvpn_tag: integrate
tags:
- DMVPN
- multicast
title: Spoke-to-Spoke IP Multicast over DMVPN?
url: /2011/04/spoke-to-spoke-ip-multicast-over-dmvpn/
---
A long-time reader has sent me an intriguing question: "would IP multicast work between DMVPN spokes?" In theory, the answer is "we could make it work", but we all know theory and practice are [not the same thing](http://en.wikiquote.org/wiki/Fact_and_theory).

To make IP multicast work between DMVPN spokes, you'd need to configure multicast propagation between them with the **ip nhrp map multicast** ***remote-spoke-NBMA*** command. In a small DMVPN network where you need IP multicast only between a handful of spokes, that might even work; obviously this trick does not scale for a number of reasons:
<!--more-->
-   Full-mesh manual configuration of multicast maps is required on spoke routers;
-   You'd have to change configurations on many spoke routers every time you add a spoke router;
-   Spoke NBMA (public-facing) addresses would have to be fixed. No more DHCP-addressed CPE devices.
-   Having a tool that would ensure you actually have a full-mesh configured would be extremely handy (hint: configuration automation). Missing multicast maps would be extremely fun to troubleshoot (not to mention the obvious increase in your job security);
-   The multicast maps would cause spoke-to-spoke IPsec sessions to be established immediately, resulting in a full mesh of IPsec sessions;
-   Multicast replication on spoke routers might become a (CPU) problem if you use low-end platforms as spoke routers;
-   Routing protocol updates would be sent over all those multicast maps, resulting in even more work for the spoke routers.

Obviously this "solution" belongs to the "_just because you could doesn't mean that you should_" department, but sometimes we're forced to do weird things to implement something our design was never meant to support. Did you ever have to deploy IP multicast over DMVPN? What's your experience?
