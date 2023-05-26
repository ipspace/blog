---
index: true
kb_section: Layer3Fabrics
minimal_sidebar: true
title: Redundant Layer-3-Only Data Center Fabrics
toc_title: Overview
url: /kb/Layer3Fabrics/
kb_tag: dc
---
I’m often getting the same question when delivering online courses or webinars focused on data center fabrics or cloud infrastructure:

> Is it possible to build a **redundant** layer-3-only fabric with no VLANs stretched across multi switches, and use X (for example, VMware NSX) on such a fabric?

{{<figure src="Nonredundant-L3-Fabric.png" caption="Layer-3-only fabric... without redundant server connections<br />Source: [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)">}}

In this document, we’ll explore the problem of using multiple IP addresses from same or different subnets on clients or servers. Using loopback addresses and routing on servers (the usual solution) is outside of the scope of this document, explore [Routing on Servers](https://my.ipspace.net/bin/list?id=Clos#ROUTING_SERVERS) part of [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar for more details.

You can find the in-depth description of various fabric-based workarounds in [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar (in particular in the [EVPN Multihoming versus MLAG](https://my.ipspace.net/bin/list?id=EVPN#MH) section).

Before moving on, a quick spoiler: while iSCSI Multipath I/O in vSphere supports layer-3-only fabrics (and even full path separation between A and B networks), [the designers of VMware NSX never got the memo](https://blog.ipspace.net/2020/02/do-we-need-complex-data-center-switches.html).
