---
date: 2022-10-13 06:06:00+00:00
evpn_tag: mpls
pre_scroll: true
tags:
- EVPN
- bridging
title: EVPN VLAN-Aware Bundle Service
---
In the _[EVPN/MPLS Bridging Forwarding Model](/2022/10/evpn-mpls-bridging-forwarding-model.html)_ blog post I mentioned numerous services defined in [RFC 7432](https://datatracker.ietf.org/doc/html/rfc7432). That blog post focused on [VLAN-Based Service Interface](https://datatracker.ietf.org/doc/html/rfc7432#section-6.1) that mirrors the [Carrier Ethernet VLAN mode](https://datatracker.ietf.org/doc/html/rfc7209#section-7).

RFC 7432 defines two other VLAN services that can be used to implement Carrier Ethernet services:

* [Port-based service](https://datatracker.ietf.org/doc/html/rfc7432#section-6.2.1) -- whatever is received on the ingress port is sent to the egress port(s)
* [VLAN bundle service](https://datatracker.ietf.org/doc/html/rfc7432#section-6.2) -- multiple VLANs sharing the same bridging table, effectively emulating single outer VLAN in Q-in-Q bridging.

And then there's the VLAN-Aware Bundle Service, where a bunch of VLANs _share the same MPLS pseudowires_ while _having separate bridging tables_.
<!--more-->
Looking at that, I was left wondering who would ever do something like that. It's not like we're trying to limit the number of VLANs on a PE-device, or the number of bridging (MAC address) tables used on that device (remember: each VLAN within that service bundle has a separate MAC address table). The only thing we're saving are MPLS labels which are signaled between the egress and ingress devices, and are never visible to the network core. Really, IETF 🤦‍♂️

Just in case you're as confused as I am, here's the [justification from RFC 7209](https://datatracker.ietf.org/doc/html/rfc7209#section-7):

> For hosted applications for data-center interconnect, network operators require the ability to extend Ethernet VLANs over a WAN using a single L2VPN instance while maintaining data-plane separation between the various VLANs associated with that instance. This is referred to as 'VLAN-aware bundling service'.

Why would they "require a single L2VPN instance"? Because the transport provider charges per label?

Anyway, time to see how that beast works. We'll use the [very same lab as before](/2022/10/evpn-mpls-bridging-forwarding-model.html), but split the hosts into two VLANs that will be provisioned as a VLAN bundle. The [Arista EOS configuration files](https://github.com/ipspace/netlab-examples/tree/master/EVPN/mpls-vlan-bundle/saved_config) are on GitHub as is the [lab topology](https://github.com/ipspace/netlab-examples/tree/master/EVPN/mpls-vlan-bundle) in case you want to recreate the lab[^V14].

[^V14]: You'll need *netlab* release 1.4 or later to recreate the lab. You can get a pre-release version (if needed) with `pip3 install --upgrade --pre networklab`.

{{<figure src="/2022/10/evpn-mpls-vlan-bundle.png" caption="Lab topology">}}

Inspecting the EVPN routes advertised by PE3, we can see that all *mac-ip* routes (RT2) have the same MPLS label, regardless of the VLAN the host belongs to. Likewise, *imet* (RT3) routes for all VLANs also have the same MPLS label.

{{<cc>}}EVPN routes advertised by PE3{{</cc>}}
```
pe1#sh bgp evpn next-hop 10.0.0.3 detail
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for mac-ip 1000 5254.009b.a561, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeMpls
      MPLS label: 1042979 ESI: 0000:0000:0000:0000:0000
BGP routing table entry for mac-ip 1001 5254.00c9.82dc, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeMpls
      MPLS label: 1042979 ESI: 0000:0000:0000:0000:0000
BGP routing table entry for imet 1000 10.0.0.3, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeMpls
      MPLS label: 1038234
      PMSI Tunnel: Ingress Replication, MPLS Label: 16611744, Leaf Information Required: false, Tunnel ID: 10.0.0.3
BGP routing table entry for imet 1001 10.0.0.3, Route Distinguisher: 65000:1
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeMpls
      MPLS label: 1038234
      PMSI Tunnel: Ingress Replication, MPLS Label: 16611744, Leaf Information Required: false, Tunnel ID: 10.0.0.3
```

If you're wondering how PE3 figures out which MAC address table to use when receiving packets over those MPLS wires you're probably not alone. The only way to do it is to _send 802.1Q tagged packets over MPLS wires_. You can see that if you inspect the MPLS LFIB on PE3.

{{<cc>}}MPLS LFIB (with VLAN tags) on PE3{{</cc>}}
```
pe3#sh mpls lfib route
MPLS forwarding table (Label [metric] Vias) - 5 routes
MPLS next-hop resolution allow default route: False
Via Type Codes:
          M - MPLS via, P - Pseudowire via,
          I - IP lookup via, V - VLAN via,
          VA - EVPN VLAN aware via, ES - EVPN ethernet segment via,
          VF - EVPN VLAN flood via, AF - EVPN VLAN aware flood via,
          NG - Nexthop group via
Source Codes:
          G - gRIBI, S - Static MPLS route,
          B2 - BGP L2 EVPN, B3 - BGP L3 VPN,
          R - RSVP, LP - LDP pseudowire,
          L - LDP, M - MLDP,
          I>BL - IS-IS SR to BGP LU, IP - IS-IS SR prefix segment,
          IA - IS-IS SR adjacency segment, I>L - IS-IS SR to LDP,
          L>I - LDP to IS-IS SR, BL - BGP LU,
          BL>L - BGP LU to LDP, L>BL - LDP to BGP LU,
          ST - SR TE policy, SMP - SR P2MP,
          BL>I - BGP LU to IS-IS SR, DE - Debug LFIB

 L     116384   [1], 10.0.0.4/32
                via M, 10.1.0.9, pop
                 payload autoDecide, ttlMode uniform, apply egress-acl
                 interface Ethernet1
 L     116385   [1], 10.0.0.2/32
                via M, 10.1.0.9, swap 116384
                 payload autoDecide, ttlMode uniform, apply egress-acl
                 interface Ethernet1
 L     116386   [1], 10.0.0.1/32
                via M, 10.1.0.9, swap 116385
                 payload autoDecide, ttlMode uniform, apply egress-acl
                 interface Ethernet1
 B2    1038234  [0]
                via AF, control word present
                     dot1q   vlan
                    | 1000 | 1000 |
                    | 1001 | 1001 |
 B2    1042979  [0]
                via VA, control word present
                     dot1q   vlan
                    | 1000 | 1000 |
                    | 1001 | 1001 |
```

{{<note>}}
The _shared label_ behavior for VLAN-aware bundles is present only with MPLS encapsulation. RFC 8365 describes VLAN-aware Bundle Service as [multiple VLAN (each with its own VNI) sharing the same MAC-VRF](https://datatracker.ietf.org/doc/html/rfc8365.html#section-5.1.2).
{{</note>}}

Does that mean that the flow of traffic would be suboptimal, or that (for example) PE2 would receive flooded traffic for *red* VLAN? Not necessarily -- every VLAN has its own MAC address table and could have its own ingress replication list.

OK, so VLAN-aware bundle service has no drawbacks. Does it have any benefits? I can't see them, unless you're worried about the number of MPLS labels, route targets, or configuration lines (BGP configuration of VLAN-aware bundle service on Arista EOS takes fewer lines than configuring individual VLANs in the BGP process). Am I missing something? Please write a comment.

**Recap**: Should you use VLAN-aware Bundle Service? [Paraphrasing James Mickens](https://blog.ipspace.net/2018/10/worth-watching-machine-learning-in.html): "In a word: don't!"
