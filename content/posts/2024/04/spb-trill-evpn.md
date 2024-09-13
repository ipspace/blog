---
title: "Why Are We Using EVPN Instead of SPB or TRILL?"
date: 2024-04-05 08:17:00+0200
tags: [ bridging, fabric, EVPN ]
series_weight: 420
evpn_tag: intro
---
Dan left an [interesting comment](/2024/03/arista-interface-ebgp/#2153) on one of my [previous blog posts](/2024/03/arista-interface-ebgp/):

> It strikes me that the entire industry lost out when we didn't do SPB or TRILL. Specifically, I like how Avaya did SPB.

Oh, we did TRILL. [Three vendors](/2022/05/cisco-fabric-path-and-friends/) did it in different [proprietary ways](/2011/03/dont-lie-about-proprietary-protocols/), but I'm digressing.
<!--more-->
TRILL [was a zombie](/2012/08/the-state-of-trill/) the moment VXLAN appeared. TRILL requires new chipsets _on every switch in the path_ whereas VXLAN runs over IP. Apart from slightly shorter packet headers, it provided nothing IP had not had for decades.

SPB was a mess. They couldn't decide whether to use VLAN tags or PBB header for extra encapsulation, resulting in SPBM and SPBV. In the end, only SPBM remained, but the damage had already been done.

SPB's development in IEEE (instead of IETF) didn't help either. The IEEE standardization process reeks of CCITT (remember the guys creating X.25?), it was either hard or impossible to access recent standards (let alone drafts), and they thought everything they created had to look like Ethernet. IEEE went as far as overcomplicating IS-IS to prevent micro-loops because they refused to add a hop count to the data-plane encapsulation[^THC]. In real life, some vendors skipped that part when implementing SPBM, assuming that the networks wouldn't be bothered (too much) by an occasional forwarding loop (yeah, that sounds reassuring).

[^THC]: TRILL was designed by people with layer-3 packet forwarding experience and had a hop count field in the TRILL header.

The original EVPN required an MPLS data plane, which was a perfect match for service providers already running MPLS. Since the early days of MPLS, you could also run MPLS over GRE, enabling a gradual deployment of MPLS over IP networks. In any case, EVPN was just another service using MPLS LSPs. Adding EVPN to an existing MPLS network was utterly non-disruptive.

Adding VXLAN encapsulation to EVPN was the watershed moment. Finally, you could decouple the end-user services from the transport core network and implement the virtual networks on edge nodes (hypervisors) with no control-plane interaction with the physical network.

SPBM required end-to-end PBB encapsulation and tight integration of edge- and core switches (every switch had to run IS-IS). You could not deploy it gradually on top of an existing bridged network; the network core had to run SPBM. While Avaya eventually added PBB-over-IP (or was it GRE?), that addition was proprietary and too late to matter. VXLAN had already won.

Now for the technical details:

> IS-IS, as an interior routing protocol, can handle 1000s routers. We don't need anything more scalable like BGP unless you're AWS/Microsoft/Google/Facebook.

I've been saying the same thing for years, and intelligent people (including those who designed AWS fabric with OSPF) know that. Only the EBGP-as-better-IGP cargo cult followers think you _need_[^IC] BGP as an underlay routing protocol in a data center fabric.

[^IC]: As opposed to "_it's cool and looks great on my resume_" or "_I have this cool gear that treats EBGP like OSPF, so let's use it._" I have nothing against [EBGP-only designs](/2024/04/repost-ebgp-only-sp-network/) _as long as they result in a simpler overall design_. IBGP-over-EBGP or EBGP-over-EBGP is (from my perspective) not in that category. Also, I wanted to point out that you don't *need* EBGP to run a data center fabric.

> IS-IS doesn’t need addressing because it’s an ISO protocol. As long as the interface can run Ethernet, an adjacency can form. No IPv4 or IPv6 addresses needed, link-local or otherwise.

IS-IS needs CLNS node addresses to run but does not need layer-3 interface addresses. However, if you want to run your transport services on top of IP (see above), you need IPv6 LLA and (at minimum) IPv4 loopback addresses.

> Keep in mind, all this “Interface EBGP Session” stuff is needed to bootstrap all the other stuff we will need: multi-protocol BGP, adjusting the NLRI in BGP, VXLAN-GPO, loopbacks for the VTEPs, routing protocols to coordinate with the devices in the overlay (e.g., firewalls), etc.

The "interface EBGP session" stuff is there only to please the cargo cult followers (or hyperscalers buying Arista and Cisco gear). EVPN using IBGP between loopback interfaces works just fine.

However, you need something to propagate endpoint reachability information between fabric edge devices. My Avaya (now Extreme) friends tell me IS-IS works fine for typical enterprise use cases. Still, I'm pretty sure we would eventually hit some limits of IS-IS LSPs ([I wrote about the details](/2014/04/is-is-in-avayas-spb-fabric-one-protocol/) almost exactly a decade ago).

Finally, EVPN advertises endpoint MAC addresses in BGP updates, which allows load balancing and ESI-based multihoming. SPBM (like traditional bridging) relies on datapath MAC learning. Comparing EVPN to SPBM is a bit like comparing a boring 4WD family sedan to a roadster[^RDS].

[^RDS]: Roadsters are great unless you're going on holiday with three kids or have a snowstorm arriving in a few hours.

As for "*routing protocols to coordinate with the devices in the overlay*," that's the bane of every "disruptive" greenfield solution (including SD-WAN). Life is simple if you limit yourself to VLANs and directly connected IP prefixes. Once you want to integrate your solution with the existing customer network, you must implement routing protocols and two-way redistribution, and your solution becomes as complex as MPLS/VPN or EVPN. For example, (according to my vague recollection of a lunch discussion) Avaya's SPBM solution had a lovely (proprietary) IP Multicast implementation that worked great *as long as the multicast domain was limited to the Avaya fabric and you did not insist on using PIM*.