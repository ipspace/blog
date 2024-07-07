---
date: 2012-02-09 08:40:00+01:00
tags:
- SDN
- OpenFlow
- overlay networks
- virtualization
title: Nicira Open vSwitch Inside vSphere/ESX
url: /2012/02/nicira-open-vswitch-inside-vsphereesx/
---
I got intrigued when reading [Nicira's white paper](http://www.nicira.com/en/network-virtualization-platform) claiming their Open vSwitch can run within vSphere/ESX hypervisor. There are three APIs that you could use to get that job done: [dvFilter API](http://blogs.vmware.com/vcloud/2010/04/what-actually-is-vmsafe-and-the-vmsafe-api.html) (intercepting VM NIC like [vCDNI](/2011/04/vcloud-director-networking/) does), the undocumented virtual switch API used by Cisco's Nexus 1000v, or the device driver interface (intercepting uplink traffic). Turns out Nicira decided to use a fourth approach using nothing but publicly available APIs.
<!--more-->
{{<figure src="/2012/02/s1600-Nicira-ESX-API.png" caption="Available ESX APIs">}}

### How relevant is this?

This blog post was written in 2012 (more than 8 years ago). In the meantime Nicira got acquired by VMware resulting in an interesting virtual switching journey:

* The original product was renamed to NSX Multi-Hypervisor and used Open vSwitch.
* NSX on VMware used VMware VDS with NSX controller as VXLAN control plane.
* NSX-T (the Grand Unifying Theory of NSX) uses a different virtual switch on ESX -- the N-VDS... until vSphere release 7 where NSX-T runs yet again on VDS 7.
* In the meantime, NSX-T on Linux uses Open vSwitch with extensions.

In short, it's an interesting mess. For more details, watch the [NSX Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive) webinar.

Meanwhile, VMware discontinued the networking API used by Cisco's Nexus 1000v (which got EOLed) and so Cisco is back to using the same tricks Nicira used 8 years ago to implement ACI virtual switch on vSphere. RFC 1925 rule 11 at its best.

### Back to Nicira...

As I wrote in the [update to the Nicira Uncloaked post](/2012/02/nicira-uncloaked/), the cool trick they used relies on a few obscure properties of the Distributed vSwitch (vDS) and statically bound Distributed Ports. Let me show you how it actually works step-by-step (if you don't want to spoil the magic, stop reading right now)\... but before starting the journey, remember where we want to end: we want to have virtual machines connected to Open vSwitch, which uses the *transport network* (VLAN tags or MAC-over-GRE tunneling) to [build virtual networks as dictated by the OpenFlow controller](/2011/10/what-is-nicira-really-up-to/) (Nicira's Network Virtualization Platform -- NVP).

{{<figure src="/2012/02/s1600-Nicira-ESX-Goal.png" caption="High-level overview of the problem they were trying to solve">}}

{{<note>}}This blog post focuses on the intra-vSphere part of the solution. For more details on the \"transport\" part (which I left cloudy for a reason), read my other OpenFlow/Nicira blog posts, for example [*What is Nicira really up to*](/2011/10/what-is-nicira-really-up-to/) and [*Decouple virtual networking from the physical world*](/2011/12/decouple-virtual-networking-from/). TL&DR summary for the differently attentive: the \"transport\" cloud is almost \"NVGRE/VXLAN with a centralized control plane\".{{</note>}}

Start with a distributed switch (vDS). It seems like it spans across a number of hosts, but that's just the management-plane perception; in reality, every vSphere host has an independent forwarding component.

{{<figure src="/2012/02/s1600-Nicira-ESX-VDS-Transport.png" caption="VMware VDS overview">}}

Now imagine you have a vDS (or a port group within a vDS) with no uplinks. It seems to span across numerous ESX hosts, you can vMotion VMs between the hosts, but only the VMs inside the same host can actually communicate.

Next, start an Open vSwitch-hosting VM in every ESX host and connect it to the isolated port group as well as the outside transport network (another port group). The traffic between VMs connected to the isolated port group and the outside world has to pass through the OVS VM, and since there is no other way for the isolated VMs to reach the outside world, there can be no forwarding loops.

{{<figure src="/2012/02/s1600-Nicira-ESX-OVS-Transport.png" caption="Open vSwitch inserted into a VDS port group">}}

Still, the VMs connected to the same port group can communicate with each other. We need another trick -- the per-port properties of statically bound Distributed Ports. If you use vDS, you can set numerous properties on individual ports (VM NICs), *including access VLAN*. Yes, you can run multiple VLANs *within a single port group.* Mindboggling. I never realized you could do that.

So this is what you do:

-   For every single VM connected to the port group, use *Virtual Switch Tagging* and set the access VLAN to a unique value (this does limit the number of VMs you can connect to the same port group to 409x, but that should be more than enough).
-   Configure the port connecting the OVS VM to the isolated port group to *Virtual Guest Tagging* and allow *promiscuous mode*.

The OVS VM will receive all traffic generated by the VMs, nicely tagged with per-VM VLAN tags.

{{<figure src="/2012/02/s1600-Nicira-ESX-VLAN.png" caption="Each VM uses a different VLAN tag to reach the Open vSwitch inside a VDS port group">}}

Finally, let's take a look deeper into the OVS VM. It needs three interfaces: VM-facing interface, transport interface (where it can use VLAN tags or MAC-over-GRE tunneling to send traffic between OVS switches), and management interface (over which it communicates with the NVP OpenFlow controller).

The VM-facing interface appears as a physical interface to Linux running inside the VM; you can create VLAN subinterfaces on top of it (one per VM) and connect individual subinterfaces (point-to-point VLAN-tagged links to individual VMs) to OVS ports.

{{<figure src="/2012/02/s1600-Nicira-ESX-Inside-VM.png" caption="A looking inside the OVS virtual machine">}}

### Does this make sense?

The switch-inside-a-VM solution has two obvious drawbacks:

-   The Open vSwitch VM becomes a single point of failure (but let's [handwave](http://tvtropes.org/pmwiki/pmwiki.php/Main/HandWave) that away -- after all, [every SPOF can be removed with High Availability](/2011/08/high-availability-fallacies/)).
-   All the inter-VM traffic has to pass through the OVS VM, which [becomes a performance bottleneck](/2011/10/what-is-nicira-really-up-to/) (you can't push more than a few Gbps through [userland](http://en.wikipedia.org/wiki/User_space)).

Does such a kludge make sense? It just might in (at least) three scenarios:

-   It enables a gradual migration from VMware environment to Xen/KVM/OpenStack.
-   It allows you to connect VMs that have to run on VMware for whatever reason to Xen/OpenStack/Quantum non-VLAN virtual networks (people [complaining about VLAN limits in certain data center switches](http://www.network-janitor.net/2011/08/wholesale-virtualisation-and-selective-qinq/) might appreciate this).
-   It makes for a nice test bed. You can test OpenFlow/OVS/NVP without fully committing to a Linux-based hypervisor.

## More information

If you're faced with the question "*what is this virtual network stuff all about?*" the [*Introduction to Virtual Networking*](http://www.ipspace.net/VMintro) webinar might give you the answers you need. [*VMware Networking Deep Dive*](http://www.ipspace.net/VMware_Networking_Deep_Dive) webinar describes distributed switches, port groups, dvFilter API and virtual appliances; the [*Cloud Computing Networking*](http://www.ipspace.net/Cloud_Computing_Networking:_Under_the_Hood) one focuses on large-scale virtual networks needed in IaaS clouds. You get immediate access to all three webinars (and a dozen more) with the [yearly subscription](http://www.ipspace.net/Subscription).
