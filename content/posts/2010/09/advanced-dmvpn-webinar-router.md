---
date: 2010-09-21 07:03:00.008000+02:00
dmvpn_tag: training
tags:
- DMVPN
title: 'Advanced DMVPN Webinar: Router Configurations'
url: /2010/09/advanced-dmvpn-webinar-router.html
---
I included 12 sets of complete router configurations with the DMVPN webinar covering every single design scenario described in the webinar. The seven router lab topology emulates an enterprise DMVPN deployment with a redundant central site, a redundant remote site (with two routers) and two non-redundant remote sites (using two uplinks in a few scenarios). The seventh router emulates the Internet. The configurations can be used on any hardware (real or otherwise) supporting recent Cisco IOS software, allowing you to test and modify the design scenarios discussed in the webinar.

{{<figure src="https://www.ipspace.net/wk/images/a/a4/DMVPN_Physical_topology_IP_addressing.png">}}
<!--more-->
The router configurations cover the following scenarios:

-   DMVPN phase 1 without IPSec, using OSPF as the routing protocol;
-   DMVPN phase 1 with shared-key IPSec (OSPF routing);
-   DMVPN phase 2 with shared-key IPSec (OSPF routing);
-   DMVPN phase 2 with default routing toward central site (DMVPN in OSPF stub area);
-   DMVPN phase 2 with uplinks to two ISPs, no IPSec and tunnel route selection;
-   DMVPN phase 2 with uplinks to two ISPs and one or two Internet VRFs;
-   DMVPN phase 2 with ODR routing;
-   DMVPN phase 2 with one-way RIP routing (hub site is passive);
-   DMVPN phase 2 with two-tier central site with IPSec offload;
-   DMVPN phase 3 with dual-star ODR routing;
-   DMVPN phase 3 with multiple hubs in the same DMVPN cloud and mixed RIP+OSPF routing over DMVPN;
