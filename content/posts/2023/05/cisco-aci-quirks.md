---
title: "Dealing with Cisco ACI Quirks"
date: 2023-05-11 06:36:00
tags: [ fabric, ACI ]
---
Sebastian described an [interesting Cisco ACI quirk](https://blog.ipspace.net/2023/04/evpn-dynamic-mac-learning.html#1790) they had the privilege of chasing around:

> We've encountered VM connectivity issues after VM movements from one vPC leaf pair to a different vPC leaf pair with ACI. The issue did not occur immediately (due to ACI's bounce entries) and only sometimes, which made it very difficult to reproduce synthetically, but due to DRS and a large number of VMs it occurred frequently enough, that it was a serious problem for us.

Here's what they figured out:

> The problem was, that sometimes the COOP database entry (ACI's separate control plane for MACs and host addresses) was not updated correctly to point to the new leaf pair.

That definitely sounds like a bug, and Erik [mentioned in a later comment that it was probably fixed in the meantime](https://blog.ipspace.net/2023/04/evpn-dynamic-mac-learning.html#1799). However, the fun part was that things worked for almost 10 minutes after the VM migration:

> After the bounce entry on the old leaf pair expired (630 seconds by default), traffic to the VM was mostly blackholed, since remote endpoint learning is disabled on border leafs and always forwarded to the spines underlay IP address for proxying.

A *bounce entry* seems to be something like MPLS/VPN PIC Edge -- the original switch knows where the MAC address has moved to, and redirects the traffic to the new location. Just having that functionality makes me worried -- contrary to MPLS/VPN networks where you could have multiple paths to the same prefix (and thus know the backup path in advance), you need a bounce entry for a MAC address only when:

* The original edge device knows the new switch the moved MAC address is attached to
* Other fabric members haven't realized that yet.
* The interim state persists long enough to be worth the extra effort.

{{<note>}}On a tangential note, now I understand why Cisco had to build Network Assurance Engine -- a reassuringly expensive software solution that seemed to have one job when we [first heard about it during Cisco Live Europe 2018](https://blog.ipspace.net/2018/02/brief-recap-tech-field-day-at-cisco.html): making sure an ACI fabric works as expected.{{</note>}}

Anyway, the organization facing that problem decided to "solve" it by limiting VM migration to a single vPC pair:

> In the end we gave up and limited the VM migration domain to a single VPC leaf pair. VMware recommends a maximum number of 64 hosts per cluster anyway.

Having high-availability vSphere clusters and more than two leaf switches, and limiting the HA domain to a single pair of leafs, definitely degrades the resilience of the overall architecture, unless they decided to limit DRS (automatic VM migrations) to a subset of cluster nodes with VM affinity while retaining the benefits of having the high-availability cluster stretched across multiple leaf pairs. It's sad that one has to go down such paths to avoid vendor bugs caused by too much unnecessary complexity.

**Want to Know More About Cisco ACI?** _[Cisco ACI Introduction](https://www.ipspace.net/Cisco_ACI_Introduction)_ and _[Cisco ACI Deep Dive](https://www.ipspace.net/Cisco_ACI_Deep_Dive)_
Webinars are waiting for you ;)


