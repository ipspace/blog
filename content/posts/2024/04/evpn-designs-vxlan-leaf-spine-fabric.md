---
title: "EVPN Designs: VXLAN Leaf-and-Spine Fabric"
series_title: "VXLAN Leaf-and-Spine Fabric"
date: 2024-04-03 07:45:00+0100
tags: [ EVPN, design, netlab ]
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

Yes, that's right: [you don't have to run EVPN](/2022/09/mlag-bridging-evpn.html) to have a working VXLAN-based fabric. However, networking vendors sometimes don't want to be too explicit about this simple fact.

{{<figure src="/2024/04/evpn-design-vxlan.png" caption="Leaf-and-Spine Fabric Using VXLAN without EVPN">}}

Don't believe me that this could work? Let's set up a lab and try it out.

### Leaf-and-Spine Lab Topology

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
* Lines 4-6: The topology uses the [**fabric** plugin](/2024/03/netlab-fabric-plugin.html) to generate a leaf-and-spine fabric. The node names of the fabric switches will be L1 through L4 and S1/S2.
* Line 8: Due to the large number of nodes, we'll use groups to manage node parameters.
* Line 9: We want _netlab_ to [creates nodes](https://netlab.tools/groups/#create-nodes-from-group-members) based on the group's **members** list so we won't have to specify them manually.
* Line 10-11: The **fabric** plugin puts all leaf switches in the **leafs** group. The leaf switches will use VLANs and VXLAN, and run OSPF.
* Line 12-13: The **fabric** plugin puts all spine switches in the **spines** group. The spine switches will run OSPF.
* Line 14-16: We must also define a few Linux hosts.
* Line 18: The VLANs will be layer-2-only; the leaf switches won't have IP addresses on VLAN interfaces.
* Lines 19-23: We must create **orange** and **blue** VLANs and add links between hosts and leaf switches (the **fabric** plugin generates intra-fabric links). We don't have to define VXLAN VNIs or ingress replication lists. By default, _netlab_ creates VNIs for every VLAN and builds ingress replication lists from loopback addresses of other VXLAN switches.
* Lines 25-26: Just for fun, let's add the *graphite* GUI to the lab topology so you can point and click your way around it. Please note you won't be able to connect to the Linux hosts with Graphite as they don't run SSH servers.

Now, we're ready to start the lab and kick the tires.

### Creating the Lab Environment {#lab}

I prefer using Arista cEOS containers on Ubuntu to run EVPN labs:

* Arista EOS has a familiar user interface
* The cEOS containers consume approximately 1G of RAM per container. You might be able to run a fabric with six switches on a 16GB laptop.
* You don't need nested virtualization when using containers inside a VM.

Using cEOS containers, you can run your tests on any x86 VM running on your laptop, your virtualization cluster[^VMW], or in a public cloud. Alternatively, if you want to [run EVPN labs on recent Apple laptops](/2024/03/netlab-bgp-apple-silicon.html), use the FRR containers.

{{<note info>}}
Starting with *netlab* release 1.8.0, you can [override the default device- and provider with environment variables](https://netlab.tools/defaults/#changing-defaults-with-environment-variables). To use my EVPN lab topologies with FRR containers, execute **export NETLAB_DEVICE=frr** in your Ubuntu VM.

You can use the same approach to start the labs with virtual machines. For example, if you insist on using Cisco Nexus OS, set these environment variables instead of changing the topology files:

```
export NETLAB_DEVICE=nxos
export NETLAB_PROVIDER=libvirt
```
{{</note>}}

[^VMW]: I wanted to write *your VMware cluster*, but I'm guessing that's not a popular option these days. I've heard good things about ProxMox, though.

If you're brand new to _netlab_, use these simple steps to set up your lab in a Ubuntu VM running on your laptop. If you want something more complex, read the [netlab installation instructions](https://netlab.tools/install/).

* Download and install [multipass](https://multipass.run/)
* [Install netlab, Ansible, Docker, and Containerlab](/2024/03/netlab-bgp-apple-silicon.html).
* If you're running on x86 hardware, [download and install the Arista cEOS container](https://netlab.tools/labs/ceos/). If you're running your Ubuntu VM on Apple silicon, tell _netlab_ you want to use FRR containers:

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
