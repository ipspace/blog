---
title: "Combining MLAG Clusters with VXLAN Fabric"
date: 2022-09-28 07:58:00
tags: [ switching,vxlan ]
series: mlag
mlag_tag: deepdive
---
In the previous MLAG Deep Dive blog posts we discussed the innards of a standalone MLAG cluster. Now let's see what happens when we connect such a cluster to a VXLAN fabric -- we'll use our standard MLAG topology and add a VXLAN transport underlay to it with another switch connected to the other end of the underlay network.

{{<figure src="/2022/09/MLAG-VXLAN-topology.jpg" caption="MLAG cluster connected to a VXLAN fabric">}}
<!--more-->
A few notes before we get to the cumbersome details:

* We still need the peer link between the MLAG cluster members. Replacing the peer link with a virtual link over the VXLAN fabric is another interesting topic that we'll deal with some other time.
* Connecting MLAG clusters in a [traditional bridging fabric](https://blog.ipspace.net/2022/09/mlag-bridging-evpn.html) is boring. Every MLAG cluster looks like a dual-homed host to adjacent clusters.
* Considerations similar to the ones described in this blog post apply to other transport technologies (TRILL, SPBM) or [proprietary fabric solutions](https://blog.ipspace.net/2022/05/cisco-fabric-path-and-friends.html), but we won't discuss them because those technologies aren't exactly mainstream anymore.

### Dynamic MAC Learning Ruins the Day

In a typical VXLAN-based fabric, we'd assign a unique VXLAN tunnel endpoint (VTEP) IP address to every leaf switch. That approach does not work for MLAG clusters *if we want to rely on dynamic MAC learning instead of using EVPN control plane*.

Imagine host A having a lot of TCP or UDP sessions with host Z:

* If the host A uses the typical 5-tuple hashing algorithm, it will probably use both uplinks (toward S1 and S2) to send Ethernet frames to Z.
* Ethernet frames with the same source MAC address (A) will be encapsulated into VXLAN frames on S1 and S2 and sent toward Sx.
* Sx might receive frames from the same source MAC address coming from two different source VTEPs (S1 and S2). That will totally confuse Sx if it uses dynamic MAC learning to build MAC-to-VTEP mapping tables

**Conclusion**: S1 and S2 must use the same source IP address when encapsulating the traffic coming from a dual-attached host.

**Aside**: The requirement to use an anycast VTEP IP address complicates the device configuration. VTEP IP address is usually attached to a loopback interface, and IP addresses configured on loopback interfaces are commonly used to set OSPF or BGP router ID.

Having two routers with the same router ID in a network running a link-state routing protocol produces interesting results. To alleviate that pitfall, vendors usually recommend configuring two loopback interfaces[^SSH], and using a static IGP router ID to ensure the automatic process doesn't select the VTEP loopback interface as the source of router ID.

[^SSH]: In case you need a stable unique IP address per box.

**Back to VXLAN**. The use of anycast VTEP IP address has an interesting side effect: load balancing works out of the box. S1 and S2 are advertising the same IP address with the same cost, and assuming the VXLAN transport network uses a leaf-and-spine topology, traffic from host Z to host A uses both switches (based on the source UDP port in the VXLAN packets).

### Orphan Hosts

Orphan hosts are (as always) a source of pain. Imagine host X communicating with host Z:

* The traffic from X to Z will be encapsulated in VXLAN packets with anycast VTEP source IP address.
* Sx will use the anycast VTEP IP address to send the traffic from Z to X, and approximately half of those packets will end on the wrong egress switch (S2).
* S2 will have to use the peer link to send the packets received over the VXLAN fabric to X.

There's a simple solution to this conundrum: use a different source VTEP IP address when encapsulating Ethernet packets received from orphan hosts. To do that, your ASIC has to support:

* Multiple destination VTEP addresses per switch -- one for dual-attached hosts, another one for orphan hosts[^CPIP]
* Selecting the source VTEP address based on the ingress interface.

[^CPIP]: It looks like the ASICs used in Cisco Nexus switches can do that -- this is exactly the functionality required for their EVPN vPC Multihoming implementation.

Looking at various VXLAN implementations, it seems like the above requirements aren't exactly a walk in the park. Obviously we don't know what data center switch ASICs can do ([thanks a million](https://blog.ipspace.net/2016/05/what-are-problems-with-broadcom.html), Broadcom, NVIDIA and friends), and people who could answer that question are not allowed to, but if you could say something without violating an NDA signed in blood, or send me an anonymous hint, you'd be most welcome. 

Finally, this is the perfect moment for EVPN pundits to tell me how all the problems I just described get solved with EVPN multihoming. That's not exactly true, and we'll discuss the nuances in the next blog post in this series.

{{<next-in-series page="/posts/mlag-deep-dive-evpn-multihoming.md" />}}
