---
date: 2022-09-26 07:21:00+00:00
netlab_tag: vxlan_evpn
series_title: Simple VXLAN Bridging
tags:
- VXLAN
- netlab
title: netlab VXLAN Bridging Example
---
[netlab release 1.3](/2022/09/netlab-1-3/) introduced support for [VXLAN transport with static ingress replication](https://netlab.tools/module/vxlan/). Time to check how easy it is to replace a VLAN trunk with VXLAN transport. We'll use the lab topology from the [VLAN trunking example](/2022/06/netsim-vlan-trunk/), replace the VLAN trunk between S1 and S2 with an IP underlay network, and [transport Ethernet frames across that network with VXLAN](https://github.com/ipspace/netlab-examples/tree/master/VXLAN/vxlan-bridging).

{{<figure src="/2022/09/vxlan-bridging.png" caption="Lab topology">}}
<!--more-->
We still have to define the VLANs; we'll set VLAN **mode** to **bridge** as we don't want to do any routing between VLANs.

{{<cc>}}Defining VLANs{{</cc>}}
```
vlans:
  red:
    mode: bridge
  blue:
    mode: bridge
```

Next: nodes and links. The only difference from the VLAN trunking topology is the last link: a point-to-point IP link between S1 and S2.

{{<cc>}}Defining nodes and links{{</cc>}}
```
nodes: [ h1, h2, h3, h4, s1, s2 ]

links:
- h1:
  s1:
    vlan.access: red
- h2:
  s2:
    vlan.access: red
- h3:
  s1:
    vlan.access: blue
- h4:
  s2:
    vlan.access: blue
- s1:
  s2:
```

Finally a touch of magic. We'll deploy VLAN, VXLAN and OSPF configuration modules on the switches -- and that's it ([full topology](https://github.com/ipspace/netlab-examples/blob/master/VXLAN/vxlan-bridging/topology.yml)).

{{<cc>}}Defining device groups{{</cc>}}
```
groups:
  hosts:
    members: [ h1, h2, h3, h4 ]
    device: linux
  switches:
    members: [ s1,s2 ]
    module: [ vlan,vxlan,ospf ]
```

Behind the scenes:

* OSPF configuration module starts OSPF routing process on both switches, enabling IP connectivity between their loopback interfaces (which are then used as VXLAN VTEPs).
* VLAN configuration module creates VLAN data structures and figures out that S1 and S2 need *red* and *blue* VLANs based on the VLAN access interfaces.
* By default, the [VXLAN configuration module](https://netlab.tools/module/vxlan/) transports all local VLANs across the underlay network. You can change that behavior with **vxlan.vlans** list, and extend only some of the VLANs across the underlay network.
* VXLAN configuration module automatically builds per-VLAN ingress replication lists for every node using **vxlan** module based on which other nodes use the same VLAN. You can even define multiple VXLAN bridging domains.

Here's a sample Arista EOS configuration generated during the **netlab initial** process:

{{<cc>}}Arista cEOS VXLAN bridging configuration{{</cc>}}
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
   vxlan vlan 1000 flood vtep 10.0.0.6
   vxlan vlan 1001 flood vtep 10.0.0.6
!
ip routing
!
router ospf 1
   router-id 10.0.0.5
   max-lsa 12000
!
end
```

Want to run this lab on your own, or [try it out with different devices](https://github.com/ipspace/netlab-examples/tree/master/VXLAN/vxlan-bridging#changing-device-types)? No problem:

* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/VXLAN/vxlan-bridging/topology.yml) into an empty directory
* Execute **netlab up -d eos -p clab** if you want to run the lab with Arista cEOS in *containerlab*, or use whichever other device type in the `-d` parameter (you can skip the `-p` parameter if you're using *libvirt*).
* Enjoy! 😊
