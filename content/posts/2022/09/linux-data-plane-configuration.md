---
cli_tag: fail
date: 2022-09-21 06:20:00+00:00
series:
- cli
series_weight: 300
tags:
- networking fundamentals
- Cumulus Linux
title: Linux Networking Data Plane Configuration
---
I spent a rainy day [implementing VLANs, VRFs, and VXLAN on Cumulus Linux VX](/2022/09/netlab-1-3-1/) and came to "appreciate" the beauties of Linux networking configuration.

**TL&DR**: It sucks

There are two major ways of configuring data plane constructs (interfaces, port channels, VLANs, VRFs) on Linux:
<!--more-->
* Use various CLI commands to add links, create bridges, make devices masters of other devices[^DEV] (that's how you put a device into a port channel or VRF), or set up protocols like STP.
* Use an intent-based system like _ifupdown_ that takes a text configuration from `/etc/network/interfaces`, reads the current system state and adjusts the system state to be close to the administrator's intent.

[^DEV]: Everything is a device on Linux -- physical interface, VLAN subinterface,  port channel, bridge, VLAN interface, VRF, tunnel, loopback... You get the idea ;)

You don't want to use the CLI commands to manipulate network devices; it's a highway to [CRUD hell](/2018/09/infrastructure-as-code-netconf-and-rest.html#crud-hell) and really hard to do right if you want to build idempotent configuration scripts (scripts that won't crash and burn if you run them more than once). If you treasure your sanity, an intent-based system is the only way to go.

To make matters even more interesting, you can choose among a plethora of intent-based systems, all solving the same problem in slightly different ways. Focusing on Cumulus Linux made my life easier: it uses an improved version of *[ifupdown](https://manpages.ubuntu.com/manpages/bionic/man5/interfaces.5.html)* that knows how to handle the newer networking constructs like VRFs.

As [expected from a Linux system utility](/2020/09/grasping-linux-networking/), the documentation sucks. While the _ifupdown_ documentation does a great job explaining the basics, once you try to configure bridges, VXLAN interfaces, or VRFs, you get into a maze of underdocumented commands, some mentioned only in the source code on GitHub. Fortunately, the Cumulus Linux documentation always describes multiple ways of configuring Linux networking objects, giving me at least some hints of what I should be searching for.

Next problem: _netlab_ [cannot build an aggregate configuration file](/2020/12/ansible-config-sections/). It uses a system of [configurable modules](https://netlab.tools/module-reference/) (each implementing a technology or a protocol) and plugins, and every one of those could modify any part of the device configuration. For example:

* The initial setup creates interfaces and assigns IP addresses to them
* The VLAN module creates bridges and adds access and trunk VLANs to interfaces
* The VRF module creates VRFs and makes them masters of other devices (bridges or interfaces)
* The VXLAN module creates VXLAN tunnels and makes them part of the system bridge.

Each of the data plane *netlab* modules thus modifies objects already created or configured by other modules -- a trivial exercise when dealing with a traditional network device that can add new configuration commands to an existing configuration. Doing that when trying to build a single text file quickly becomes a Mission Impossible.

Fortunately, *ifupdown* supports multiple configuration files and can even combine the desired state for a single interface from numerous entries spread across those files. It looked like a perfect fit until I hit another snag (this time, most probably related to my Ubuntu installation, as I couldn't reproduce it on a freshly-built VM): trying to reload the state of all devices resulted in a weird error in the DHCP client.

Long story short, I couldn't use `ifreload -a` to adjust the data plane state to the changed intent. I solved that with *ifupdown* classes (look at the *netlab* [configuration scripts](https://github.com/ipspace/netlab/tree/dev/netsim/ansible/templates) if you want to know the dirty details) and discovered all sorts of interesting quirks -- I guess nobody ever tried to put a single device into a half-dozen classes.

### But Wait, It Gets Worse

I thought I figured everything out, created templates using *ifupdown* for physical interfaces, bridges, VLAN interfaces, VLAN subinterfaces, VRFs, and VXLAN interfaces. Everything worked.

Next day, I decided to unify the Cumulus Linux and FRR container BGP configuration[^FRBGP], and found out that the unnumbered EBGP sessions wouldn't start. Fortunately I had to deal with that in the past[^WH1] and knew exactly what the problem was: there was no IPv6 link-local address (LLA) on the interfaces (root cause: I was using an ancient Cumulus Linux container image, everything works with recent images).

As the unnumbered EBGP sessions worked in earlier *netlab* releases, I thought the failure was caused by my rewriting of the interface configuration template.

Hours later I came to the sad conclusion that:

* It's impossible to configure IPv6 LLA with *ifupdown*. Even `iface inet6 auto`  (which would enable SLAAC, but also LLA) doesn't work on Cumulus Linux.
* Changing IPv6 interface parameters in FRR has no impact.
* The only way to enable IPv6 on an interface is \
  `echo 0 >/proc/sys/net/ipv6/conf/_ifname_/disable_ipv6`. WT\*\*???

I hate using three mechanisms to configure a single object (an interface). If anyone knows a better way to enable IPv6 LLA (without a static IPv6 address) on a Linux interface, please write a comment.

Just in case this long rant confused someone: Cumulus Linux ships with IPv6 enabled (but not configured) on all interfaces, so you always get IPv6 link-local addresses, and unnumbered EBGP sessions work.

[^WH1]: Read "I wasted three hours a few weeks ago, so I didn't have to waste them now". Cumulus Linux BGP Unnumbered documentation somehow fails to mention the "you need working IPv6 LLA" detail.

[^FRBGP]: They are both using FRR, so it makes no sense to have two configuration templates doing the same stuff.

### Now What?

To be fair, Cumulus engineers tried to solve the misery I just described with two systems: Network Command Line Utility (NCLU) in Cumulus Linux 4.x and NVIDIA User Experience (NVUE) in Cumulus Linux 5.x. Both of them look great until you hit their limits. The inability to enable IPv6 LLA[^LLAON] on an interface without configuring a static IPv6 address is one of them[^WTM]. No surprise there, they are both tweaking `/etc/network/interfaces` and FRR configuration. In the end, you're forced to go back to the underlying configuration files and tweak system settings.

[^LLAON]: Something you could do on most major network operating systems for ages

[^WTM]: But wait, there's more. I have at least two other rants in the "to-write" queue.

Not good enough? You could try Dell OS10[^LLADell] or VyOS -- they both seem to be riding on top of Linux and use yet another syntax to configure the same networking objects using the same CLI commands or Netlink calls. As Andrew Tanenbaum [said](https://wiki.c2.com/?AndrewTanenbaum):

[^LLADell]: Looking at the *netlab* initial configuration template Stefano Sasso created for Dell OS10, it has the **ipv6 enable** interface configuration command.

> The nice thing about standards is that you have so many to choose from; furthermore, if you do not like any of them, you can just wait for next year's model.

{{<note>}}Some other network operating systems like Arista EOS or Cisco Nexus OS run on top of Linux, but they usually don't use Linux networking objects but deal directly with ASICs.{{</note>}}


