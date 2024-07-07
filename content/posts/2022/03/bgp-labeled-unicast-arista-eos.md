---
title: "BGP Labeled Unicast on Arista EOS"
date: 2022-03-29 07:50:00
tags: [ BGP, MPLS ]
pre_scroll: True
---
A week ago I described how [Cisco IOS implemented BGP Labeled Unicast](/2022/03/bgp-labeled-unicast-cisco-ios/). In this blog post we'll focus on Arista EOS using [the same lab as before](https://github.com/ipspace/netlab-examples/tree/master/MPLS/ldp-bgp-lu):

{{<figure src="/2022/03/bgp-lu-topology.bgp-eos.jpg" caption="BGP sessions in the BGP-LU lab">}}

<!--more-->
{{<note info>}}Arista EOS has two sets of routing daemons configured as *ribd* or *multi-agent* model. This blog post is describing the behavior of *multi-agent* model.{{</note>}}

Arista EOS treats Labeled Unicast as a completely separate address family:

{{<cc>}}BGP-LU configuration on Arista EOS{{</cc>}}
```
pe1#show run sect bgp
router bgp 65000
   router-id 10.0.0.1
   bgp advertise-inactive
   neighbor 10.0.0.4 remote-as 65000
   neighbor 10.0.0.4 next-hop-self
   neighbor 10.0.0.4 update-source Loopback0
   neighbor 10.0.0.4 description rr
   neighbor 10.0.0.4 send-community standard extended
   neighbor 10.1.0.1 remote-as 65101
   neighbor 10.1.0.1 description ce1
   neighbor 10.1.0.1 send-community standard
   !
   address-family ipv4
      neighbor 10.0.0.4 activate
      neighbor 10.1.0.1 activate
      network 10.0.0.1/32
   !
   address-family ipv4 labeled-unicast
      neighbor 10.0.0.4 activate
      neighbor 10.1.0.1 activate
      network 10.0.0.1/32
```

An IP prefix can be advertised with or without a label, but it has to be listed in a **network** statement in the corresponding address family (or redistributed into it).

While it looks like BGP routing processes on Arista EOS store labeled and unlabeled prefixes in the same BGP RIB (at least according to the **show ip bgp** printouts), the RIB contains two copies of the same prefix if they were advertised over the two address families. 

For example, the RIB table on PE1 contains two copies of all IPv4 prefixes advertised in our lab apart from the prefix advertised by CE1 which does not use IPv4 Labeled Unicast.

{{<cc>}}IPv4 BGP prefixes on PE1{{</cc>}}
```
pe1#show ip bgp
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
Route status codes: s - suppressed, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup, L - labeled-unicast
                    % - Pending BGP convergence
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI Origin Validation codes: V - valid, I - invalid, U - unknown
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >  L   10.0.0.1/32            -                     -       -          -       0       i
 * >      10.0.0.2/32            10.0.0.2              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
 * >  L   10.0.0.2/32            10.0.0.2              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
 * >      10.0.0.4/32            10.0.0.4              0       -          100     0       i
 * >  L   10.0.0.4/32            10.0.0.4              0       -          100     0       i
 * >      10.0.0.5/32            10.1.0.1              0       -          100     0       65101 i
 * >      10.0.0.6/32            10.0.0.2              0       -          100     0       65102 i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
 * >  L   10.0.0.6/32            10.0.0.2              0       -          100     0       65102 i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
```

Looking at an individual prefix, you'll notice that both copies are the **best** routes (in their corresponding address families):

{{<cc>}}BGP entries for 10.0.0.6 on PE1{{</cc>}}
```
pe1#show ip bgp 10.0.0.6
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for 10.0.0.6/32
 Paths: 2 available
  65102
    10.0.0.2 from 10.0.0.4 (10.0.0.4)
      Origin IGP, metric 0, localpref 100, IGP metric 30, weight 0, tag 0
      Received 01:36:01 ago, valid, internal, best
      Originator: 10.0.0.2, Cluster list: 10.0.0.4
      Rx SAFI: Unicast
      Tunnel RIB eligible
  65102
    10.0.0.2 labels [ 100000 ] from 10.0.0.4 (10.0.0.4)
      Origin IGP, metric 0, localpref 100, IGP metric 30, weight 0, tag 0
      Received 01:35:57 ago, valid, internal, best
      Originator: 10.0.0.2, Cluster list: 10.0.0.4
      Local MPLS label: 100001
      Rx SAFI: MplsLabel
      Tunnel RIB eligible
```

