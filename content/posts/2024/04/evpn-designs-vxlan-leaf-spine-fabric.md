---
title: "EVPN Designs: VXLAN Leaf-and-Spine Fabric"
series_title: "VXLAN Leaf-and-Spine Fabric"
date: 2024-04-03 07:45:00+0100
tags: [ EVPN, design, netlab, vxlan ]
netlab_tag: evpn_dg
evpn_tag: designs
pre_scroll: True
---
In this series of blog posts, we'll explore numerous routing protocol designs that can be used to implement EVPN-with-VXLAN L2VPNs in a leaf-and-spine data center fabric. Every design will come with a companion _netlab_ topology you can use to create a lab and explore the behavior of leaf- and spine switches.

Our leaf-and-spine fabric will have four leaves and two spines (but feel free to adjust the lab topology **fabric** parameters to build larger fabrics). The fabric will provide layer-2 connectivity to **orange** and **blue** VLANs. Two hosts will be connected to each VLAN to check end-to-end connectivity.
<!--more-->
{{<figure src="/2024/04/evpn-design-fabric.png" caption="Leaf-and-Spine Fabric Topology">}}

We'll start with the most straightforward design:

* An IP fabric running OSPF as the routing protocol
* VXLAN is used to transport Ethernet frames across the fabric
* The fabric uses ingress replication on leaf switches and does not run EVPN.

Yes, that's right: [you don't have to run EVPN](/2022/09/mlag-bridging-evpn/) to have a working VXLAN-based fabric. However, networking vendors sometimes don't want to be too explicit about this simple fact.

{{<figure src="/2024/04/evpn-design-vxlan.png" caption="Leaf-and-Spine Fabric Using VXLAN without EVPN">}}

**Benefits:**

* The design is as simple as it gets. It's simpler than the traditional L2 fabric (no spanning tree or MLAG in the fabric core) or EVPN.
* You don't need to run BGP in your fabric; everyone in your team probably knows how to configure OSPF in area 0.
* You won't experience any interoperability problems even if you believe in the fairy tale of multi-vendor fabrics. The only interaction between leaf switches is the data-plane VXLAN encapsulation.

**Drawbacks:**

