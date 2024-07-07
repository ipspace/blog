---
date: 2015-09-14 09:27:00+02:00
lastmod: 2022-03-31 16:03:00
tags:
- VXLAN
- data center
title: VXLAN Hardware Gateway Overview
url: /2015/09/vxlan-hardware-gateway-overview/
---
One of my readers stumbled upon blog post from 2011 explaining the potential implementations of VXLAN hardware gateways, and asked me if that information is still relevant.

I knew that I'd included tons of information in the [Data Center Fabrics](http://www.ipspace.net/Data_Center_Fabrics) and [VXLAN Deep Dive](http://www.ipspace.net/VXLAN_Technical_Deep_Dive) webinars, but couldn't find anything on the web, so I decided to fix that in 2015.
<!--more-->
## 2020 Update

As expected, the information published in 2015 did not age well. Here's a short summary of the current state of data center switches; you might still find some useful information in the rest of the blog post.

* Data center switches from all major vendors support VXLAN.
* Arista, Cisco, Cumulus, and Juniper support EVPN control plane, multicast-based VXLAN, and statically configured ingress replication. I did not check HP or Dell, and Brocade is gone anyway.
* Multicast-based VXLAN became a niche solution. While you can still configure static ingress replication lists, everyone is pushing EVPN control plane.
* VXLAN routing is available on switches using vendor silicon (most Cisco Nexus switches, Juniper QFX10K), and on switches using the following merchant silicon: Trident-2+, Trident-3 or later, Jericho (deep buffer), Mellanox Spectrum. Broadcom Tomahawk does not support VXLAN routing; switch vendors might use tricks like recirculation or multi-stage switching to get it done (more info in the updated VXLAN webinar).
* OVSDB is obsolete, as is VMware NSX-V. VMware NSX-T integration with hardware gateways uses EVPN.

Have I missed something? Please leave a comment!

## Original Blog Post

Here's a brief overview of what individual vendors' hardware gateways (ToR switches) can or cannot do (to the best of my knowledge).

| Vendor | Multicast VXLAN | OVSDB | VXLAN Routing | EVPN |
|--------|:---------------:|:-----:|:-------------:|:----:|
| Arista |          ✅     |   ✅  | 7150 only     |      |
| Brocade|                 |   ✅  |               |      |
| Cisco  |          ✅     |   ✅  |  ✅      | Nexus 7K/9K |
| Citrix Netscaler |✅     |       |               |      |
| Cumulus |                |   ✅  |               |      |
| Dell   |                 |   ✅  |               |      |
| F5 BIG-IP |       ✅     |   ✅  |  ✅          |       |
| HP     |      ✅ (\*)    |   ✅ (\*) |  ✅      |       |
| Juniper|      ✅ (\*)    |   ✅  | MX and EX9200 |       |
{.fmtTable}

### Notes

-   Nuage (or Alcatel Lucent) has Virtualized Services Gateway, which is another VXLAN gateway, but as I couldn't find any documentation on Nuage or Alcatel Lucent web site (and the VSP documentation is behind a regwall), it's not on the list. [Five years later](/2010/09/hiding-documentation-will-they-never/), some vendors still haven't got the memo.
-   A10 Networks is another vendor who hasn\'t got that same memo yet.
-   HP has VXLAN support on several Data Center switches, but according to the configuration guide(s) at the moment only 5930 supports multicast VXLAN and OVSDB. Please check HP documentation for up-to-date status;
-   Juniper QFX5100, QFX10K, EX9200 and MX routers support VXLAN and OVSDB. QFX10K does not support multicast VXLAN (yet). Only EX9200 and MX routers support VXLAN routing.
-   Multicast VXLAN support allows ToR switch to interact with Cisco Nexus 1000V and pre-NSX VMware VXLAN implementations;
-   OVSDB is the protocol used by VMware NSX for Multiple Hypervisors to configure ToR switches. We don't know yet what VMware will use when support for hardware gateways will be added to NSX for vSphere, but I wouldn't be surprised if they were to use OVSDB;
-   VXLAN routing is tricky -- more details [here](/2014/07/layer-3-switching-over-vxlan-revisited/) and [here](/2015/03/video-routing-over-vxlan/);
-   EVPN control plane enables large L2 fabrics built on top of VXLAN and controller federation;

For more details, go watch the two webinars (links above).