Even more interesting, Arista EOS does not enter the labeled unicast prefixes into the IP routing table by default. After deactivating the neighbors in the IPv4 address family on the route reflector (turning the central AS into BGP-LU-only AS), the routing table on PE2 no longer contains the BGP route for CE1.

{{<figure src="/2022/03/bgp-lu-only-topology.jpg" caption="Route reflector in AS6500 propagates only BGP-LU prefixes">}}

{{<cc>}}BGP table and IP routing table on PE2 after the reconfiguration of route reflector in AS65000{{</cc>}}
```
pe2#show ip bgp
...
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >  L   10.0.0.1/32            10.0.0.1              0       -          100     0       i Or-ID: 10.0.0.1 C-LST: 10.0.0.4
 * >      10.0.0.2/32            -                     -       -          -       0       i
 * >  L   10.0.0.2/32            -                     -       -          -       0       i
 * >  L   10.0.0.4/32            10.0.0.4              0       -          100     0       i
 * >      10.0.0.6/32            10.1.0.5              0       -          100     0       65102 i
 * >  L   10.0.0.6/32            10.1.0.5              0       -          100     0       65102 i
pe2#show ip route bgp
...
 B E      10.0.0.6/32 [200/0] via 10.1.0.5, Ethernet1
```

You have to configure **bgp labeled-unicast rib ip** within the BGP routing process to use labeled unicast prefixes for IP forwarding. Doing that on PE1 brings the BGP prefix for CE2 into the routing table, including the label stack built from BGP-LU and LDP labels:

{{<cc>}}BGP prefixes and BGP routes in the IP routing table on PE1{{</cc>}}
```
pe1#show ip bgp
BGP routing table information for VRF default
...
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            -                     -       -          -       0       i
 * >  L   10.0.0.1/32            -                     -       -          -       0       i
 * >  L   10.0.0.2/32            10.0.0.2              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
 * >  L   10.0.0.4/32            10.0.0.4              0       -          100     0       i
 * >      10.0.0.5/32            10.1.0.1              0       -          100     0       65101 i
 * >  L   10.0.0.6/32            10.0.0.2              0       -          100     0       65102 i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
pe1#show ip route bgp
...
 B E      10.0.0.5/32 [200/0] via 10.1.0.1, Ethernet1
 B I      10.0.0.6/32 [200/0] via BGP LU Push tunnel index 23
                                 via LDP tunnel index 2, label 100000
                                    via 10.1.0.9, Ethernet2, label 116385
```

The **bgp labeled-unicast rib ip** nerd knob solves the IP forwarding challenges on PE1, but we're still missing the BGP prefix for CE1 on PE2 -- CE1 advertises its prefix only over IPv4 AF and that advertisement never gets across IPv4-LU-only route reflector.

I couldn't find a way to import routes from IPv4 address family into IPv4 Labeled Unicast address family, so it looks like we have these design options:

* Use BGP-LU to distribute next hop labels for other services (Inter-AS MPLS/VPN Option C typically uses this approach as does SR-MPLS-over-BGP). IPv4-LU/IPv6-LU address families are totally independent from the IPv4/IPv6 address families and are not used for IP forwarding.
* Use BGP-LU to distribute BGP prefixes that can be used for IP forwarding. Labeled prefixes are preferred over unlabeled ones, but you SHOULD run labeled- and unlabeled address families in parallel in a non-homogeneous environment to ensure at least one of them has a usable prefix.

Have I missed something? Please write a comment!

### Summary: Arista EOS

* Labeled unicast is configured as an independent address family. BGP neighbors have to be activated within the **ipv4 labeled-unicast** or **ipv6 labeled-unicast** address family.
* BGP prefixes must be originated within **ipv4/ipv6** and/or **ipv4 labeled-unicast/ipv6 labeled-unicast** address families. Unlabeled BGP prefixes cannot be imported into labeled address family or vice versa. Routes redistributed into BGP are not redistributed into **labeled-unicast** address families[^NN].
* Separate updates are sent for labeled and unlabeled prefixes.
* Labeled prefixes are not inserted into the IP routing- and forwarding tables unless you configure **bgp labeled-unicast rib ip** within the BGP routing process.

[^NN]: Or I missed another nerd knob, in which case please write  a comment and I'll fix the blog post.