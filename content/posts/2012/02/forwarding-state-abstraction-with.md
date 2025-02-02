---
date: 2012-02-01 06:56:00+01:00
tags:
- MPLS
- switching
- workshop
- TRILL
- virtualization
title: Forwarding State Abstraction with Tunneling and Labeling
url: /2012/02/forwarding-state-abstraction-with/
---
Yesterday I described how the [limited flow setup rates offered by most commercially-available switches](/2012/01/fib-update-challenges-in-openflow/) force the developers of [production-grade OpenFlow controllers](http://www.necam.com/pflow/) to [drop the microflow ideas](http://www.cmlab.csie.ntu.edu.tw/~kenneth/qing2011/paper/6.pdf) and focus on state abstraction ([people living in a dreamland usually go in a totally opposite direction](/2011/10/openflow-and-state-explosion/)). Before going into OpenFlow-specific details, let's review the existing forwarding state abstraction technologies.
<!--more-->
### A Mostly Theoretical Detour

Most forwarding state abstraction solutions that I'm aware of (and I'm positive Petr Lapukhov will give me tons of useful pointers to a completely different universe) use a variant of *Forwarding Equivalence Class* (FEC) concept from MPLS:

-   All the traffic that expects the same forwarding behavior gets the same label;
-   The intermediate nodes no longer have to inspect the individual packet/frame headers; they forward the traffic solely based on the FEC indicated by the label.

The grouping/labeling operation thus [greatly reduces the forwarding state in the core nodes](/2012/01/bgp-free-service-provider-core-in/) (you can call them P-routers, backbone bridges, or whatever other terminology you prefer) and improves the core network convergence due to significantly reduced number of forwarding entries in the core nodes.

{{<figure src="/2012/02/s1600-MPLS_Forwarding.png" caption="MPLS forwarding diagram from the [Enterprise MPLS/VPN Deployment webinar](http://www.ipspace.net/Enterprise_MPLS_VPN_Deployment)">}}

The core network convergence is improved due to *reduced state* not due to *pre-computed alternate paths* that [Prefix-Independent Convergence](/2012/01/prefix-independent-convergence-pic/) or MPLS Fast Reroute uses.

### From Theory to Practice

There are two well-known techniques you can use to transport traffic grouped in a FEC across the network core: [tunneling and virtual circuits](/2011/10/mpls-is-not-tunneling/) (or *Label Switched Paths* if you want to use non-ITU terminology).

When you use ***tunneling***, the FEC is the tunnel endpoint -- all traffic going to the same tunnel egress node uses the same tunnel destination address.

All sorts of tunneling mechanisms have been proposed to scale layer-2 broadcast domains and virtualized networks (IP-based layer-3 networks scale way better by design):

{{<note warn>}}As of February 2022 (when I updated this blog post), vCDNI and NVGRE are long gone, and SPBM and TRILL are mostly obsolete. Everyone is using VXLAN or Geneve.{{</note>}}

-   [Provider Backbone Bridges](http://en.wikipedia.org/wiki/IEEE_802.1ah-2008) (PBB -- 802.1ah), [Shortest Path Bridging-MAC](http://en.wikipedia.org/wiki/Shortest_Path_Bridging#Shortest_Path_Bridging-MAC_-_SPBM) (SPBM -- 802.1aq) and [vCDNI](/2011/04/vcloud-director-networking/) use MAC-in-MAC tunneling -- the destination MAC address used to forward user traffic across the network core is the egress bridge or the destination physical server (for vCDNI).

{{<figure src="/2012/02/s1600-SPBM_Forwarding.png" caption="SPBM forwarding diagram from the [Data Center 3.0 for Networking Engineers](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers) webinar">}}

-   [VXLAN](/2011/08/finally-mac-over-ip-based-vcloud/), NVGRE and [GRE (used by Open vSwitch)](/2011/10/what-is-nicira-really-up-to/) use MAC-over-IP tunneling, which scales way better than MAC-over-MAC tunneling because the core switches can do another layer of state abstraction (subnet-based forwarding and IP prefix aggregation).

{{<figure src="/2012/02/s1600-vXLAN-Typical-Architecture.png" caption="Typical VXLAN architecture - from the [Introduction to Virtual Networking](http://www.ipspace.net/Introduction_to_Virtualized_Networking) webinar">}}

-   [TRILL](http://en.wikipedia.org/wiki/TRILL) is closer to VXLAN/NVGRE than to SPB/vCDNI as it [uses full L3 tunneling between TRILL endpoints](/2010/08/trill-and-8021aq-are-like-apples-and/) with L3 forwarding inside RBridges and L2 forwarding between RBridges.

{{<figure src="/2012/02/s1600-TRILL_Forwarding.png" caption="TRILL forwarding diagram from the [Data Center 3.0 for Networking Engineers](http://www.ipspace.net/Data_Center_3.0_for_Networking_Engineers) webinar">}}

With ***tagging*** or ***labeling*** a short tag is attached in front of the data (ATM VPI/VCI, MPLS label stack on point-to-point links) or somewhere in the header (VLAN tags) instead of encapsulating the user's data into a full L2/L3 header. The core network devices perform packet/frame forwarding based exclusively on the tags. That's how [SPBV](http://en.wikipedia.org/wiki/Shortest_Path_Bridging#Shortest_Path_Bridging-VID_-_SPBV), MPLS and ATM work.

{{<figure src="/2012/02/s1600-MPLS_Frame_Format.png" caption="MPLS-over-Ethernet frame format from the [Enterprise MPLS/VPN Deployment webinar](http://www.ipspace.net/Enterprise_MPLS_VPN_Deployment)">}}

MPLS-over-Ethernet commonly used in today's high-speed networks is an abomination as it uses both L2 tunneling between adjacent LSRs and labeling \... but that's what you get when you have to reuse existing hardware to support new technologies.

{{<next-in-series page="/posts/2012/02/virtual-circuits-in-openflow-10-world.md" />}}

### Revision History

2022-02-16
: Cleaned up the blog post and added a note listing the obsolete technologies.

