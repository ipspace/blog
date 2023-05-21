---
date: 2022-10-17 06:12:00+00:00
netlab_tag: vlan_vrf
series_title: Router-on-a-Stick Example
tags:
- netlab
title: netlab Router-on-a-Stick Example
---
In early June 2022 I described [a netlab topology using VLAN trunks](/2022/06/netsim-vlan-trunk.html) in *netlab*. That topology provided pure bridging service for two IP subnets. Now let's go a step further and add a router-on-a-stick: 

* S1 and S2 are layer-2 switches (no IP addresses on *red* or *blue* VLANs).
* ROS is a router-on-a-stick routing between *red* and *blue* VLANs.
* Hosts on *red* and *blue* VLANs should be able to ping each other.

{{<figure src="/2022/10/netlab-router-stick.png" caption="Lab topology">}}
<!--more-->
We'll start with the [VLAN trunks lab topology file](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-trunk/topology.yml). We'll keep the VLANs, but make them pure layer-2 VLANs with **mode: bridge** setting:

{{<cc>}}Defining VLANs{{</cc>}}
```
vlans:
  red:
    mode: bridge
  blue:
    mode: bridge
```

Next, we'll define the groups of devices:

{{<cc>}}Defining nodes and groups{{</cc>}}
```
provider: clab

groups:
  hosts:
    members: [ h1, h3 ]
    device: linux
  switches:
    members: [ s1, s2 ]
    module: [ vlan ]
    device: eos
  routers:
    members: [ ros ]
    module: [ vlan ]
    device: eos 
```

Finally, we need nodes and links. The only change from the previous topology is **vlan.mode** setting on the router -- we have to set it to **route** to tell *netlab* we want to have a router connecting two VLANs and not a switch.

{{<cc>}}Defining nodes and links{{</cc>}}
```
nodes:
  h1:
  h3:
  s1:
  s2:
  ros:
    vlan.mode: route

links:
- h1:
  s1:
    vlan.access: red
- h3:
  s1:
    vlan.access: blue
- s1:
  s2:
  vlan.trunk: [ red, blue ]
- s2:
  ros:
  vlan.trunk: [ red, blue ]
```

And that's all you have to do. Execute **netlab up**[^HW] and start exploring. Want to use some other device instead of Arista cEOS? Add **-d _device_** to **netlab up** command, for example `netlab up -d cumulus`.

[^HW]: After doing the mandatory homework like [creating a Ubuntu VM](https://netlab.tools/install/ubuntu-vm/), [installing the software](https://netlab.tools/labs/clab/), and [downloading Arista cEOS container](https://netlab.tools/labs/ceos/).

Here are the relevant parts of Arista cEOS configuration (for the few readers who still don't have a working *netlab* environment):

{{<cc>}}Arista cEOS router-on-a-stick configuration{{</cc>}}
```
vlan 1000
   name red
!
vlan 1001
   name blue
!
interface Ethernet1
   description ros -> s2
   mac-address 52:dc:ca:fe:05:01
   no switchport
!
interface Ethernet1.1
   description ros -> [h3,s1,s2]
   encapsulation dot1q vlan 1001
   ip address 172.16.1.5/24
!
interface Ethernet1.2
   description ros -> [h1,s1,s2]
   encapsulation dot1q vlan 1000
   ip address 172.16.0.5/24
```

Want to run this lab on your own, or [try it out with different devices](https://github.com/ipspace/netlab-examples/tree/master/VLAN/vlan-router-on-a-stick#changing-device-types)? No problem:

* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-router-on-a-stick/topology.yml) into an empty directory
* Execute **netlab up**
* Enjoy! 😊