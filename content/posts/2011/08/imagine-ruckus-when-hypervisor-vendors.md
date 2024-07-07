---
date: 2011-08-03 06:33:00.002000+02:00
tags:
- bridging
- data center
- TRILL
- virtualization
title: Imagine the Ruckus When the Hypervisor Vendors Wake Up
url: /2011/08/imagine-ruckus-when-hypervisor-vendors/
---
It seems that most networking vendors consider the Flat Earth architectures the new bonanza. Everyone is running to join the gold rush, from Cisco's FabricPath and Brocade's VCS to HP's IRF and Juniper's upcoming QFabric. As always, the standardization bodies are following the industry with a [large buffet of standards](/2010/08/how-many-large-scale-bridging-standards/) to choose from: [TRILL](/2010/07/why-is-trill-not-routing-at-layer-2/), 802.1ag (SPB), [802.1Qbg (EVB)](/2011/05/edge-virtual-bridging-evb-8021qbg-eases/) and [802.1bh (Port extenders)](/2011/06/vn-tag8021qbh-basics/).
<!--more-->
The only viable argument the whole industry has for the push toward large(r) layer-2 domains is [VM mobility](/2010/09/vmotion-elephant-in-data-center-room/) -- if you want to migrate a live virtual machine across the data center and retain its sessions, it has to stay in the same VLAN due to simplistic virtual switches offered by hypervisor vendors (be it VMware, Microsoft, Citrix or open-source community) and [lack of session layer in the TCP/IP stack](/2009/08/what-went-wrong-tcpip-lacks-session/).

Imagine one of the hypervisor vendors eventually wakes up, [realizes a server has two external connections](/2011/07/vsphere-50-new-networking-features/) (storage *and* network), and delivers [IP-over-IP](http://searchtelecom.techtarget.com/tip/How-to-build-a-scalable-IaaS-cloud-network-infrastructure) or [MAC-over-IP](/2011/06/vcider-climbing-virtual-networking/) connectivity ([MPLS](/2011/05/complexity-belongs-to-network-edge/), mGRE with NHRP or even [LISP](/2011/06/inter-dc-ip-based-vmotion-with-lisp/) would be better due to easy integration with existing hardware devices, but most vSwitch vendors would probably want to avoid any control plane investment).

All of a sudden, all we need in the Data Center is layer-3 connectivity designed and implemented using the same mechanisms we've been using for the last 30 years to build the (somewhat scalable) Internet. The only reason for the layer-2 gold rush is gone.

### My Wild Speculations

I'm guessing that most vendors have already seen the writing on the wall. Glacial progress of 802.1Qbg and the (so far) [empty promises of EVB support](http://www.juniper.fr/us/en/local/pdf/whitepapers/standardizing-datacenter-server-network.pdf) we hear from some vendors would certainly indicate that.

TRILL seems to be completed, but nobody has implemented it yet (although I'm positive HP will follow through on its promises now that the standards are ratified). The only two jumping on the TRILL-ish bandwagon so far are Cisco and Brocade, each one with a proprietary implementation (FabricPath and [VCS Fabric](/2011/03/dont-lie-about-proprietary-protocols/)).

[802.1aq](http://packetpushers.net/case-shortest-path-bridging-802-1aq-spb/) seems to be in a slightly better shape, but then it addresses a number of Service Provider problems as well, so it's worth implementing just to get rid of the Spanning Tree Protocol in your SP-focused gear.

In the end, it will be interesting to see how many of the promised flat-earth features will eventually get implemented, particularly by those vendors that don't invest much in R&D.
