---
title: "EVPN Hub-and-Spoke Layer-3 VPN"
date: 2024-09-18 07:59:00+0200
tags: [ netlab, EVPN, design ]
netlab_tag: vxlan_evpn
evpn_tag: vpn_topo
series: hub_spoke_vpn
---
Now that we figured out [how to implement a hub-and-spoke VPN design on a single PE-router](/2024/09/hub-spoke-single-pe/), let's do the same thing with EVPN. It turns out to be trivial:

* We'll split the single PE router into three PE devices (**pe_a**, **pe_b**, and **pe_h**)
* We'll add a core router (**p**) and connect it with all three PE devices.

As we want to use EVPN and have a larger core network, we'll also have to enable VLANs, VXLAN, BGP, and OSPF on the PE devices.

This is the topology of our expanded lab:
<!--more-->
{{<figure src="/2024/09/hub-spoke-evpn-topology.png">}}

And this is the [_netlab_](https://netlab.tools/) description of the [lab topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/l3vpn-hub-spoke/topology.yml):

{{<printout>}}
defaults.device: eos
provider: clab

module: [ bgp ]
plugin: [ bgp.session ]

groups:
  ce:
    device: frr
    members: [ ce_s1, ce_s2, ce_hub ]
  pe:
    members: [ pe_a, pe_b, pe_h ]
    module: [ bgp, vrf, evpn, vlan, vxlan, ospf ]
    bgp.as: 65000

vrfs:
  s_1:
    links: [ pe_a-ce_s1 ]
    export: [ hub_egress ]
    import: [ hub_ingress ]
    evpn.transit_vni: True
  s_2:
    links: [ pe_b-ce_s2 ]
    export: [ hub_egress ]
    import: [ hub_ingress ]
    evpn.transit_vni: True
  hub_ingress:
    links:
    - pe_h:
      ce_hub:
        bgp.as_override: True
    evpn.transit_vni: True
  hub_egress:
    links: [ pe_h-ce_hub ]
    evpn.transit_vni: True

nodes:
  pe_a:
  pe_b:
  pe_h:
  p:
    module: [ ospf ]
  ce_hub:
    bgp.as: 65100
  ce_s1:
    bgp.as: 65101
  ce_s2:
    bgp.as: 65102

links: [ pe_a-p, pe_b-p, pe_h-p ]
{{</printout>}}

Most of the topology has been explained in the [previous blog post](/2024/09/hub-spoke-single-pe/); here's the gist of the changes:

* We need three PE routers (lines 11-14). They have to run VRFs (or we wouldn't have L3VPN), OSPF (to connect to the P router), BGP (to support EVPN), VXLAN (to transport customer data), VLANs (because the VXLAN module relies on the VLAN module), and EVPN (for obvious reasons: see blog title)
* We have to enable EVPN transit VNI in all VRFs (lines 21, 26, 32, 35). Each VRF will have a different transit VNI.
* We need a core router running OSPF (lines 41-42) and links between the PE routers and the core router (line 50).

Does this really work? You bet!

```
$ netlab connect ce_s1 traceroute ce_s2
Connecting to container clab-l3vpn-hub-sp-ce_s1, executing traceroute ce_s2
traceroute to ce_s2 (10.0.0.7), 30 hops max, 46 byte packets
 1  pe_a-s_1 (10.1.0.14)  0.004 ms  0.002 ms  0.001 ms
 2  pe_h-hub_ingress (10.1.0.22)  3.403 ms  0.995 ms  0.951 ms
 3  ce_hub (10.1.0.25)  0.969 ms  0.836 ms  0.793 ms
 4  pe_h-hub_egress (10.1.0.26)  0.973 ms  0.740 ms  0.643 ms
 5  pe_b-s_2 (10.1.0.18)  2.079 ms  1.212 ms  1.082 ms
 6  ce_s2 (10.0.0.7)  1.051 ms  1.057 ms  0.989 ms
 ```

Want to try it out yourself?

* [Open the netlab-examples repository in a GitHub Codespace](https://blog.ipspace.net/2024/07/netlab-examples-codespaces/)
* [Copy the cEOS container into the codespace](https://blog.ipspace.net/2024/07/arista-eos-codespaces/)
* Change directory to `EVPN/l3vpn-hub-spoke`
* Execute **netlab up**

Alternatively, you could execute **netlab up -d frr** if you don't want to waste time with Arista cEOS containers.

### Behind the Scenes

Let's track the propagation of the BGP route for the CE_S2 loopback prefix (10.0.0.7/32) to see how the whole setup works. Here's the table of loopback prefixes to make it easier to track what's going on:

| Node/Interface | IPv4 Address | IPv6 Address | Description |
|----------------|-------------:|-------------:|-------------|
| **ce_hub** |  10.0.0.5/32 |  | Loopback |
| **ce_s1** |  10.0.0.6/32 |  | Loopback |
| **ce_s2** |  10.0.0.7/32 |  | Loopback |
| **p** |  10.0.0.4/32 |  | Loopback |
| **pe_a** |  10.0.0.1/32 |  | Loopback |
| **pe_b** |  10.0.0.2/32 |  | Loopback |
| **pe_h** |  10.0.0.3/32 |  | Loopback |
{.fmtTable}

Here's the overview of the VRFs we're using:

| VRF | RD | Export RT | Import RT | EVPN VNI |
|-----|---:|-----------|-----------|---------:|
| hub_egress | 65000:4 | 65000:4 | 65000:4 | 200003 |
| hub_ingress | 65000:3 | 65000:3 | 65000:3 | 200002 |
| s_1 | 65000:1 | 65000:4 | 65000:3 | 200000 |
| s_2 | 65000:2 | 65000:4 | 65000:3 | 200001 |
{.fmtTable}

CE_S2 is connected to VRF `s_2` on PE_B, so let's start there:

```
pe-b>show ip bgp 10.0.0.7/32 vrf s_2
BGP routing table information for VRF s_2
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for 10.0.0.7/32
 Paths: 2 available
  65102
    10.1.0.17 from 10.1.0.17 (10.0.0.7)
      Origin IGP, metric 0, localpref 100, IGP metric 0, weight 0, tag 0
      Received 01:00:20 ago, valid, external, best
      Rx SAFI: Unicast
  65100 65100 65102
    10.0.0.3 from 10.0.0.3 (10.0.0.3), imported EVPN route, RD 65000:3
      Origin IGP, metric 0, localpref 100, IGP metric 30, weight 0, tag 0
      Received 01:00:12 ago, valid, internal
      Extended Community: Route-Target-AS:65000:3 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:8d:a1:38
      Remote VNI: 200002
      Rx SAFI: Unicast
```

PE_B has two BGP paths for the 10.0.0.7/32 prefix: the VRF BGP path advertised by CE_S2 and the BGP-EVPN path advertised by the  PE_H (10.0.0.3). According to the RT community, the BGP-EVPN path originated in the `hub_ingress` VRF.

PE_B prefers the path advertised by CE_S2, and as the `s_2` VRF has EVPN transit VNI, it copies that path into a route-type-5 (ip-prefix) EVPN update (the top path in the following printout):

```
pe-b>show bgp evpn route-type ip-prefix 10.0.0.7/32
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65000
BGP routing table entry for ip-prefix 10.0.0.7/32, Route Distinguisher: 65000:2
 Paths: 1 available
  65102
    - from - (0.0.0.0)
      Origin IGP, metric 0, localpref 100, weight 0, tag 0, valid, external, best
      Extended Community: Route-Target-AS:65000:4 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:0d:a4:e5
      VNI: 200001
BGP routing table entry for ip-prefix 10.0.0.7/32, Route Distinguisher: 65000:3
 Paths: 1 available
  65100 65100 65102
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:3 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:8d:a1:38
      VNI: 200002
```

How do we know the top path originated from PE_B? The next hop is not set yet; it's usually set to the source IP address of the BGP session when the BGP updates are sent.

Moving on to PE_H. It has two entries for 10.0.0.7/32 in its BGP EVPN table and an entry in each VRF (`hub_ingress` and `hub_egress`)

```
pe-h>show bgp evpn route-type ip-prefix 10.0.0.7/32
BGP routing table information for VRF default
Router identifier 10.0.0.3, local AS number 65000
BGP routing table entry for ip-prefix 10.0.0.7/32, Route Distinguisher: 65000:2
 Paths: 1 available
  65102
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:4 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:0d:a4:e5
      VNI: 200001
BGP routing table entry for ip-prefix 10.0.0.7/32, Route Distinguisher: 65000:3
 Paths: 1 available
  65100 65100 65102
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, external, best
      Extended Community: Route-Target-AS:65000:3 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:8d:a1:38
      VNI: 200002

pe-h>show ip bgp 10.0.0.7/32 vrf all
BGP routing table information for VRF hub_egress
Router identifier 10.0.0.3, local AS number 65000
BGP routing table entry for 10.0.0.7/32
 Paths: 1 available
  65102
    10.0.0.2 from 10.0.0.2 (10.0.0.2), imported EVPN route, RD 65000:2
      Origin IGP, metric 0, localpref 100, IGP metric 30, weight 0, tag 0
      Received 01:11:09 ago, valid, internal, best
      Extended Community: Route-Target-AS:65000:4 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:0d:a4:e5
      Remote VNI: 200001
      Rx SAFI: Unicast
BGP routing table information for VRF hub_ingress
Router identifier 10.0.0.3, local AS number 65000
BGP routing table entry for 10.0.0.7/32
 Paths: 1 available
  65100 65100 65102
    10.1.0.21 from 10.1.0.21 (10.0.0.5)
      Origin IGP, metric 0, localpref 100, IGP metric 0, weight 0, tag 0
      Received 01:11:09 ago, valid, external, best
      Rx SAFI: Unicast
```

PE_H is using the EVPN route advertised by PE_B (now we can see that the BGP next hop is 10.0.0.2). It imports the EVPN route into the `hub_egress` VRF and advertises it to the Hub router.

The Hub router advertises the same prefix back to PE_B over the `hub_ingress` EBGP session (notice a change in the next hop and the AS path), and PE_H exports that prefix back into EVPN (the second EVPN route with no next-hop information).

Finally, PE_A received two EVPN routes for 10.0.0.7/32, one from PE_B (10.0.0.2), the other one from PE_H (10.0.0.3):

```
pe-a>show bgp evpn route-type ip-prefix 10.0.0.7/32
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for ip-prefix 10.0.0.7/32, Route Distinguisher: 65000:2
 Paths: 1 available
  65102
    10.0.0.2 from 10.0.0.2 (10.0.0.2)
      Origin IGP, metric 0, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:4 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:0d:a4:e5
      VNI: 200001
BGP routing table entry for ip-prefix 10.0.0.7/32, Route Distinguisher: 65000:3
 Paths: 1 available
  65100 65100 65102
    10.0.0.3 from 10.0.0.3 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:3 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:8d:a1:38
      VNI: 200002
```

The route advertised by PE_H has a route target that matches the import route target of the `s_1` VRF and gets imported into it:

```
pe-a>show ip bgp 10.0.0.7/32 vrf s_1
BGP routing table information for VRF s_1
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for 10.0.0.7/32
 Paths: 1 available
  65100 65100 65102
    10.0.0.3 from 10.0.0.3 (10.0.0.3), imported EVPN route, RD 65000:3
      Origin IGP, metric 0, localpref 100, IGP metric 30, weight 0, tag 0
      Received 06:39:40 ago, valid, internal, best
      Extended Community: Route-Target-AS:65000:3 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:8d:a1:38
      Remote VNI: 200002
      Rx SAFI: Unicast
```

The data-plane setup is very similar to the one we've observed in the [common services VRF scenario](/2024/08/evpn-common-services-vrf/). You can find the details there or start the lab and explore.

{{<next-in-series page="/posts/2024/09/hub-spoke-mpls.html">}}
For the sake of completeness, I'll do another blog post implementing hub-and-spoke VPN with MPLS transport and MPLS/VPN control plane, but it might take a while.
{{</next-in-series>}}

### Reference Information

This is the relevant part of the PE_H configuration (EVPN, BGP, VRFs). It was generated exclusively with _netlab_ configuration templates; all I did was run **netlab up** and enjoy the results. You can find the [other router configurations](https://github.com/ipspace/netlab-examples/tree/master/EVPN/l3vpn-hub-spoke/config) in the [*netlab-examples* GitHub repository](https://github.com/ipspace/netlab-examples/).

```
vrf instance hub_egress
   rd 65000:4
!
vrf instance hub_ingress
   rd 65000:3
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vrf hub_egress vni 200003
   vxlan vrf hub_ingress vni 200002
!
ip routing vrf hub_egress
ip routing vrf hub_ingress
!
router bgp 65000
   router-id 10.0.0.3
   neighbor 10.0.0.1 remote-as 65000
   neighbor 10.0.0.1 update-source Loopback0
   neighbor 10.0.0.1 description pe_a
   neighbor 10.0.0.1 send-community standard extended large
   neighbor 10.0.0.2 remote-as 65000
   neighbor 10.0.0.2 update-source Loopback0
   neighbor 10.0.0.2 description pe_b
   neighbor 10.0.0.2 send-community standard extended large
   !
   address-family evpn
      neighbor 10.0.0.1 activate
      neighbor 10.0.0.2 activate
   !
   !
   vrf hub_egress
      rd 65000:4
      route-target import evpn 65000:4
      route-target export evpn 65000:4
      router-id 10.0.0.3
      neighbor 10.1.0.25 remote-as 65100
      neighbor 10.1.0.25 description ce_hub
      neighbor 10.1.0.25 send-community standard large
      redistribute connected
      !
      address-family ipv4
         neighbor 10.1.0.25 activate
         redistribute connected
   !
   vrf hub_ingress
      rd 65000:3
      route-target import evpn 65000:3
      route-target export evpn 65000:3
      router-id 10.0.0.3
      neighbor 10.1.0.21 remote-as 65100
      neighbor 10.1.0.21 description ce_hub
      neighbor 10.1.0.21 send-community standard large
      redistribute connected
      !
      address-family ipv4
         neighbor 10.1.0.21 activate
         redistribute connected
```
