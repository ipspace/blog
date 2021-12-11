---
title: "Building Unnumbered Ethernet Lab with netsim-tools"
date: 2021-04-05 05:57:00
tags: [ IP routing, automation ]
series: netsim
lastmod: 2021-07-12 18:10:00
netsim_tag: use
---
Last week I described the new features [added to netsim-tools release 0.4](https://netsim-tools.readthedocs.io/en/latest/release/0.4.html), including support for [unnumbered interfaces](https://netsim-tools.readthedocs.io/en/latest/addressing.html#unnumbered-interface-support) and [OSPF routing](https://netsim-tools.readthedocs.io/en/latest/module/ospf.html). Now let's see how I used them to build a multi-vendor lab to test which platforms could be made to interoperate when running OSPF over unnumbered Ethernet interfaces.

{{<note info>}}This blog post has been updated to use the new **netlab** CLI introduced in *netsim-tools* release 0.8{{</note>}}
<!--more-->
I needed to define an unnumbered addressing pool first:

```
addressing:
  core:
    unnumbered: true
```

I wanted to run OSPF on all devices in the lab:

```
module: [ ospf ]
```

I built Vagrant/libvirt boxes for four different platforms (Arista vEOS 4.25.0, Cisco IOS XE 16.06.01, Cisco Nexus 9000v NXOS 9.3(6), Juniper vSRX 3.0 Junos 20.3R1.8), so I needed four nodes in my lab network. As each node uses a different Vagrant box, I couldn't use default device type:

```
nodes:
- name: c_nxos
  device: nxos
- name: c_csr
  device: csr
- name: a_eos
  device: eos
- name: j_vsrx
  device: vsrx
```

Finally, I created a full mesh of P2P links. Each link has two nodes connected to it, and uses **core** (unnumbered) address pool.

```
links:
- c_nxos:
  a_eos:
  role: core

- c_nxos:
  c_csr:
  role: core

- c_nxos:
  j_vsrx:
  role: core

- a_eos:
  j_vsrx:
  role: core

- a_eos:
  c_csr:
  role: core

- c_csr:
  j_vsrx:
  role: core
```

**Notes:**
* You did notice I didn't have to define interfaces on individual nodes, right?
* I had to use a dictionary format to specify custom addressing pool, otherwise I could specify the links as simple strings like `c_nxos-a_eos`

## Next Steps

* [Install *netsim-tools*](https://netsim-tools.readthedocs.io/en/latest/install.html) and a lab virtualization provider of your choice.
* Create **Vagrantfile**, Ansible inventory in **hosts.yml**, and **ansible.cfg** with **netlab create** command.
* Start the lab with **vagrant up**
* Wait for the network devices to boot. Write this blog post while waiting. At least the *libvirt* provider starts them in parallel (as opposed to *virtualbox* provider that starts them in sequence).
* Deploy IP addressing and OSPF routing configuration with **‌netlab initial -v** (v = verbose). [Here's the log file](https://github.com/ipspace/netsim-examples/blob/master/routing/unnumbered/config.log) in case you'd like to see how it worked.
* Use **netlab connect** to connect to lab devices and inspect the results.
* Destroy the lab with **vagrant destroy --force**.

## Results

It works. The only glitch I encountered was the incorrect subnet mask in Arista EOS hello packets:

* OSPFv2 RFC (RFC 2328) specifies that the subnet mask in hello packets sent over unnumbered interfaces should be 0.0.0.0.
* Arista EOS 4.25.0 sends the subnet mask used by the interface supplying the IP address -- 255.255.255.255.
* Cisco IOS and Nexus OS [ignore the subnet mask](https://blog.ipspace.net/2008/10/ospf-ignores-subnet-mask-mismatch-on.html) and establish the adjacency.
* Junos rejects the incoming hello packets due to invalid subnet mask.

A quick search found an Arista EOS support article describing the **‌interface unnumbered hello mask tx 0.0.0.0** configuration command that solved the problem. Mission accomplished. I also added that command to EOS OSPF configuration template (until the [netsim-tools](https://github.com/ipspace/netsim-tools) release 0.5 is out, you'll find it in the [dev_0.5](https://github.com/ipspace/netsim-tools/tree/dev_0.5) branch).

## More to Explore

[Directory with all relevant lab files](https://github.com/ipspace/netsim-examples/tree/master/routing/unnumbered) including:

* [Network topology](https://github.com/ipspace/netsim-examples/blob/master/routing/unnumbered/unnumbered.yml)
* [Vagranfile](https://github.com/ipspace/netsim-examples/blob/master/routing/unnumbered/Vagrantfile) (imagine copy-pasting it together manually)
* [Configuration deployment log file](https://github.com/ipspace/netsim-examples/blob/master/routing/unnumbered/config.log)
* [Final device configurations](https://github.com/ipspace/netsim-examples/tree/master/routing/unnumbered/config)

You might also want to watch the *[Using OSPF in Leaf-and-Spine Fabrics](https://my.ipspace.net/bin/list?id=Clos#L3_SINGLE)* videos that inspired me to run this test.

### Revision History

2021-07-12
: Updated the blog post to use the new **netlab** CLI.

