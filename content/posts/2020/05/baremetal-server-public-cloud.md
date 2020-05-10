---
title: "Do We Need Bare Metal Servers in Public and Private Clouds?"
date: 2020-05-13 06:33:00
tags: [ cloud, design, data center ]
---
Whenever I was [comparing VMware NSX and Cisco ACI](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN) a few years ago (in late 2010s in case you're reading this in a far-away future), someone would inevitably ask "_and how would you connect a [bare metal server](https://en.wikipedia.org/wiki/Bare-metal_server) to a VMware NSX environment?_"

While [NSX-T has that capability since release 2.5](https://my.ipspace.net/bin/get/NSX/1.1A%20-%20NSX%20Data%20Center%20Products.mp4?doccode=NSX) (more about that in a later blog post), let's start with the big question: why would you need to?
<!--more-->
Hardware-assisted server virtualization came a very long way since the early days of VMware ESX, and [paravirtualization](https://en.wikipedia.org/wiki/Paravirtualization) significantly reduced the impact of virtualization on I/O operations &ndash; the last figures I've seen claimed that _virtualization tax_ (performance drop when running on a hypervisor) dropped to a few percent. Combine that with the increased flexibility server virtualization gives you like on-the-fly ability to increase resources available to a VM, or migrate a running instance to another physical server, and one has to wonder why we're still so obsessed with owning or renting physical servers.

{{<note info>}}One of my public cloud provider customers told me years ago that they decided to run a single VM on a dedicated hypervisor host whenever their tenants would ask for a bare metal server. The ability to add RAM or CPU cores, or to migrate the tenant VM to another physical server for maintenance or upgrade reasons was way more valuable than virtualization-related loss of performance.{{</note>}}

I could find just a few reasons that could justify bare metal servers:

* **Licensing limitations** - if you're forced to deal with a software company that wants to charge you for any CPU socket their software _could potentially run on till the heat death of the universe_, you better [get rid of that software](https://aws.amazon.com/blogs/aws/migration-complete-amazons-consumer-business-just-turned-off-its-final-oracle-database/), or run it in a way where even their lawyers couldn't dream up a reason to charge you more.
* **Nested virtualization** - You want to run your own hypervisor, and need some functionality that cannot be provided with [hardware-assisted virtualization](https://en.wikipedia.org/wiki/X86_virtualization#Hardware-assisted_virtualization)... or you want to run nested virtualization yourself (hint: hardware is usually not able to implement [turtles-all-the-way-down designs](https://en.wikipedia.org/wiki/Turtles_all_the_way_down)).
* **Very high I/O performance** - While I haven't heard anyone complaining (too much) about the impact of virtualization on CPU performance (assuming a single-VM environment with no noisy neighbors and a CPU core dedicated to the hypervisor), software implementation of I/O operations could pose an interesting challenge. For example, no-one sane would run High-Frequency Trading applications on top of virtual switches.
* **Security** - Hypervisor exploits remain a recurring nightmare of some security practitioners... although the impacts of those hypothetical exploits are greatly reduced if you're running a single VM on a hypervisor host.
* **Mindset** - There's nothing better than the warm and fuzzy feeling of having your own server... even if it's just one of many sitting in a data center at an undisclosed location.
* **Marketing** - Your architecture (or a kludge implemented for some other customer) supports bare metal servers... and of course you start seeing them everywhere.

Have I missed anything? Please write a comment...