---
date: 2010-07-19 06:49:00.005000+02:00
tags:
- switching
- data center
- virtualization
title: Server Virtualization Has Totally Changed the Data Center Networking
url: /2010/07/server-virtualization-has-totally/
---
There's an extremely good reason Brad Hedlund mentioned server virtualization in his [career advice](http://twitter.com/bradhedlund/statuses/18541080479): it has fundamentally changed the Data Center networking.

Years ago, we've treated servers as oversized IP hosts. From the networking perspective, they were no different from other IP hosts. Some of them had [weird clustering requirements](/2009/08/turn-switch-into-hub-microsoft-way/), some of them had [multiple uplinks that had to be managed somehow](/2009/06/multihomed-ip-hosts/), but those were just minor details. Server virtualization is a completely different beast.
<!--more-->
Let's take a look at the server virtualization from the networking perspective. This technology allows you to run multiple totally independent servers (virtual machines) inside the same physical server. Obviously each one of these virtual servers needs its own IP address, has to communicate with the outside world and (potentially) belongs to a different security zone than other servers running on the same hardware. Some VMs might also need to communicate with other VMs running on the same physical server (for example, a web server VM communicating with a database VM).

Some people have "solved" the problem by installing numerous NICs (Network Interface Cards) in the same physical server, connecting the server to a switch (or two of them for redundancy) in a "cow milking machine configuration".

{{<figure src="/2010/07/s1600-SV_Nic_Per_VM.png" caption="NIC-per-VM design">}}

### Virtual switches

Obviously this is an ugly solution wasting money on NIC cards and switch ports (just imagine making it truly redundant). Virtualization vendors have solved the problem in an elegant (in their opinion) way: they've implemented a switch inside the virtualization software. All of a sudden, all virtual machines in the same physical server can communicate with each other and the outside world.

{{<figure src="/2010/07/s1600-SV_Embedded_L2SW.png" caption="Layer-2 virtual switch in the hypervisor">}}

The communication between the VMs and the outside worlds seems to be solved, but the networking headaches have just started: all of a sudden you have extra switches (over which you have no control) popping up in your network, in some cases even without your awareness, as the server team might decide to deploy pilot VMware or Hyper-V servers without notifying anyone else.

The VMware implementation of the switch cannot generate a forwarding loop. It strictly separates *uplink* and *host* ports, never forwards a packet from one *uplink* port to another and drops packets sent from local MAC addresses if they arrive through the *uplink* port (indicating a bridging loop somewhere else). Hyper-V is not so picky; it's quite easy to generate a nice network meltdown if you enable bridging between two *uplink* interfaces.

### Security concerns

An extra (virtual) switch in the physical server should make the security engineers nervous; after all, sometimes the VMs running in the same physical server belong to different security zones (I leave it up to you to decide whether that's a good idea or not). No problem, the vendors will tell you, you just have to implement VLANs in your VMware switch and assign virtual machines to different VLANs.

{{<figure src="/2010/07/s1600-SV_Hyper_Trunking.png" caption="VLAN trunking from hypervisor virtual switch">}}

End result: not only are we getting extra switches in our network (we could protect ourselves against that with BPDU guard), now we're getting switches that require trunked ports. The dividing line between the networking team and the server team is thus getting very blurry and they have to start working together to ensure that the server and network settings are aligned and that the new virtual switches deployed in the Data Center do not destroy its design or disrupt its operations.

To make the second task easier, Cisco introduced the Nexus 1000V software. It's a NX-OS control plane implementation running as a virtual machine on VMware ESX. Nexus 1000V uses VMware API to control distributed VMware ESX switches and presents the network engineers the familiar NX-OS CLI and feature set (in-depth description of Nexus 1000V is available in the chapter 9 of the NX-OS and Cisco Nexus Switching book).

## More Details

You\'ll learn more about networking aspects of the new Data Center architectures in the [Data Center Infrastructure for Networking Engineers](http://www.ipspace.net/DC30) webinar.
