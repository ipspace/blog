---
title: "EVPN Designs: Multi-Pod with IP-Only WAN Routers"
series_title: "Inter-AS Option C (IP-only WAN routers)"
date: 2025-10-15 08:12:00+0200
tags: [ EVPN, design, netlab, vxlan ]
netlab_tag: evpn_dg
evpn_tag: designs
pre_scroll: True
---
In the [multi-pod EVPN design](/2025/10/evpn-designs-multi-pod/), I described a simple way to merge two EVPN fabrics into a single end-to-end fabric. Here are a few highlights of that design:

* Each fabric is running OSPF and IBGP, with core (spine) devices being route reflectors
* There's an EBGP session between the WAN edge routers (sometimes called border leafs)
* Every BGP session carries IPv4 (underlay) and EVPN (overlay) routes.

In that design, the WAN edge routers have to support EVPN (at least in the control plane) and carry all EVPN routes for both fabrics. Today, we'll change the design to use simpler WAN edge routers that support only IP forwarding.
<!--more-->
Here's the lab setup we'll use. Each site has:

* A unique BGP AS number (65001 and 65002)
* An EVPN PE-device (leaf -- LA, LB) to which a Linux host is connected
* A spine switch (CA, CB) acting as a BGP route reflector
* A WAN edge router (WA, WB) connecting the site to the other site

{{<figure src="/2025/10/evpn-inter-as-c-topology.png" caption="Lab topology">}}

IPv4 BGP sessions are established as before; there's an IPv4 EBGP session between the WAN edge routers to exchange the (underlay) EVPN next-hop (VTEP) addresses:

{{<figure src="/2025/10/evpn-inter-as-c-bgp-ipv4.png" caption="BGP sessions with IPv4 address family">}}

However, instead of the EVPN address family using the EBGP session between the WAN edge routers, we'll establish a multihop EBGP session between the route reflectors. That EBGP session will carry only EVPN routes, not the IPv4 ones[^RRv4].

[^RRv4]: Enabling IPv4 address family on the multihop EBGP session would lead to recursive routing loop; the proof is left as an exercise for the reader.

{{<figure src="/2025/10/evpn-inter-as-c-bgp-evpn.png" caption="BGP sessions carrying EVPN routes (CA-CB is a multihop EBGP session between loopback interfaces)">}}

After establishing the multihop EVPN EBGP session between the route reflectors, we no longer need EVPN routes on the WAN edge routers, allowing us to use devices that do not support EVPN on the WAN edge. Effectively, we've implemented the *Inter-AS Option C*  design with EVPN/VXLAN.

### Does It Work?

