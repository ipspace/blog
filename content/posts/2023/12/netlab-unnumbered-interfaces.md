---
title: "Review: Unnumbered Interfaces in netlab"
date: 2023-12-18 08:23:00+0100
series: unnumbered-interfaces
tags: [ netlab ]
netlab_tag: use
---
A while ago, [Chris Parker](https://www.networkfuntimes.com/about/) published a nice blog post explaining how to [configure unnumbered interfaces with IS-IS in Junos](https://www.networkfuntimes.com/is-is-and-unnumbered-ethernet-interfaces-in-junos/). It's well worth reading, but like my [Unnumbered Ethernet Interfaces](/2021/06/unnumbered-ethernet-interfaces/) blog post, it only covers one network operating system. What if you want to do something similar on another platform?

How about using the collective efforts of the team developing device configuration templates for _[netlab](https://github.com/ipspace/netlab)_? As of December 2023 _netlab_ supports:
<!--more-->
* [Unnumbered interfaces](https://netlab.tools/platforms/#initial-device-configurations) on 11 different platforms
* [IS-IS on 13 platforms](https://netlab.tools/platforms/#supported-configuration-modules) and OSPF on 18 platforms.
* [OSPF with unnumbered Ethernet interfaces](https://netlab.tools/module/ospf/#platform-support) on 11 platforms and [IS-IS with unnumbered Ethernet interfaces](https://netlab.tools/module/isis/#platform-support) on 10 platforms.

{{<note info>}}Don't trust the above figures, we keep improving _netlab_. Check _netlab_ documentation, but even that might not be up to date (some people find it easier to add a feature than to document it). **[netlab show modules](https://netlab.tools/netlab/show/#netlab-show-modules)** command is the ultimate source-of-truth.{{</note>}}

All you have to do to test the unnumbered Ethernet interface functionality on the device of your choice is to store the following YAML snippet in `topology.yml` and execute **netlab up**:

```
defaults.device: eos        # Change to your preferred device type
addressing.p2p.ipv4: True   # Use IPv4 unnumbered P2P links
module: [ isis ]            # Change to OSPF if needed
nodes: [ r1, r2 ]
links: [ r1-r2 ]
```

Best of all, you need absolutely no license to run *netlab* or any of the underlying software (Linux, Ubuntu, KVM, libvirt, Vagrant, Docker, containerlab, Ansible, and a dozen Python libraries).

Unfortunately, you will have to deal with the networking vendors that make you jump through the hoops to get the VM images or containers[^HM] and invest some time in building Vagrant boxes because those same vendors can't be bothered to add another step to the build process.

[^HM]: Notable exceptions: downloading Cumulus Linux, FRR,  Nokia SR Linux, and VyOS requires no extra effort. Junos vEvolved is free to download, but you must build a Vagrant box. Downloading Arista vEOS/cEOS and Cisco Nexus OS requires registration.