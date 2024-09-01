---
title: "Routing Table and BGP RIB on SR Linux"
date: 2024-09-04 07:24:00+0200
tags: [ BGP ]
---
Ages ago, I described how "traditional" network operating systems [used the BGP Routing Information Base (BGP RIB), the system routing table (RIB), and the forwarding table (FIB)](/2010/09/ribs-and-fibs/). Here's the TL&DR:

1. Routes received from BGP neighbors are stored in BGP RIB.
2. Routes redistributed into BGP from other protocols are (re)created in the BGP RIB.
3. BGP selects the best routes in BGP RIB using its convoluted set of rules.
4. Best routes from the BGP RIB are advertised to BGP neighbors
5. Best routes from the BGP RIB compete (based on their administrative distance) against routes from other routing protocols to enter the IP routing table (system RIB)
6. Routes from the system RIB are copied into FIB after their next hops are fully evaluated (a process that might involve multiple recursive lookups).
<!--more-->
FRRouting [modified that process](/2024/03/frr-rib-fib/) a bit. It uses the system RIB as a *repository of all routes*. The final steps in the above process are thus:

5. Best routes from the BGP RIB are copied into the system RIB
6. The routing table manager (zebra) selects the best routes from the system RIB based on their administrative distance
7. Best RIB routes are copied into FIB (after the next-hop resolution)

Expecting something along those lines, I was totally flabbergasted when I tried to fix a few SR Linux _netlab_ configuration templates. I wasn't able to figure out whether SR Linux uses the BGP RIB as the system RIB, but all system routes automatically appear in the BGP RIB.

Let me illustrate what I'm talking about with a simple network using an SR Linux router and two adjacent routers: R1 (running OSPF) and X2 (running BGP).

{{<ascii>}}
┌────────┐    ┌─────────┐    ┌────────┐
│   R1   │    │   SRL   │    │   X2   │
│10.0.0.1├────┤10.0.0.42├────┤10.0.0.2│
└────────┘    └─────────┘    └────────┘
    ◄─────────────► ◄────────────►     
          OSPF           EBGP
{{</ascii>}}

Here's the _netlab_ topology file I used to create the lab:

{{<printout>}}
defaults.device: frr
provider: clab
addressing.p2p.ipv4: True

nodes:
  srl:
    module: [ ospf, bgp ]
    bgp.as: 65000
    device: srlinux
    id: 42
    bgp.advertise_loopback: false
  r1:
    module: [ ospf ]
  x2:
    module: [ bgp ]
    bgp.as: 65001

links: [ srl-r1, srl-x2 ]
{{</printout>}}

Notes:

* I'm using unnumbered IPv4 links to keep the routing table as clean as possible (line 3)
* SRL is not advertising its loopback IP address into BGP. X2 should receive no BGP routes from SRL (line 11)

The IP routing table on SR Linux contains the expected prefixes:

{{<ascii>}}
A:srl# show route-table ipv4-unicast summary | as text
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
IPv4 unicast route table of network instance default
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
+--------------------+------+-----------+---------------------+---------+---------+--------+-----------+------------+------------+------------+---------------+
|       Prefix       |  ID  |   Route   |     Route Owner     | Active  | Origin  | Metric |   Pref    |  Next-hop  |  Next-hop  |   Backup   | Backup Next-  |
|                    |      |   Type    |                     |         | Network |        |           |   (Type)   | Interface  |  Next-hop  | hop Interface |
|                    |      |           |                     |         | Instanc |        |           |            |            |   (Type)   |               |
|                    |      |           |                     |         |    e    |        |           |            |            |            |               |
+====================+======+===========+=====================+=========+=========+========+===========+============+============+============+===============+
| 10.0.0.1/32        | 0    | ospfv2    | ospf_mgr            | True    | default | 16     | 10        | 169.254.0. | ethernet-  |            |               |
|                    |      |           |                     |         |         |        |           | 1 (direct) | 1/1.0      |            |               |
| 10.0.0.2/32        | 0    | bgp       | bgp_mgr             | True    | default | 0      | 170       | fe80::a8c1 | ethernet-  |            |               |
|                    |      |           |                     |         |         |        |           | :abff:fe4e | 1/2.0      |            |               |
|                    |      |           |                     |         |         |        |           | :f30b      |            |            |               |
|                    |      |           |                     |         |         |        |           | (direct)   |            |            |               |
| 10.0.0.42/32       | 4    | host      | net_inst_mgr        | True    | default | 0      | 0         | None       | None       |            |               |
|                    |      |           |                     |         |         |        |           | (extract)  |            |            |               |
+--------------------+------+-----------+---------------------+---------+---------+--------+-----------+------------+------------+------------+---------------+
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
IPv4 routes total                    : 3
IPv4 prefixes with active routes     : 3
IPv4 prefixes with active ECMP routes: 0
{{</ascii>}}

