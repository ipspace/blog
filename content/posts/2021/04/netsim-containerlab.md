---
title: "Netsim-tools Release 0.5 Work with Containerlab"
date: 2021-04-14 07:26:00
lastmod: 2021-07-12 18:12:00
tags: [ netlab ]
netlab_tag: archive
---
**TL&DR**: If you happen to like working with containers, you could use netsim-tools release 0.5 to provision your container-based Arista EOS labs.

**Why does it matter?** Lab setup is blindingly fast, and it's easier to integrate your network devices with other containers, not to mention the crazy idea of running your network automation CI pipeline on Gitlab CPU cycles. Also, you could use the same netsim-tools topology file and provisioning scripts to set up container-based or VM-based lab.

**What is containerlab?** A [cool project](https://containerlab.srlinux.dev/) that builds realistic virtual network topologies with containers. [More details...](https://netdevops.me/2021/containerlab-your-network-centric-labs-with-a-docker-ux/)
<!--more-->
This is a simple topology file (let's call it *topology.yml*) I used to test the setup; it creates a two-switch lab with a link between the switches.

```
provider: clab
defaults:
  device: eos

nodes:
- s1
- s2

links:
- s1-s2
```

Next steps after installing Docker, [containerlab](https://containerlab.srlinux.dev/install/) and [netsim-tools](https://netlab.tools/install/):

* [Create the containerlab topology file](https://netlab.tools/netlab/create/) (*clab.yml*), Ansible inventory (*hosts.yml*), *host_vars*, *group_vars*, and *ansible.cfg* with **netlab create** 
* Start the lab with **sudo containerlab deploy -t clab.yml**
* [Deploy initial configurations](https://netlab.tools/configs/) with **netlab initial**

Change the **provider** from *clab* to *libvirt* or *virtualbox* and you'll get a Vagrantfile that will set up two VMs with a point-to-point link between them[^1]. Add `module: [ ospf ]` and you'll get OSPF routing configured together with IP addresses. How cool is that? ;)

For more details, [read the netsim-tools documentation](https://netlab.tools/), [download the code](https://github.com/ipspace/netlab) or [install it as a Python3 package](https://netlab.tools/install/), and enjoy.

[^1]: The latest EOS version downloadable as Vagrant box is 4.21.14M.

### Revision History

2021-07-12
: Updated the blog post to use the new **netlab** CLI.
