---
title: "EVPN Designs: EVPN IBGP over IPv4 EBGP"
series_title: "EVPN IBGP over IPv4 EBGP"
date: 2024-11-25 10:57:00+0200
tags: [ EVPN, design, netlab, vxlan ]
netlab_tag: evpn_dg
evpn_tag: designs
pre_scroll: True
---
We'll conclude the [EVPN designs saga](/tag/evpn/#designs) with the *"most creative"* design promoted by some networking vendors: running an IBGP session (carrying EVPN address family) between loopbacks advertised with EBGP IPv4 address family.

{{<figure src="/2024/11/evpn-design-ibgp-over-ebgp.png" caption="Oversimplified IBGP-over-EBGP design">}}

There's just a tiny gotcha in the above *Works Best in PowerPoint* diagram. IBGP assumes the BGP neighbors are *in the same autonomous system* while EBGP assumes they are *in different autonomous systems*. The usual way out of that *OMG, I painted myself into a corner* situation is to use *BGP local AS* functionality on the underlay EBGP session:
<!--more-->

* All routers are in the same BGP AS. The sessions between loopback interfaces are thus IBGP sessions.
* The routers use *local AS* functionality on the underlay BGP sessions to persuade the BGP neighbors they belong to different autonomous systems. As both BGP neighbors use the same trick, the underlay BGP session becomes an EBGP session.

{{<figure src="/2024/11/evpn-design-ibgp-over-ebgp-asn.png" caption="Using BGP Local AS functionality to turn IBGP sessions into EBGP sessions">}}

If the above diagram made your head explode and you started wondering why someone would try to make you implement something as convoluted instead of a much simpler [IBGP-over-IGP design](/2024/05/evpn-designs-ibgp-full-mesh/), you're not alone.

The networking engineers who implemented this design based on the recommendation from their favorite vendor usually find a variety of explanations for why it is better than the alternatives; I particularly love the *it's simpler than running single-area OSPF over unnumbered fabric interfaces* one. In reality, the root cause is either:

