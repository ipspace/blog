---
title: "Configuring Management IP Addresses to Virtual Network Devices"
date: 2026-09-14 07:29:00+0200
tags: [ netlab ]
netlab_tag: details
---
It goes without saying that if you want to configure (virtual) network devices with any semi-sane configuration mechanism[^XCC], the device must have a working IP address. Here's the time-honored method[^ACJ] to assign an IP address to a virtual network device:

* Start the virtual machine (using a GUI)[^BPI]
* Open a new window: either a telnet session to the virtual console port or a full-blown virtual console (GUI) session.
* Manually configure the IP address, the SSH server, and the user credentials on the first interface.
<!--more-->

[^XCC]: Which, by definition, does not include the (virtual) console cable connected to the (virtual) serial port.

[^ACJ]: Adored by the mouse-addicted CLI jockeys

[^BPI]: Bonus points if you boot a CD-ROM (ISO) image and go through a lengthy installation process.

Some networking CLI jockeys[^VWA] still find that the [pinnacle of evolution](/2025/01/common-labbing-misconceptions/). Everyone else (including software developers) realized ages ago that we need something better: consistent, predictable management IP addresses assigned automatically by the orchestration system.

[^VWA]: And VMware administrators managing a few virtual machines

That's easy to do in the pure container world. After all, the container Ethernet interfaces are just [one half of the vEth virtual cable](/2025/02/virtual-lab-links/#docker) residing in a separate namespace, and the host operating system has full access to them. Configuring their IP addresses is trivial. Worst case, use **ip netns exec _container_ ip address add _ip_ dev eth0** (note: the **eth0** device that gets the IP address is within the container namespace).

What about the virtual machines? We use the same IPv4 address assignment mechanism we use elsewhere: DHCPv4; that's why every cloud-ready device image includes a working DHCP client and a default username, or a *cloud-init* client that lets you specify user credentials when creating the virtual machine.

However, most networking devices don't start with a DHCP client configured on their first interface; that's why we have to [build custom Vagrant boxes](/2022/02/netsim-build-vagrant-boxes/) before we can use networking devices with Vagrant or *netlab*. The initial configuration of those custom Vagrant boxes also includes the management VRF, the SSH server, and the user credentials.

{{<note info>}}
Just in case you're wondering how we build those boxes: some networking devices (Junos, ASAv) can read the initial configuration from a virtual CD-ROM attached to the virtual machine. Most devices must be configured through a virtual console session, usually via the venerable virtual console cable connected to the virtual serial port.
{{</note>}}

Things get a tiny bit more interesting in the IPv6 world. Most operating systems have IPv6 enabled by default and use SLAAC to get a working IPv6 address. Unfortunately, most cloud providers that have ever faced a large-enough scaling challenge[^XVM] hate unpredictable dynamic IP addresses and control-plane address-discovery mechanisms. Every large public cloud assigns predictable, preconfigured IPv6 addresses to virtual machines via DHCPv6, including the one built by the company otherwise [engaged in a nonsense](/2021/10/ipv6-multiple-addresses-per-interface/)[^YCMTU] anti-DHCPv6 crusade[^HRP].

[^XVM]: Which, it seems, by definition excludes VMware.

[^HRP]: Sometimes, hard reality prevails over religious considerations, more so if you're the one bearing the costs of your religious beliefs.

[^YCMTU]: Including a *[you can't make this shit up](/2025/09/android-dhcpv6-prefix-delegation/)* twist

So far, so good:

* We can assign IP addresses to container interfaces directly
* We use DHCPv4/DHCPv6 to give IPv4/IPv6 addresses to properly-preconfigured virtual machines.

What about [virtual machines running in containers](/2026/09/running-virtual-machines-in-containers/)? The container orchestration system assigns the IP address to the container interface, and somehow that IP address must get to the VM running inside that container. One could (theoretically) start a DHCP server inside the container and use DHCP to assign an IP address to the VM management interface; the *vrnetlab* project took a different approach: the container initialization script (which also starts the VM) uses a *telnet* session to its loopback interface to reach the virtual serial port of the virtual machine and an equivalent of an *expect* script to:

* Abort the auto-configuration process (if needed)
* Start a console session
* Enter configuration mode
* Download the startup configuration, including the management IP address, the SSH server configuration, and the user credentials.

It looks like we truly cannot escape the curse of the virtual console cable 🤦‍♂️