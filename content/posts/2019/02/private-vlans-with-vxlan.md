---
date: 2019-02-21 08:29:00+01:00
evpn_tag: details
tags:
- VXLAN
- data center
- EVPN
title: Private VLANs With VXLAN
url: /2019/02/private-vlans-with-vxlan.html
---
I got this remark from a reader after he read the [VXLAN and Q-in-Q blog post](/2019/01/q-in-q-support-in-multi-site-evpn.html):

> Another area with a feature gap with EVPN VXLAN is Private VLANs with VXLAN. They're not supported on either Nexus or Juniper switches.

I have one word on using private VLANs in 2019: Don't. They are messy and complicated to maintain (not to mention how exciting it gets to combine virtual and physical switches).
<!--more-->
Having said that, as EVPN supports Route Distinguishers and Route Targets, it should be possible to implement a 2-VRF hub-and-spoke VPN topology (like the one we described in the original *MPLS and VPN Architectures* book) and even configure inter-VRF routing on the hub device assuming the hardware supports VXLAN-to-VXLAN routing.

{{<note>}}Has anyone done that? I hope not. Is anything along these lines supported? I have no idea -- if you know more, please write a comment.{{</note>}}

Nonetheless, I strongly recommend using microsegmentation (ACLs in front of servers or virtual machines) in data center environments instead of Private VLANs, especially if you're running a virtualized environment.

{{<note>}}Hub-and-spoke VPN topologies in service provider networks are a different beast; you can't use microsegmentation there.{{</note>}}

---

Want to know more about VXLAN and EVPN? Why don't you:

-   Start with [Introduction to Virtual Networking](https://www.ipspace.net/Introduction_to_Virtualized_Networking) if you're just starting with network virtualization;
-   Watch [Networking in Private and Public Clouds](https://www.ipspace.net/Networking_in_Private_and_Public_Clouds) to understand the challenges we're trying to solve and explore various approaches to virtual networking;
-   Continue with a [deep dive into VXLAN](https://www.ipspace.net/VXLAN_Technical_Deep_Dive);
-   Conclude the journey with [EVPN deep dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive).
