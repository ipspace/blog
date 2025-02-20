---
title: "Stub Networks in Virtual Labs"
date: 2025-02-25 07:55:00+0100
tags: [ virtualization, netlab ]
netlab_tag: use
---
The previous blog posts described how virtualization products create [LAN segments](/2025/02/virtual-lab-links/) and [point-to-point links](/2025/02/virtual-labs-p2p-links/). 

However, sometimes we need *stub segments* -- segments connected to a single router or switch -- because we don't want to waste resources creating hosts attached to a network device, but would still prefer a more realistic mechanism than static routes to inject IP subnets into routing protocols.
<!--more-->
### QEMU Tunnels to Nowhere

Creating stub segments for KVM virtual machines is trivial:

* Define a VM virtual interface based on UDP tunnels ([more details](/2025/02/virtual-labs-p2p-links/#qemu)).
* Use a bogus remote IP address in the tunnel definition.

The VM-generated traffic will be duly encapsulated, sent to the remote IP address, and dropped once someone realizes the remote IP address is not reachable.

{{<figure src="/2025/02/qemu-stub.png" caption="QEMU sending VM packets to nowhere">}}

### Container Stub Interfaces

One would expect the container stub interfaces to be trivial. After all, Linux has many networking constructs, and one of them must be a good fit for our requirements.

Interestingly, *containerlab* did not provide anything along these lines when we created the *[containerlab provider](https://netlab.tools/labs/clab/)* for *[netlab](https://netlab.tools/)*.  We "solved" the problem with fake Linux bridges: a container stub interface would be implemented as a vEth pair connected to a dummy Linux bridge.

{{<figure src="/2025/02/clab-stub-bridge.png" caption="Using a Linux bridge to create a virtual stub link">}}

Recent *containerlab* releases introduced *[dummy interfaces](https://containerlab.dev/manual/topo-def-file/#dummy)* -- a perfect match for what we needed (or so it seemed).

{{<figure src="/2025/02/containerlab-dummy.png" caption="Containerlab creates a dummy interface within a container">}}

Containerlab uses the Linux *dummy* interface to create an extra Ethernet-like interface within the container. For example, when using the following *netlab* topology, the host H1 has a "real" Ethernet interface (half of a [vEth pair](/2025/02/virtual-labs-p2p-links/#clab)) and a dummy interface with an Ethernet-like name:

{{<cc>}}*netlab* topology creating a P2P link and a stub interface{{</cc>}}
```
provider: clab
defaults.device: linux

nodes: [ h1, h2 ]
links: [ h1-h2, h1 ]
```

{{<cc>}}Ethernet-like interfaces on H1{{</cc>}}
```
h1:/# ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
3451: eth0@if3452: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:c0:a8:79:65 brd ff:ff:ff:ff:ff:ff
3453: eth1@if3454: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether aa:c1:ab:9e:0a:ff brd ff:ff:ff:ff:ff:ff
3455: eth2: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN
    link/ether aa:c1:ab:78:04:62 brd ff:ff:ff:ff:ff:ff
```

Unfortunately, some network device container implementations are too picky. The UNKNOWN state of the **eth2** interface is the first potential problem, but there are others. A detailed look at the dummy interface reveals that Linux claims its minimum and maximum MTU are zero.

{{<cc>}}The details of the dummy interface{{</cc>}}
```
# ip -d link show eth2
3463: eth2: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/ether aa:c1:ab:73:44:06 brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 0 maxmtu 0
    dummy numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
```

VyOS hates that. It checks the minimum and maximum MTU of the Ethernet interfaces and fails miserably. We had to rename the stub interfaces to **dumX** interfaces to make it happy (it checks the MTU on the **eth** interfaces, but not on **dum** interfaces).

Arista cEOS exhibits even more bizarre behavior. It will not run OSPF on the dummy interface unless you configure it to use a point-to-point network type.

If we use the same *netlab* topology to start a network with two Arista cEOS containers running OSPF, we get the following results on H1[^OR]:

[^OR]: Assuming you're using netlab release 1.9.4. Release 1.9.4-post1 changes the OSPF network type of stub interfaces (and tells you it did so).

{{<cc>}}OSPF is not running on a dummy interface Ethernet2{{</cc>}}
```
h1#show ip ospf int brief
   Interface          Instance VRF        Area            IP Address         Cost  State      Nbrs
   Lo0                1        default    0.0.0.0         10.0.0.1/32        10    DR         0
   Et1                1        default    0.0.0.0         10.1.0.1/30        10    P2P        1
h1#show run int ethernet 2
interface Ethernet2
   description h1 -> stub [stub]
   mac-address 52:dc:ca:fe:01:02
   no switchport
   ip address 172.16.0.1/24
   ip ospf area 0.0.0.0
```

If you change the OSPF network type on Ethernet2 to point-to-point, the interface will magically become part of the OSPF process.

{{<cc>}}Changing the OSPF network type makes OSPF work as expected{{</cc>}}
```
h1#conf t
h1(config)#interface Ethernet2
h1(config-if-Et2)#ip ospf network point-to-point
h1(config-if-Et2)#
h1#show ip ospf int brief
   Interface          Instance VRF        Area            IP Address         Cost  State      Nbrs
   Lo0                1        default    0.0.0.0         10.0.0.1/32        10    DR         0
   Et1                1        default    0.0.0.0         10.1.0.1/30        10    P2P        1
   Et2                1        default    0.0.0.0         172.16.0.1/24      10    P2P        0
```