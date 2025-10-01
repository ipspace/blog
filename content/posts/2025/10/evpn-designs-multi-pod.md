---
title: "EVPN Designs: Multi-Pod Fabrics"
series_title: "Multi-Pod Fabrics"
date: 2025-10-01 07:59:00+0200
tags: [ EVPN, design, netlab, vxlan ]
netlab_tag: evpn_dg
evpn_tag: designs
pre_scroll: True
---
In the [EVPN Designs: Layer-3 Inter-AS Option A](/2025/08/evpn-designs-interas-a/), I described the simplest multi-site design in which the WAN edge routers exchange IP routes in individual VRFs, resulting in two isolated layer-2 fabrics connected with a layer-3 link.

Today, let's explore a design that will excite the True Believers in end-to-end layer-2 networks: two EVPN fabrics connected with an EBGP session to form a unified, larger EVPN fabric. We'll use the same "physical" topology as the previous example; the only modification is that the WA-WB link is now part of the underlay IP network.
<!--more-->
{{<figure src="/2025/08/evpn-inter-as-topology.png" caption="Lab topology">}}

This is how the EVPN/EBGP routing is set up:

* The switches within a single site run OSPF, IBGP with core routers acting as route reflectors, and IPv4+EVPN address family running over the IBGP sessions
* The WAN edge routers use an EBGP session to exchange IPv4 and EVPN prefixes.
* The WAN edge routers do not change the next hop of the EVPN prefixes. The overlay traffic is transported as pure IP traffic between the ingress (LA) and egress (LB) switches.

{{<figure src="/2025/10/evpn-multi-pod-bgp.png" caption="BGP sessions (IBGP sessions are brown, EBGP sessions are red)">}}

The [_netlab_ topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/inter-as-multi-pod/topology.yml) we'll use to create this design is very similar to the one we used in the previous example. Here are the changes between the two:

{{<printout>}}
--- ../inter-as-a/topology.yml
+++ topology.yml
@@ -2,6 +2,8 @@ provider: clab

 provider: clab
-defaults.device: frr
+defaults.device: eos
 defaults.outputs.graph.attributes.node.rank: int
+evpn.session: [ ibgp, ebgp ]
+bgp.community.ebgp: [ standard, extended ]

 groups:
@@ -18,4 +20,5 @@ groups:
   spines:
     members: [ ca, cb ]
+    bgp.rr: True
     graph.rank: 1
   leafs:
@@ -25,5 +28,4 @@ vrfs:
 vrfs:
   tenant:
-    links: [ wa-wb ]          # Inter-AS VRF link (inter-AS option A)
     evpn.transit_vni: True    # Symmetric IRB in Site-A and Site-B

@@ -41,2 +43,4 @@ links:
 - group: site_b               # Site B (core-to-leaf, core-to-WAN edge)
   members: [ cb-lb, cb-wb ]
+- group: wan
+  members: [ wa-wb ]
+{{</printout>}}

