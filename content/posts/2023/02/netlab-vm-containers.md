---
date: 2023-02-06 06:51:00+00:00
netlab_tag: guidelines
series_title: Mix Containers and VMs in the Same Lab Topology
tags:
- netlab
title: Mix Containers and VMs with netlab Release 1.5.0
---
Maybe it's just me, but I always need a few extra devices in my virtual labs to have endpoints I could ping to/from or to have external routing information sources. We used VRF- and VLAN tricks in the days when we had to use physical devices to carve out a dozen hosts out of a single Cisco 2501, and life became much easier when you could spin up a few additional virtual machines in a virtual lab instead.

Unfortunately, those virtual machines eat precious resources. For example, *netlab* allocates [1GB to every Linux virtual machine](https://netlab.tools/platforms/#supported-virtualization-providers) when you only need `bash` and `ping`. Wouldn't it be great if you could start that `ping` in a *busybox* container instead?
<!--more-->
Combining virtual machines running under KVM with Docker-controlled containers was always tricky, particularly when you wanted to have them organized in a complex virtual network. *containerlab* solved the container connectivity bit, and the *vrnetlab* project gave us the tools to package network OS virtual machines into containers (running VM instances inside containers), but wouldn't it be better to have native VMs and containers working together? That's what *netlab* release 1.5.0 can do.

### How to Set It Up?

The user experience is as seamless as I could make it. One of the virtualization providers is the *primary* provider (specified in the topology **provider** parameter), and all devices in the lab use that virtualization provider unless you select another one with the node (or group) **provider** parameter. For example, this is how you could combine Linux end-hosts running in containers with a VXLAN fabric built from Nexus OS virtual machines:

```
provider: libvirt

groups:
  hosts:
    members: [ h1, h2 ]
    device: linux
    provider: clab
  switches:
    members: [ s1,s2 ]
    device: nxos
    module: [ vlan,vxlan,ospf ]

vlans:
  red:
    mode: bridge

nodes: [ h1, h2, s1, s2 ]

links:
- s1:
  s2:
- h1:
  s1:
    vlan.access: red
- h2:
  s2:
    vlan.access: red
```

Unfortunately, it would be too hard to provide a true mix-and-match experience. In release 1.5.0, the primary provider has to be *libvirt*; you can use *containerlab* as the secondary provider. The up-to-date list of compatible providers is always available in the [online documentation](https://netlab.tools/providers/#combining-virtualization-providers).

### Behind the Scenes

As you might have expected, there's a complex bowl of spaghetti mess behind the scenes:  

-   Virtual machines and containers running SSH daemons must share the same management IP subnet. Fortunately, *containerlab* has a parameter specifying a Linux bridge used for the management subnet, and *netlab* knows the name of the *libvirt* management bridge (it has to be created during the **netlab up** process).
-   *netlab* uses UDP tunnels for point-to-point VM-to-VM links. Those links must be converted into links using a Linux bridge when at least one of the nodes is a container.
-   *containerlab* can connect containers to existing Linux bridges, but you have to know the bridge name, and it's impossible to specify that with the *vagrant-libvirt* plugin. **netlab up** has to execute **vagrant up** to get the VM portion of the lab running, inspect the *libvirt* networks to get the Linux bridge names, modify the *containerlab* configuration file, and execute **containerlab** to start the container portion of the lab.

Long story short: you MUST use **netlab up** to start the lab, or you'll get a fascinating hard-to-clean-up mess.

### Getting Started

To get more details and learn about additional features included in release 1.5.0, [read the release notes](https://netlab.tools/release/1.5/#release-1-5-0). To upgrade, execute `pip3 install --upgrade networklab`.

New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
