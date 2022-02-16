---
title: "Build Vagrant Boxes for Your Network Devices with netsim-tools"
date: 2022-02-10 07:45:00
tags: [ automation ]
series: netsim
netsim_tag: overview
lastmod: 2022-02-15 14:37:00
---
One of the toughest hurdles to overcome when building your own virtual networking lab is the slog of downloading VM images for your favorite network devices and building Vagrant boxes[^VB] in case you want to use them with Vagrant or [netsim-tools](https://netsim-tools.readthedocs.io/en/latest/index.html).

You can find box-building recipes on the Internet -- [codingpackets.com has a dozen of them](https://codingpackets.com/blog/tag/vagrant/) -- but they tend to be a bit convoluted and a smidge hard-to-follow the first time you're trying to build the boxes (trust me, I've been there).
<!--more-->
I finally had enough and built a simple scaffold for libvirt box-building. It takes the mundane parts out of the process:

* Starting a VM (you still have to download the disk image though)
* Killing the VM after you're done with initial configuration
* Packing the VM disk as a Vagrant box and adding the desired metadata. 

There are people out there who automated the whole process ([example](https://github.com/mweisel/cisco-nxos9kv-vagrant-libvirt)). I don't want to be a perpetual maintainer of ever-changing quirks -- you'll still have to do a few bits on your own with the help of as-simple-as-they-can-get instructions.

The current version of *netsim-tools* can build [Arista vEOS](https://netsim-tools.readthedocs.io/en/latest/labs/eos.html), [Nexus 9300v](https://netsim-tools.readthedocs.io/en/latest/labs/nxos.html), [Cisco CSR](https://netsim-tools.readthedocs.io/en/latest/labs/csr.html), and [Juniper vSRX](https://netsim-tools.readthedocs.io/en/latest/labs/vsrx.html) boxes (you can always find the up-to-date list [here](https://netsim-tools.readthedocs.io/en/latest/labs/libvirt.html#creating-vagrant-boxes)). If you feel like contributing another box-building recipe please get in touch.

**Other options:**

* It seems like [vrnetlab project](https://github.com/vrnetlab/vrnetlab) automated building Docker containers for a number of platforms. You could build those, add them to *netsim-tools*, and use the with *containerlab* platform.
* GNS3 is always an option for GUI enthusiasts.

[^VB]: Cisco Nexus 9300v, Arista vEOS, and Cumulus VX are available as a Vagrant box for VirtualBox. Cumulus VX is also available as a Vagrant box for libvirt. YMMV.

### Release History

2022-02-15
: [*netsim-tools* release 1.1.3](https://netsim-tools.readthedocs.io/en/latest/release/1.1.html#new-functionality-in-release-1-1-3) added build recipes for Cisco CSR and Juniper vSRX.