---
date: 2008-06-26 11:42:00+02:00
eigrp_tag: deploy
lastmod: 2020-12-28 10:32:00
tags:
- EIGRP
- BGP
- MPLS VPN
title: Using EIGRP in MPLS VPN Networks
url: /2008/06/simple-eigrp-in-mpls-vpn-networks/
---
We described EIGRP-in-VRF in [MPLS and VPN Architectures, Volume II](http://www.amazon.com/gp/product/1587051125?ie=UTF8&tag=cisioshinandt-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=1587051125). A few details have changed in the meantime; you have to configure the following features to get EIGRP running within MPLS/VPN environment:

-   The **autonomous-system** command within the VRF address family is mandatory, even if the VRF AS number matches the EIGRP process number.
-   The default BGP-to-EIGRP redistribution metric has to be configured, otherwise remote EIGRP routes will not be redistributed even though they have EIGRP metric encoded in extended BGP communities.
-   Things work best if you disable auto-summary on PE-routers.
<!--more-->
{{<ct3_rescue>}}

Support for EIGRP as a PE-CE routing protocol in MPLS VPN environment has been introduced in Cisco IOS releases 12.2(15)T, 12.3, 12.0(22)S and 12.2(18)S. The basic configuration for simple VPNs having sites with a single PE-CE link is very simple:

-   EIGRP routing process is configured for the desired VRF.
-   Two-way redistribution between PE-CE EIGRP and core BGP is configured within the VRF address family.

EIGRP routes redistributed from VRF address family into VPNv4 BGP carry EIGRP-specific extended communities that transport EIGRP route attributes (metric vector, route type and AS number) across core BGP. Routes sourced by EIGRP in one site are thus redistributed as internal EIGRP routes with proper vector and composite metric into EIGRP running on other sites.

### Configuration

The VRF and EIGRP configuration on the PE-R1 router in the sample network shown in the following figure is included below.

{{<figure src="/2008/06/SingleHomed_EIGRP_VPN.png" caption="Lab topology">}}

{{<cc>}}PE-R1 configuration{{</cc>}}
```
ip vrf Cust
 rd 65000:1
 route-target export 65001:1
 route-target import 65001:1
!
interface Serial1/4
 description Link to S2
 ip vrf forwarding Cust
 ip address 10.0.7.9 255.255.255.252
!
router eigrp 11
 !
 address-family ipv4 vrf Cust
  autonomous-system 234
  network 0.0.0.0
  no auto-summary
  redistribute bgp 65000 metric 2000 1000 255 1 1500
 exit-address-family
!
router bgp 65000
 !
 address-family ipv4 vrf Cust
  no synchronization
  redistribute eigrp 234
 exit-address-family
```

When configuring EIGRP on the PE-router, follow these rules:

-   A single global EIGRP process can be used for multiple VRFs regardless of the EIGRP AS number used in the global and VRF EIGRP processes.
-   The AS number used by the VRF EIGRP process *must* be configured with the **autonomous-system** router configuration command, otherwise the per-VRF EIGRP configuration will not be saved into NVRAM.
-   The EIGRP process number used within the **ipv4 vrf** address family is the number configured with the **autonomous-system** command, not the global process number configured with the **router eigrp** command. In the sample configuration, you have to use **redistribute eigrp 234** when redistributing from EIGRP to BGP within the *Cust* VRF.
-   EIGRP **auto-summary** should be disabled.
-   Default redistribution metric has to be specified on BGP-to-EIGRP redistribution, either with the **default-metric** or **redistribute bgp metric** router configuration command. The default metric is ignored for VPN EIGRP routes redistributed from BGP into EIGRP, but the route redistribution does not work without the default metric.

### Monitoring

Full complement of EIGRP **show** commands is available for EIGRP process running in VRF; you just need to add **vrf** ***name*** to the **show** commands. You can view the VRF EIGRP neighbors:

{{<cc>}}EIGRP neighbors in a VRF{{</cc>}}
```
PE-R1#show ip eigrp vrf Cust neighbors
EIGRP-IPv4 neighbors for process 234
H   Address         Interface       Hold Uptime   SRTT   RTO  Q  Seq
                                    (sec)         (ms)       Cnt Num
0   10.0.7.10       Se1/4             14 00:31:52   21   200  0  105
```

The EIGRP topology table contains local routes as well as VPNv4 routes redistributed from BGP (indicated by the *via VPNv4 Sourced* keyword):

{{<cc>}}EIGRP topology table on a PE-router{{</cc>}}
```
PE-R1#show ip eigrp vrf Cust topology
EIGRP-IPv4 Topology Table for AS(234)/ID(10.0.7.9) Routing Table: Cust

Codes: P - Passive, A - Active, U - Update, Q - Query, R - Reply,
       r - reply Status, s - sia Status

P 10.0.7.8/30, 1 successors, FD is 2169856
        via Connected, Serial1/4
P 10.0.1.7/32, 1 successors, FD is 2297856
        via 10.0.7.10 (2297856/128256), Serial1/4
P 10.2.5.0/24, 1 successors, FD is 28160
        via VPNv4 Sourced (28160/0)
P 10.0.1.5/32, 1 successors, FD is 2297856
        via VPNv4 Sourced (2297856/0)
P 10.2.6.0/24, 1 successors, FD is 2195456
        via 10.0.7.10 (2195456/281600), Serial1/4
P 10.0.7.28/30, 1 successors, FD is 2169856
        via VPNv4 Sourced (2169856/0)
```

The local EIGRP routes appear as native EIGRP routes in the VRF IP routing table; remote EIGRP routes appear as BGP routes on the PE-router:

{{<cc>}}Remote EIGRP routes appear as BGP routes in VRF routing table{{</cc>}}
```
PE-R1#show ip route vrf Cust | begin Gateway
Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 14 subnets, 3 masks
B        10.0.1.5/32 [200/2297856] via 10.0.7.26, 00:29:40
D        10.0.1.7/32 [90/2297856] via 10.0.7.10, 00:33:19, Serial1/4
C        10.0.7.8/30 is directly connected, Serial1/4
B        10.0.7.28/30 [200/0] via 10.0.7.26, 00:29:25
B        10.2.5.0/24 [200/0] via 10.0.1.1, 00:30:55
D        10.2.6.0/24 [90/2195456] via 10.0.7.10, 00:33:19, Serial1/4
```

However, the same routes appear as internal EIGRP routes on the CE-router:

{{<cc>}}Remote EIGRP routes appear as EIGRP routes on a CE-router{{</cc>}}
```
S2#show ip route | begin Gateway
Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 13 subnets, 3 masks
C       10.0.7.8/30 is directly connected, Serial1/0
C       10.0.1.7/32 is directly connected, Loopback0
D       10.2.5.0/24 [90/2172416] via 10.0.7.9, 00:31:46, Serial1/0
D       10.0.1.5/32 [90/2809856] via 10.0.7.9, 00:30:19, Serial1/0
C       10.2.6.0/24 is directly connected, FastEthernet0/0
D       10.0.7.28/30 [90/2681856] via 10.0.7.9, 00:30:17, Serial1/0
```

