---
date: 2021-06-21 06:06:00+00:00
evpn_tag: intro
tags:
- data center
- bridging
- EVPN
title: Comparing EVPN with Flood-and-Learn Fabrics
---
One of ipSpace.net subscribers sent me this question after watching the _[EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)_ webinar:

> Do you have a writeup that compares and contrasts the hardware resource utilization when one uses flood-and-learn or BGP EVPN in a leaf-and-spine network?

I don't... so let's fix that omission. In this blog post we'll focus on pure layer-2 forwarding (aka *[bridging](/2011/02/how-did-we-ever-get-into-this-switching/)*), a follow-up blog post will describe the implications of adding EVPN IP functionality.
<!--more-->
We'll compare the traditional bridging (using MLAG) with VXLAN-based bridging using IP multicast in the underlay, head-end replication, or EVPN control plane. We'll stay at a pretty high level because it's [impossible to get the hardware documentation for switching ASICs](/2016/05/what-are-problems-with-broadcom/), and because the details always depend on the specific ASIC, [software vendor’s use of ASIC resources](/2021/02/rant-broadcom-nos-vendors/), quality of ASIC vendor SDK… and I’m definitely not touching those cans of worms.

---

[Pete Lumbis](https://www.ipspace.net/Author:Pete_Lumbis) and [Dinesh Dutt](https://www.ipspace.net/Author:Dinesh_Dutt) helped me figure out or confirmed some of the details. Thanks a million!

---

Every bridging implementation needs two data structures:

* Interfaces (links)
* MAC table (or tables)

An implementation might use a single MAC table or different MAC tables for unicast and multicast forwarding[^1]. In any case, MAC tables on edge switches are not changed regardless of what forwarding mechanism you use -- the edge switches still have to know the MAC addresses of all nodes attached to configured VLANs.

There's a major difference in MAC table utilization on core switches: 

* In traditional bridging implementation, the core switches must know all MAC addresses of all nodes in the network;
* When using VXLAN, SPB, or TRILL, the core switches know the IP- or MAC addresses of edge switches, but are not aware of edge devices.

Traditional bridging, VXLAN (without EVPN), SPB, or TRILL use dynamic MAC learning, so there's no control-plane difference between them. EVPN uses BGP to propagate MAC addresses, but only across the network. Local MAC addresses are still gathered with the flood-and-learn mechanism. In any case, learning MAC addresses is a control-plane functionality and does not affect the hardware resources (apart from the CPU load incurred).

Finally, there's flooding. Every bridging implementation must support flooding. An EVPN implementation could *optimize* flooding behavior with functionality like *proxy ARP* or *no unknown unicast flooding*, but as long as you want to retain [transparent bridging semantics](/2010/07/bridges-kludge-that-shouldnt-exist/) to support [broken crapware](/2018/01/revisited-need-for-stretched-vlans/), you have to implement flooding.

Hardware-based multicast is often implemented with a bitmask of outgoing interfaces attached to a multicast MAC address. In traditional bridging and other methods that use underlay packet replication (SPB, TRILL, VXLAN with IP multicast), there's a single uplink interface per VLAN, and there's absolutely no difference between the uplink interface being a physical uplink (STP), port channel (STP+MLAG) or VXLAN tunnel with a multicast destination address.

Head-end (ingress node) replication uses more hardware resources. VTEP tunnels are usually implemented with virtual interfaces, and every multicast entry (remember: broadcast is just a particular kind of multicast) contains numerous outgoing interfaces (VTEP tunnels)... but still: all you need for ingress replication (as opposed to traditional bridging) is a longer bitmask. Every decent data center switching ASIC supports at least 128 remote VTEPs per VNI -- problem solved unless you're building a huge fabric.

**Long story short**: there's no significant difference in hardware resource utilization on edge switches. Bridging is bridging, no matter how it's implemented.

For more bridging-versus-routing details, watch the _[Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101)_ part of _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar.

[^1]: From the packet forwarding perspective, broadcast is just a very specific case of multicast. Unknown unicast flooding is a specific case of broadcast.