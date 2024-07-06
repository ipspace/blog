---
title: "FRRouting Claims IBGP Loopbacks Are Inaccessible"
date: 2024-03-27 08:10:00+0100
tags: [ BGP ]
pre_scroll: True
---
Last week, I explained the differences between FRRouting and more traditional networking operating systems in scenarios where [OSPF and IBGP advertise the same prefix](/2024/03/frr-rib-fib.html):

* Traditional networking operating systems enter only the OSPF route into the IP routing table.
* FRRouting enters OSPF and IBGP routes into the IP routing table.
* On all platforms I've tested, only the OSPF route gets into the forwarding table[^WK].

[^WK]: To be fair, we're in the "probably, but who knows" territory ;) While OSPF and BGP report different next hops for the same prefix, the directly adjacent next hop is the same.

One could conclude that it's perfectly safe to advertise the same prefixes in OSPF and IBGP. The OSPF routes will be used within the autonomous system, and the IBGP routes will be propagated over EBGP to adjacent networks. Well, one would be surprised 🤦‍♂️
<!--more-->
### In Case You Don't Follow the Links

You REALLY SHOULD HAVE read the previous blog post describing the network topology. Here's the topology diagram in case you didn't do that:

{{<ascii>}}
┌─────────────────────────────────────────┐
│                                         │
│                  ┌────────┐  ┌────────┐ │
│ ┌─────────────┐  │   R1   │  │   R2   │ │
│ │172.16.0.0/24├──┤10.0.0.1├──┤10.0.0.2│ │
│ └─────────────┘  └────────┘  └────────┘ │
│ AS 65000                                │
└─────────────────────────────────────────┘
{{</ascii>}}

### Back to BGP

First, there's the ancient question, "*Should a router advertise a BGP route if it's not using it?*" I never understood what the big deal was[^PWAC]; if someone decided a prefix is worth advertising in BGP, and the current router knows how to send traffic to that prefix, there's little harm in advertising the prefix. Anyway, Cisco IOS [gets nervous](/2007/12/what-is-bgp-rib-failure.html), and old Arista EOS releases refused to advertise the prefix to other BGP neighbors[^BC]; you had to calm them down with the **bgp advertise-inactive** incantation.

[^PWAC]: If you have more information, please write a comment.

[^BC]: While the Arista EOS documentation still describes the **bgp advertise-inactive** command, it looks like that behavior has changed (or at least I couldn't reproduce it).

FRRouting has no such qualms. The IBGP routes are the best BGP routes it knows; BGP ignores OSPF routes (both routes get in the routing table anyway), and life goes on. Well, not exactly. FRRouting running on R2 refuses to accept the IBGP route for the R1's loopback prefix. The prefix is in the BGP table (R1 is advertising it), but it's not the best BGP route for 10.0.0.1/32:

```
r2# show ip bgp
BGP table version is 2, local router ID is 10.0.0.2, vrf id 0
Default local pref 100, local AS 65000
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

    Network          Next Hop            Metric LocPrf Weight Path
   i10.0.0.1/32      10.0.0.1(r1)             0    100      0 i
 *> 10.0.0.2/32      0.0.0.0(r2)              0         32768 i
 *>i172.16.0.0/24    10.0.0.1(r1)             0    100      0 i
```

The explanation is bizarre: the next hop is supposedly inaccessible while it happily hums along in the IP routing table:

```
r2# show ip bgp 10.0.0.1
BGP routing table entry for 10.0.0.1/32, version 0
Paths: (1 available, no best path)
  Not advertised to any peer
  Local
    10.0.0.1(r1) (inaccessible, import-check enabled) from r1(10.0.0.1) (10.0.0.1)
      Origin IGP, metric 0, localpref 100, invalid, internal
      Last update: Thu Mar  7 16:36:09 2024

r2# show ip route
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

K>* 0.0.0.0/0 [0/0] via 192.168.121.1, eth0, 00:16:45
O>* 10.0.0.1/32 [110/20] via 10.1.0.1, eth1, weight 1, 00:16:31
O   10.0.0.2/32 [110/10] via 0.0.0.0, lo0 onlink, weight 1, 00:16:41
C>* 10.0.0.2/32 is directly connected, lo0, 00:16:43
O   10.1.0.0/30 [110/10] is directly connected, eth1, weight 1, 00:16:41
C>* 10.1.0.0/30 is directly connected, eth1, 00:16:43
B   172.16.0.0/24 [200/0] via 10.0.0.1 (recursive), weight 1, 00:16:30
                            via 10.1.0.1, eth1, weight 1, 00:16:30
O>* 172.16.0.0/24 [110/20] via 10.1.0.1, eth1, weight 1, 00:16:31
C>* 192.168.121.0/24 is directly connected, eth0, 00:16:45
```

It is true that a BGP update saying "the prefix 10.0.0.1/32 has the BGP next hop 10.0.0.1" looks funky when considered in isolation. Still, we have a perfectly valid OSPF route for 10.0.0.1 in the IP routing table and the IP forwarding table, and we know that BGP checks the IP routing table when evaluating the viability of BGP next hops.

The only explanation I could come up with is that we're experiencing a side effect of a too-aggressive recursive routing prevention logic. We have a severe problem if the *best* route for 10.0.0.1/32 has 10.0.0.1 as the next hop, and it makes perfect sense to refuse such an entry. However, in our case, the *best* route for 10.0.0.1/32 is an OSPF route, not an IBGP route.

I tried to figure out what scenario could make an IBGP route for an IBGP loopback the best route in the IP routing table. The only one I could come up with was the [EVPN IBGP-over-EBGP](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics#IBGP-Based_EVPN_on_Top_of_EBGP-Based_Fabric_Routing) design pushed by too many vendors. You get the horrendous mess you deserve if you use it and enable (or forget to disable) the IPv4 address family on an IBGP session running between IPv4 loopbacks advertised over the EBGP IPv4 address family[^TIO].

The correct "solution" to that problem should be to tell the cargo cult followers, "You're not experienced enough to use that design," but we know no vendor would ever do that. It seems someone took the easy way out and broke otherwise reasonable designs in the name of supporting stuff BGP was never supposed to deal with. Still, I remain an eternal optimist, hoping I missed something obvious. Please write a comment if I did.

[^TIO]: Trust me, I tried it once.
