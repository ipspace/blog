---
title: "Links in Virtual Labs"
date: 2025-02-03 08:27:00+0100
tags: [ virtualization, netlab ]
netlab_tag: use
---
There are three major ways to connect network devices in the physical world:

* Point-to-point links between devices (usually using some variant of Ethernet)
* Multi-access layer-1 networks running some IEEE 802.x encapsulation on top of that (GPON, WiFi, Ethernet hubs)
* Multi-access switched layer-2 network (dumb switches, hopefully running some STP variant)

Implementing these connections in virtual labs is a bit harder than one might think, as all virtualization solutions assume you plan to run virtual servers connected to Ethernet segments.
<!--more-->
### The Big Picture

Every virtualization solution I've seen so far (VMware ESX, Hyper-V, KVM, containers with Docker) connects virtual machines or containers to a virtual ~~bridge~~ switch:

{{<figure src="/2025/02/vlinks-vswitch.png" caption="Virtual switch in VMware ESXi">}}

The *virtual NIC* in the above diagram is not necessarily an interface. The virtualization software *emulates* the virtual NIC hardware or I/O registers[^PV] to give the virtual machine the impression that it has an Ethernet interface:

[^PV]: Ignoring for the moment the *paravirtual* solutions that use shared memory and system calls from virtual machines to the hypervisor.

{{<figure src="/2025/02/vlinks-vnic.png" caption="Hypervisor software emulates virtual interfaces">}}

### KVM/libvirt Networks Use Linux Bridges