* A product manager desperately trying to look cool
* Trying to put some lipstick on a product that works well in the EVPN-over-IBGP world (but sucks when trying to run EVPN over EBGP) to make it [enticing to the GIFEE crowd](/2024/10/evpn-designs-ebgp-ebgp/#fix) that can't spell anything but BGP.

Anyway, if you're desperate to try out this spaghetti mess of complexity, we have you covered. _netlab_ supports this design (and all other designs in this series), and the [sample topology](https://github.com/ipspace/netlab-examples/blob/master/EVPN/ibgp-ebgp/topology.yml) is [available on GitHub](https://github.com/ipspace/netlab-examples/tree/master/EVPN/ibgp-ebgp).

{{<printout>}}
defaults.device: eos
provider: clab

plugin: [ fabric ]

bgp.as: 65000
bgp.activate.ipv4: [ ebgp ]                     # Activate IPv4 only on EBGP sessions
defaults.bgp.warnings.missing_igp: False        # Skip the "you probably need an IGP" warnings

groups:
  _auto_create: True
  leafs:
    members: [ L1, L2, L3, L4 ]
    module: [ bgp, vlan, vxlan, evpn ]
  spines:
    members: [ S1, S2 ]
    module: [ bgp, evpn ]
    bgp.rr: True
  hosts:
    members: [ H1, H2, H3, H4 ]
    device: linux

vlan.mode: bridge
vlans:
  orange:
    links: [ H1-L1, H2-L3 ]
  blue:
    links: [ H3-L2, H4-L4 ]

links:
- L1:
    bgp.local_as: 65101
  S1:
    bgp.local_as: 65200
- L1:
    bgp.local_as: 65101
  S2:
    bgp.local_as: 65200
- L2:
    bgp.local_as: 65102
  S1:
    bgp.local_as: 65200
- L2:
    bgp.local_as: 65102
  S2:
    bgp.local_as: 65200
- L3:
    bgp.local_as: 65103
  S1:
    bgp.local_as: 65200
- L3:
    bgp.local_as: 65103
  S2:
    bgp.local_as: 65200
- L4:
    bgp.local_as: 65104
  S1:
    bgp.local_as: 65200
- L4:
    bgp.local_as: 65104
  S2:
    bgp.local_as: 65200

tools:
  graphite:
{{</printout>}}

We had to make these changes to the [IBGP with route reflectors topology](/2024/09/evpn-designs-ibgp-rr/#lab) to make it work:

* We can no longer use the *fabric* plugin, as we have to configure link-specific parameters on every fabric link.
* The IPv4 address family is activated only on EBGP sessions (line 7)
* _netlab_ should not complain that we need an IGP (line 8). We know better.
* We have to define individual fabric links and specify BGP local AS numbers for both nodes attached to the fabric links (lines 30-62).
* The lab topology does not use unnumbered fabric links to work with a broader range of devices. If you want to test the interface EBGP sessions, add `addressing.p2p.ipv4: True` to the lab topology.

Assuming you already set up the lab infrastructure, you can start the lab with the **netlab up** command. You can also [start the lab in a GitHub Codespace](/2024/07/netlab-examples-codespaces/) (the directory is `EVPN/ibgp-ebgp`); you'll still have to [import the Arista cEOS container](/2024/07/arista-eos-codespaces/), though.

Here are the relevant bits of L1 configuration if you don't want to get your hands dirty. You can also get complete configurations for [Arista EOS](https://github.com/ipspace/netlab-examples/tree/master/EVPN/ibgp-ebgp/eos) and [FRRouting](https://github.com/ipspace/netlab-examples/tree/master/EVPN/ibgp-ebgp/frr) on [GitHub](https://github.com/ipspace/netlab-examples/tree/master/EVPN/ibgp-ebgp).

```
vlan 1000
   name orange
!
interface Vlan1000
   description VLAN orange (1000) -> [H1,H2,L3]
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vlan 1000 vni 101000
!
router bgp 65000
   router-id 10.0.0.1
   no bgp default ipv4-unicast
   neighbor 10.0.0.5 remote-as 65000
   neighbor 10.0.0.5 update-source Loopback0
   neighbor 10.0.0.5 description S1
   neighbor 10.0.0.5 send-community standard extended large
   neighbor 10.0.0.6 remote-as 65000
   neighbor 10.0.0.6 update-source Loopback0
   neighbor 10.0.0.6 description S2
   neighbor 10.0.0.6 send-community standard extended large
   neighbor 10.1.0.2 remote-as 65200
   neighbor 10.1.0.2 local-as 65101 no-prepend replace-as
   neighbor 10.1.0.2 description S1
   neighbor 10.1.0.6 remote-as 65200
   neighbor 10.1.0.6 local-as 65101 no-prepend replace-as
   neighbor 10.1.0.6 description S2
   !
   vlan 1000
      rd 10.0.0.1:1000
      route-target import 65000:1000
      route-target export 65000:1000
      redistribute learned
   !
   address-family evpn
      neighbor 10.0.0.5 activate
      neighbor 10.0.0.6 activate
   !
   address-family ipv4
      neighbor 10.1.0.2 activate
      neighbor 10.1.0.6 activate
      network 10.0.0.1/32
!
end
```

### Does It Work?

Of course, it does. The IPv4 BGP sessions look like EBGP sessions:

{{<cc>}}BGP neighbors for the IPv4 unicast address family on L1 running Arista EOS{{</cc>}}
```
L1#show bgp ipv4 unicast summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  S1                       10.1.0.2 4 65200             18        17    0    0 00:09:43 Estab   4      4
  S2                       10.1.0.6 4 65200             18        20    0    0 00:09:43 Estab   4      4
```

The IPv4 BGP routes look like they're coming through a series of autonomous systems:

{{<cc>}}IPv4 BGP routes on L1 running Arista EOS{{</cc>}}
```
L1#show bgp ipv4 unicast
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed contributor, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >      10.0.0.2/32            10.1.0.2              0       -          100     0       65200 65102 i
 *        10.0.0.2/32            10.1.0.6              0       -          100     0       65200 65102 i
 * >      10.0.0.3/32            10.1.0.2              0       -          100     0       65200 65103 i
 *        10.0.0.3/32            10.1.0.6              0       -          100     0       65200 65103 i
 * >      10.0.0.4/32            10.1.0.2              0       -          100     0       65200 65104 i
 *        10.0.0.4/32            10.1.0.6              0       -          100     0       65200 65104 i
 * >      10.0.0.5/32            10.1.0.2              0       -          100     0       65200 i
 * >      10.0.0.6/32            10.1.0.6              0       -          100     0       65200 i
```

Meanwhile, the EVPN address family runs over IBGP sessions:

{{<cc>}}BGP neighbors for the EVPN address family on L1 running Arista EOS{{</cc>}}
```
L1#show bgp evpn summary
BGP summary information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  S1                       10.0.0.5 4 65000             25        20    0    0 00:12:41 Estab   4      4
  S2                       10.0.0.6 4 65000             25        20    0    0 00:12:41 Estab   4      4
```

Not surprisingly (spines are route reflectors), L1 receives a variety of EVPN routes from other leaf switches, and EVPN works in exactly the same way as it did in the IBGP-over-OSPF scenario:

{{<cc>}}EVPN routes on L1 running Arista EOS{{</cc>}}
```
L1#show bgp evpn
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                    c - Contributing to ECMP, % - Pending best path selection
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >Ec    RD: 10.0.0.3:1000 mac-ip aac1.ab46.fb62
                                 10.0.0.3              -       100     0       i Or-ID: 10.0.0.3 C-LST: 10.0.0.5
 *  ec    RD: 10.0.0.3:1000 mac-ip aac1.ab46.fb62
                                 10.0.0.3              -       100     0       i Or-ID: 10.0.0.3 C-LST: 10.0.0.5
 * >      RD: 10.0.0.1:1000 mac-ip aac1.ab95.68cd
                                 -                     -       -       0       i
 * >      RD: 10.0.0.1:1000 imet 10.0.0.1
                                 -                     -       -       0       i
 * >Ec    RD: 10.0.0.2:1001 imet 10.0.0.2
                                 10.0.0.2              -       100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.5
 *  ec    RD: 10.0.0.2:1001 imet 10.0.0.2
                                 10.0.0.2              -       100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.5
 * >Ec    RD: 10.0.0.3:1000 imet 10.0.0.3
                                 10.0.0.3              -       100     0       i Or-ID: 10.0.0.3 C-LST: 10.0.0.5
 *  ec    RD: 10.0.0.3:1000 imet 10.0.0.3
                                 10.0.0.3              -       100     0       i Or-ID: 10.0.0.3 C-LST: 10.0.0.5
 * >Ec    RD: 10.0.0.4:1001 imet 10.0.0.4
                                 10.0.0.4              -       100     0       i Or-ID: 10.0.0.4 C-LST: 10.0.0.5
 *  ec    RD: 10.0.0.4:1001 imet 10.0.0.4
                                 10.0.0.4              -       100     0       i Or-ID: 10.0.0.4 C-LST: 10.0.0.5
```


### Is It Worth the Effort?

Probably not. I might be biased, but I find OSPF over unnumbered interfaces simpler than configuring BGP neighbors and keeping track of BGP local AS numbers.

Also, if this is your vendor's recommended design, it might be time to look around. Who knows what else is lurking in the shadows?
