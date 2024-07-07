---
title: "Making LLDP Work with Linux Bridge"
date: 2020-12-16 07:05:00
tags: [ switching, virtualization ]
---
Last week I described how I [configured PVLAN on a Linux bridge](/2020/12/pvlan-libvirt/). After checking the desired partial connectivity with **ios_ping** I wanted to verify it with LLDP neighbors. Ansible **ios_facts** module collects LLDP neighbor information, and it should be really easy using those facts to check whether port isolation works as expected.

{{<cc>}}Ansible playbook displaying LLDP neighbors on selected interface{{</cc>}}
```
---
- name: Display LLDP neighbors on selected interface
  hosts: all
  gather_facts: true
  vars:
    target_interface: GigabitEthernet0/1
  tasks:
  - name: Display neighbors gathered with ios_facts
    debug:
      var: ansible_net_neighbors[target_interface]
```

Alas, none of the routers saw any neighbors on the target interface.
<!--more-->
Fortunately, I wasn't the [first one experiencing this problem](https://xkcd.com/979/). It turns out Linux bridge blocks packets sent to IEEE-reserved MAC addresses (MAC addresses used by LLDP, LACP, STP, 802.1X, PBB control plane), but you can change that behavior by modifying the **group_fwd_mask** system parameter.

You can find all the gory details in a [blog post by Robin Gilijamse](https://interestingtraffic.nl/2017/11/21/an-oddly-specific-post-about-group_fwd_mask/), what we need to do is to [set group_fwd_mask to 0x4000](https://the-bitmask.com/2017/08/04/fwd-lldp-frames-on-linuxbridge/). To do that we need to write the desired value into **‌/sys/class/net/*device*/bridge/group_fwd_mask**. The device name is the Linux bridge name (not *libvirt* network name) and to find it, we need to use **virsh net-info** command.

Another boring task worth automating. Here's the Bash script doing it (invoke it with *libvirt* network name).

```
#!/bin/bash
network=${1:-NBMA}
bridge=$(virsh net-info ${network}|grep Bridge|awk '{ print $2 }')
echo "libvirt network ${network} is Linux bridge ${bridge}"
echo "... enabling LLDP on ${bridge}"
sudo sh -c "echo 0x4000 >/sys/class/net/${bridge}/bridge/group_fwd_mask"
```

After changing the **group_fwd_mask**, LLDP works like a charm:

{{<figure src="/2020/12/pvlan-lldp.png" caption="LLDP neighbors on a hub-and-spoke PVLAN bridge">}}

### More Information

* I covered fact gathering on network devices in the *[Getting Operational Data](https://my.ipspace.net/bin/list?id=Ansible#NET_DATA)* part of *[Ansible for Networking Engineers](https://www.ipspace.net/Ansible_for_Networking_Engineers)* webinar.
* Dinesh Dutt covered network simulation with Vagrant in [*Network Simulation Tools*](https://my.ipspace.net/bin/list?id=NetTools#SIMULATE) part of [*Network Automation Tools*](https://www.ipspace.net/Network_Automation_Tools) webinar.
* There's no better way to master network automation than enrolling in [Building Network Automation Solutions online course](https://www.ipspace.net/Building_Network_Automation_Solutions).
