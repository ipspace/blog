---
anycast_tag: lab
date: 2022-11-21 06:18:00+00:00
netlab_tag: vlan_vrf
series:
- anycast
series_title: IRB with Anycast Gateways
tags:
- netlab
title: 'netlab: IRB with Anycast Gateways'
---
[netlab release 1.4](/2022/11/netlab-release-1-4-0.html) added support for static anycast gateways and VRRP. Today we'll use that functionality to add anycast gateways to the [VLAN trunk lab](/2022/06/netsim-vlan-trunk.html):

{{<figure src="/2022/06/vlan-trunk.png" caption="Lab topology">}}

We'll start with the [VLAN trunk lab topology](https://github.com/ipspace/netlab-examples/blob/master/VLAN/vlan-trunk/topology.yml) and make the following changes:
<!--more-->
* We'll rearrange the node list to make sure the switches get the lowest possible node ID:

{{<code>}}nodes: [ <b>s1, s2</b>, h1, h2, h3, h4 ]
{{</code>}}

* The switches have to use the new **gateway** module:

{{<code>}}groups:
&nbsp;&nbsp;switches:
&nbsp;&nbsp;&nbsp;&nbsp;members: [ s1, s2 ]
&nbsp;&nbsp;&nbsp;&nbsp;module: [ vlan, <b>gateway</b> ]
&nbsp;&nbsp;&nbsp;&nbsp;device: eos
{{</code>}}

* We have to enable first-hop gateway on VLAN links:

{{<code>}}vlans:
&nbsp;&nbsp;red:
&nbsp;&nbsp;&nbsp;&nbsp;<b>gateway: True</b>
&nbsp;&nbsp;blue:
&nbsp;&nbsp;&nbsp;&nbsp;<b>gateway: True</b>
{{</code>}}

* The default FHRP protocol is **anycast** (we could also use VRRP), and the default shared IP address is the last IP address in the subnet. We'll use the first IP address in the subnet:

```
gateway.id: 1
```

After starting the lab you'll notice the change in node identifiers and interface IP addresses. Without the anycast gateway, _netlab_ assigns node ID 1 (and loopback IP address 10.0.0.1) to S1. Now that the node ID 1 is reserved, S1 gets loopback address 10.0.0.2.

The only other change on the switches is the VLAN interface configuration -- _netlab_ configures **ip address** as well as **ip virtual-router address** on EOS devices:

{{<cc>}}VLAN interface configuration on S1{{</cc>}}
```
interface Vlan1000
   description VLAN red (1000) -> [h1,s2,h2]
   ip address 172.16.0.2/24
   ip virtual-router address 172.16.0.1/24
!
interface Vlan1001
   description VLAN blue (1001) -> [h3,s2,h4]
   ip address 172.16.1.2/24
   ip virtual-router address 172.16.1.1/24
!
ip virtual-router mac-address 02:00:ca:fe:00:ff
```

Finally, the static routes on Linux hosts use the anycast gateway IP address (the default route points to the management network):

{{<cc>}}Static routes on H1{{</cc>}}
```
h1:/# ip route
default via 192.168.121.1 dev eth0
10.0.0.0/24 via 172.16.0.1 dev eth1
10.1.0.0/16 via 172.16.0.1 dev eth1
10.2.0.0/24 via 172.16.0.1 dev eth1
172.16.0.0/24 dev eth1 scope link  src 172.16.0.4
172.16.0.0/16 via 172.16.0.1 dev eth1
192.168.121.0/24 dev eth0 scope link  src 192.168.121.104
```

Want to run this lab on your own, or [try it out with different devices](https://github.com/ipspace/netlab-examples/tree/master/routing/anycast-gateway#changing-device-types)? No problem:

* [Install netlab](https://netlab.tools/install/)
* [Download the relevant containers](https://netlab.tools/labs/clab/) or [create Vagrant boxes](https://netlab.tools/labs/libvirt/)
* Download the [topology file](https://github.com/ipspace/netlab-examples/blob/master/routing/anycast-gateway/topology.yml) into an empty directory
* Execute **netlab up**
* Enjoy! 😊