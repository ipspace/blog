---
date: 2020-12-17 07:26:00+00:00
lastmod: 2022-02-15 14:10:00
netlab_tag: overview
tags:
- netlab
title: Build Your Virtual Lab Faster with netlab
---
_This blog post describes the reasons I started working on netlab. We got incredibly far in the meantime; check [netlab documentation](https://netlab.tools/) for more details._

I love my new Vagrant+Libvirt virtual lab environment -- it creates virtual machines in parallel and builds labs much faster than my previous VirtualBox-based setup. Eight CPU cores and 32 GB of RAM in my Intel NUC don't hurt either. 

However, it's still ridiculously boring to set up a new lab. Vagrantfiles describing the private networks I need for routing protocol focused network simulations are a mess to write, and it takes way too long to log into all the devices, configure common parameters, enable interfaces...
<!--more-->
So instead of spending 15 minutes editing a Vagrantfile to get the P2P links I needed and another five minutes furiously typing in Cisco IOS CLI, I [spent a few days](https://xkcd.com/1319/) writing tools to get the job done... but now I'll be able to build the next three labs [so much faster](https://xkcd.com/974/) ;)

Anyway, you might find the tools interesting, so I pushed them into a [public Github repository](https://github.com/ipspace/netlab) and wrote what I hope is [decent documentation](https://netlab.tools/).

The crown jewel of the collection is a tool that takes network topology description in a YAML file that I made as simple as possible, [creates addressing plan, Vagrantfile, Ansible inventory, and a data model describing all the network devices in details](https://netlab.tools/netlab/create/). For example, all I needed to get my lab up and running was this:

```
defaults:
  device: iosv

nodes: [ pe1, p1, p2, pe2 ]
links:
- pe1-p1
- pe1-p2
- pe2-p1
- pe2-p2
```

Here's the part of the resulting Vagrantfile describing pe1:

```
  config.vm.define "pe1" do |pe1|
    pe1.vm.provider :libvirt do |domain|
      domain.management_network_mac = "08-4F-A9-00-00-01"
    end
    pe1.vm.box = "cisco/iosv"
    pe1.vm.synced_folder ".", "/vagrant", disabled: true
    pe1.ssh.insert_key = false
    pe1.vm.boot_timeout = 180
    pe1.vm.guest = :freebsd

    pe1.vm.provider :libvirt do |domain|
      domain.nic_adapter_count = 8
      domain.memory = 512
      domain.cpus = 1
      domain.driver = "kvm"
      domain.nic_model_type = "e1000"
    end
##
    pe1.vm.network :private_network,
                  :libvirt__tunnel_type => "udp",
                  :libvirt__tunnel_local_ip => "127.1.1.1",
                  :libvirt__tunnel_local_port => "10001",
                  :libvirt__tunnel_ip => "127.1.2.1",
                  :libvirt__tunnel_port => "10001",
                  :libvirt__iface_name => "vgif_pe1_1",
                  auto_config: false
    pe1.vm.network :private_network,
                  :libvirt__tunnel_type => "udp",
                  :libvirt__tunnel_local_ip => "127.1.1.2",
                  :libvirt__tunnel_local_port => "10002",
                  :libvirt__tunnel_ip => "127.1.3.1",
                  :libvirt__tunnel_port => "10001",
                  :libvirt__iface_name => "vgif_pe1_2",
                  auto_config: false
  end
```

... and here's the **host_vars/pe1/topology.yml** file describing interfaces, IP addresses, and expected neighbors of PE1:

```
---
links:
- ifindex: 1
  ifname: GigabitEthernet0/1
  ip: 10.1.0.1/30
  neighbors:
    p1:
      ifname: GigabitEthernet0/1
      ip: 10.1.0.2/30
  remote_id: 2
  remote_ifindex: 1
- ifindex: 2
  ifname: GigabitEthernet0/2
  ip: 10.1.0.5/30
  neighbors:
    p2:
      ifname: GigabitEthernet0/1
      ip: 10.1.0.6/30
  remote_id: 3
  remote_ifindex: 1
loopback: 10.0.0.1
mgmt_ip: 192.168.121.101
mgmt_mac: 08-4F-A9-00-00-01
```

**Next step**: an Ansible playbook started with **netlab initial** command that generates initial device configuration based on interfaces and IP addresses specified in **links** dictionary. Single command, no parameters (apart from specifying Ansible inventory), no configuration (because I have per-platform initial configuration templates).

The same playbook can also be used to configure OSPF, BGP, IS-IS, EIGRP...

**End result**: it takes just a few minutes to set up a brand-new lab topology. Of course I wasted more time developing the tools than I'll save in my lifetime, but maybe some of you will find them useful, add support for different Vagrant providers or network devices, and send a few karma points my way ;)

### Release History

2022-02-15
: Updated the blog post with features from netsim-tools release 1.1.