While it's hard to figure out what's going on behind the scenes in VMware ESXi, it's trivial to explore the Linux virtual networking. Let's set up a very simple [netlab topology](https://netlab.tools/topology-overview/) with two hosts connected to a shared segment:

{{<cc>}}netlab topology used to create a libvirt segment{{</cc>}}
```
nodes:
  h1:
    device: linux
  h2:
    device: linux

links: [ h1-h2 ]
```

_netlab_ tells Vagrant that it has to connect H1 and H2 with a *libvirt* private network, and Vagrant calls *libvirt* to create the network (X_1):

{{<cc>}}libvirt virtual networks after the lab is started{{</cc>}}
```
$ virsh net-list
 Name              State    Autostart   Persistent
----------------------------------------------------
 default           active   yes         yes
 vagrant-libvirt   active   no          yes
 X_1               active   yes         yes
```

The X_1 network uses `virbr1` Linux bridge:

{{<cc>}}Find the Linux bridge used by a libvirt virtual network{{</cc>}}
```
$ virsh net-info X_1
Name:           X_1
UUID:           2994e8b1-b69b-4eaf-8801-d5fe1302ff65
Active:         yes
Persistent:     yes
Autostart:      yes
Bridge:         virbr1
```

There are two interfaces (one per VM) connected to the `virbr1` bridge:

{{<cc>}}Find the interfaces connected to a Linux bridge{{</cc>}}
```
$ brctl show virbr1
bridge name	bridge id		STP enabled	interfaces
virbr1		8000.525400f97191	no		vgif_h1_1
							vgif_h2_1
```

The two interfaces are *tap interfaces* -- special interfaces that allow the virtualization software to capture packets sent to them and insert them into the virtual machine. However, **there is no Linux interface implementing the virtual machine interface** (put a pin in that thought; you'll need it in the next blog post).

{{<cc>}}The details of a tap interface serving a virtual machine{{</cc>}}
```
$ ip -d link show vgif_h1_1
33867: vgif_h1_1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master virbr1 state UNKNOWN mode DEFAULT group default qlen 1000
    link/ether fe:54:00:f5:27:fa brd ff:ff:ff:ff:ff:ff promiscuity 1 minmtu 68 maxmtu 65521
    tun type tap pi off vnet_hdr on persist off
    bridge_slave state forwarding priority 32 cost 100 hairpin off guard off root_block off fastleave off learning on flood on port_id 0x8002 port_no 0x2 designated_port 32770 designated_cost 0 designated_bridge 8000.52:54:0:f9:71:91 designated_root 8000.52:54:0:f9:71:91 hold_timer    0.00 message_age_timer    0.00 forward_delay_timer    0.00 topology_change_ack 0 config_pending 0 proxy_arp off proxy_arp_wifi off mcast_router 1 mcast_fast_leave off mcast_flood on mcast_to_unicast off neigh_suppress off group_fwd_mask 0 group_fwd_mask_str 0x0 vlan_tunnel off isolated off addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
```

### Connecting Containers to Linux Bridges

Container orchestration solutions use a slightly different approach. Container interfaces are Linux interfaces *in a different network namespace*. That makes it impossible to connect them to a Linux bridge. To connect a container to a Linux bridge, you have to:

* Create *a pair* of virtual Ethernet interfaces connected with a virtual cable (vEth pair)
* Connect one of the vEth interfaces to the Linux bridge (make the Linux bridge the master of the vEth interface)
* Migrate the other vEth interface to the container namespace and rename it to **ethX**.

{{<figure src="/2025/02/veth-bridge.png" caption="Containers connected to a Linux bridge">}}

Let's start a slightly larger[^P2P] netlab topology to explore what's going on behind the scenes:

[^P2P]: _netlab_ would ask _containerlab_ to create a point-to-point link between containers if we were using the two host topology.

{{<cc>}}netlab topology used to create containers connected to a Linux bridge{{</cc>}}
```
provider: clab

nodes:
  h1:
    device: linux
  h2:
    device: linux
  h3:
    device: linux

links: [ h1-h2-h3 ]
```

After starting the lab, our Linux host has two additional bridges -- a lab management network and a data-plane bridge connecting three Linux containers:

{{<cc>}}Linux bridges after the container lab was started{{</cc>}}
```
$ brctl show
bridge name	bridge id		STP enabled	interfaces
X_1		8000.363f459a1c59	no		h1_eth1
							h2_eth1
							h3_eth1
br-c16a1e42cdb8		8000.02424d2659f3	no		veth3a66ccf
							veth56c6b05
							vethfa4725c
docker0		8000.02429c2dee48	no
virbr0		8000.525400d00378	yes
```

Each host interface is the "public" side of the vEth pair:

{{<cc>}}The details of an interface connected to the lab data-plane bridge{{</cc>}}
```
$ ip -d link show h1_eth1
33876: h1_eth1@if33877: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9500 qdisc noqueue master X_1 state UP mode DEFAULT group default
    link/ether aa:c1:ab:f9:63:f8 brd ff:ff:ff:ff:ff:ff link-netnsid 0 promiscuity 1 minmtu 68 maxmtu 65535
    veth
    bridge_slave state forwarding priority 32 cost 2 hairpin off guard off root_block off fastleave off learning on flood on port_id 0x8001 port_no 0x1 designated_port 32769 designated_cost 0 designated_bridge 8000.36:3f:45:9a:1c:59 designated_root 8000.36:3f:45:9a:1c:59 hold_timer    0.00 message_age_timer    0.00 forward_delay_timer    0.00 topology_change_ack 0 config_pending 0 proxy_arp off proxy_arp_wifi off mcast_router 1 mcast_fast_leave off mcast_flood on mcast_to_unicast off neigh_suppress off group_fwd_mask 0 group_fwd_mask_str 0x0 vlan_tunnel off isolated off addrgenmode eui64 numtxqueues 16 numrxqueues 16 gso_max_size 65536 gso_max_segs 65535
```

The other side of the vEth pair is visible in the container namespace:

{{<cc>}}The container side of the vEth pairs{{</cc>}}
```
$ netlab connect h1
Connecting to container clab-X-h1, starting bash

h1:/# ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
33872: eth0@if33873: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:c0:a8:79:65 brd ff:ff:ff:ff:ff:ff
33877: eth1@if33876: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether aa:c1:ab:ac:d2:b5 brd ff:ff:ff:ff:ff:ff
```

Note the weird interface names in the **ip link** printouts:

* Host interface `h1_eth1` is associated with `if33877`
* Container interface `eth1` is associated with `if33876`

As the two interfaces are in different namespaces, the **ip link** command cannot print the actual name of the other end of the vEth pair, but the two sequence numbers are highly suggestive.

### Are We Good to Go?

**TL&DR: No.**

Linux bridges have a tiny problem: Linux developers know too much about networking protocols[^VN]. Linux bridges [reluctantly pass some layer-2 control protocols](https://blog.ipspace.net/2020/12/linux-bridge-lldp/), won't pass LACP frames (you can't build a LAG between two network devices), and run STP unless configured otherwise.

[^VN]: You won't experience any such problems with vSphere virtual switches. [Dropping BPDUs](https://blog.ipspace.net/2012/09/dear-vmware-bpdu-filter-bpdu-guard/) is the pinnacle of ESXi achievements.

You could replace Linux bridges with Open vSwitches (you're allowed to forward anything in the brave new Software Defined world) or find a hack that will result in a point-to-point link between two virtual machines or containers -- the topic of the next blog post.

{{<next-in-series page="/posts/2025/02/no-such-post">}}**Coming up next:** point-to-point links in virtual labs{{</next-in-series>}}
