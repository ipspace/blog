---
title: "Networking Hardware/Software Disaggregation in 2022"
date: 2022-05-16 06:36:00
tags: [ SDN ]
---
I started preparing the materials for the _SDN -- 10 years later_ webinar, and plan to publish a series of blog posts documenting what I found on various aspects of what could be considered SDN[^SDN]. I'm pretty sure I missed quite a few things; your comments are most welcome.

Let's start with an easy one: software/hardware disaggregation in network devices. 

### Open-Source Network Operating Systems

I found several widely-used open-source[^OS] network operating systems:
<!--more-->
[^OS]: Using whatever definition of _open_. ASIC device drivers are often shipping as a binary blob.

[^SDN]: There's no need to argue what SDN means, we all know it means _Still Don't Know_.

* Cumulus Linux
* Dell OS10 (seems to be a successor of Force10 FTOS)
* VyOS
* [SONiC](https://en.wikipedia.org/wiki/SONiC_(operating_system))

It seems that most of these systems run on a variety of switches from whitebox- and traditional data center switching vendors.

Then there are things likes [FBOSS](https://github.com/facebook/fboss). Is anyone (apart from their creator) using them? I have no idea.

### Linux Device Drivers

You need at least two software components to glue a network operating system to the hardware[^SW]:

[^SW]: Assuming we're dealing with a platform that uses an ASIC for hardware-based packet forwarding

* ASIC driver (sometimes called *abstraction layer*)
* Platform drivers (something to control the fans, front-panel LEDs...)

There are two competing approaches to ASIC device drivers:

* [Switch Abstraction Interface](https://www.opencompute.org/documents/switch-abstraction-interface-ocp-specification-v0-2-pdf) (SAI) -- standardized ASIC programming API embraced by Open Compute Project (OCP)
* [switchdev](https://www.kernel.org/doc/html/latest/networking/switchdev.html) -- a Linux kernel API that offloads data plane processing from Linux kernel to an ASIC.

{{<note info>}}Want to know what's the difference between SAI and switchdev? Dinesh Dutt covered this topic in the _[Network Operating System Models](https://www.ipspace.net/Network_Operating_System_Models)_ webinar.{{</note>}}

[Open Network Linux (ONL)](https://github.com/opencomputeproject/OpenNetworkLinux) includes a large number of *platform* drivers.

Finally, there's [Stratum](https://opennetworking.org/stratum/) from Open Networking Foundation. If I got it right, ONF dropped OpenFlow and focused on P4, which works best on ASICs with flexible forwarding pipeline like the Barefoot/Intel Tofino ASIC[^P4B]. No wonder the majority of the Technical Steering Team members work for Intel.

[^P4B]: Even though I found a presentation claiming [you can use P4 to program switches with fixed forwarding pipeline](https://opennetworking.org/wp-content/uploads/2019/09/3.30pm-Max-Pudelko-Stratum-FPM-Compiler.pdf). On a totally unrelated topic, you can also run Unix on PDP-11 emulated in JavaScript.

### Open-Source Operating Systems on Hardware from Traditional Vendors

Most of the traditional data center switching vendors had to [support SONiC](https://github.com/sonic-net/SONiC/wiki/Supported-Devices-and-Platforms) or offer SAI interface on their hardware, or they wouldn't be able to sell their boxes to hyperscalers (or at least Microsoft):

* Arista supports SONiC on a wide variety of switches using Tomahawk[^TH], Trident[^TD], Jericho[^JR], or Tofino[^TF] chipsets.
* Dell supports SONiC on switches using Tomahawk and Trident chipsets.
* Juniper supports SONiC on two spine switches using Tomahawk chipset.
* Cisco supports [SAI on some Nexus 9200 and Nexus 9300 switches](https://blogs.cisco.com/datacenter/new-portability-options-for-ciscos-data-center-networking), which means you can run SONiC on them. They also support [SONiC on Cisco 8000 routers](https://blogs.cisco.com/sp/cisco-goes-sonic-on-cisco-8000).

[^TH]: High-speed Broadcom ASIC used on spine switches

[^TD]: Feature-rich Broadcom ASIC used on leaf switches

[^JR]: Broadcom ASIC with large buffers and forwarding tables

[^TF]: Barefoot (now Intel) ASIC with programmable forwarding pipeline and P4 support.

### Proprietary Network Operating Systems on Whitebox Hardware

The previous section should have made it abundantly clear that traditional networking vendors don't mind selling _disaggregated_ hardware (without their software) to large customers. Are they also willing to sell their software to run on third-party hardware? You bet:

* You could run [Cisco IOS-XR on third-party hardware](https://xrdocs.io/cloud-scale-networking/blogs/2018-03-08-enabling-ios-xr-on-third-party-network-hardware/)
* Juniper is talking about _disaggregated Junos_, but all I could find was a [way to run Junos VM on their NFX150 CPE platform](https://www.juniper.net/documentation/us/en/software/junos/nfx150-getting-started/topics/topic-map/nfx150-overview.html), and a datasheet [claiming you can run Junos on a single Accton Edgecore switch](https://www.juniper.net/assets/us/en/local/pdf/datasheets/1000641-en.pdf).
* Supposedly you could run Arista cEOS (EOS in a container) on third-party whitebox switches. Based on my [recent cEOS experience](https://blog.ipspace.net/2022/03/dataplane-quirks-virtual-devices.html) I have to wonder how much functionality you'd get beyond the basic L2+L3 forwarding. The only other reasonable hit I got for "Arista EOS whitebox" was a pointer to my [2015 April 1st blog post](https://blog.ipspace.net/2015/04/arista-eos-available-on-whitebox.html).

Then there's a plethora of niche vendors offering their network operating systems on whitebox hardware, including Arrcus (ArcOS), IP Infusion (OcNOS), Pluribus, and RtBrick.

Have I missed something? Your comments (preferably including links to documentation) would be most welcome.