Of course it does. [Start the lab](#lab) and check it out. Here are the EVPN routes you can see on an Arista EOS switch:

{{<cc>}}Type-3 (VTEPs) and type-5 (IP prefixes) EVPN routes on LB running Arista EOS{{</cc>}}
```
lb#show bgp evpn
BGP routing table information for VRF default
Router identifier 10.0.0.6, local AS number 65002
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.1:1000 imet 10.0.0.1
                                 10.0.0.1              -       100     0       65001 i
 * >      RD: 10.0.0.6:1001 imet 10.0.0.6
                                 -                     -       -       0       i
 * >      RD: 65000:1 ip-prefix 172.16.0.0/24
                                 10.0.0.1              -       100     0       65001 i
 * >      RD: 65000:1 ip-prefix 172.16.1.0/24
                                 -                     -       -       0       i
```

These are the details of the type-5 (IP prefix) route advertised by LA as seen on LB:

{{<cc>}}The details of a type-5 EVPN route propagated across multi-pod fabric{{</cc>}}
```
lb#show bgp evpn route-type ip-prefix 172.16.0.0/24 detail
BGP routing table information for VRF default
Router identifier 10.0.0.6, local AS number 65002
BGP routing table entry for ip-prefix 172.16.0.0/24, Route Distinguisher: 65000:1
 Paths: 1 available
  65001
    10.0.0.1 from 10.0.0.5 (10.0.0.5)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1 TunnelEncap:tunnelTypeVxlan EvpnRouterMac:00:1c:73:e9:97:bb
      VNI: 200000
```

The route's next hop is LA (correct -- next hops should not change in multi-pod deployments), and the router advertising the route to LB is CB (also correct).

### Behind the Scenes

Let's analyze the [_netlab_ topology file](https://github.com/ipspace/netlab-examples/blob/master/EVPN/inter-as-c/topology.yml) used to create the lab in case you're interested in recreating (or modifying) it.

{{<printout>}}
---
provider: clab
defaults.device: eos

module: [ bgp, ospf, evpn ]
evpn.session: [ ibgp ]
bgp.community.ebgp: [ standard, extended ]
plugin: [ ebgp.multihop ]

bgp.multihop:
  sessions: [ ca-cb ]
  activate.ipv4: evpn
{{</printout>}}

* We're using Arista EOS (line 3) containers (line 2)
* The three lab-wide modules are BGP, OSPF, and EVPN (line 5)
* EVPN routes are exchanged only on (regular) IBGP sessions (line 6)
* We have to transport extended communities on EBGP sessions (line 7)
* We're using the **ebgp.multihop** plugin to create the multihop EBGP session (line 8)
* There's a multihop EBGP session between CA and CB (line 11)
* The IPv4 multihop EBGP sessions should enable only the EVPN address family (line 12)

The device group definitions are a bit more complex than they were in the previous examples:

{{<printout start="13">}}
groups:
  _auto_create: True
  site_a:                     # Site A - core, leaf, wan edge
    members: [ la, ca, wa ]
    bgp.as: 65001
  site_b:
    members: [ wb, cb, lb ]   # Site B - core, leaf, wan edge
    bgp.as: 65002
  hosts:
    members: [ ha, hb ]       # Hosts attached to leaf-A and leaf-B
    device: linux
  spines:
    members: [ ca, cb ]
    module: [ ospf, bgp, evpn ]
    bgp.rr: True
    graph.rank: 1
  leafs:
    members: [ la, lb ]
    module: [ ospf, bgp, vxlan, vlan, vrf, evpn ]
    graph.rank: 2
  wan:
    members: [ wa, wb ]
    module: [ ospf, bgp ]
    graph.rank: 2
{{</printout>}}

* Site-A (LA, CA, WA) has BGP ASN 65001 (lines 16-18)
* Site-B (LA, CA, WA) has BGP ASN 65002 (lines 19-21)
* The spine switches run OSPF, BGP, and EVPN. They are also BGP route reflectors (lines 25-28)
* The leaf switches run not only OSPF, BGP, and EVPN in the control plane, but also VLANs, VRFs, and VXLAN in the data plane (lines 30-32)
* The WAN edge routers run just OSPF and BGP (lines 34-36)
* I had to set [**graph.rank** parameter](/2025/09/netlab-graphs-layout/#rank) on most devices to generate nice-looking graphs.

The rest of the [_netlab_ lab topology file](https://github.com/ipspace/netlab-examples/blob/master/EVPN/inter-as-c/topology.yml) is unchanged; for more details, read the [EVPN Designs: Layer-3 Inter-AS Option A](/2025/08/evpn-designs-interas-a/#topo) and [EVPN Designs: Multi-Pod Fabrics](/2025/10/evpn-designs-multi-pod/#topo) blog posts.

### Kicking the Tires { #lab }

Exploring whether your favorite device supports this design is trivial[^IST]:

[^IST]: After investing the time needed to build the lab environment

* Set up a _netlab_ environment ([example](https://blog.ipspace.net/2024/04/evpn-designs-vxlan-leaf-spine-fabric/#lab), [installation guide](https://netlab.tools/install/), using [GitHub Codespaces](/2024/07/netlab-examples-codespaces/) with [Arista cEOS containers](https://blog.ipspace.net/2024/07/arista-eos-codespaces/))
* Download the [lab topology file](https://github.com/ipspace/netlab-examples/blob/master/EVPN/inter-as-c/topology.yml) into an empty directory or use `netlab up https://github.com/ipspace/netlab-examples/blob/master/EVPN/inter-as-c/topology.yml` ([more details](/2025/09/netlab-download-url/))
* Execute `netlab up`, optionally adding  `-d _your_device_` and  `-p _provider_`. The lab topology uses Arista EOS containers; to use SR Linux, use `-d srlinux`, to use Aruba AOS-CX VMs, use `-d arubacx -p libvirt` ([more options](https://netlab.tools/module/evpn/)).

### More Details

Want to know more? Watch the free videos from the *Using VXLAN and EVPN in Multi-Pod and Multi-Site Fabric* presentation by Lukas Krattiger -- part of [Multi-Pod and Multi-Site Fabrics](https://my.ipspace.net/bin/list?id=Clos#MULTISITE) section of [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.
