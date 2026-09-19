---
title: "EVPN with SR-MPLS Core"
date: 2026-09-22 07:25:00+0200
tags: [ SR-MPLS, netlab ]
sr-mpls_tag: lab
netlab_tag: ignore
---
After a [long journey](/tag/sr-mpls/#try), we finally we got to the final scenario in my ITNOG10 [Segment Routing workshop](/2026/04/sr-mpls-workshop/): EVPN services over an SR-MPLS core.

I used the same lab topology as in the [previous services-focused scenarios](/2026/09/sr-mpls-bgp-free/) blog post, replacing two PE-to-host subnets with a stretched VLAN. 

{{<figure src="/2026/09/sr-mpls-fun.png" caption="EVPN over SR-MPLS core">}}
<!--more-->
### Does It Work?

Fortunately (for my demo) Arista implemented EVPN-over-MPLS in EOS, so I didn't have to go shopping for another device. After the BGP session is established between the PE routers and the EVPN address family is negotiated, we can admire the EVPN type-3 routes with MPLS labels:

{{<printout highlight="yes" caption="EVPN type-3 routes on Arista EOS running EVPN over MPLS">}}
pe1#show bgp evpn detail
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for imet 10.0.0.2, Route Distinguisher: 10.0.0.2:1000
 Paths: 1 available
  Local
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref -, weight 0, tag 0, valid, local, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 1040999
      PMSI Tunnel: Ingress Replication, MPLS Label: 16655984, Leaf Information Required: false, Tunnel ID: 10.0.0.2
BGP routing table entry for imet 10.0.0.3, Route Distinguisher: 10.0.0.3:1000
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 1040999
      PMSI Tunnel: Ingress Replication, MPLS Label: 16655984, Leaf Information Required: false, Tunnel ID: 10.0.0.3
{{</printout>}}

Unfortunately, we can't see the two-label stack in the EVPN routes on Arista EOS. We have to use another command to figure out how the local device (PE1) reaches the remote PE router (PE2), and we have to go even further if we want to see the actual label:

{{<printout highlight="yes" caption="Transport tunnel from PE1 to PE2 as shown by Arista EOS">}}
pe1#show tunnel rib 10.0.0.3/32 candidates
Tunnel RIB: system-tunnel-rib
   Endpoint          Tunnel Type         Index(es)       Tunnel Preference    Tunnel Metric
----------------- ------------------- --------------- ----------------------- -------------
   10.0.0.3/32       IS-IS SR IPv4       2               65                   0
{{</printout>}}

However, once HA pings HB, we get the EVPN type-2 routes:

{{<printout highlight="yes" caption="EVPN MAC-IP routes for HA and HB on PE1 running Arista EOS">}}
pe1#show bgp evpn route-type mac-ip detail
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for mac-ip aac1.ab6b.03b4, Route Distinguisher: 10.0.0.2:1000
 Paths: 1 available
  Local
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref -, weight 0, tag 0, valid, local, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 1047390 ESI: 0000:0000:0000:0000:0000
BGP routing table entry for mac-ip aac1.abb4.bb24, Route Distinguisher: 10.0.0.3:1000
 Paths: 1 available
  Local
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeMpls
      MPLS label: 1047390 ESI: 0000:0000:0000:0000:0000
{{</printout>}}

And finally, we can look at the layer-2 routing table (L2RIB) to observe the MPLS label stack (even though the transport label is still not displayed):

{{<printout highlight="yes" caption="Layer-2 routing table for the tenant VLAN on PE1 running Arista EOS">}}
pe1#show l2rib input all detail
caf0.0001.0001, VLAN 1006, seq 1, pref 16, learnedDynamicMac, source: Local Dynamic
   Ethernet1
aac1.ab6b.03b4, VLAN 1000, seq 1, pref 16, learnedDynamicMac, source: Local Dynamic
   Ethernet2
aac1.ab82.bb99, VLAN 1006, seq 1, pref 16, learnedDynamicMac, source: Local Dynamic
   Ethernet1
aac1.abb4.bb24, VLAN 1000, seq 1, pref 16, evpnDynamicRemoteMac, source: BGP
   Label entry 1: 1047390
      Tunnel IS-IS SR IPv4 (2), TEP 10.0.0.3/32
{{</printout>}}


### Lab Topology {#lab}

Here are the changes I made to the [MPLS/VPN topology](https://github.com/ipspace/SR-workshop/blob/main/2-fun/2-mpls-vpn/topology.yml) to replace MPLS/VPN with EVPN services:

* I removed MPLS- and VRF-related settings
* I had to configure SR-MPLS transport for EVPN (the default transport is VXLAN):

{{<printout caption="Configuring EVPN transport">}}
evpn.transport: sr
{{</printout>}}

* The *edge* devices (PE routers) use VLAN and EVPN modules instead of MPLS and VRF:

{{<printout caption="Modified definition of the edge group">}}
groups:
  edge:
    members: [ pe1, pe2 ]
    module: [ isis, bgp, sr, vlan, evpn ]
{{</printout>}}

* The PE-to-host links are defined as part of the *tenant* VLAN:

{{<printout caption="Links in the tenant VRF">}}
vlans:
  tenant:
    mode: bridge
    links: [ ha-pe1, hb-pe2 ]
{{</printout>}}

* Finally, I had to enable EVPN for the *tenant* VLAN (that's done automatically for VXLAN-enabled VLANs, but we cannot use the same trick for MPLS-based EVPN):

{{<printout caption="Enabling EVPN for the tenant VLAN">}}
evpn.vlans: [ tenant ]
{{</printout>}}

The final lab topology is [here](https://github.com/ipspace/SR-workshop/blob/main/2-fun/3-evpn/topology.yml).

### Try It Out

The [workshop GitHub repository](https://github.com/ipspace/SR-workshop) includes the [installation guidelines](https://github.com/ipspace/SR-workshop/blob/main/docs/use.md); you might want to read them first. After that, you can:

* [Start a GitHub Codespace](https://github.com/codespaces/new/ipspace/sr-workshop)
* [Import an Arista cEOS container](https://blog.ipspace.net/2024/07/arista-eos-codespaces/) into it ([alternate step-by-step instructions](https://arista.my.site.com/AristaCommunity/s/article/cEOS-lab-in-Github-Codespaces))
* Change directory to `2-fun/3-evpn`
* Execute **netlab up**
* Have fun
