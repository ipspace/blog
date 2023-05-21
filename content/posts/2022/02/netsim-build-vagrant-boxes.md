---
date: 2022-02-10 07:45:00+00:00
lastmod: 2022-02-15 14:37:00
netlab_tag: overview
tags:
- netlab
title: Build Vagrant Boxes for Your Network Devices
---
One of the toughest hurdles to overcome when building your own virtual networking lab is the slog of downloading VM images for your favorite network devices and building Vagrant boxes[^VB] in case you want to use them with Vagrant or [netlab](https://netlab.tools/).

You can find box-building recipes on the Internet -- [codingpackets.com has a dozen of them](https://codingpackets.com/blog/tag/vagrant/) -- but they tend to be a bit convoluted and a smidge hard-to-follow the first time you're trying to build the boxes (trust me, I've been there).
<!--more-->
I finally had enough and built a simple scaffold for libvirt box-building. It takes the mundane parts out of the process:

* Starting a VM (you still have to download the disk image though)
* Killing the VM after you're done with initial configuration
* Packing the VM disk as a Vagrant box and adding the desired metadata. 

There are people out there who automated the whole process ([example](https://github.com/mweisel/cisco-nxos9kv-vagrant-libvirt)). I don't want to be a perpetual maintainer of ever-changing quirks -- you'll still have to do a few bits on your own with the help of as-simple-as-they-can-get instructions.

The current netlab version can build [Arista vEOS](https://netlab.tools/labs/eos/), [Nexus 9300v](https://netlab.tools/labs/nxos/), [Cisco CSR](https://netlab.tools/labs/csr/), and [Juniper vSRX](https://netlab.tools/labs/vsrx/) boxes (you can always find the up-to-date list [here](https://netlab.tools/labs/libvirt/#building-your-own-boxes)). If you feel like contributing another box-building recipe please get in touch.

**Other options:**

* It seems like [vrnetlab project](https://github.com/vrnetlab/vrnetlab) automated building Docker containers for a number of platforms. You could build those, add them to *netlab*, and use the with *containerlab* platform.
* GNS3 is always an option for GUI enthusiasts.

[^VB]: Cisco Nexus 9300v, Arista vEOS, and Cumulus VX are available as a Vagrant box for VirtualBox. Cumulus VX is also available as a Vagrant box for libvirt. YMMV.

### Release History

2022-02-15
: [*netsim-tools* release 1.1.3](https://netlab.tools/release/1.1/#new-functionality-in-release-1-1-3) added build recipes for Cisco CSR and Juniper vSRX.