---
title: "Repost: Campus-Wide Wireless Roaming with EVPN"
date: 2024-04-22 08:05:00+0200
tags: [ IP routing, EVPN ]
---
As a response to my [LISP vs EVPN: Mobility in Campus Networks](https://blog.ipspace.net/2024/04/mobility-campus-networks-lisp-evpn.html) blog post, Route Abel [provided interesting real-life details](https://blog.ipspace.net/2024/04/mobility-campus-networks-lisp-evpn.html#2220) of a large-scale campus wireless testing using EVPN and VXLAN tunnels to a central aggregation point (slightly edited):

---

I was arguing for VxLAN EVPN with some of my peers, but I had no direct hands-on knowledge of how it would actually perform and very limited ability to lab it on hardware. My client was considering deploying Campus VxLAN, and they have one of the largest campuses in North America.
<!--more-->
Arista helped them test roaming on Campus EVPN. Here is the description from my contact at Arista.

Roaming and MAC moves across an EVPN/VxLAN environment were a concern to XXXX, and we had our PM & SysTest teams help address their concerns back in Oct 2022.

They simulated 60k clients across 2500 APs, and MAC moves at various frequencies; XXXX's client scale is closer to 30k for the Home Office.

Here are the highlights of our PM team's recommendations.

* **WiFi Data Path:** The recommendation is to use a VXLAN tunnel mode back to a pair of dedicated aggregation switches so the MAC moves do not update across the fabric.
* **WiFi VLAN:** Single or Multiple VLANs do not matter, as all the client traffic is tunneled to the aggregation switch pair.
* **Wired Design:** The Choice of L2 or L3 at access leaves does not matter for WiFi clients, as the MAC visibility is on the aggregation switch pair.
* **Roaming:** Seamless roaming across the entire campus without impacting any apps.
* **DHCP Broadcast/ mDNS**: DHCP broadcast will be flooded on the wired side from the aggregation switch pair. Need DHCP broadcast to unicast conversion on wireless.
