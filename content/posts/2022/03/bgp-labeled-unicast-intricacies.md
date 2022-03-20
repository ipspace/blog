---
title: "BGP Labeled Unicast Intricacies"
date: 2022-03-23 07:50:00
tags: [ BGP, MPLS ]
pre_scroll: True
draft: True
---
While researching the BGP RFCs for the *[Three Dimensions of BGP Address Family Nerd Knobs](https://blog.ipspace.net/2022/01/bgp-af-nerd-knobs.html)*, I figured out that the BGP Labeled Unicast (BGP-LU, advertising MPLS labels together with BGP prefixes) uses a different address family. So far so good.

Now for the intricate bit: a BGP router might negotiate IPv4 and IPv4-LU address families with a neighbor. Does that mean that it's advertising every IPv4 prefix twice, once without a label, and once with a label? Should that be the case, how are those prefixes stored in the receiving router BGP table? As always, the correct answer is "_it depends_", this time on the network operating system implementation.
<!--more-->
### Setting the Stage

Whenever I get a question along the lines "_what would happen if..._" I always ask the sender "_... and did you consider testing that in a lab?_"[^STOP]. Let's do that: we'll test Cisco IOSv[^XES] and Arista EOS behavior in a simple lab with three autonomous systems and a route reflector in the central autonomous system. The lab topology file is [available on GitHub](https://github.com/ipspace/netsim-examples/tree/master/MPLS/ldp-bgp-lu); you'll need *netsim-tools* release 1.2 to deploy the lab[^NSBeta].

{{<figure src="/2022/03/bgp-lu-topology.bgp.png" caption="BGP sessions in the BGP-LU lab">}}

[^XES]: Cisco IOS XE seems to behave in exactly the same way.

[^STOP]: ... often followed by no reply whatsoever. Some people think they can use bloggers as Free Encyclopedia of Useless Trivia and walk away when asked to do a bit of homework first.

{{<note info>}}Please note that I'm not saying one implementation is more correct or better than the other. They are just different, and you should understand what the differences are.

Also, I probably missed a few Arista EOS nerd knobs, and it could be that BGP-LU in EOS works best with SR-MPLS. If you know more, please leave a comment and I'll update the blog post.{{</note>}}

[^NSBeta]: *netsim-tools* release 1.2 is available as a beta release. Follow the [installation instructions](https://netsim-tools.readthedocs.io/en/latest/install.html), and upgrade the *netsim-tools* package with `pip3 install --upgrade --pre netsim-tools`.

### Cisco IOS Behavior

Cisco IOS configures labeled unicast as an add-on to IPv4 or IPv6 address family:

{{<cc>}}BGP-LU configuration on Cisco IOS{{</cc>}}
```
router bgp 65000
 bgp router-id 10.0.0.1
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 neighbor 10.0.0.4 remote-as 65000
 neighbor 10.0.0.4 description rr
 neighbor 10.0.0.4 update-source Loopback0
 neighbor 10.1.0.1 remote-as 65101
 neighbor 10.1.0.1 description ce1
 !
 address-family ipv4
  network 10.0.0.1 mask 255.255.255.255
  neighbor 10.0.0.4 activate
  neighbor 10.0.0.4 send-community both
  neighbor 10.0.0.4 next-hop-self
  neighbor 10.0.0.4 send-label explicit-null
  neighbor 10.1.0.1 activate
  neighbor 10.1.0.1 send-community
  neighbor 10.1.0.1 send-label explicit-null
```

Both address families are negotiated on a BGP session...

{{<cc>}}BGP address families negotiated between PE1 and CE1 (both running Cisco IOS){{</cc>}}
```
pe1#show ip bgp neighbors 10.1.0.1 | section capabilities
  Neighbor capabilities:
    Route refresh: advertised and received(new)
    Four-octets ASN Capability: advertised and received
    Address family IPv4 Unicast: advertised and received
    ipv4 MPLS Label capability: advertised and received
    Enhanced Refresh Capability: advertised and received
    Multisession Capability:
    Stateful switchover support enabled: NO for session 1
```

... but only one update (with a label) is sent or received for every prefix. IPv4 address family is not used at all.

{{<cc>}}BGP updates between PE1 and CE1 (both running Cisco IOS){{</cc>}}
```
pe1#show debug
IP routing:
  BGP updates debugging is on for neighbor 10.1.0.1 (inbound) for all address families

pe1#clear ip bgp 10.1.0.1
pe1#
BGP(0): (base) 10.1.0.1 send UPDATE (format) 10.0.0.6/32, next 10.1.0.2, label 22, metric 0, path 65102, label 22
BGP(0): (base) 10.1.0.1 send UPDATE (format) 10.0.0.4/32, next 10.1.0.2, label 17, metric 0, path Local, label 17
BGP(0): (base) 10.1.0.1 send UPDATE (format) 10.0.0.1/32, next 10.1.0.2, label 0, metric 0, path Local, label exp-null
BGP(0): redist event (1) request for 10.1.0.1/32
BGP(0): 10.1.0.1 rcvd UPDATE w/ attr: nexthop 10.1.0.1, origin i, metric 0, merged path 65101, AS_PATH
BGP(0): 10.1.0.1 rcvd 10.0.0.5/32, label 0
```

### Arista EOS Behavior

We'll change the default device type in **netlab up** command to test Arista vEOS behavior with the same lab topology:

```
netlab up -d eos
```

Arista EOS configures BGP LU in a separate **labeled-unicast** address family:

```
pe1#show run section bgp
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

EOS treats IPv4 and IPv4-LU as completely independent address families. Local labels are assigned to prefixes received over **labeled-unicast** address family, but not to prefixes received over IPv4 address family. I found no way to assign a label to a prefix if the prefix originator did not do that (but I might be missing something).

Even more, if you want to advertise BGP prefixes with labels, you MUST list subnets you want to have advertised within the **labeled-unicast** address family.

Not surprisingly, the BGP table contains labeled and unlabeled routes:

{{<cc>}}BGP table with labeled and unlabeled prefixes on PE1 running Arista vEOS{{</cc>}}
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
 * >  L   10.0.0.5/32            10.1.0.1              0       -          100     0       65101 i
 * >      10.0.0.6/32            10.0.0.2              0       -          100     0       65102 i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
 * >  L   10.0.0.6/32            10.0.0.2              0       -          100     0       65102 i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
```

Even more interesting, every specific prefix has two **best** routes:

{{<cc>}}Best BGP routes for CE2 loopback interface on PE1 (both running Arista EOS){{</cc>}}
```
pe1#show ip bgp 10.0.0.6
BGP routing table information for VRF default
Router identifier 10.0.0.1, local AS number 65000
BGP routing table entry for 10.0.0.6/32
 Paths: 2 available
  65102
    10.0.0.2 from 10.0.0.4 (10.0.0.4)
      Origin IGP, metric 0, localpref 100, IGP metric 30, weight 0, tag 0
      Received 00:45:31 ago, valid, internal, best
      Originator: 10.0.0.2, Cluster list: 10.0.0.4
      Rx SAFI: Unicast
      Tunnel RIB eligible
  65102
    10.0.0.2 labels [ 100003 ] from 10.0.0.4 (10.0.0.4)
      Origin IGP, metric 0, localpref 100, IGP metric 30, weight 0, tag 0
      Received 00:45:31 ago, valid, internal, best
      Originator: 10.0.0.2, Cluster list: 10.0.0.4
      Local MPLS label: 100003
      Rx SAFI: MplsLabel
      Tunnel RIB eligible
```

The labeled BGP prefix is used to set up MPLS forwarding table, but not the IP routing table:

{{<cc>}}IP routing table entry for CE2 loopback on PE1 (both running Arista EOS){{</cc>}}
```
pe1#show ip route 10.0.0.6
...
 B I      10.0.0.6/32 [200/0] via 10.0.0.2/32, LDP tunnel index 2
                                 via 10.1.0.9, Ethernet2, label 116385
```

If we disable the IPv4 address family neighbors on PE1, the BGP table contains only the labeled routes:

{{<cc>}}Disabling IPv4 address family neighbors on PE1{{</cc>}}
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
      no neighbor 10.0.0.4 activate
      no neighbor 10.1.0.1 activate
      network 10.0.0.1/32
   !
   address-family ipv4 labeled-unicast
      neighbor 10.0.0.4 activate
      neighbor 10.1.0.1 activate
      network 10.0.0.1/32
```

{{<cc>}}BGP table on PE1 after disabling IPv4 address family for all neighbors{{</cc>}}
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
 * >  L   10.0.0.2/32            10.0.0.2              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
 * >  L   10.0.0.4/32            10.0.0.4              0       -          100     0       i
 * >  L   10.0.0.5/32            10.1.0.1              0       -          100     0       65101 i
 * >  L   10.0.0.6/32            10.0.0.2              0       -          100     0       65102 i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
```

While that looks great, the BGP prefixes are no longer in the IP routing table because they are not advertised within the IPv4 address family.

## Mixed Environment

For the final test, we'll change PE1 from Cisco IOSv to Arista EOS. All other lab devices will be running Cisco IOSv.

```
netlab up -s nodes.pe1.device=eos
```

As expected, the BGP table on Arista EOS contains only the labeled prefixes (Cisco IOS is not advertising anything over IPv4 AF when the IPv4-LU AF is negotiated):

{{<cc>}}BGP table on PE1 running Arista EOS in an IOSv-based lab{{</cc>}}
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
 * >  L   10.0.0.2/32            10.0.0.2              0       -          100     0       i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
 * >  L   10.0.0.4/32            10.0.0.4              0       -          100     0       i
 * >  L   10.0.0.5/32            10.1.0.1              0       -          100     0       65101 i
 * >  L   10.0.0.6/32            10.0.0.2              0       -          100     0       65102 i Or-ID: 10.0.0.2 C-LST: 10.0.0.4
```

What about the IP routing table? It's missing BGP prefixes:

{{<cc>}}IP routing table on PE1 running Arista EOS in an IOSv-based lab{{</cc>}}
```
pe1#show ip route
...
Gateway of last resort is not set

 C        10.0.0.1/32 is directly connected, Loopback0
 O        10.0.0.2/32 [110/12] via 10.1.0.9, Ethernet2
 O        10.0.0.3/32 [110/11] via 10.1.0.9, Ethernet2
 O        10.0.0.4/32 [110/12] via 10.1.0.9, Ethernet2
 C        10.1.0.0/30 is directly connected, Ethernet1
 C        10.1.0.8/30 is directly connected, Ethernet2
 O        10.1.0.12/30 [110/11] via 10.1.0.9, Ethernet2
 O        10.1.0.16/30 [110/11] via 10.1.0.9, Ethernet2
 C        192.168.121.0/24 is directly connected, Management1
```

So how do you make BGP Labeled Unicast work between Cisco IOS and Arista EOS? Your guess might be better than mine. Should that be the case, please leave a comment.