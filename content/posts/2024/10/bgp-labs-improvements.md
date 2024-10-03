---
title: "BGP Labs: Improvements (September 2024)"
date: 2024-10-04 07:59:00+02:00
tags: [ BGP, netlab ]
netlab_tag: ignore
BGP_tag: lab
---
I spent a few days in a beautiful place with suboptimal Internet connectivity. The only thing I could do whenever I got bored (without waiting for the Internet gnomes to hand-carry the packets across the mountain passes) was to fix the [BGP labs](https://bgplabs.net/) on a [Ubuntu VM running on my MacBook Air](https://blog.ipspace.net/2024/03/netlab-bgp-apple-silicon/) (hint: it all works).

Big things first. I added validation to these labs:

* [Use BGP Timers and BFD to Speed Up BGP Convergence](https://bgplabs.net/basic/7-bfd/)
* [EBGP Sessions over IPv6 LLA Interfaces](https://bgplabs.net/basic/d-interface/)
* [MD5 Passwords and GTSM](https://bgplabs.net/basic/6-protect/)
* [Establish an IBGP Session](https://bgplabs.net/ibgp/1-edge/)
* [Build a Transit Network with IBGP](https://bgplabs.net/ibgp/2-transit/)
* [Use BGP Route Reflectors](https://bgplabs.net/ibgp/3-rr/)
* [Using No-Export Community to Filter Transit Routes](https://bgplabs.net/policy/d-no-export/)
<!--more-->
More (behind the scenes) validation goodies: I changed the old validation tests to use the new(er) validation plugin architecture. That made them easier to maintain and will result in better diagnostics once I fix a few additional things in _netlab_ release 1.9.1.

The next thing that has been stuck on my to-do list for way too long: the labs should not rely on router loopback prefixes advertised as IBGP routes. [FRRouting hates that idea](https://blog.ipspace.net/2024/03/frr-ibgp-loopbacks/), forcing me to use an ancient FRRouting version in the lab exercises. As it's bad form to advertise /32 prefixes into BGP anyway, I decided to redo all labs that relied on that feature. Now you can run BGP labs with the latest FRRouting release and get cool stuff like BGP debugging printouts in the vtysh shell.

While cleaning things up, I also removed the old topologies using [custom device configurations](https://netlab.tools/custom-config-templates/) to configure Cumulus Linux devices, giving you more options for the external routers. Most labs now require _netlab_ release 1.6.4. That release has been around for almost a year, and it makes no sense to support older releases.

Finally, as I had to redo most labs with FRRouting containers (I'm not fluent enough in SR Linux; FRRouting is my only option if I want to run labs on a Macbook), I discovered nasty bugs in the [Use BGP Timers and BFD to Speed Up BGP Convergence](https://bgplabs.net/basic/7-bfd/), [Build a Transit Network with IBGP](https://bgplabs.net/ibgp/2-transit/), and [BGP-Free Core in a Transit Network](https://bgplabs.net/challenge/40-mpls-core/) labs. The FRRouting daemons needed to implement the required device configuration were not started, making it (almost) impossible to complete the lab exercise. That should be fixed now; all labs should work with FRRouting containers (apart from the [TCP-AO lab](https://bgplabs.net/basic/9-ao/) where we're probably still waiting for Linux kernel support).

On a personal note, the "missing daemons" bug made me sad. It's been around for at least a year, and nobody reported it. Does that mean that nobody is using the labs, that everyone gave up before getting to IBGP, that nobody is running the labs with GitHub Codespaces (where FRRouting is the best option), or that you simply didn't find it worthwhile to report the bug?