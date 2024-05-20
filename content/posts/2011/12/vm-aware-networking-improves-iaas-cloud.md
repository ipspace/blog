---
date: 2011-12-05 06:26:00+01:00
tags:
- switching
- cloud
- virtualization
title: VM-aware Networking Improves IaaS Cloud Scalability
url: /2011/12/vm-aware-networking-improves-iaas-cloud.html
lastmod: 2024-05-20 17:58:00+02:00
---
In the [*VMware vSwitch -- the baseline of simplicity*](https://blog.ipspace.net/2011/12/vmware-vswitch-baseline-of-simplicity.html) post I described simple layer-2 switches offered by most hypervisor vendors and the scalability challenges you face when trying to build large-scale solutions with them. You can solve at least one of the scalability issues: VM-aware networking solutions available from most data center networking vendors dynamically adjust the list of VLANs on server-to-switch links.
<!--more-->
{{<note warn>}}The blog post was written more than a decade ago. In the meantime, EVB failed miserably, and most vendors stopped talking about automated VLAN provisioning. The kludges they had to implement to work around [VMware's ignorance of networking](https://blog.ipspace.net/2019/10/the-cost-of-disruptiveness-and.html) were probably too brittle.{{</note>}}

### What's the Problem

Let's briefly revisit the problem: vSwitches have almost no control plane. Thus, a vSwitch cannot tell the adjacent physical switches what VLANs it needs to support VMs connected to it. Lacking that information, you have to configure a wide range of VLANs on the server-facing ports on the physical switch to allow the free movement of VMs between the servers (hypervisor hosts).

The following diagram illustrates the problem:

-   Two tenants are running in a vSphere cluster (ESX-A and ESX-B);
-   *Red* tenant is using VLAN 100, *Blue* tenant is using VLAN 200;
-   With the VM distribution shown in the diagram, ESX-A needs access to VLAN 100; ESX-B needs access to VLAN 200.
-   As the networking gear cannot predict how the VMs will move between vSphere hosts, you have to configure both VLANs on all server-facing ports (Ge1/0 on SW-1 and Ge2/3 on SW-2) as well as on all inter-switch links.

The list of VLANs configured on the server-facing ports of the access-layer switches thus commonly includes completely unnecessary VLANs.

{{<figure src="/2011/12/s320-VLANRange.png" caption="Every VLAN is configured on every server-facing port">}}

The wide range of VLANs configured on all server-facing ports causes indiscriminate flooding of broadcasts, multicasts and unknown unicasts to all the servers, even when those packets are not needed by the servers (because the VLAN on which they're flooded is not active in the server). The flooded packets increase the utilization of the server uplinks; their processing (and dropping) also increases the CPU load.

### The "Standard" Solution

[VSI Discovery Protocol (VDP)](https://blog.ipspace.net/2011/05/edge-virtual-bridging-evb-8021qbg-eases.html), part of Edge Virtual Bridging (EVB, 802.1Qbg) would solve that problem, but it's not implemented in any virtual switch. Consequently, there's no support in the physical switches, although [HP](http://h30499.www3.hp.com/hpeb/attachments/hpeb/bladesblog00/130/1/VEPA-EVB%20Industry%20Whitepaper.pdf) and [Force10](https://blog.ipspace.net/2011/04/new-data-center-switches-from-force10.html) keep promising EVB support; HP for more than a year.

The closest we've ever got to a shipping EVB-like product is [Cisco's VM-FEX](https://blog.ipspace.net/2011/08/vm-fex-how-convoluted-can-you-get.html). The Virtual Ethernet Module (VEM) running within the vSphere kernel uses a protocol similar to VDP to communicate its VLAN/interface needs with the UCS manager.

{{<figure src="/2011/12/s320-Lochnessmonster.jpg" href="http://en.wikipedia.org/wiki/Loch_Ness_Monster" caption="More people have seen Nessie than an EVB-compliant vSwitch">}}

{{<note info>}}In the meantime, Force10 got acquired, HP dropped another data center switching line after acquiring Aruba, and VMware stopped supporting third-party virtual switches. None of that stopped vendor marketers from evangelizing the next big thing.{{</note>}}

### The Real-World Workarounds

Faced with the lack of EVB support (or any other similar control-plane protocol) in the vSwitches, the networking vendors implemented a variety of kludges. Some of them were implemented in the access-layer switches (Arista's [VM Tracer](https://blog.ipspace.net/2011/06/automatic-edge-vlan-provisioning-with.html), Force10's HyperLink, Brocade's vCenter Integration), others in network management software (Juniper's Junos Space Virtual Control and ALU's OmniVista Virtual Machine Monitor).

In all cases, a VM-aware solution must first discover the network topology. Almost all solutions send CDP packets from access-layer switches and use CDP[^CDP] listeners in the vSphere hosts to discover host-to-switch connectivity. The CDP information gathered by vSphere hosts is usually extracted from vCenter using VMware's API (yes, you typically have to talk to the vCenter if you want to communicate with the VMware environment).

[^CDP]: Sadly, that's not a typo. VMware included a vendor-proprietary protocol in its low-cost license; you must pay extra for a standard protocol (LLDP).

Have you noticed I mentioned VMware API in the previous paragraph? Because no hypervisor vendor bothered to implement a standard protocol, the networking vendors have to implement a different solution for each hypervisor. Almost all of the VM-aware solutions support vSphere/vCenter, a few vendors claim they also support Xen, KVM, or Hyper-V, and I haven't seen anyone supporting anything beyond the big four.

After the access-layer topology has been discovered, the VM-aware solutions track VM movements between hypervisor hosts and dynamically adjust the VLAN range on access-layer switch ports. Ideally, you'd combine that with MVRP in the network core to trim the VLANs further, but only a few vendors implemented MVRP (and supposedly, only a few customers are using it). [QFabric](https://blog.ipspace.net/search?q=qfabric) is a shining (proprietary) exception: because its architecture mandates [single ingress lookup which should result in a list of egress ports](https://blog.ipspace.net/2011/09/qfabric-part-3-forwarding.html), it also performs optimum VLAN flooding.

{{<note info>}}MVRP became obsolete once we started using VXLAN and EVPN. EVPN automatically builds optimal ingress replication lists based on VLANs configured on edge ports.{{</note>}}

### Does It Matter?

Without VM-aware networking, you must configure every VM-supporting VLAN on every switch-facing port, reducing the whole data center network to a single broadcast domain (effectively a single VLAN from the scalability perspective). If your data center has just a few large VLANs, you probably don't care (most hypervisor hosts have to see most of the flooded VLAN traffic anyway); if you have a large number of small VLANs, VM-aware networking makes perfect sense.

Using the rough estimates from the [RFC 5556 (section 2.6)](http://tools.ietf.org/html/rfc5556#section-2.6), implementing VM-aware networking moves us from *around 1,000 end-hosts in a single bridged LAN* to *100,000 end-hosts inside 1,000 VLANs*. While I wouldn't run 100,000 VMs in a purely bridged environment, the scalability improvements you can gain with VM-aware networking are definitely worth the investment.