* You must manage the ingress replication lists[^NOMC] on the leaf switches. Not a big deal if your fabric never grows or if you use a configuration generation tool (including Excel ;)
* You cannot use the fancy stuff like ARP suppression or EVPN-based MLAG (but maybe you're better off not using them anyway).
* Some vendors support [anycast first-hop gateway](/2013/05/optimal-l3-forwarding-with-varp-and/) (which is a good thing) only with EVPN.

[^NOMC]: Please don't tell me you can use IP multicast. I would prefer EVPN over IP multicast and PIM any day of the week, including a troubleshooting exercise at 2 AM on a Sunday.

Don't believe me that this design could work? Let's set up a lab and try it out.

### Leaf-and-Spine Lab Topology {#topo}

This is the _netlab_ lab topology description we'll use to set up our leaf-and-spine fabric:

{{<printout>}}
defaults.device: eos
provider: clab

plugin: [ fabric ]
fabric.spines: 2
fabric.leafs: 4

groups:
  _auto_create: True
  leafs:
    module: [ ospf, vlan, vxlan ]
  spines:
    module: [ ospf ]
  hosts:
    members: [ H1, H2, H3, H4 ]
    device: linux

vlan.mode: bridge
vlans:
  orange:
    links: [ H1-L1, H2-L3 ]
  blue:
    links: [ H3-L2, H4-L4 ]

tools:
  graphite:
{{</printout>}}

Let's go through it line-by-line:

* Lines 1-2: I will use Arista cEOS containers. More details [later](#lab)
* Lines 4-6: The topology uses the [**fabric** plugin](/2024/03/netlab-fabric-plugin/) to generate a leaf-and-spine fabric. The node names of the fabric switches will be L1 through L4 and S1/S2.
* Line 8: Due to the large number of nodes, we'll use groups to manage node parameters.
* Line 9: We want _netlab_ to [creates nodes](https://netlab.tools/groups/#create-nodes-from-group-members) based on the group's **members** list so we won't have to specify them manually.
* Line 10-11: The **fabric** plugin puts all leaf switches in the **leafs** group. The leaf switches will use VLANs and VXLAN, and run OSPF.
* Line 12-13: The **fabric** plugin puts all spine switches in the **spines** group. The spine switches will run OSPF.
* Line 14-16: We must define a few Linux hosts to test end-to-end connectivity.
* Line 18: The VLANs will be layer-2-only; the leaf switches won't have IP addresses on VLAN interfaces.
* Lines 19-23: We must create **orange** and **blue** VLANs and add links between hosts and leaf switches (the **fabric** plugin generates intra-fabric links). We don't have to define VXLAN VNIs or ingress replication lists. By default, _netlab_ creates VNIs for every VLAN and builds ingress replication lists from loopback addresses of other VXLAN switches.
* Lines 25-26: For fun, add the *graphite* GUI to the lab topology so you can point and click around it. Please note you won't be able to connect to the Linux hosts with Graphite as they don't run SSH servers.

Now, we're ready to start the lab and kick the tires.

### Creating the Lab Environment {#lab}

I prefer using Arista cEOS containers on Ubuntu to run EVPN labs:

* Arista EOS has a familiar user interface and uses the same configuration mechanism for data- and control planes.
* The cEOS containers consume approximately 1G of RAM per container. You can run a fabric with six switches on a 16GB laptop.
* You don't need nested virtualization when using containers inside a VM.

Using cEOS containers, you can run your tests on any x86 VM running on your laptop, your virtualization cluster[^VMW], or in a public cloud. If you want to [run EVPN labs on recent Apple laptops](/2024/03/netlab-bgp-apple-silicon/), you can choose between Arista cEOS, FRRouting, or Nokia SR Linux containers (all three of them have an ARM image).

You can also [start the lab in a GitHub Codespace](/2024/07/netlab-examples-codespaces/) (the directory is `EVPN/vxlan-fabric`); you'll still have to [import the Arista cEOS container](/2024/07/arista-eos-codespaces/), though.

{{<note info>}}
Starting with *netlab* release 1.8.0, you can [override the default device- and provider with environment variables](https://netlab.tools/defaults/#changing-defaults-with-environment-variables). To use my EVPN lab topologies with FRR containers, execute **export NETLAB_DEVICE=frr** in your Ubuntu VM.

You can use the same approach to start the labs with virtual machines. For example, if you insist on using Cisco Nexus OS, set these environment variables instead of changing the topology files:

```
export NETLAB_DEVICE=nxos
export NETLAB_PROVIDER=libvirt
```
{{</note>}}

[^VMW]: I wanted to write *your VMware cluster*, but I'm guessing that's not a popular option these days. I've heard good things about ProxMox, though.

If you're new to _netlab_, follow these simple steps to set up your lab in an Ubuntu VM running on your laptop. If you want something more complex, read the [netlab installation instructions](https://netlab.tools/install/).

* Download and install [multipass](https://multipass.run/)
* [Install netlab, Ansible, Docker, and Containerlab](/2024/03/netlab-bgp-apple-silicon/).
* [Download and install the Arista cEOS container](https://netlab.tools/labs/ceos/). Alternatively, tell _netlab_ you want to use FRR containers:

```
$ export NETLAB_DEVICE=frr
```

* Download the lab topology file into an empty directory on your Ubuntu instance:

```
$ mkdir fabric-test
$ cd fabric-test
$ wget https://raw.githubusercontent.com/ipspace/netlab-examples/master/EVPN/vxlan-fabric/topology.yml
```

* Start the lab with **netlab up**. Give OSPF a few seconds after the lab is configured to establish adjacencies.
* Connect to H1 with **netlab connect H1** and try to ping H2:

```
$ netlab connect H1
Connecting to container clab-vxlan-fabric-H1, starting bash
H1:/# ping H2
PING H2 (172.16.0.8): 56 data bytes
64 bytes from 172.16.0.8: seq=0 ttl=64 time=1.547 ms
64 bytes from 172.16.0.8: seq=1 ttl=64 time=2.494 ms
^C
--- H2 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 1.547/2.020/2.494 ms
```

Mission Accomplished!

### Behind the Scenes {#config}

This is the relevant part of the configuration of L1 running Arista EOS (you can view complete configurations for all switches on GitHub).

{{<printout>}}
vlan 1000
   name orange
!
interface Ethernet1
   description L1 -> S1
   ip address 10.1.0.1/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet2
   description L1 -> S2
   ip address 10.1.0.5/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Ethernet3
   mac-address 52:dc:ca:fe:01:03
   switchport access vlan 1000
!
interface Loopback0
   ip address 10.0.0.1/32
   ip ospf area 0.0.0.0
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vlan 1000 vni 101000
   vxlan vlan 1000 flood vtep 10.0.0.3
!
router ospf 1
   router-id 10.0.0.1
{{</printout>}}

Let's walk through the VXLAN-related parts. You have to:

* Define a VLAN (line 1) and use it on some Ethernet ports (line 18).
* Create a VXLAN interface (line 24) and specify the VTEP interface (line 25).
* Map VLAN ID into VXLAN VNI (line 27)
* Create a VXLAN ingress replication list for all VLANs or an individual VLAN (line 28).

I told you, it's as easy as it can get ;)

Let's throw a few **show** commands in for good measure. VLAN 1000 is active on Ethernet3 and Vxlan1 interfaces:

```
L1#show vlan
VLAN  Name                             Status    Ports
----- -------------------------------- --------- -------------------------------
1     default                          active
1000  orange                           active    Et3, Vx1
```

VLAN 1000 is mapped to VNI 101000:

```
L1#show vxlan vni
VNI to VLAN Mapping for Vxlan1
VNI          VLAN       Source       Interface       802.1Q Tag
------------ ---------- ------------ --------------- ----------
101000       1000       static       Ethernet3       untagged
                                     Vxlan1          1000
```

The ingress replication list has one remote VTEP:

```
L1#show vxlan vtep detail
Remote VTEPS for Vxlan1:

VTEP           Learned Via         MAC Address Learning       Tunnel Type(s)
-------------- ------------------- -------------------------- --------------
10.0.0.3       control plane       datapath                   flood

Total number of remote VTEPS:  1
```

MAC address table for VLAN 1000 has two entries (one of them reachable over VXLAN):

```
L1#show mac address-table
          Mac Address Table
------------------------------------------------------------------

Vlan    Mac Address       Type        Ports      Moves   Last Move
----    -----------       ----        -----      -----   ---------
1000    aac1.ab49.a48a    DYNAMIC     Vx1        1       0:00:09 ago
1000    aac1.ab4f.d1fb    DYNAMIC     Et3        1       0:01:15 ago
```

The MAC address reachable over VXLAN sits behind VTEP 10.0.0.3:

```
L1#show vxlan address-table
          Vxlan Mac Address Table
----------------------------------------------------------------------

VLAN  Mac Address     Type      Prt  VTEP             Moves   Last Move
----  -----------     ----      ---  ----             -----   ---------
1000  aac1.ab49.a48a  DYNAMIC   Vx1  10.0.0.3         1       0:00:47 ago
Total Remote Mac Addresses for this criterion: 1
```

Could you teach your entry-level engineers to use this when troubleshooting connectivity problems? I bet you could.

Unfortunately, I'm only too aware that some networking engineers hate simple solutions[^VKA]. Next time, we'll throw EVPN into the mix, yet again starting with a straightforward design: running a full mesh of IBGP sessions between leaf switches.

[^VKA]: Or drank too much vendor Kool-Aid, or need to pad their resume, or (in a few cases) have a network extensive enough that they need more complex technologies to cope with its scale.

{{<next-in-series page="/posts//2024/05/evpn-designs-ibgp-full-mesh.html"/>}}

### Revision History

2025-08-11
: Arista EOS containers are available as ARM images and can be used on Apple silicon