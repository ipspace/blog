---
date: 2022-09-12 06:01:00+00:00
netlab_tag: vlan_vrf
series_title: VRF Lite Topology with VLAN Trunks
tags:
- netlab
title: 'netlab: VRF Lite Topology with VLAN Trunks'
---
In the [last blog post in the *VLANs and VRFs in netlab*](/2022/06/netsim-vlan-vrf/) series, I described how we can combine VLANs and VRFs and create a VRF Lite solution with stretched VLANs. Wonder how hard would it be to create a routed multi-hop [VRF Lite](/2022/04/netsim-vrf-lite/) topology? It's trivial.

{{<figure src="/2022/09/netlab-vrf-lite-routed.png" caption="Routed VRF Lite lab topology">}}
<!--more-->
Let's start with the nodes. We won't need any extra attributes on individual nodes, so we can define them as a simple list:

```
nodes: [r1, r2, r3, h1, h2, h3, h4 ]
```

Next, we'll define two groups: Linux *hosts* and *routers*. We won't define the device type in the *routers* group so you can use [whatever devices you want](https://netlab.tools/platforms/) as long as they [support VLANs, VRFs and OSPF](https://netlab.tools/platforms/#supported-configuration-modules) -- the [configuration modules](https://netlab.tools/module-reference/) we need to get the virtual interfaces and routing protocols up and running.

```
groups:
  routers:
    members: [ r1,r2,r3 ]
    module: [ vlan,vrf,ospf ]
  hosts:
    device: linux
    members: [ h1,h2,h3,h4 ]
```

Next, we need two VRFs and two VLANs (one per VRF). The magic trick that makes VRF Lite work is **mode: route** in VLAN definition that changes VLANs from a stretched bridging thingy to an interface encapsulation thingy -- a different IP subnet is assigned to the VLAN instance on every physical link.

```
vrfs:
  red:
  blue:

vlans:
  red:
    mode: route
    vrf: red
  blue:
    mode: route
    vrf: blue
```

Speaking of links: here's the list of links. The links between routers are VLAN trunks; the links between hosts and routers are simple Ethernet interfaces in VRFs:

```
links:
- r1:
  r2:
  vlan.trunk: [ red, blue ]
- r2:
  r3:
  vlan.trunk: [ red, blue ]  
- h1:
  r1:
    vrf: red
- h3:
  r1:
    vrf: blue
- h2:
  r3:
    vrf: red
- h4:
  r3:
    vrf: blue
```

That's it. Execute **netlab up -d _your-device_**[^HW] (after downloading the [final topology file](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-trunk-vrf/topology.yml)) and you'll have a multi-VRF lab using VLAN trunks.

[^HW]: Assuming you completed your homework, [installed the software](https://netlab.tools/install/), and created a Vagrant box for your network devices.

Here are the relevant parts of Arista EOS configuration in case you're wondering what we achieved with this simple lab topology file:

{{<cc>}}Routed VRF Lite configuration on R1{{</cc>}}
```
vlan 1000
   name red
!
vlan 1001
   name blue
!
vrf instance blue
   rd 65000:2
!
vrf instance red
   rd 65000:1
!
interface Ethernet1
   description r1 -> r2
   no switchport
!
interface Ethernet1.1
   description r1 -> [r2]
   encapsulation dot1q vlan 1001
   vrf blue
   ip address 172.16.6.1/24
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet1.2
   description r1 -> [r2]
   encapsulation dot1q vlan 1000
   vrf red
   ip address 172.16.7.1/24
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet2
   description r1 -> [h1] [stub]
   vrf red
   ip address 172.16.2.1/24
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet3
   description r1 -> [h3] [stub]
   vrf blue
   ip address 172.16.3.1/24
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Loopback0
   ip address 10.0.0.1/32
!
ip routing
ip routing vrf blue
ip routing vrf red
!
router ospf 100 vrf red
   router-id 10.0.0.1
   passive-interface Ethernet2
!
router ospf 101 vrf blue
   router-id 10.0.0.1
   passive-interface Ethernet3
```

Here's the R2 configuration showing how multi-hop VRF lite works with VLAN subinterfaces:

{{<cc>}}Routed VRF Lite configuration on R2{{</cc>}}
```
vlan 1000
   name red
!
vlan 1001
   name blue
!
vrf instance blue
   rd 65000:2
!
vrf instance red
   rd 65000:1
!
interface Ethernet1
   description r2 -> r1
   no switchport
!
interface Ethernet1.1
   description r2 -> [r1]
   encapsulation dot1q vlan 1001
   vrf blue
   ip address 172.16.6.2/24
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet1.2
   description r2 -> [r1]
   encapsulation dot1q vlan 1000
   vrf red
   ip address 172.16.7.2/24
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet2
   description r2 -> r3
   no switchport
!
interface Ethernet2.1
   description r2 -> [r3]
   encapsulation dot1q vlan 1001
   vrf blue
   ip address 172.16.8.2/24
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet2.2
   description r2 -> [r3]
   encapsulation dot1q vlan 1000
   vrf red
   ip address 172.16.9.2/24
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Loopback0
   ip address 10.0.0.2/32
!
ip routing
ip routing vrf blue
ip routing vrf red
!
router ospf 100 vrf red
   router-id 10.0.0.2
!
router ospf 101 vrf blue
   router-id 10.0.0.2
```

Want to run this lab on your own, or [try it out with different devices](https://github.com/ipspace/netlab-examples/tree/master/VRF/multihop-vrf-lite#changing-device-types)? No problem:

* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/VRF/multihop-vrf-lite/topology.yml) into an empty directory
* Execute **netlab up -d _your-device_**
* Enjoy! 😊