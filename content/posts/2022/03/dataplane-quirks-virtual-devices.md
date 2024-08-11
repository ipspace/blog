---
title: "Data Plane Quirks in Virtual Network Devices"
date: 2022-03-03 07:48:00
tags: [ NFV ]
lastmod: 2022-03-09 07:44:00
---
Have you noticed an [interesting twist in the ICMP Redirects saga](/2022/02/nexus-icmp-redirects/): operating systems of some network devices might install redirect entries and use them for control plane traffic -- an interesting implementation side effect of the architecture of most modern network devices.

A large majority of network devices run on some variant of Linux or \*BSD operating system, the only true exception being ancient operating systems like Cisco IOS[^XE]. The network daemons populate various routing protocol tables and compute the best routes that somehow get merged into a single routing table *that might still be just a data structure in some user-mode process*.
<!--more-->
{{<note info>}}The blog post was augmented with extensive feedback from [Béla Várkonyi](https://www.linkedin.com/in/belavarkonyi/). Thanks a million Béla!{{</note>}}

What happens next depends on the network operating system implementation (you might watch the excellent _[Network Operating System Models](https://www.ipspace.net/Network_Operating_System_Models)_ webinar for more details). Some solutions (example: Cumulus Linux) copy the computed forwarding table (FIB) into the Linux routing table and use the Linux routing table as the source-of-truth to set up the ASIC (hardware forwarding) tables. Other solutions (example: Arista EOS) program the ASIC directly and insert just enough information into the Linux routing table to make the control plane work. There's nothing wrong with either approach... until you're trying to figure out how your network is going to behave by setting up its digital twin[^BS] in a virtual lab.

[^XE]: Cisco IOS XE is an interesting hybrid running Cisco IOS control plane as a single process on top of the Linux kernel. Packet forwarding is implemented in dedicated CPU cores (ISR 4000, CSR 1000v) or in ASICs (ASR 900, Catalyst).

[^BS]: I know that's another bullshit-bingo-winning nonsense, but you have to admit it sounds cool ;)

Here's what you might experience when doing that:

* Load balancers and firewalls are usually using software-based packet forwarding. There's usually no difference between running them in a sheet metal envelope or as a VM.
* Low-end routers with CPU-based packet forwarding should behave the same way when ran as a VM... unless they're using hardware offload in which case you might experience a difference between hardware- and software implementation. I found absolutely no difference between Cisco IOS running on a low-end router and Cisco IOS running as a VM, and CSR 1000v was designed to be used as a VM anyway. Would CSR 1000v behave in exactly the same way as ISR 4000 routers? Probably not.
* IOS XR has two simulation images, one focusing on control plane functionality (route reflector), the other one with a full data plane that is nonetheless significantly different from the hardware implementation ([source](#1073)). I still have no idea what Juniper vMX is doing apart from the obvious fact that it's implemented as two virtual machines (control-plane VM and data-plane VM). Insightful comments are most welcome.
* Data center switches ran as virtual devices usually use Linux kernel for packet forwarding -- after all, these virtual machines are not meant to be a replacement for the actual switches. Some implementations might behave similarly to their physical counterparts, others show significant deviation from what you might expect. For example, I couldn't get [ECMP load balancing to work](/2021/11/anycast-mpls/) with vEOS or cEOS.

Don't get me wrong: there's nothing wrong with virtual machines not implementing all the intricacies of the hardware data plane when they are supposed to be used for control-plane tests or validation... but you have to understand the limitations. You cannot expect to be able to fully validate network operation after a configuration change in a virtual lab if you cannot emulate all data plane functionality.

### Containers Are Even More Interesting

Some vendors provide virtual versions of their network operating systems in container format. You SHOULD NOT use them for anything more than control-plane functionality. Here are just a few minor details we found so far:

* The last time I tested Juniper cRPD it couldn't report its interfaces, making it impossible to use Ansible to configure it.
* It's pretty much impossible to load a kernel module within a container. For example, Cumulus implementation of MLAG does not work in a container due to a custom **bridge** kernel module. Michael Kashin solved that problem by [packing a Firecracker VM into a container](https://networkop.co.uk/post/2021-05-cumulus-ignite/). While that approach solves the data plane issues, it loses most benefits we could get from containerized network devices like a single copy of Linux or shared code/memory.

### Revision History

### Revision History

2024-08-10
: MPLS data plane works in cEOS release 4.32.1F and is supported in _netlab_ release 1.9.0. Removed a mention of that limitation.

2022-03-09
: Added a few container quirks.

2022-03-04
: Added the details provided by [Béla Várkonyi](https://www.linkedin.com/in/belavarkonyi/)
