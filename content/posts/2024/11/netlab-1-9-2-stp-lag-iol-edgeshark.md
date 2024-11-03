---
title: "netlab 1.9.2: STP, LAG, Cisco IOL, Edgeshark"
series_title: "Spanning Tree, Link Aggregation, Cisco IOS-on-Linux, Edgeshark"
date: 2024-11-04 08:13:00+02:00
tags: [ netlab ]
netlab_tag: release
---
While I was busy [fixing bugs](https://netlab.tools/release/1.9/#bug-fixes-in-release-1-9-2) in the [_netlab_ release 1.9.2](https://netlab.tools/release/1.9/), other contributors added exciting new features:

* Jeroen van Bemmel added the [spanning tree](https://netlab.tools/module/stp/) and [link aggregation](https://netlab.tools/module/lag/) configuration modules, initially implemented on Arista EOS, Cumulus Linux, and FRR.
* Dan Partelly added the **[netlab exec](https://netlab.tools/netlab/exec/)** command that can execute the same command on a set of network devices, [support](https://netlab.tools/extool/edgeshark/) for [Edgeshark](https://github.com/siemens/edgeshark), and [support for Cisco IOS on Linux (IOL) and Cisco IOS layer-2 image on Linux (IOLL2)](https://netlab.tools/platforms/), the latter after a heroic uphill battle with ancient software ([part 1](https://github.com/ipspace/netlab/issues/1381), [part 2](https://github.com/ipspace/netlab/discussions/1470)).

Other new features include:
<!--more-->
* Cisco IOSv and IOSvL2 running in [*vrnetlab* containers](https://netlab.tools/labs/clab/#clab-vrnetlab)
* [First-hop gateways](https://netlab.tools/module/gateway/#module-gateway) and [DHCP clients/relays](https://netlab.tools/module/dhcp/#module-dhcp) [VLANs](https://netlab.tools/module/vlan/#module-vlan)
* [Changing interface names](https://netlab.tools/links/#links-ifname) in virtual machines and containers.
* [Packet capture](https://netlab.tools/netlab/capture/#netlab-capture) for vrnetlab containers
* [Consistent libvirt VM UUID](https://netlab.tools/labs/libvirt/#libvirt-vm-settings) for devices that generate serial number from VM UUID
* Enabling DHCP for all hosts connected to a link or VLAN with the [**dhcp.client** link attribute](https://netlab.tools/module/dhcp/#dhcp-parameters-link)
* Enable or disable VRRP [on individual interfaces](https://netlab.tools/module/gateway/#gateway-intf)
* Node-level **gateway** parameters to set per-node VRRP priority
* Changing [the containerlab ‘prefix’ attribute](https://netlab.tools/labs/clab/#clab-prefix) to change container names
* Support for the [**clab.dns** attribute](https://netlab.tools/labs/clab/#clab-other-parameters) to set container DNS servers and search domain settings
* [Alternate loopback pools](https://netlab.tools/nodes/#node-loopback) make implementing a multi-site loopback addressing scheme easier.
* The [**check.config** plugin](https://netlab.tools/plugins/check.config/#plugin-check-config) removes missing custom configuration templates from lab devices, preventing crashes in Ansible playbooks.

### Upgrading or Starting from Scratch?

* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
