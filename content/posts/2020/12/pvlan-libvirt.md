---
title: "Implement Private VLAN Functionality with Linux Bridge and Libvirt"
date: 2020-12-09 07:20:00
tags: [ virtualization, switching ]
---
I wanted to test routing protocol behavior (IS-IS in particular) on partially meshed multi-access layer-2 networks like private VLANs or Carrier Ethernet E-Tree service. I recently spent plenty of time creating a Vagrant/libvirt lab environment on my Intel NUC running Ubuntu 20.04, and I wanted to use that environment in my tests.

**Challenge-of-the-day**: How do you implement private VLAN functionality with Vagrant using libvirt plugin?

There might be interesting KVM/libvirt options I've missed, but so far I figured two ways of connecting Vagrant-controlled virtual machines in libvirt environment:
<!--more-->
* Use UDP tunnels to create [point-to-point pseudowires](https://codingpackets.com/blog/pseudo-wires-with-vagrant-and-libvirt/).
* Use Linux bridges.

Partially meshed networks becomes interesting when you have more than two nodes. Linux bridge it is.

**Next challenge**: how do you implement private VLAN on a Linux bridge?

There are tons of posts on the Internet describing how to use **ebtables** to implement partial connectivity between devices connected to a Linux bridge (including a [really good one by Vincent Bernat](https://vincent.bernat.ch/en/blog/2017-linux-bridge-isolation)), but all those recipes seemed way too complex. Finally I stumbled upon **isolated** option of **bridge** command -- another one of those wonderful features documented in a single sentence on a man page.

> Controls whether a given port will be isolated, which means it will be able to communicate with non-isolated ports only. By default this flag is off.

That seemed to be exactly what I needed. Time to do some tests.

I decided to use a totally isolated Linux bridge with no IP configured on it (preventing any interaction with the host TCP/IP stack). This is (part of the) Vagrantfile I used to create the bridge and connect virtual machines to it:

```
config.vm.define "c1" do |c1|
c1.vm.network :private_network,
              :libvirt__network_name => "PVLAN",
              :libvirt__forward_mode => "veryisolated",
              :libvirt__dhcp_enabled => false,
              :auto_config => false
end
```

**Important details:**

* The **libvirt__network_name** is the bridge name *within libvirt environment*. The Linux bridge name will be different.
* Unless you use **veryisolated** forwarding mode, Vagrant becomes nervous about lack of usable IP addresses on that subnet.
* Disable DHCP because you can't run a DHCP server on a network not connected to host TCP/IP stack.
* Disable interface auto-configuration. We'll configure IP addressing with an Ansible playbook.

After bringing up an environment with three Cisco IOS devices, I configured IP addresses on their GigabitEthernet0/1 interfaces ([GigabitEthernet0/0 is used as Vagrant management interface](https://codingpackets.com/blog/cisco-iosv-vagrant-libvirt-box-install/)) and performed a quick ping test using this Ansible playbook:

```
---
- name: Ping all Ansible hosts connected to target interface
  hosts: all
  gather_facts: true
  vars:
    target_interface: GigabitEthernet0/1
  tasks:
  - cisco.ios.ios_ping:
      dest: "{{ hostvars[item].ansible_net_interfaces[target_interface]
                .ipv4[0].address }}"
      count: 3
    loop: "{{ groups['all'] }}"
    when: item != inventory_hostname
```

A few notes:

* I'm using network device fact gathering (available in Ansible 2.9 or 2.10, never figured that out) to get configured IP addresses. The list of addresses configured on individual interfaces is available in **ansible_net_interfaces**.
* The **ios_ping** task is run in a loop that is executed for all Ansible devices in group **all**. Yes, I know that also means every device will ping itself. Sometimes that's not a bad idea.
* The IP address to ping is extracted from the **ansible_net_interfaces** host variable for the target host. I'm using the first IPv4 address assigned to the specified interface name.

Here's a screen shot of the first run of that playbook:

{{<figure src="/2020/12/pvlan-ping-1.png" caption="Pings work. Life is good.">}}

Next step: enable port isolation on ports connecting two out of three virtual machines to my Linux bridge. To do that, I needed to know the names of the interfaces created by Vagrant libvirt provider. The easiest way to get them is to get the list of interfaces connected to the virtual machines I wanted to isolate:

```
$ virsh domiflist PVLAN_c2
 Interface   Type      Source            Model   MAC
--------------------------------------------------------------------
 vnet2       network   vagrant-libvirt   e1000   08:4f:a9:00:00:02
 vnet3       network   PVLAN             e1000   52:54:00:55:90:8f
$ virsh domiflist PVLAN_c3
 Interface   Type      Source            Model   MAC
--------------------------------------------------------------------
 vnet4       network   vagrant-libvirt   e1000   08:4f:a9:00:00:03
 vnet5       network   PVLAN             e1000   52:54:00:11:59:14
```

**Notes:**

* Names of virtual machines created by Vagrant are a combination of Vagrantfile directory and VM name specified in Vagrantfile. I have my Vagrantfile in *NBMA* directory, and the VM names are *c1*, *c2* and *c3*.
* The interfaces listed in the printout are Linux interfaces, the name of the bridge (*Source*) is *libvirt* private network name. To find the name of the underlying Linux bridge use **virsh net-info**.

After enabling port isolation on **vnet3** and **vnet5** with **bridge link set dev *name* isolated on**, *c2* and *c3* can no longer ping each other. Mission accomplished.

{{<figure src="/2020/12/pvlan-ping-failed.png" caption="C2 and C3 can no longer ping each other">}}

The mandatory final step: automate all the boring tasks. The interface names can change every time Vagrant recreates the environment, so I needed a more generic solution. This is a Bash script I'm using to enable bridge port isolation.

```
#!/bin/bash
domain_prefix=$(basename $(pwd))
pvlan_switch=NBMA
isolated='c2 c3'
for node in $isolated
do
  domain=${domain_prefix}_${node}
  device=$(virsh domiflist $domain|grep ${pvlan_switch}|awk '{ print $1 }')
  if [ -n "$device" ]; then
    echo "VM $domain is attached to ${pvlan_switch} with $device"
    sudo bridge link set dev $device isolated on
    echo "... $device isolated"
  else
    echo "VM $domain is NOT attached to ${pvlan_switch}"
  fi
done
```

**Notes:**

* Yes, **virsh** is as bad as Cisco IOS -- it cannot spell JSON. I had to use **awk** to get the device name I needed. Stop complaining about the awful state of Cisco IOS **show** commands.

### More Information

* I covered fact gathering on network devices in the *[Getting Operational Data](https://my.ipspace.net/bin/list?id=Ansible#NET_DATA)* part of *[Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers)* webinar.
* Dinesh Dutt covered network simulation with Vagrant in [*Network Simulation Tools*](https://my.ipspace.net/bin/list?id=NetTools#SIMULATE) part of [*Network Automation Tools*](https://www.ipspace.net/Network_Automation_Tools) webinar.
* [Brad Searle](https://www.linkedin.com/in/bradleysearle/) published a large collections of useful [Vagrant-with-libvirt tricks](https://codingpackets.com/blog/tag/libvirt/).

Finally, there's no better way to master network automation than enrolling in [Building Network Automation Solutions online course](https://www.ipspace.net/Building_Network_Automation_Solutions).
