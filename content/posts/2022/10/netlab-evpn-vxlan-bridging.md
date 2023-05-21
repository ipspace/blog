---
date: 2022-10-03 07:21:00+00:00
netlab_tag: vxlan_evpn
pre_scroll: true
series_title: Simple EVPN/VXLAN Bridging
tags:
- VXLAN
- EVPN
- netlab
title: netlab EVPN/VXLAN Bridging Example
---
[netlab release 1.3](/2022/09/netlab-1-3.html) introduced support for [VXLAN transport with static ingress replication](https://netlab.tools/module/vxlan/) and [EVPN control plane](https://netlab.tools/module/evpn/). Last week we [replaced a VLAN trunk with VXLAN transport](/2022/09/netlab-vxlan-bridging.html), now we'll [replace static ingress replication with EVPN control plane](https://github.com/ipspace/netlab-examples/tree/master/EVPN/vxlan-bridging).

{{<figure src="/2022/10/evpn-vxlan-bridging-topology.png" caption="Lab topology">}}
<!--more-->
We'll start with the [VXLAN bridging topology](https://github.com/ipspace/netlab-examples/blob/master/VXLAN/vxlan-bridging/topology.yml) and add [EVPN configuration module](https://netlab.tools/module/evpn/) to the switches. We'll also have to add [BGP configuration module](https://netlab.tools/module/bgp/) (EVPN needs BGP) and define BGP AS with **bgp.as** global parameter... and that's it -- now we have a working EVPN/VXLAN lab.

{{<cc>}}Adding EVPN and BGP configuration modules{{</cc>}}
```
groups:
  switches:
    members: [ s1,s2 ]
    module: [ vlan,vxlan,ospf,bgp,evpn ]

bgp.as: 65000
```

Behind the scenes *netlab*:

* As in the previous example, [configures OSPF and VXLAN](/2022/09/netlab-vxlan-bridging.html). VXLAN VNIs no longer use the ingress replication lists.
* Starts BGP process on S1 and S2, and builds an IBGP session between the loopback interfaces.
* Assigns EVPN RT/RD to every VLAN with a VXLAN VNI.
* Activates EVPN address family on the IBGP session between S1 and S2.

Now for an interesting plot twist. Everything *netlab* does works on multiple network operating systems[^HD]. All you have to do to build a multi-vendor lab using Arista EOS and Cumulus Linux is to add device types to the switches.

[^HD]: *netlab* supports [15 different platforms](https://netlab.tools/platforms/), and [most configuration modules support at least a half-dozen platforms](https://netlab.tools/platforms/#supported-configuration-modules).

{{<cc>}}Building a multi-vendor EVPN/VXLAN lab{{</cc>}}
```
nodes:
  s1:
    device: eos
  s2:
    device: cumulus
```

Start the lab with **netlab up** and it all works. Here's the BGP table as observed on S1 (Arista EOS):

{{<cc>}}EVPN BGP table on Arista EOS{{</cc>}}
```
s1#sh bgp evpn
BGP routing table information for VRF default
Router identifier 10.0.0.5, local AS number 65000
Route status codes: s - suppressed, * - valid, > - active, E - ECMP head, e - ECMP
                    S - Stale, c - Contributing to ECMP, b - backup
                    % - Pending BGP convergence
Origin codes: i - IGP, e - EGP, ? - incomplete
AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

          Network                Next Hop              Metric  LocPref Weight  Path
 * >     RD: 10.0.0.6:1000 mac-ip aac1.ab17.1b03 fe80::a8c1:abff:fe17:1b03
                                 10.0.0.6              -       100     0       i
 * >     RD: 10.0.0.6:1001 mac-ip aac1.ab17.1b03 fe80::a8c1:abff:fe17:1b03
                                 10.0.0.6              -       100     0       i
 * >     RD: 10.0.0.6:1000 mac-ip aac1.abcf.8cf5
                                 10.0.0.6              -       100     0       i
 * >     RD: 10.0.0.6:1000 mac-ip aac1.abcf.8cf5 172.16.0.2
                                 10.0.0.6              -       100     0       i
 * >     RD: 10.0.0.6:1000 imet 10.0.0.6
                                 10.0.0.6              -       100     0       i
 * >     RD: 10.0.0.6:1001 imet 10.0.0.6
                                 10.0.0.6              -       100     0       i
 * >     RD: 10.0.0.5:1000 imet 10.0.0.5
                                 -                     -       -       0       i
 * >     RD: 10.0.0.5:1001 imet 10.0.0.5
                                 -                     -       -       0       i
```

You can also use *netlab* to learn how to configure *netlab*-supported features on platforms you're not familiar with[^NOPT]. Here are the relevant snippets of Arista EOS configuration generated during the **netlab initial** process:

[^NOPT]: You'll get *working* configurations that might not be *optimal* or adhering to *vendor best practices*. If you feel we did a bad job configuring a platform you're an expert in, please submit a pull request.

{{<cc>}}Arista cEOS EVPN/VXLAN bridging configuration{{</cc>}}
```
hostname s1
!
spanning-tree mode mstp
!
vlan 1000
   name red
!
vlan 1001
   name blue
!
interface Ethernet1
   switchport access vlan 1000
!
interface Ethernet2
   switchport access vlan 1001
!
interface Ethernet3
   description s1 -> s2
   no switchport
   ip address 10.1.0.1/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Loopback0
   ip address 10.0.0.5/32
   ip ospf area 0.0.0.0
!
interface Vlan1000
   description VLAN red (1000) -> [h1,h2,s2]
!
interface Vlan1001
   description VLAN blue (1001) -> [h3,h4,s2]
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vlan 1000 vni 101000
   vxlan vlan 1001 vni 101001
!
router bgp 65000
   router-id 10.0.0.5
   no bgp default ipv4-unicast
   bgp advertise-inactive
   neighbor 10.0.0.6 remote-as 65000
   neighbor 10.0.0.6 next-hop-self
   neighbor 10.0.0.6 update-source Loopback0
   neighbor 10.0.0.6 description s2
   neighbor 10.0.0.6 send-community standard extended
   !
   vlan 1000
      rd 10.0.0.5:1000
      route-target import 65000:1000
      route-target export 65000:1000
      redistribute learned
   !
   vlan 1001
      rd 10.0.0.5:1001
      route-target import 65000:1001
      route-target export 65000:1001
      redistribute learned
   !
   address-family evpn
      neighbor 10.0.0.6 activate
   !
   address-family ipv4
      neighbor 10.0.0.6 activate
      network 10.0.0.5/32
!
router ospf 1
   router-id 10.0.0.5
   max-lsa 12000
!
end
```

Collecting Cumulus Linux configuration is a bit more of an effort. Here's a summary of how the bridging interfaces are configured (collected from a variety of `/etc/network/interfaces.d` files):

{{<cc>}}Cumulus Linux interface configuration{{</cc>}}
```
iface bridge
	bridge-vlan-aware yes
	bridge-vids 1001
	bridge-vids 1000
	bridge-ports swp1
	bridge-ports swp2
	bridge-ports vni-101000
	bridge-ports vni-101001

iface swp1
	bridge-access 1000
	
iface swp2
	bridge-access 1001
	
iface vni-101000
	bridge-access 1000
	vxlan-id 101000
	vxlan-learning no
	
iface vni-101001
	bridge-access 1001
	vxlan-id 101001
	vxlan-learning no
```

... and here is the FRR control plane configuration:

{{<cc>}}Cumulus Linux FRR configuration{{</cc>}}
```
router bgp 65000
 bgp router-id 10.0.0.6
 no bgp default ipv4-unicast
 neighbor 10.0.0.5 remote-as 65000
 neighbor 10.0.0.5 description s1
 neighbor 10.0.0.5 update-source lo
 !
 address-family ipv4 unicast
  network 10.0.0.6/32
  neighbor 10.0.0.5 activate
  neighbor 10.0.0.5 next-hop-self
 exit-address-family
 !
 address-family l2vpn evpn
  neighbor 10.0.0.5 activate
  advertise-all-vni
  vni 101001
   rd 10.0.0.6:1001
   route-target import 65000:1001
   route-target export 65000:1001
  exit-vni
  vni 101000
   rd 10.0.0.6:1000
   route-target import 65000:1000
   route-target export 65000:1000
  exit-vni
  advertise-svi-ip
  advertise ipv4 unicast
 exit-address-family
!
router ospf
 ospf router-id 10.0.0.6
```

Want to run this lab on your own, or [try it out with different devices](https://github.com/ipspace/netlab-examples/tree/master/EVPN/vxlan-bridging#changing-device-types)? No problem:

* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/EVPN/vxlan-bridging/topology.yml) into an empty directory
* Change device types (and the provider if needed) in the topology file and execute **netlab up**. You can also change the topology parameters with **netlab up** [CLI arguments](https://netlab.tools/netlab/up/#usage).
* Enjoy! 😊