However, all those prefixes also appear in the BGP table:

```
A:srl# show protocols bgp routes ipv4 summary
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP route table of network-instance "default"
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Status codes: u=used, *=valid, >=best, x=stale
Origin codes: i=IGP, e=EGP, ?=incomplete
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
+------+------------------+--------------------------+------+------+---------------------------------------------------+
| Stat |     Network      |         Next Hop         | MED  | LocP |                     Path Val                      |
|  us  |                  |                          |      | ref  |                                                   |
+======+==================+==========================+======+======+===================================================+
| u*>  | 10.0.0.1/32      | 169.254.0.1              | 16   |      |  i                                                |
| u*>  | 10.0.0.2/32      | fe80::a8c1:abff:fecf:209 | -    |      | [65001] i                                         |
|      |                  | a%ethernet-1/2.0         |      |      |                                                   |
| u*>  | 10.0.0.42/32     | 0.0.0.0                  | -    |      |  i                                                |
+------+------------------+--------------------------+------+------+---------------------------------------------------+
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
3 received BGP routes: 3 used, 3 valid, 0 stale
3 available destinations: 0 with ECMP multipaths
```

Here's the SR Linux BGP configuration. I used _netlab_ to generate it and then removed all **export-policy** statements[^NC]. As you can see, it contains no **network** statement or route redistribution.

[^NC]: In this scenario, the _netlab_-configured export policies are effectively a no-op, but I wanted to have as simple a configuration as possible.

```
A:srl# info protocols bgp
    protocols {
        bgp {
            admin-state enable
            autonomous-system 65000
            router-id 10.0.0.42
            dynamic-neighbors {
                interface ethernet-1/2.0 {
                    peer-group intf-ethernet-1/2
                    allowed-peer-as [
                        65001..65001
                    ]
                }
            }
            ebgp-default-policy {
                import-reject-all false
                export-reject-all false
            }
            afi-safi ipv4-unicast {
                admin-state enable
            }
            group intf-ethernet-1/2 {
                admin-state enable
                afi-safi ipv4-unicast {
                    admin-state enable
                    ipv4-unicast {
                        advertise-ipv6-next-hops true
                        receive-ipv6-next-hops true
                    }
                }
                afi-safi ipv6-unicast {
                    admin-state disable
                }
                send-community {
                    standard true
                    large true
                }
                timers {
                    connect-retry 10 !!! Reduce default 120s to 10s
                    minimum-advertisement-interval 1
                }
            }
        }
    }
```

Now, let's take a look at the unexpected OSPF route in the BGP RIB:

```
A:srl# show protocols bgp routes ipv4 prefix 10.0.0.1/32
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Show report for the BGP routes to network "10.0.0.1/32" network-instance  "default"
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Network: 10.0.0.1/32
Received Paths: 1
  Path 1: <Best,Valid,Used,>
    Route source    : neighbor 0.0.0.0
    Route Preference: MED is 16, No LocalPref
    BGP next-hop    : 169.254.0.1
    Path            :  i
    Communities     : None
Path 1 was advertised to:
[  ]
```

Here are the important bits:

