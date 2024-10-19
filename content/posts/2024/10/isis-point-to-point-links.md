---
title: "Lab: Configure IS-IS on Point-to-Point Links"
series_title: "Configure IS-IS on Point-to-Point Links"
date: 2024-10-22 08:24:00+02:00
tags: [ IS-IS, netlab ]
netlab_tag: ignore
ISIS_tag: lab
redirect: https://isis.bgplabs.net/basic/3-p2p/
---
From a very high-level perspective, OSPF and IS-IS are quite similar. Both were created in the Stone Age of networking, and both differentiate between multi-access LAN segments and point-to-point serial interfaces. Unfortunately, that approach no longer works in the Ethernet Everywhere world where most of the point-to-point links look like LAN segments, so we always have to change the default settings to make an IGP work better.

That's what you'll do in [today's lab exercise](https://isis.bgplabs.net/basic/3-p2p/), which also explains the behind-the-scenes differences between point-to-point and multi-access links and the intricate world of three-way handshake.

{{<figure src="https://isis.bgplabs.net/basic/topology-frrouting.png">}}
