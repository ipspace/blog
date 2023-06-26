---
title: "Dataplane MAC Learning with EVPN"
date: 2023-09-18 06:34:00
draft: True
tags: [ EVPN, bridging ]
---
Johannes Resch submitted the following comment to https://blog.ipspace.net/2023/04/evpn-dynamic-mac-learning.html.

---

Interesting subject! I've also recently noticed some vendors claiming that dataplane MAC learning is so much better because it reduces the number of BGP updates in large scale SP EVPN deployments. Apparently, some of them are working on IETF drafts to bring dataplane MAC learning "back" to EVPN. Not sure if this is really a relevant point - we know that BGP scales nicely, and its relatively easy to deploy virtualized RR with sufficient VPU resources.
