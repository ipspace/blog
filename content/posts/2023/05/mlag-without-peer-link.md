---
date: 2023-05-11 07:54:00+00:00
mlag_tag: evpn
series:
- mlag
tags: [ switching, VXLAN ]
title: MLAG Clusters without a Physical Peer Link
---
With the widespread deployment of Ethernet-over-something technologies, it became possible to build MLAG clusters without a physical peer link, replacing it with a virtual link across the core fabric. Avaya was one of the first vendors to implement virtual peer links with Provider Backbone Bridging (PBB) transport, and some data center switching vendors (example: Cisco) offer similar functionality with VXLAN transport.

Removing a physical peer link allows you to build a perfectly symmetrical physical fabric in which the leaf roles are determined exclusively by the device configuration. As always, the devil is in the details -- a vendor implementing a virtual peer link must address these challenges:
<!--more-->
-   Neighbor loss detection
-   Peer link traffic filters
-   Redirection of traffic sent to the wrong member of the MLAG cluster

{{<figure src="/2023/05/MLAG-virtual-peer-link.png" caption="MLAG cluster with a virtual peer link over VXLAN fabric">}}

{{<note info>}}This blog post assumes the VXLAN (or PBB) fabric uses dynamic MAC learning. We'll discuss the implications of the EVPN control plane in the next blog post. Please note that some vendors support virtual peer-link only with the EVPN control plane.{{</note>}}

{{<tldr model="somewhat excited ChatGPT GPT-4" comment="The regular summary sounded like an abstract of a research paper written by a team of terminally-bored people. Had to tell ChatGPT to spice it up a notch (you don't want to know how cheerleading the 'excited' summary was 😆).">}}Embracing virtual peer links transforms MLAG clusters by achieving symmetrical physical fabric. While these innovations present enticing possibilities, they also introduce challenges in neighbor loss detection, traffic filtering, and redirection. To navigate these complexities, some vendors smartly leverage the EVPN control plane for smoother implementation.{{</tldr>}}

## Neighbor Loss Detection

It's hard to figure out the majority of the cluster in case of cluster partitioning if it only has two nodes. Traditional MLAG implementations tried to address that with a combination of peer link and a fabric keepalive protocol running across the core fabric.

Implementations using a virtual peer link no longer have two independent paths to the other members of the MLAG cluster, making it harder to make a reliable neighbor-or-fabric-loss detection. Typical workarounds include:

-   Running MLAG keepalive protocol over the out-of-band management network
-   Monitoring the state of the uplinks and assuming the loss of MLAG keepalive means loss of MLAG peer[^OU] if a switch has at least some operational uplinks.

[^OU]: You could also be facing a partitioned core fabric, where you'd have to deal with a much larger problem than an MLAG cluster split brain.

Regardless of how the vendors implement MLAG neighbor loss detection, it's inevitably less reliable than using a physical link bundle as a peer link -- we're dealing with a scenario similar to [stretching a firewall cluster across multiple data centers](https://blog.ipspace.net/2011/04/distributed-firewalls-how-badly-do-you.html).

## Peer Link Traffic Filters

Traditional MLAG implementations [use access control lists on links belonging to multi-chassis link aggregation groups](https://blog.ipspace.net/2022/06/mlag-deep-dive-flooding.html) to ensure an MLAG cluster member never sends traffic received over a peer link to a dual-attached node. For example, when X in the above diagram sends a broadcast ARP request, the packet received by S2 over the peer link should be forwarded to Y but not B (because S1 already sent the packet to B).

Vendors usually implement those access control lists by checking the incoming interface (peer link), which is harder to do when dealing with a virtual peer link. A VXLAN-encapsulated packet S2 receives from S1 is almost identical to a VXLAN-encapsulated packet Sx sends when forwarding an ARP request from Z.

There are three obvious ways to emulate the traditional peer link behavior:

-   Match the source underlay address (VTEP for VXLAN, core MAC address for PBB/SPB). This is the approach recommended in [RFC 8365](https://datatracker.ietf.org/doc/html/rfc8365#section-8.3.1). Cisco Cloud ASICs[^CS] seem to be using it in vPC Fabric Peering -- they require a dedicated loopback IP address for the peer link.
-   Use a different VXLAN VNI (or SPB SID) for VLANs traffic transported over the peer link, which might (depending on hardware implementation) reduce the total number of switching domains.
-   Use one of the reserved bits in VXLAN header to indicate another member of the MLAG cluster sent the packet the over the virtual peer link.

The mechanism a vendor can use is limited by the hardware capabilities. Unfortunately, I couldn't find anything that would help me understand what's going on behind the scenes; feedback is (as always) most welcome.

[^CS]: I'm mentioning Cisco Nexus switches because Cisco has the best-documented scalability limits, and some reasonably-good _packet walks_ presentations.

## Traffic Redirection

As discussed in the [MLAG-with-VXLAN](https://blog.ipspace.net/2022/09/mlag-deep-dive-vxlan-fabric.html) part of this series, we must use anycast VTEP addresses if we want to rely on dynamic learning of source MAC addresses of encapsulated MAC frames. That approach inevitably results in some traffic arriving at the wrong member of the MLAG cluster.

Traditional MLAG solutions forward the misdirected traffic onto the peer link. When using a virtual peer link, the switch receiving the traffic has to redirect it back into the overlay network, requiring packet recirculation or hardware support for [VXLAN-to-VXLAN (or PBB-to-PBB) bridging](https://blog.ipspace.net/2022/06/vxlan-bridging-dci.html).

## In a Nutshell

Virtual peer link is an excellent solution from the fabric design perspective but a nightmare to implement correctly. No wonder some vendors only support it with the EVPN control plane.

For more details, watch the *[EVPN Multihoming versus MLAG](https://my.ipspace.net/bin/list?id=EVPN#MH)* part of the _[EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)_ webinar.

## Just in Case You Got This Far ;)

Here's the excited (aka Kool-Aid) summary generated by ChatGPT 🤣

> Unleashing the power of virtual peer links, MLAG clusters are revolutionized with symmetrical physical fabric! Despite the thrilling potential, this game-changer grapples with challenges like neighbor loss detection, traffic filtering, and redirection. But fear not, as some vendors heroically conquer these hurdles by harnessing the EVPN control plane!
