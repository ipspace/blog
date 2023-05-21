---
date: 2023-02-27 07:02:00+00:00
netlab_tag: use
tags:
- netlab
title: Suspending Devices in netlab Labs
---
A networking engineer [tired of waiting for network devices to start](https://blog.ipspace.net/2023/02/virtual-device-boot-times.html) sent me this question:

> Can you suspend VMs in netlab? I use this trick in vSphere with CSR1Kv.

**TL&DR**: Maybe. Probably not.
<!--more-->
_netlab_ tries to stay as far away from reinventing the wheels as possible[^VP] and offloads all the virtualization and orchestration tasks to other tools like KVM/libvirt and Vagrant. With that in mind, let's rephrase the question as "_can you use Vagrant to suspend/resume a network device VM in KVM/libvirt environment and what would be the impact of doing that on netlab?_"

[^VP]: ... although it does have to configure virtual plumbing when [mixing virtual machines and containers](/2023/02/netlab-vm-containers.html).

In theory, the answer is "_yeah, why not._" In practice, my very first test failed[^GTP].

I decided to use the simplest possible topology: two Arista vEOS devices running OSPF to check whether they could exchange control-plane traffic over a Vagrant-provisioned connection.

[^GTP]: ... proving yet again the existence of the theory-practice gap.

```
defaults.device: eos
nodes: [ r1, r2 ]
module: [ ospf ]
links: [ r1, r2, r1-r2 ]
```

I started the lab with **netlab up**, which configured the management bridge and [executed **vagrant up** to start the lab followed by an Ansible playbook to configure the devices](https://netlab.tools/netlab/up/).

Next, I executed **vagrant suspend**. No errors, the VMs were suspended. I checked the list of virtual networks with **virsh net-list** and they were still there. So far, so good.

Finally, I tried to resurrect the VMs with **vagrant resume**. One of them came up immediately, the other one got totally bricked -- SSH didn't work and I wasn't able to access it with **virsh console** which connects to the virtual console serial port.

The same procedure might work with other network devices, but I'm not sure whether saving a minute or two is worth the hassle. I prefer to start my labs from scratch with freshly-minted configuration (hint: you can use **[netlab restart](https://netlab.tools/netlab/restart/)** to do it).

### Getting Started

Want to know more about *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/). You might also want to watch the _[Using netlab to Build Networking Labs](https://my.ipspace.net/bin/list?id=NetTools#NETLAB)_ section of  _[Network Automation Tools](https://www.ipspace.net/Network_Automation_Tools)_ webinar.