* The lab is using Arista EOS instead of FRR due to the [IBGP loopback bug](https://blog.ipspace.net/2024/03/frr-ibgp-loopbacks/) (line 7)
* EVPN address family is enabled on IBGP and EBGP sessions (line 9)
* The extended BGP communities have to be sent over EBGP sessions (line 10) ([more details](/2024/10/evpn-designs-ebgp/))
* The core switches are BGP route reflectors (line 16) ([more details](/2024/09/evpn-designs-ibgp-rr/))
* The VRF link between WA and WB is removed (line 22)
* Instead of a VRF link, we have an underlay link connecting WA and WB (line 28)

{{<note info>}}
* The complete lab topology is [available on GitHub](https://github.com/ipspace/netlab-examples/blob/master/EVPN/inter-as-multi-pod/topology.yml).
* The lab topology is explained in more detail in the [EVPN Designs: Layer-3 Inter-AS Option A](/2025/08/evpn-designs-interas-a/#topo) blog post.
* If you're new to _netlab_, you might want to read the previous [EVPN Designs](/tag/evpn/#designs) and [Using VRFs and VLANs](/tag/netlab/#using-vrfs-and-vlans) blog posts.
{{</note>}}

Let's see how the EVPN routes are propagated between LA and LB (all other devices just reflect/forward the routes). Here's the EVPN BGP table on LB after the first ping between HA and HB:

{{<cc>}}EVPN BGP table on LB{{</cc>}}
```
lb#show bgp evpn
BGP routing table information for VRF default
Router identifier 10.0.0.6, local AS number 65002
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.1:1000 mac-ip aac1.ab41.97dd
                                 10.0.0.1              -       100     0       65001 i Or-ID: 10.0.0.4 C-LST: 10.0.0.5
 * >      RD: 10.0.0.1:1000 mac-ip aac1.ab41.97dd 172.16.0.7
                                 10.0.0.1              -       100     0       65001 i Or-ID: 10.0.0.4 C-LST: 10.0.0.5
 * >      RD: 10.0.0.6:1001 mac-ip aac1.abec.2f03
                                 -                     -       -       0       i
 * >      RD: 10.0.0.6:1001 mac-ip aac1.abec.2f03 172.16.1.8
                                 -                     -       -       0       i
 * >      RD: 10.0.0.1:1000 imet 10.0.0.1
                                 10.0.0.1              -       100     0       65001 i Or-ID: 10.0.0.4 C-LST: 10.0.0.5
 * >      RD: 10.0.0.6:1001 imet 10.0.0.6
                                 -                     -       -       0       i
 * >      RD: 65000:1 ip-prefix 172.16.0.0/24
                                 10.0.0.1              -       100     0       65001 i Or-ID: 10.0.0.4 C-LST: 10.0.0.5
 * >      RD: 65000:1 ip-prefix 172.16.1.0/24
                                 -                     -       -       0       i
```

* Every EVPN device has type-2 routes for all hosts in both sites (LB has type-2 routes for HA and HB). Stretched VLAN is thus a no-brainer.
* LB also has a prefix route for 172.16.0.0/24 advertised by LA.

Next, let's inspect one of the EVPN routes advertised by LA, for example, the **mac-ip** route for HA:

{{<cc>}}EVPN routes advertised by LA as seen by LB{{</cc>}}
```
lb#show bgp evpn route-type mac-ip next-hop 10.0.0.1 detail
BGP routing table information for VRF default
Router identifier 10.0.0.6, local AS number 65002
BGP routing table entry for mac-ip aac1.ab41.97dd, Route Distinguisher: 10.0.0.1:1000
 Paths: 1 available
  65001
    10.0.0.1 from 10.0.0.5 (10.0.0.5)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Originator: 10.0.0.4, Cluster list: 10.0.0.5
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000 ESI: 0000:0000:0000:0000:0000
BGP routing table entry for mac-ip aac1.ab41.97dd 172.16.0.7, Route Distinguisher: 10.0.0.1:1000
 Paths: 1 available
  65001
    10.0.0.1 from 10.0.0.5 (10.0.0.5)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Originator: 10.0.0.4, Cluster list: 10.0.0.5
      Extended Community: Route-Target-AS:65000:1 Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:a3:d9:29
      VNI: 101000 L3 VNI: 200000 ESI: 0000:0000:0000:0000:0000
```

The EVPN routes advertised by LA have:

* LA (10.0.0.1) as the next hop, meaning that LB and LA can exchange VXLAN traffic directly.
* CB (10.0.0.5 -- the route reflector) as the neighbor sending the BGP route
* WB (10.0.0.4 -- the WAN edge router) as the originator of the reflected route

Apart from that, all the other information in the EVPN routes observed on LB is the same as if LA were to send it directly. No wonder everything works as expected ;)

Don't trust me? Build the lab and explore!

### Kicking the Tires

Exploring the EVPN behavior of your favorite devices is trivial[^IST]:

[^IST]: After investing the time needed to build the lab environment

* Set up a _netlab_ environment ([example](https://blog.ipspace.net/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#lab), [installation guide](https://netlab.tools/install/), using [GitHub Codespaces](/2024/07/netlab-examples-codespaces/))
* Download the [lab topology file](https://github.com/ipspace/netlab-examples/blob/master/EVPN/inter-as-multi-pod/topology.yml) into an empty directory or use `netlab up https://github.com/ipspace/netlab-examples/blob/master/EVPN/inter-as-multi-pod/topology.yml` ([more details](/2025/09/netlab-download-url/))
* Execute `netlab up`, optionally adding  `-d _your_device_` and  `-p _provider_`. The lab topology uses Arista EOS containers; to use SR Linux, use `-d srlinux`, to use Aruba AOS-CX VMs, use `-d arubacx -p libvirt` ([more options](https://netlab.tools/module/evpn/)).

### More Details

Want to know more? Watch the free videos from the *Using VXLAN and EVPN in Multi-Pod and Multi-Site Fabric* presentation by Lukas Krattiger -- part of [Multi-Pod and Multi-Site Fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) section of [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.
