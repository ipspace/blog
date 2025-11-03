---
title: "One-Arm Hub-and-Spoke VPN on Arista EOS"
date: 2025-11-11 07:28:00+0100
tags: [ netlab, design ]
netlab_tag: mpls
series: hub_spoke_vpn
---
In September 2024, I described how you can build [One-Arm Hub-and-Spoke VPN with MPLS/VPN](/2024/09/hub-spoke-one-arm/). In that blog post, I mentioned that the solution doesn't work on Arista EOS because it allocates MPLS labels to whole VRFs ([per-VRF label allocation](/2024/10/mpls-vpn-prefix-vrf-labels/)).

Arista fixed this particular annoyance in the EOS release 4.34.2F. It still uses per-VRF label allocation, but now, you can assign a different label *to the default route*. Let's see how that works with our [one-arm hub-and-spoke topology](https://github.com/ipspace/netlab-examples/blob/master/MPLS/hub-spoke-one-arm/topology.yml):
<!--more-->
After starting the lab with Arista EOS devices, the spoke-to-spoke traceroute (from CE_1 to CE_2) still gets turned around at the hub PE-router and never reaches the hub CE-router:

```
ce_s1(bash)# traceroute ce_s2
traceroute to ce_s2 (10.0.0.7), 30 hops max, 46 byte packets
 1  Ethernet2.s_1.pe_a (10.1.0.13)  10.306 ms  0.554 ms  0.526 ms
 2  Ethernet1.p (10.1.0.1)  33.994 ms  3.209 ms  2.256 ms
 3  Ethernet1.pe_h (10.1.0.10)  7.429 ms  2.571 ms  2.573 ms
 4  Ethernet1.pe_b (10.1.0.6)  17.294 ms  5.228 ms  4.204 ms
 5  ce-s2 (10.0.0.7)  3.723 ms  3.775 ms  2.984 ms
```

No surprise there; the IP routing table on PE_A confirms that the hub PE-router (PE_H) allocates the same label to all VRF routes:

```
pe-a#show ip route vrf s_1 bgp | begin Gateway
Gateway of last resort:
 B I      0.0.0.0/0 [200/0]
           via 10.0.0.3/32, LDP tunnel index 2, label 100000
              via 10.1.0.1, Ethernet1, label 100000

 B I      10.0.0.5/32 [200/0]
           via 10.0.0.3/32, LDP tunnel index 2, label 100000
              via 10.1.0.1, Ethernet1, label 100000
 B E      10.0.0.6/32 [200/0]
           via 10.1.0.14, Ethernet2
 B I      10.1.0.20/30 [200/0]
           via 10.0.0.3/32, LDP tunnel index 2, label 100000
              via 10.1.0.1, Ethernet1, label 100000
```

Next, let's apply a bit of the magic:

```
pe-h#conf t
pe-h(config)#router bgp 65000
pe-h(config-router-bgp)#vrf hub
pe-h(config-router-bgp-vrf-hub)#route-target export vpn-ipv4 label allocation nexthop default-route
```

The label for the default route in the IP routing table on PE_A immediately changes to a different value:

```
pe-a#show ip route vrf s_1 bgp | begin Gateway
Gateway of last resort:
 B I      0.0.0.0/0 [200/0]
           via 10.0.0.3/32, LDP tunnel index 2, label 100001
              via 10.1.0.1, Ethernet1, label 100000

 B I      10.0.0.5/32 [200/0]
           via 10.0.0.3/32, LDP tunnel index 2, label 100000
              via 10.1.0.1, Ethernet1, label 100000
 B E      10.0.0.6/32 [200/0]
           via 10.1.0.14, Ethernet2
 B I      10.1.0.20/30 [200/0]
           via 10.0.0.3/32, LDP tunnel index 2, label 100000
              via 10.1.0.1, Ethernet1, label 100000
```

On PE_H, the label 100001 points to PE_H -> CE_HUB interface with the next hop being the IP address of CE_HUB:

```
pe-h#show mpls lfib route 100001
...
 B3    100001   [0]
                via M, 10.1.0.22, pop
                 payload autoDecide, ttlMode uniform, dscpMode uniform, apply egress-acl
                 interface Ethernet2
```

After that change, the traffic between CE_S1 and CE_S2 passes through CE_HUB as expected:

```
ce_s1(bash)# traceroute ce_s2
traceroute to ce_s2 (10.0.0.7), 30 hops max, 46 byte packets
 1  Ethernet2.s_1.pe_a (10.1.0.13)  0.796 ms  0.377 ms  0.275 ms
 2  Ethernet1.p (10.1.0.1)  2.875 ms  1.928 ms  1.978 ms
 3  Ethernet1.pe_h (10.1.0.10)  1.816 ms  1.746 ms  1.826 ms
 4  eth1.ce_hub (10.1.0.22)  2.194 ms  2.120 ms  2.073 ms
 5  Ethernet2.hub.pe_h (10.1.0.21)  2.098 ms  1.961 ms  1.976 ms
 6  Ethernet3.p (10.1.0.9)  4.610 ms  4.634 ms  5.929 ms
 7  Ethernet1.pe_b (10.1.0.6)  5.633 ms  5.230 ms  5.123 ms
 8  ce-s2 (10.0.0.7)  4.662 ms  5.076 ms  6.305 ms
```

Mission accomplished ;)

Read the [original blog post](/2024/09/hub-spoke-one-arm/) for more details. I also updated the lab topology to create a custom configuration template for Arista EOS and FRR; after starting the lab, execute **netlab config deflabel -l pe_h** to configure per-prefix label allocation on FRR and default route label allocation on EOS.
