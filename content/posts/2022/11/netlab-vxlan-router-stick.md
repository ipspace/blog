---
date: 2022-11-14 07:18:00+00:00
netlab_tag: vxlan_evpn
series_title: VXLAN Router-on-a-Stick Example
tags:
- netlab
- VXLAN
title: netlab VXLAN Router-on-a-Stick Example
---
In October 2022 I described how you could [build a VLAN router-on-a-stick topology with _netlab_](/2022/10/netlab-router-stick.html). With the new [features added in netlab release 1.4](/2022/11/netlab-release-1-4-0.html)[^VLI] we can do the same for VXLAN-enabled VLANs -- we'll build a lab where a router-on-a-stick will do VXLAN-to-VXLAN routing.

{{<figure src="/2022/11/netlab-vxlan-router-stick.png" caption="Lab topology">}}
<!--more-->

* S1 is a VXLAN-enabled layer-2 switch (no IP addresses on *red* or *blue* VLANs).
* VXLAN is enabled on S2, but it has no VLANs -- it's a pure IP transport device[^RTR].
* ROS has two VXLAN-enabled VLANs. It has IP addresses on VLAN interfaces, so it can route between the two VLANs, resulting in connectivity between H1 and H2.

[^VLI]: The router-on-a-stick has no physical VLAN-enabled ports, but we still need VLAN interfaces for VXLAN-enabled VLANs to route between them.

[^RTR]: A device formerly known as Router

Our lab topology will be very similar to the [VLAN router-on-a-stick topology](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-router-on-a-stick/topology.yml).

We have to define the two VLANs and a VRF[^RL]:

```
vrfs:
  tenant:

vlans:
  red:
    vrf: tenant
  blue:
    vrf: tenant
```

[^RL]: Routing on VXLAN interfaces that are in global routing table could have [interesting side effects](/2022/10/use-vrf-for-vxlan-vlans.html).

We'll use netlab groups to define most of the node parameters. Layer-2 switches need VLAN, VXLAN, and OSPF modules. They should not do any IP forwarding on the VLANs -- **vlan.mode** has to be set to **bridge**.

```
groups:
  switches:
    members: [ s1, s2 ]
    module: [ vlan,vxlan,ospf ]
    vlan.mode: bridge
```

The router needs all the modules used by the layer-2 switches, and the VRF module. It also needs IP address on VLAN interfaces, so we'll set **vlan.mode** to **irb**:

```
groups:
  routers:
    members: [ ros ]
    module: [ vlan,vxlan,ospf,vrf ]
    vlan.mode: irb
```

{{<note warn>}}We want the router to route between VXLAN-enabled VLAN interfaces, so we MUST set the **vlan.mode** to **irb**. Setting **vlan.mode** to **route** would not create the VLAN interfaces.{{</note>}}

Finally, we need a few hosts, the list of nodes, and the list of links:

```
groups:
  hosts:
    members: [ h1, h2 ]
    device: linux

nodes: [ h1, h2, s1, s2, ros ]

links:
- h1:
  s1:
    vlan.access: red
- h2:
  s1:
    vlan.access: blue
- s1-s2
- s2-ros
```

Unfortunately, the above lab topology wouldn't work:

* ROS (like S2) has no need for *red* or *blue* VLANs, so they are not added to the node data
* Because there's no *red* or *blue* VLAN in ROS node data, the VLAN interfaces are not created on ROS.
* No VLAN interfaces ==> no routing.

Somehow we have to make sure the *red* and the *blue* VLAN are defined on ROS. We could add them to node data or to the *routers* group. I decided to use the latter approach; you can find the [final topology file](https://github.com/ipspace/netlab-examples/blob/master/VXLAN/vxlan-router-stick/topology.yml) in the [_netlab-examples_ GitHub repository](https://github.com/ipspace/netlab-examples/tree/master/VXLAN/vxlan-router-stick).

```
groups:
  routers:
    members: [ ros ]
    module: [ vlan,vxlan,ospf,vrf ]
    vlans:
      red:
      blue:
```

Now we're ready to roll. Execute **netlab up**[^HW] and start exploring. Want to use some other device instead of Arista cEOS? Add **-d _device_** to **netlab up** command, for example `netlab up -d cumulus`.

[^HW]: After doing the mandatory homework like [creating a Ubuntu VM](https://netlab.tools/install/ubuntu-vm/), [installing the software](https://netlab.tools/labs/clab/), and [downloading Arista cEOS container](https://netlab.tools/labs/ceos/).

Haven't installed *netlab* yet? Well, you should; in the meantime, here's the Arista cEOS configuration for the VXLAN router-on-a-stick:

{{<cc>}}Arista cEOS VXLAN router-on-a-stick configuration{{</cc>}}
```
vlan 1000
   name red
!
vlan 1001
   name blue
!
vrf instance tenant
   rd 65000:1
!
management api http-commands
   no shutdown
!
management api gnmi
   transport grpc default
!
management api netconf
   transport ssh default
!
interface Ethernet1
   description ros -> s2
   mac-address 52:dc:ca:fe:05:01
   no switchport
   ip address 10.1.0.5/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Loopback0
   ip address 10.0.0.5/32
   ip ospf area 0.0.0.0
!
interface Management0
   ip address 192.168.121.105/24
   no lldp transmit
   no lldp receive
!
interface Vlan1000
   description VLAN red (1000) -> [h1,s1]
   vrf tenant
   ip address 172.16.0.5/24
   ip ospf area 0.0.0.0
!
interface Vlan1001
   description VLAN blue (1001) -> [h2,s1]
   vrf tenant
   ip address 172.16.1.5/24
   ip ospf area 0.0.0.0
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vlan 1000 vni 101000
   vxlan vlan 1001 vni 101001
   vxlan vlan 1000 flood vtep 10.0.0.3
   vxlan vlan 1001 flood vtep 10.0.0.3
!
ip routing
ip routing vrf tenant
!
router ospf 1
   router-id 10.0.0.5
   max-lsa 12000
!
router ospf 100 vrf tenant
   router-id 10.0.0.5
   interface unnumbered hello mask tx 0.0.0.0
   max-lsa 12000
```

Want to run this lab on your own, or [try it out with different devices](https://github.com/ipspace/netlab-examples/tree/master/VXLAN/vxlan-router-stick)? No problem:

* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/VXLAN/vxlan-router-stick/topology.yml) into an empty directory
* Execute **netlab up**
* Enjoy! 😊