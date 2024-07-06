---
date: 2011-11-10 16:45:00+01:00
tags:
- security
- virtualization
title: Juniper’s Virtual Gateway – a Virtual Firewall Done Right
url: /2011/11/junipers-virtual-gateway-virtual.html
---
{{<note warn>}}VMsafe Network API is obsolete, which made Juniper's Virtual Gateway obsolete (EOL: 2016). This blog post thus has only historical value documenting different architectural approaches. For up-to-date information on firewall service insertion in vSphere environments watch *[Firewalling and Security](https://my.ipspace.net/bin/list?id=NSX#FW)* section of the _[VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)_ webinar.{{</note>}}

I stumbled upon VMsafe Network API (the API formerly known as dvFilter) while developing my [VMware Networking Deep Dive](https://www.ipspace.net/VMnet) webinar, set up the vShield App 4.1 in a lab, figured out how it works (including a few caveats), and assumed that's how most virtual firewalls using dvFilter work. Boy was I wrong!
<!--more-->
{{<note update>}}**Update 2014-02-09:** Virtual Gateway has been renamed to Firefly Host and stopped working with vSphere 5.5 which no longer contains the deprecated VMsafe API used by Virtual Gateway/Firefly Host.{{</note>}}

Basics first: the VMsafe Network API is an API within the ESX hypervisor kernel that allows a third party to insert a filter (a loadable kernel module) in front of the virtual NICs (the filters are automatically configured in the VMX file). The filter can do anything it wants with the VM traffic; including modifying or encapsulating it ([vCDNI](/2011/04/vcloud-director-networking.html) is implemented as a dvFilter kernel module).

{{<figure src="/2011/11/s320-VGW_kernel.png" caption="dvFilter in an ESXi Host">}}

In most cases, the loadable kernel module interacts with a VM that configures it (vCDNI is an exception; when implemented within the vCloud Director framework, it works without a VM). The communication between the kernel module and the controller VM must be protected from prying eyes (remember: we're implementing virtual firewalls), so it goes through a hidden vSwitch.

{{<figure src="/2011/11/s320-VGW_full.png" caption="Typical Use of dvFilter API">}}

The controller VM thus has to run in the same vSphere host as the kernel module. You got that right: one extra VM per vSphere host. On top of that, every virtual firewall product usually has a management VM that pushes the configuration to controller VMs running in individual vSphere hosts.

### What\'s the Difference?

As always, the devil is in the details. vSphere Zones/App 4.1 (and a number of other products) uses *Slow Path* -- every single packet sent or received by protected VMs goes through the vSphere Zones firewall VM (a Linux VM using iptables/ebtables with a GUI front-end).

Not only that, you can't protect just a few VMs in a vSphere host. Once you load vSphere Zones kernel module into the ESX kernel, traffic from all VMs has to pass through the firewall VM -- the moment you start or vMotion a VM to a vSphere host running vShield Zones/App, the dvFilter configuration appears in the VMX file.

{{<figure src="/2011/11/s320-VGW_SlowPath.png" caption="Virtual Gateway slow path">}}

The above description applies to vShield Zones/App 4.1. [vShield 5.0 release notes](http://www.vmware.com/support/vshield/doc/releasenotes_vshield_50.html) mention "*improved performance due to architectural improvements*". I wasn't able to test vShield 5.0 yet; if you know more, please write a comment.

Juniper's Virtual Gateway uses a completely different approach. It still needs per-host firewall VM, but uses it only for configuration and logging purposes. All the traffic filtering is performed in the module loaded in the hypervisor kernel (*Fast Path*). Not only that, you can specify which VMs or portgroups are protected, further reducing the CPU overhead.

{{<figure src="/2011/11/s320-VGW_FastPath.png"  caption="Virtual Gateway fast path">}}

The performance difference between different virtual firewall products is astounding: while Slow Path-based solutions top out at approximately 3-4 Gbps (which is very close to the results I got with my vShield Zones 4.1 tests), Juniper's Virtual Gateway reduces the overall throughput by only around 10% (they pushed 30 Gbps through an ESX host in the tests).

Even more, VM-based virtual firewalls are CPU bound (the 3-4 Gbps is what you can squeeze out of a single vCPU), while Juniper's firewall, running within the hypervisor kernel, uses multiple cores assigned to the protected VMs. Pushing the performance even further, Virtual Gateway uses per-VM connection tables and rulesets.

