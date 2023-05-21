---
title: "MTU Settings in Virtual Network Devices"
date: 2022-01-27 09:34:00
tags: [ virtualization, Cumulus Linux ]
---
When I finally[^1] managed to get SR Linux running with *netlab*, I wanted to test how it interacts with Cumulus VX and FRR in an OSPF+BGP lab... and failed. [Jeroen Van Bemmel](https://github.com/jbemmel) quickly identified the culprit: MTU. Yeah, it's always the MTU (or DNS, or BGP).

I never experienced a similar problem, so of course I had to identify the root cause:
<!--more-->
* There is no standard mechanism to pass network MTU to physical Ethernet NICs. Most everyone therefore uses 1500 bytes as the default MTU[^CL].
* Traditional network operating systems (Cisco IOS) have their opinions baked into the source code.
* Linux-based virtual devices might inherit the MTU from whatever Linux kernel thinks is a good idea.
* While the emulated "traditional" NICs (example: the venerable E1000 NIC used by Nexus OS) have no opinion about the correct MTU size, paravirtual drivers (at least [virtio](https://docs.oasis-open.org/virtio/virtio/v1.1/virtio-v1.1.html) -- see *feature bits*) have an option of passing the MTU size from the hypervisor to the guest device driver (and thus the operating system), and libvirt has an option of [setting MTU size](https://libvirt.org/formatdomain.html#mtu-configuration) in VM definition file (domain XML file). Is anyone using it? Is it possible to configure VM MTU size that way? I have no idea, comments welcome.
* Container-based solutions inherit the interfaces from the container orchestration system. Those interfaces have whatever MTU the container orchestration system found appropriate.

[^CL]: Cumulus Linux [changed the default MTU to 9216](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-42/Layer-1-and-Switch-Ports/Interface-Configuration-and-Management/Switch-Port-Attributes/) in release 4.2

In our particular case, Cumulus VX and FRR running in containers had MTU set to 9500 while SR Linux had its MTU set to 1500 -- Jeroen had to configure lower MTU  to get SR Linux to work with SR OS.

Next question: why would SR Linux and SR OS have a different default MTU sizes? SR Linux is a real container while SR OS is not available in container format (as of January 2022); what you're running in *containerlab* is really a VM packaged in a container file together with QEMU ([see vrnetlab for details](https://github.com/vrnetlab/vrnetlab)). As a VM, SR OS uses the Ethernet default MTU size (1500) while SR Linux uses whatever the container orchestration system (*containerlab* in my case) sets us, and it happens to be 9500.

Finally, where did the high default MTU come from? It's not Linux default, and it's definitely not set that way in other container orchestration systems like Docker. Turns out that *containerlab* [sets the MTU to 9500](https://containerlab.srlinux.dev/manual/network/#point-to-point-links) on vEth links. Mystery solved ;)

So how did we get Cumulus VX and SR Linux to work together? We had to implement MTU parameter (on interface, link, node, and lab level) in *netlab*, and set the default to 1500 for container-based network devices.

## Keep Exploring

* The virtual networking fundamentals are covered in _[Introduction to Virtualized Networking](https://www.ipspace.net/Introduction_to_Virtualized_Networking)_ webinar.
* To learn how containers work behind the scenes, watch _[Introduction to Docker](https://www.ipspace.net/Introduction_to_Docker)_ and _[Docker Networking Deep Dive](https://www.ipspace.net/Docker_Networking_Deep_Dive)_ webinars. They do focus on Docker, but they also explain the namespace concepts and virtual Ethernet links used by almost any container orchestration system.
* Ready for a large glob of complexity? Enjoy the _[Kubernetes Networking Deep Dive](https://www.ipspace.net/Kubernetes_Networking_Deep_Dive)_.

[^1]: I struggled with an old version of an Ansible collection; Jeroen has published [detailed installation instructions](https://netlab.tools/caveats/#nokia-sr-linux) in the meantime.