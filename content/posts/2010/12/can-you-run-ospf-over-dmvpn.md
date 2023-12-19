---
date: 2010-12-22 07:21:00+01:00
dmvpn_tag: routing
ospf_tag: dmvpn
tags:
- DMVPN
- OSPF
title: Can You Run OSPF over DMVPN?
url: /2010/12/can-you-run-ospf-over-dmvpn.html
---
Ian sent me a really good OSPF-over-DMVPN question after watching my [DMVPN webinar](https://www.ipspace.net/DMVPN):

> In the DMVPN webinar you discuss OSPF design and configuration. However, Cisco design guide says you should use a different routing protocol from what you use on your LAN but you seem to suggest it is okay to extend your OSPF network out to the DMVPN edge by continuing to use OSPF albeit in a different area.

The main issue you face when running OSPF over DMVPN is scalability: OSPF does not scale as well as other routing protocols when used over DMVPN.
<!--more-->
Because OSPF is a link-state protocol, the topology database of every spoke router has to contain full topology of the DMVPN area (and LSAs for all IP prefixes inserted into the area by ABRs) and if you believe a low-end router cannot handle more than 50 routers in an OSPF area (that's the "classic" OSPF design recipe), you see how limited we are. Furthermore, DMVPN cloud has to be a single subnet, so all the spoke routers attached to the same DMVPN cloud have to be in the same OSPF area.

{{<note info>}}You can implement [OSPF flood reduction](https://blog.ipspace.net/2010/01/ospf-flooding-filters-in-hub-and-spoke.html) on the hub router in combination with reliable static default routing on the spokes to increase OSPF scalability.{{</note>}}

You can make things a bit better by making the DMVPN area totally stubby (in which case you need Internet VRF for Phase 2 DMVPN), so at least the changes in the non-DMVPN part of the network are not causing SPFs (or partial SPFs).

According to now-gone Cisco's presentations, the number of spoke sites in an OSPF-based DMVPN can be pushed to low hundreds, while you can go above 500 with EIGRP and above 1000 with passive RIP or BGP

### Summary

OSPF over DMVPN works just fine as long as the number of spoke sites is low (I would keep it below 100, but it obviously depends on the CPU capabilities of the platform you're using for the spoke sites). Keep the DMVPN subnet in a separate area and make that area a stub or totally stubby area. If you have more spoke sites, it makes more sense to go with a distance vector protocol and redistribution.
