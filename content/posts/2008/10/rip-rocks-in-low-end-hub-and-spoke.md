---
date: 2008-10-01 06:49:00.001000+02:00
ospf_tag: dmvpn
tags:
- OSPF
- RIP
title: RIP Rocks in Low-End Hub-and-Spoke Networks
url: /2008/10/rip-rocks-in-low-end-hub-and-spoke.html
---
Yesterday, I introduced a scenario where [RIP would (in my opinion) work much better than OSPF](https://blog.ipspace.net/2008/09/why-is-rip-still-kicking.html). If you were not persuaded by the "[management-level](http://en.wikipedia.org/wiki/Pointy-Haired_Boss)" arguments, let's focus on the technical details (but make sure you [read the scenario](https://blog.ipspace.net/2008/09/why-is-rip-still-kicking.html) first).

All you ever want to advertise to the remote sites in this design is the default route (or a network-wide summary). Alternatively, you might want to advertise only a route to a central LAN or server. Both requirements are easily met with RIP per-interface output filters. Doing something similar with OSPF is close to impossible. Either you place every remote site into a separate OSPF area (don't even think about doing it; there could be hundreds of sites), or the routes within an area will leak between the remote sites.

RIP is also more stable than OSPF in this setup. Whenever a remote site disappears, the change in the OSPF area is unnecessarily propagated to all other remote sites in the same area. RIP doesn't propagate the topology change; the central site's output route filter stops all unnecessary updates.

As you know, OSPF requires hello packets and adjacencies to work correctly. Therefore, the central hub router must track the adjacency states of hundreds of neighbors. When using RIP, the central router couldn't care less ... it sends out its routes every so often, collects whatever comes back, and reports when a new remote route is received, or an old one disappears.

