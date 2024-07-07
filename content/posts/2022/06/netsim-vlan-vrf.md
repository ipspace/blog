---
date: 2022-06-13 06:38:00+00:00
netlab_tag: vlan_vrf
series_title: Combining VLANs with VRFs
tags:
- netlab
title: 'netlab: Combining VLANs with VRFs'
---
Last two weeks we focused on [access VLANs](/2022/05/netsim-vlan-simple/) and [VLAN trunk](/2022/06/netsim-vlan-trunk/) *[netlab](https://netlab.tools/)* implementation. Can we combine them with [VRFs](/2022/04/netsim-vrf-lite/)? Of course.

The trick is very simple: attributes within a VLAN definition become attributes of VLAN interfaces. Add `vrf` attribute to a VLAN and you get all VLAN interfaces created for that VLAN in the corresponding VRF. Can't get any easier, can it?

How about extending our VLAN trunk lab topology with VRFs? We'll put *red* VLAN in *red* VRF and *blue* VLAN in *blue* VRF.
<!--more-->
{{<figure src="/2022/06/vlan-vrf.png" caption="Combining VLANs with VRFs">}}

We'll take the existing [VLAN trunk lab topology](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-trunk/topology.yml) and modify it a bit. First, we have to enable VRF support on the switches -- we'll add `vrf` module to the list of modules used by S1 and S2.

{{<cc>}}Add VRF module to the switches group{{</cc>}}
```
groups:
  switches:
    members: [ s1, s2 ]
    module: [ vlan,vrf ]
    device: eos
```

Next, we have to define the VRFs.

{{<cc>}}VRF definitions in lab topology{{</cc>}}
```
vrfs:
  red:
  blue:
```

{{<note info>}}*netlab* automatically allocates route distinguishers and route targets to VRFs. Obviously you could override those values if you like particular RD/RT values or if you're building complex topologies.{{</note>}}

Finally, a bit of magic dust: add `vrf` attribute to VLAN definitions:

{{<cc>}}VLAN definitions in lab topology{{</cc>}}
```
vlans:
  red:
    vrf: red
  blue:
    vrf: blue
```

That's it. Execute **netlab up**[^HW] (after downloading the [final topology file](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-trunk-vrf/topology.yml)) and you'll have a multi-VRF lab using a VLAN trunk.

[^HW]: Assuming you completed your homework and [created a Ubuntu VM](https://netlab.tools/install/ubuntu-vm/), [installed the software](https://netlab.tools/labs/clab/), and [downloaded Arista cEOS container](https://netlab.tools/labs/ceos/).

Here are the relevant parts of Arista cEOS configuration in case you're wondering what we achieved with the few extra lines in lab topology file:

{{<cc>}}VRF+VLAN configuration on Arista cEOS{{</cc>}}
```
spanning-tree mode mstp
!
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
   mac-address 52:dc:ca:fe:05:01
   switchport access vlan 1000
!
interface Ethernet2
   mac-address 52:dc:ca:fe:05:02
   switchport access vlan 1001
!
interface Ethernet3
   description s1 -> s2
   mac-address 52:dc:ca:fe:05:03
   switchport trunk allowed vlan 1000-1001
   switchport mode trunk
!
interface Vlan1000
   description VLAN red (1000) -> [h1,s2,h2]
   vrf red
   ip address 172.16.0.5/24
!
interface Vlan1001
   description VLAN blue (1001) -> [h3,s2,h4]
   vrf blue
   ip address 172.16.1.5/24
!
ip routing
ip routing vrf blue
ip routing vrf red
```

Want to run this lab on your own, or [try it out with different devices](https://github.com/ipspace/netlab-examples/tree/master/VLAN/vlan-trunk-vrf#changing-device-types)? No problem:

* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-trunk-vrf/topology.yml) into an empty directory
* Execute **netlab up**
* Enjoy! 😊