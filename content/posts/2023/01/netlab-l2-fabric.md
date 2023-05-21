---
date: 2023-01-23 07:44:00+00:00
netlab_tag: vlan_vrf
pre_scroll: true
series_title: Building a Layer-2 Fabric
tags:
- netlab
title: 'netlab: Building a Layer-2 Fabric'
---
A friend of mine decided to use _netlab_ to build a simple traditional data center fabric, and asked me a question along these lines:

> How do I make all the ports be L2 by default i.e. not have IP address assigned to them?

Trying to answer his question way too late in the evening (I know, I shouldn't be doing that), I focused on the "_no IP addresses_" part. To get there, you [have to use the **l2only** pool](https://netlab.tools/example/addressing-tutorial/#layer-2-only-links-using-l2only-address-pool) or disable IPv4 prefixes in the [built-in address pools](https://netlab.tools/example/addressing-tutorial/#using-built-in-address-pools), for example:
<!--more-->
```
addressing:
  lan:
    ipv4: False
  p2p:
    ipv4: False

nodes:
  l1:
  l2:
  s1:
  s2:
  h1:
      device: linux
  h2:
      device: linux

links:
- l1-s1
- l2-s1
- l1-s2
- l2-s2
- l1-h1
- l2-h2
```

{{<note info>}}You have to use the `ipv4: False` instead of simpler `p2p: {}` syntax that is used to define the **l2only** pool because _netlab_ merges lab topology settings with the default system settings, and the default settings already include **ipv4** prefixes in most addressing pools.{{</note>}}

It turned out my friend wanted to build a layer-2-only leaf-and-spine fabric, and the above topology wouldn't do that. _netlab_ assumes you want to use [layer-3 interfaces](https://blog.ipspace.net/2022/09/interfaces-ports.html) unless you use VLANs on them and would configure something equivalent to **no switchport** on data center switches as part of initial configuration. To build a pure layer-2 fabric, you have to build it within a VLAN:

* Use VLAN module in the lab topology[^AC]:

[^AC]: I love to use Arista cEOS containers with *clab* -- the lab start time is too short to make a coffee let alone a sandwich.

```
defaults.device: eos
provider: clab
module: [ vlan ]
```

* Create a VLAN and optionally set its VLAN ID. Make sure the VLAN **mode** is set to **bridge** or you'll get IP addresses on all [VLAN interfaces](https://blog.ipspace.net/2022/09/vlan-interfaces.html).

```
vlans:
  fabric:
    id: 100
    mode: bridge
```

* Configure access VLAN **fabric** on all links:

```
links:
- l1:
  s1:
  vlan.access: fabric
- l2:
  s1:
  vlan.access: fabric
- l1:
  s2:
  vlan.access: fabric
- l2:
  s2:
  vlan.access: fabric
- l1:
  h1:
  vlan.access: fabric
- l2:
  h2:
  vlan.access: fabric
```

{{<note>}}
Notes:

* The **links** part of the lab topology is way too verbose for my tastes and will get significantly shorter once we implement [link groups](https://github.com/ipspace/netlab/issues/707).
* While the switches won't get IP addresses on VLAN interfaces, hosts do (because they are not VLAN aware). You can ping between **h1** and **h2** once the lab is up and running.
* You could use VLAN 1 as native VLAN on VLAN trunks between the switches, but that would make the lab topology even more verbose.
{{</note>}}

Now we're ready to roll. Execute **netlab up**[^HW], wait for STP to do its job, and check connectivity between **h1** and **h2**.

[^HW]: After doing the mandatory homework like [creating a Ubuntu VM](https://netlab.tools/install/ubuntu-vm/), [installing the software](https://netlab.tools/labs/clab/), and [downloading Arista cEOS container](https://netlab.tools/labs/ceos/).

For the two readers who haven't installed *netlab* yet: here's the Arista cEOS configuration for **l1**:

{{<cc>}}Cleaned-up Arista cEOS configuration for L1{{</cc>}}
```
spanning-tree mode mstp
!
vlan 100
   name fabric
!
interface Ethernet1
   switchport access vlan 100
!
interface Ethernet2
   switchport access vlan 100
!
interface Ethernet3
   switchport access vlan 100
!
interface Loopback0
   ip address 10.0.0.1/32
!
interface Management0
   ip address 192.168.121.101/24
   no lldp transmit
   no lldp receive
!
interface Vlan100
   description VLAN fabric (100) -> [s1,s2,h1,l2,h2]
```

Want to run this lab on your own, or [try it out with different devices](https://github.com/ipspace/netlab-examples/tree/master/VLAN/l2-fabric)? No problem:

* Make sure [_netlab_ implementation of your preferred device supports VLANs](https://netlab.tools/module/vlan/#platform-support).
* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/VLAN/l2-fabric/topology.yml) into an empty directory
* Execute **netlab up**
* Enjoy! 😊