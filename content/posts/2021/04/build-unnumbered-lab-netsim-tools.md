---
date: 2021-04-05 05:57:00+00:00
lastmod: 2022-02-15 15:00:00
netlab_tag: use
series:
- unnumbered-interfaces
tags:
- IP routing
- netlab
title: Building Unnumbered Ethernet Lab with netlab
---
Last week I described the new features [added to netsim-tools release 0.4](https://netlab.tools/release/0.4/), including support for [unnumbered interfaces](https://netlab.tools/addressing/#unnumbered-interface-support) and [OSPF routing](https://netlab.tools/module/ospf/). Now let's see how I used them to build a multi-vendor lab to test which platforms could be made to interoperate when running OSPF over unnumbered Ethernet interfaces.

{{<note info>}}
* This blog post has been updated to use the new **netlab** CLI introduced in *netsim-tools* release 0.8 and new IPAM features introduced in release 1.0
* *netsim-tools* project [has been renamed to *netlab*](/2022/08/netsim-netlab/).
{{</note>}}
<!--more-->
First I needed to make P2P links within the lab unnumbered. Setting **unnumbered** attribute on the built-in **p2p** pool is good enough (for more details read the [addressing tutorial](https://netlab.tools/example/addressing-tutorial/)):

```
addressing:
  p2p:
    unnumbered: true
```

I wanted to run OSPF on all devices in the lab:

```
module: [ ospf ]
```

I built Vagrant/libvirt boxes for four different platforms (Arista vEOS 4.25.0, Cisco IOS XE 16.06.01, Cisco Nexus 9000v NXOS 9.3(6), Juniper vSRX 3.0 Junos 20.3R1.8), so I needed four nodes in my lab network. As each node uses a different Vagrant box, I couldn't use default device type:

```
nodes:
  c_nxos:
    device: nxos
  c_csr:
    device: csr
  a_eos:
    device: eos
  j_vsrx:
    device: vsrx
```

Finally, I created a full mesh of P2P links using the simplest possible link definition format (a list of strings in `A-B` format):

```
links:
- c_nxos-a_eos
- c_nxos-c_csr
- c_nxos-j_vsrx
- a_eos-j_vsrx
- a_eos-c_csr
- c_csr-j_vsrx
```

**Notes:**
* You did notice I didn't have to define interfaces on individual nodes, right?

## Next Steps

* [Install *netlab*](https://netlab.tools/install/) and a lab virtualization provider of your choice.
* Create Vagrant and Ansible configuration files, start the lab, and configure it with a single command: **netlab up**. [Here's the log file](https://github.com/ipspace/netlab-examples/blob/master/routing/unnumbered/config.log) in case you'd like to see how it worked.
* Wait for the network devices to boot. Write this blog post while waiting for Nexus 9300v and vSRX to boot. At least the *libvirt* provider starts them in parallel (as opposed to *virtualbox* provider that starts them in sequence).
* Use **netlab connect** to connect to lab devices and inspect the results.
* Destroy the lab with **netlab down**.

## Results

It works. The only glitch I encountered was the incorrect subnet mask in Arista EOS hello packets:

* OSPFv2 RFC (RFC 2328) specifies that the subnet mask in hello packets sent over unnumbered interfaces should be 0.0.0.0.
* Arista EOS 4.25.0 sends the subnet mask used by the interface supplying the IP address -- 255.255.255.255.
* Cisco IOS and Nexus OS [ignore the subnet mask](/2008/10/ospf-ignores-subnet-mask-mismatch-on/) and establish the adjacency.
* Junos rejects the incoming hello packets due to invalid subnet mask.

A quick search found an Arista EOS support article describing the **interface unnumbered hello mask tx 0.0.0.0** configuration command that solved the problem. Mission accomplished. I also added that command to EOS OSPF configuration template, so you don't have to worry about that when deploying your labs with *netlab*.

## More to Explore

[Directory with all relevant lab files](https://github.com/ipspace/netlab-examples/tree/master/routing/unnumbered) including:

* [Network topology](https://github.com/ipspace/netlab-examples/blob/master/routing/unnumbered/topology.yml)
* [Vagranfile](https://github.com/ipspace/netlab-examples/blob/master/routing/unnumbered/Vagrantfile) (imagine copy-pasting it together manually)
* [Configuration deployment log file](https://github.com/ipspace/netlab-examples/blob/master/routing/unnumbered/config.log)
* [Final device configurations](https://github.com/ipspace/netlab-examples/tree/master/routing/unnumbered/config)

You might also want to watch the *[Using OSPF in Leaf-and-Spine Fabrics](https://my.ipspace.net/bin/list?id=Clos#L3_SINGLE)* videos that inspired me to run this test.

### Revision History

2022-08-27
: *netsim-tools* has been renamed to *netlab*

2022-02-15
: Updated the blog post to use new features from *netsim-tools* release 1.1.

2021-07-12
: Updated the blog post to use the new **netlab** CLI.
