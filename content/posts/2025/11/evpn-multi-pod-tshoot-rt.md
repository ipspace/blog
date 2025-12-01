---
title: "Multi-Pod EVPN Troubleshooting (Route Targets)"
date: 2025-11-25 07:49:00+0200
tags: [ EVPN, netlab ]
evpn_tag: details
netlab_tag: evpn_dg
---
Last week, we [fixed the incorrect BGP next hops](/2025/11/evpn-multi-pod-tshoot-example/) in our sample [multi-pod EVPN fabric](/2025/10/evpn-designs-multi-pod/). With that fixed, every PE device should see every other PE device as a remote VTEP for ingress replication purposes. However, that's not the case; let's see why and fix it.

**Note:** This is the fourth blog post in the Multi-Pod EVPN series. If you stumbled upon it, start with the [design overview](/2025/10/evpn-designs-multi-pod/) and [troubleshooting overview](/2025/10/troubleshoot-multi-pod-evpn/) posts. More importantly, familiarize yourself with the topology we'll be using; it's described in the [Multi-Pod EVPN Troubleshooting: Fixing Next Hops](/2025/11/evpn-multi-pod-tshoot-example/).

Ready? Let's go. Here's our network topology:
<!--more-->
{{<figure src="/2025/11/evpn-tshoot-topo.png">}}

### What's the Problem?

As I explained in the [previous blog post](/2025/11/evpn-multi-pod-tshoot-example/), use the EVPN type-3 (Inclusive Multicast Ethernet Tag) to verify that EVPN routes are propagated as expected and that the BGP next hops are correct. This is the printout you would get on LA after fixing the BGP next hop misconfiguration:

{{<cc>}}IMET routes on LA{{</cc>}}
```
la#show bgp evpn route-type imet
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65001
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.2:1000 imet 10.0.0.2
                                 -                     -       -       0       i
 * >      RD: 10.0.0.4:1000 imet 10.0.0.4
                                 10.0.0.4              -       100     0       65002 i
```

We have two IMET routes on LA, one local, the other advertised by LB. The next hops are correct, and the routes are valid and best. However, LA refuses to recognize LB as the remote VTEP for our VLAN.

{{<cc>}}Remote VTEPs on LA{{</cc>}}
```
la#show vxlan vtep
Remote VTEPS for Vxlan1:

VTEP       Tunnel Type(s)
---------- --------------

Total number of remote VTEPS:  0
```

### Spot the Difference

As before, let's look into the details of the IMET routes. Can you spot the crucial difference between the two?

{{<cc>}}Details of IMET routes on LA{{</cc>}}
```
la#show bgp evpn route-type imet detail
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65001
BGP routing table entry for imet 10.0.0.2, Route Distinguisher: 10.0.0.2:1000
 Paths: 1 available
  Local
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref -, weight 0, tag 0, valid, local, best
      Extended Community: Route-Target-AS:65001:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000
      PMSI Tunnel: Ingress Replication, MPLS Label: 101000, Leaf Information Required: false, Tunnel ID: 10.0.0.2
BGP routing table entry for imet 10.0.0.4, Route Distinguisher: 10.0.0.4:1000
 Paths: 1 available
  65002
    10.0.0.4 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65002:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000
      PMSI Tunnel: Ingress Replication, MPLS Label: 101000, Leaf Information Required: false, Tunnel ID: 10.0.0.4
```

Most of the route attributes match (VNI, MPLS label, encapsulation type), but the route targets are different.

Let's see what route targets LA imports into its MAC VRF:

{{<cc>}}BGP MAC-VRF configuration on LA{{</cc>}}
```
router bgp 65001
   vlan 1000
      rd 10.0.0.2:1000
      route-target import 65001:1000
      route-target export 65001:1000
      redistribute learned
```

No wonder LA ignores the route from LB. The route target community LB attaches to its routes does not match the import route target on LA.

{{<long-quote>}}
It took me quite a bit of effort to persuade _netlab_ to misconfigure the leaf switches, as it insists on creating a working network.

In real life, it's easy to get this mismatch if you configure the two fabrics independently and connect them later. Even worse (for this scenario), some EVPN implementations use *automatic route targets* derived from local BGP AS number and VLAN ID. In those cases, a mismatch is almost guaranteed if you don't configure route targets manually.

Want even more confusion? I've heard of implementations ignoring the AS part of the route target because they're focused on EVPN-over-EBGP. Troubleshooting such implementations in multi-vendor deployments must be a real treat.
{{</long-quote>}}

We could fix the problem in one of two ways:

1. Add remote import route targets on LA and LB.
2. Fix the import and export route targets to use a consistent value across autonomous systems.

While the first approach is non-disruptive, it does not scale well if you plan to add more pods to your fabric. Let's go with the second one and change the import and export route targets to 65000:1.

### Are We Done Yet?

After fixing the route target values, all IMET routes on LA have the same route target:

{{<cc>}}IMET routes on LA after we fixed the route targets{{</cc>}}
```
la#show bgp evpn route-type imet detail
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65001
BGP routing table entry for imet 10.0.0.2, Route Distinguisher: 10.0.0.2:1000
 Paths: 1 available
  Local
    - from - (0.0.0.0)
      Origin IGP, metric -, localpref -, weight 0, tag 0, valid, local, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000
      PMSI Tunnel: Ingress Replication, MPLS Label: 101000, Leaf Information Required: false, Tunnel ID: 10.0.0.2
BGP routing table entry for imet 10.0.0.4, Route Distinguisher: 10.0.0.4:1000
 Paths: 1 available
  65002
    10.0.0.4 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65000:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000
      PMSI Tunnel: Ingress Replication, MPLS Label: 101000, Leaf Information Required: false, Tunnel ID: 10.0.0.4
```

LA also recognizes LB as a remote VTEP and will flood the BUM frames on VLAN 1000 to it:

{{<cc>}}Remote VTEPs on LA{{</cc>}}
```
la#show vxlan vtep detail
Remote VTEPS for Vxlan1:

VTEP           Learned Via         MAC Address Learning       Tunnel Type(s)
-------------- ------------------- -------------------------- --------------
10.0.0.4       control plane       control plane              flood

Total number of remote VTEPS:  1
```

However, we still have a problem on LB; it does not recognize LA as a remote VTEP:

{{<cc>}}LB still does not have remote VTEPs{{</cc>}}
```
lb#show vxlan vtep detail
Remote VTEPS for Vxlan1:

VTEP       Learned Via       MAC Address Learning       Tunnel Type(s)
---------- ----------------- -------------------------- --------------

Total number of remote VTEPS:  0
```

{{<next-in-series page="/posts/2025/12/evpn-multi-pod-tshoot-xc.md">}}
What could possibly be wrong now? We'll figure it out in the next blog post in this series.
{{</next-in-series>}}