* The route source is the local router (the route was redistributed into BGP)
* The MED is set to OSPF cost.
* **The route was not advertised to anyone else** (that's why X2 receives no BGP routes from SRL)

How does that last bit of magic work? SR Linux uses a default BGP **export-policy**[^ONRM] that matches only routes learned via BGP. Routes imported into the BGP RIB from other sources are  thus not advertised to BGP neighbors.

[^ONRM]: Outbound neighbor route map for people more familiar with the *industry-standard CLI* terminology.

That approach makes BGP prefix origination and route redistribution somewhat different from anything else I've seen so far. Instead of the **network** statement, you must match the prefixes in the outbound **export-policy**. Instead of route redistribution, you must match the **protocol** in the outbound **export-policy**. As you could have different export policies for individual neighbors, you have unlimited potential for job security ;)

To complete the example, this is the routing policy you could use to originate a local prefix into BGP (the equivalent of the **network** statement).

```
A:srl# info routing-policy
    routing-policy {
        prefix-set default_bgp_advertise {
            prefix 10.0.0.42/32 mask-length-range exact {
            }
        }
        policy default_bgp_export {
            default-action {
                policy-result reject
            }
            statement prefixes {
                match {
                    prefix-set default_bgp_advertise
                }
                action {
                    policy-result accept
                }
            }
            statement bgp {
                match {
                    protocol bgp
                }
                action {
                    policy-result accept
                }
            }
        }
```

Likewise, here's the routing policy you could use to redistribute connected subnets and OSPF routes into BGP. As in the previous example, you must match the BGP routes, or the neighbors won't get them.

```
A:srl# info routing-policy
        policy default_bgp_export {
            default-action {
                policy-result reject
            }
            statement bgp {
                match {
                    protocol bgp
                }
                action {
                    policy-result accept
                }
            }
            statement export_local {
                match {
                    protocol local
                }
                action {
                    policy-result accept
                }
            }
            statement export_ospfv2 {
                match {
                    protocol ospfv2
                }
                action {
                    policy-result accept
                }
            }
            statement export_ospfv3 {
                match {
                    protocol ospfv3
                }
                action {
                    policy-result accept
                }
            }
        }
```

Is there something wrong with the SR Linux approach? Of course not; it gets the job done. You might argue, however, that it could be violating the [Principle of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment). Imagine you want to set MED on the BGP routes SRL advertises to X2. Here's a simple routing policy to do it:

```
A:srl# info routing-policy policy set-med
    routing-policy {
        policy set-med {
            statement med-is-42 {
                action {
                   policy-result accept
                   bgp {
                        med {
                            set 42
                        }
                    }
                }
            }
        }
    }
```

Now, try to guess what happens if you apply this routing policy to a BGP neighbor.

Done? Here are the results:

```
$ netlab connect x2 --show ip bgp
Connecting to container clab-X-x2, executing vtysh -c "show ip bgp"
BGP table version is 3, local router ID is 10.0.0.2, vrf id 0
Default local pref 100, local AS 65001
Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
               i internal, r RIB-failure, S Stale, R Removed
Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
Origin codes:  i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

    Network          Next Hop            Metric LocPrf Weight Path
 *> 10.0.0.1/32      eth1                    42             0 65000 i
 *> 10.0.0.2/32      0.0.0.0(x2)              0         32768 i
 *> 10.0.0.42/32     eth1                    42             0 65000 i
```

The export policy we configured accepted *all routes in the BGP RIB*, set their MED to 42, and advertised them to the EBGP neighbor. The BGP RIB contains routes from all routing sources, so the neighbor got a bit more than we probably wanted to send.

The quick fix (in this case) would be to add **match protocol bgp** to the routing policy, but what if you want to combine prefix origination, route redistribution, and per-neighbor policies? Until SR Linux release 24.7.1, you had to deal with the [Cartesian product hell](/2013/10/flow-table-explosion-with-openflow-10/). SR Linux release 24.7.1 introduced a chain of BGP export policies; I'll probably write a follow-up blog post once we ship _netlab_ release 1.9.1 ;)

