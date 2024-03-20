---
date: 2022-10-05 06:29:00+00:00
evpn_tag: mpls
pre_scroll: true
tags:
- EVPN
- MPLS
title: EVPN/MPLS Bridging Forwarding Model
---
Most networking engineers immediately think about VXLAN and data center switches when they hear about EVPN. While that's the most hyped use case, EVPN standardization started in 2012 as a layer-2 VPN solution on top of MPLS transport trying to merge the best of VPLS and MPLS/VPN worlds.

If you want to understand how any technology works, and what its quirks are, you have to know how it was designed to be used. In this blog post we'll start that journey exploring the basics of EVPN used in a [simple MLPS network with three PE-routers](https://github.com/ipspace/netlab-examples/tree/master/EVPN/mpls-bridging):

{{<figure src="/2022/10/evpn-mpls-topology.png" caption="Lab topology">}}
<!--more-->
The PE-routers are running Arista EOS[^MPLS_EOS]. Their [configuration is available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/EVPN/mpls-bridging/saved_configs); you can also use *netlab* to [recreate the lab](https://github.com/ipspace/netlab-examples/tree/master/EVPN/mpls-bridging).

[^MPLS_EOS]: I thought I'd have to use a SP-focused operating system like Junos or a resource hog like Nexus OS to get EVPN working with MPLS, and was amazed when I found out Arista EOS supports it. Great job!

After the lab is started, the EVPN BGP table on all three PE-routers contains an entry for every attached host (*mac-ip*, type-2 route), and an entry for every VLAN segment (*imet* or *inclusive multicast Ethernet tag*, type-3 route):

{{<cc>}}EVPN BGP table on PE1{{</cc>}}
```
pe1#sh bgp evpn
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending BGP convergence
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.3:1000 mac-ip 5254.0023.89db
                                 10.0.0.3              -       100     0       i
 * >      RD: 10.0.0.1:1000 mac-ip 5254.005c.41af
                                 -                     -       -       0       i
 * >      RD: 10.0.0.3:1000 mac-ip 5254.005e.10e0
                                 10.0.0.3              -       100     0       i
 * >      RD: 10.0.0.2:1000 mac-ip 5254.00f6.f9da
                                 10.0.0.2              -       100     0       i
 * >      RD: 10.0.0.1:1000 imet 10.0.0.1
                                 -                     -       -       0       i
 * >      RD: 10.0.0.2:1000 imet 10.0.0.2
                                 10.0.0.2              -       100     0       i
 * >      RD: 10.0.0.3:1000 imet 10.0.0.3
                                 10.0.0.3              -       100     0       i
```

All EVPN routes have two attributes that should be very familiar to the MPLS/VPN cognoscenti: a *route distinguisher* that is used to make non-unique elements like MAC- or IP addresses[^DUPMAC] globally unique, and *route targets* that are used to import and export routes between VRFs. As we're discussing a bridged topology today, those VRFs would be called MAC-VRFs.

[^DUPMAC]: While the burnt-in MAC addresses should be globally unique, locally-administered ones don't have to be. For example, HSRP computes the shared MAC address from the HSRP group ID, and if you use the same HSRP group in two subnets, you'll get duplicate MAC addresses.

In simple VLAN bridging use cases, we usually use the **loopback_ip**:**vlan_id** form of the route distinguishers and **bgp_asn**:**vlan_id**‌‌ form of the route targets, for example:

{{<cc>}}Detailed view of an EBGP route{{</cc>}}
```
pe1#sh bgp evpn route-type imet 10.0.0.3 detail
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for imet 10.0.0.3, Route Distinguisher: 10.0.0.3:1000
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 435282
      PMSI Tunnel: Ingress Replication, MPLS Label: 6964512, Leaf Information Required: false, Tunnel ID: 10.0.0.3
```

Let's focus on the type-3 routes first. Egress nodes use them to advertise every VLAN they are connected to[^VLAN_SVC] together with an MLPS label that ingress nodes could use to send BUM packets to that egress node. The type-3 routes are used by ingress nodes (assuming the route target in the EVPN route matches the *import* route target) to build replication trees[^P2MP] -- type-3 EVPN routes effectively build a mesh of flooding pseudowires across an MPLS fabric

{{<figure src="/2022/10/evpn-mpls-full-mesh.png" caption="Full mesh of MPLS pseudowires between PE-routers bridging VLAN 1000">}}

[^VLAN_SVC]: A bit of an oversimplification. I'm describing a VLAN-based service here. EVPN has a half-dozen service types.

[^P2MP]: You can also optimize bandwidth utilization and make your life more "interesting" trying to implement P2MP MPLS circuits. Trying to make them work across multiple vendors must be great fun.

Whenever an ingress node needs to flood a BUM packet, it sends a copy to every other node in the same flooding domain, usually *using a different MPLS label stack for every egress node*. Looking at the *imet* EVPN routes on PE1, you'll notice different MPLS labels (advertised by egress PE-router) and tunnel labels (advertised by LDP) in every route.

{{<cc>}}EVPN *imet* routes on PE1{{</cc>}}
```
pe1#sh bgp evpn route-type imet detail
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for imet 10.0.0.1, Route Distinguisher: 10.0.0.1:1000
 Paths: 1 available
  Local
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref -, weight 0, valid, local, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 415282
      PMSI Tunnel: Ingress Replication, MPLS Label: 6644512, Leaf Information Required: false, Tunnel ID: 10.0.0.1
BGP routing table entry for imet 10.0.0.2, Route Distinguisher: 10.0.0.2:1000
 Paths: 1 available
  Local
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 425282
      PMSI Tunnel: Ingress Replication, MPLS Label: 6804512, Leaf Information Required: false, Tunnel ID: 10.0.0.2
BGP routing table entry for imet 10.0.0.3, Route Distinguisher: 10.0.0.3:1000
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 435282
      PMSI Tunnel: Ingress Replication, MPLS Label: 6964512, Leaf Information Required: false, Tunnel ID: 10.0.0.3
```

Based on the above printout: whenever PE1 needs to flood a BUM packet in VLAN 1000, it sends a copy toward PE2 with label stack 425282/6804512 and another copy toward PE3 with label stack 435282/6964512.

The type-3 EVPN routes provide enough information to build a more scalable VPLS implementation[^MH], but EVPN goes a step further: every egress PE-device advertises every locally-known MAC address (and associated IPv4 or IPv6 address) with a type-2 EVPN route that carries its own MPLS label.

[^MH]: Ignoring the multihoming or MLAG details -- this is an introductory blog post, not an EVPN/MPLS book.

An EVPN implementation might decide to use the same MPLS label for flooding and unicast IP addresses, to use two labels (one for flooding, one for unicast), or to use a dedicated label for every MAC address. The printout of type-2 routes advertised by PE3 makes it clear that Arista EOS implementation uses a single MPLS label (different from the flooding label) for unicast traffic:

{{<cc>}}EVPN type-2 routes for H3 and H4 as advertised by PE2{{</cc>}}
```
pe1#sh bgp evpn route-type mac-ip rd 10.0.0.3:1000 detail
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for mac-ip 5254.0023.89db, Route Distinguisher: 10.0.0.3:1000
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 435899 ESI: 0000:0000:0000:0000:0000
BGP routing table entry for mac-ip 5254.005e.10e0, Route Distinguisher: 10.0.0.3:1000
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 435899 ESI: 0000:0000:0000:0000:0000
```

The flexibility of using dynamically-built mesh of pseudowires to transport L2VPN data enables EVPN to mirror the capabilities of MPLS/VPN to support all sorts of crazy VPN topologies. It's trivial to build a common services VPN or a hub-and-spoke VPN (Carrier Ethernet E-Tree service) -- take my configurations and play with import/export route targets, or wait for the next blog post in this series.

### Want to Know More?

Krzysztof Grzegorz Szarkowicz (the author of *MPLS in the SDN Era* book) described [EVPN in MPLS-based environments](https://my.ipspace.net/bin/list?id=EVPN#SP) in the [EVPN Deep Dive webinar](https://www.ipspace.net/EVPN_Technical_Deep_Dive).
