---
title: "Using VXLAN and EVPN to Build a WAN Network"
date: 2023-06-30 13:21:00
tags: [ EVPN, VXLAN, WAN, design ]
draft: True
---
do any of you have encountered edge fabric that uses leaf and spine with evpn vxlan? So for dc fabric we for sure used leaf and spine, but for edge fabric ( branches, internet, 3rd party connection, and cloud direct connect ) leafs will connect to ce routers. On our old dc edge fabric traditionally uses core-dist, but the old dc is not multitenant. the edge fabric and DC fabric then will be connected through border. So dc fabric border meets border edge
The reason for evpn leaf spine being:
IBgp peer between wan routers, internet router can leverage edge fabric even across dc. So that our dci can be pure layer 3. Dci is also used by dc fabric.
Didn't need to uses chassis distribution switch. Can use fixed size chassis so less blast radius.
Multitenancy so that different subsidiaries can be in it's own vrf easily with evpn

Yes, I’ve seen people using VXLAN in WAN, either with static ingress replication or EVPN. You can also use EVPN with MPLS transport.
People are also extending L2 networks between data centers with VXLAN/EVPN (not necessarily a good idea, but let’s not go there). If you want to do that then it doesn’t hurt if your switches can do VXLAN-to-VXLAN bridging:
https://blog.ipspace.net/2022/06/vxlan-bridging-dci.html
Finally, EVPN is probably mature enough to use as a pure L3VPN solution (I would run some tests first), so you could use it to build WAN multitenancy. However, you might have to figure out how to go from L2+L3 EVPN in the data center to L3-only WAN EVPN. Never tried to set that up.
