---
title: "Example: Multi-Pod EVPN Troubleshooting (Part 1)"
date: 2025-11-18 08:27:00+0200
tags: [ EVPN, netlab ]
evpn_tag: details
netlab_tag: evpn_dg
netlab_title: "Multi-Pod EVPN Troubleshooting (Part 1)"
---
Last month, I wrote about the [specifics of troubleshooting](/2025/10/troubleshoot-multi-pod-evpn/) [multi-pod EVPN designs](/2025/10/evpn-designs-multi-pod/). Today, I'd like to start a journey through an example in which (channeling my inner CCIE preparation lab instructor) I broke as many things as I could think of.

Here's the lab topology we'll use (and as usual, the corresponding _netlab_ topology file and device configurations are on GitHub). Our network has two sites (pods), each with a spine switch, a leaf switch, and a host attached to the leaf switch. The inter-pod link is connected to the spine switches to minimize the number of devices.
<!--more-->
{{<figure src="/2025/11/evpn-tshoot-topo.png">}}

Each site is running an IGP and IBGP. The spine switches exchange IPv4 and EVPN routes over an EBGP session. The BGP sessions mostly follow the physical links.

### Are We Getting the Routes?

There are tons of things that can go wrong in a complex design like ours, making the [bisection troubleshooting](https://en.wikipedia.org/wiki/Bisection_(software_engineering)) one of the fastest ways to identify the problem. I'll start with "Is the control plane working?", in particular, "Do I see EVPN routes from LA on LB and vice versa?" If we can see the EVPN routes from the other pod, the BGP route propagation works correctly, and we should focus on the contents of the EVPN routes. Otherwise, we should start investigating the BGP sessions.

Every VTEP in an EVPN network should generate an *inclusive multicast* (type 3, IMET) EVPN route to allow other VTEPs to build ingress replication lists. Checking for the presence of these routes is thus an ideal starting point. 

Here are the IMET routes on LA and LB. The BGP transport of EVPN routes between our pods clearly works; there must be something wrong with the contents of the EVPN routes.

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
          RD: 10.0.0.4:1000 imet 10.0.0.4
                                 10.1.0.2              -       100     0       65002 i
```

{{<cc>}}IMET routes on LB{{</cc>}}
```
lb#show bgp evpn route-type imet
BGP routing table information for VRF default
Router identifier 10.0.0.4, local AS number 65002
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >      RD: 10.0.0.2:1000 imet 10.0.0.2
                                 10.0.0.2              -       100     0       65001 i
 * >      RD: 10.0.0.4:1000 imet 10.0.0.4
                                 -                     -       -       0       i
```

Can you spot the difference between the two printouts? 

Let me help you: the two IP addresses associated with a remote IMET route on LB are the same but differ on LA, so let's investigate the details of how LA sees the LB's IMET route:

{{<cc>}}IMET route details on LA{{</cc>}}
```
la#show bgp evpn route-type imet 10.0.0.4 detail
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65001
BGP routing table entry for imet 10.0.0.4, Route Distinguisher: 10.0.0.4:1000
 Paths: 1 available
  65002
    10.1.0.2 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, invalid, internal
      Extended Community: Route-Target-AS:65002:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000
      PMSI Tunnel: Ingress Replication, MPLS Label: 101000, Leaf Information Required: false, Tunnel ID: 10.0.0.4
```

The tunnel ID 10.0.0.4 (LB) is correct, but the next hop (10.1.0.2) advertised by 10.0.0.1 (LA) is not. The EVPN next hop should not change in a multi-pod EVPN design; we're dealing with the first misconfiguration.

### Fixing Next Hops

To identify the router changing the next hop, follow the BGP sessions toward the source (LB). The next hop is changed on CA, but not on CB:

{{<cc>}}The IMET route on CA{{</cc>}}
```
ca#show bgp evpn route-type imet 10.0.0.4 detail
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65001
BGP routing table entry for imet 10.0.0.4, Route Distinguisher: 10.0.0.4:1000
 Paths: 1 available
  65002
    10.1.0.2 from 10.1.0.2 (10.0.0.3)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, external, best
      Extended Community: Route-Target-AS:65002:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000
      PMSI Tunnel: Ingress Replication, MPLS Label: 101000, Leaf Information Required: false, Tunnel ID: 10.0.0.4
```

{{<cc>}}The IMET route on CB{{</cc>}}
```
cb# show bgp l2vpn evpn route detail type 3
Route Distinguisher: 10.0.0.2:1000
BGP routing table entry for 10.0.0.2:1000:[3]:[0]:[32]:[10.0.0.2]
Paths: (1 available, best #1)
  Advertised to peers:
  10.0.0.4 10.1.0.1
  Route [3]:[0]:[32]:[10.0.0.2]
  65001
    10.0.0.2 from 10.1.0.1 (10.0.0.1)
      Origin IGP, valid, external, bestpath-from-AS 65001, best (First path received)
      Last update: Sat Nov 15 08:33:14 2025
      PMSI Tunnel Type: Ingress Replication, label: 101000
Route Distinguisher: 10.0.0.4:1000
BGP routing table entry for 10.0.0.4:1000:[3]:[0]:[32]:[10.0.0.4]
Paths: (1 available, best #1)
  Advertised to peers:
  10.0.0.4 10.1.0.1
  Route [3]:[0]:[32]:[10.0.0.4]
  Local, (Received from a RR-client)
    10.0.0.4 (metric 20) from 10.0.0.4 (10.0.0.4)
      Origin IGP, localpref 100, valid, internal, bestpath-from-AS Local, best (First path received)
      Extended Community: RT:65002:1000 ET:8
      Last update: Sat Nov 15 08:33:17 2025
      PMSI Tunnel Type: Ingress Replication, label: 101000
```

**Conclusion:** CB is changing the EVPN next hop when advertising EVPN routes over the EBGP session. Let's inspect the EVPN configuration on CB:

{{<cc>}}FRRouting EVPN configuration on CB{{</cc>}}
```
router bgp 65002
 bgp router-id 10.0.0.3
 no bgp default ipv4-unicast
 bgp cluster-id 10.0.0.3
 bgp bestpath as-path multipath-relax
 neighbor 10.0.0.4 remote-as 65002
 neighbor 10.0.0.4 description lb
 neighbor 10.0.0.4 update-source lo
 neighbor 10.1.0.1 remote-as 65001
 neighbor 10.1.0.1 description ca
 !
 address-family l2vpn evpn
  neighbor 10.0.0.4 activate
  neighbor 10.0.0.4 route-reflector-client
  neighbor 10.1.0.1 activate
  neighbor 10.1.0.1 next-hop-self
  advertise-all-vni
  advertise-svi-ip
  advertise ipv4 unicast
 exit-address-family
```

It's relatively easy to identify the incorrect configuration once you know what to look for: the **neighbor next-hop-self** command should not be used in the EVPN address family.

{{<note warn>}}
Configuring a similar command on Arista EOS stops the propagation of EVPN routes over the EBGP session, resulting in a confusing scenario where the BGP session works, the EVPN address family is negotiated, but the spine switch sends no routes.

That behavior forced me to use FRRouting on CB to demonstrate the impact of next-hop mangling.
{{</note>}}

Removing that command results in correct BGP next hops on LA:

{{<cc>}}LA's view of IMET route advertised by LB after we fixed the next-hop handling on CB{{</cc>}}
```
la#show bgp evpn route-type imet 10.0.0.4 detail
BGP routing table information for VRF default
Router identifier 10.0.0.2, local AS number 65001
BGP routing table entry for imet 10.0.0.4, Route Distinguisher: 10.0.0.4:1000
 Paths: 1 available
  65002
    10.0.0.4 from 10.0.0.1 (10.0.0.1)
      Origin IGP, metric -, localpref 100, weight 0, tag 0, valid, internal, best
      Extended Community: Route-Target-AS:65002:1000 TunnelEncap:tunnelTypeVxlan
      VNI: 101000
      PMSI Tunnel: Ingress Replication, MPLS Label: 101000, Leaf Information Required: false, Tunnel ID: 10.0.0.4
```

However, the IMET route advertised by LB is still not recognized as a valid remote VTEP on LA:

{{<cc>}}Remote VTEPs on LA{{</cc>}}
```
la#show vxlan vtep
Remote VTEPS for Vxlan1:

VTEP       Tunnel Type(s)
---------- --------------

Total number of remote VTEPS:  0
```

{{<next-in-series page="/posts/2025/11/evpn-multi-pod-tshoot-part-2.md">}}
What could possibly be wrong now? We'll figure it out in the next blog post in this series.
{{</next-in-series>}}
