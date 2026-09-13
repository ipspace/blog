---
date: 2022-02-10 07:45:00+00:00
lastmod: 2026-09-13 12:58:00
netlab_tag: overview
tags:
- netlab
title: Build Vagrant Boxes for Your Network Devices
---
One of the toughest hurdles to overcome when building your own virtual networking lab is the slog of downloading VM images for your favorite network devices and building Vagrant boxes[^VB] in case you want to use them with Vagrant or [netlab](https://netlab.tools/).

You can find box-building recipes on the Internet -- [codingpackets.com](https://codingpackets.com/blog#vagrant) has at least a dozen -- but they tend to be a bit convoluted and a smidge hard to follow the first time you're trying to build the boxes (trust me, I've been there).
<!--more-->
I finally had enough and built a simple scaffold for Vagrant box-building for the vagrant-libvirt provider. You still have to deal with vendors stonewalling the image-downloading process, but then the **[netlab libvirt package](https://netlab.tools/netlab/libvirt/#netlab-libvirt-package)** command takes the mundane parts out of the process:

* It copies the VM image into a temporary directory (recent Linux distributions don't give KVM/libvirt access to your home directory)
* When needed, it unpacks/converts the VM image (we support QCOW, OVA, ZIP, and ISO formats)
* It starts a VM and kills it after you're done with initial configuration
* It packs the modified VM disk image as a Vagrant box and adds the desired metadata.

While there are people brave enough to go for a fully automated process ([example](https://github.com/mweisel/cisco-nxos9kv-vagrant-libvirt)), I don't want to be a perpetual maintainer of ever-changing quirks -- you'll still have to do a few bits on your own with the help of as-simple-as-they-can-get instructions.

The current netlab version can build [around two dozen Vagrant boxes](https://netlab.tools/labs/libvirt/#libvirt-build-boxes) (the up-to-date list is [here](https://netlab.tools/labs/libvirt/#libvirt-build-boxes)). If you feel like contributing another box-building recipe, please [submit a PR](https://netlab.tools/dev/guidelines/).

**Other options:**

* You can use the [vrnetlab fork](https://github.com/srl-labs/vrnetlab) to build [VM-in-Docker containers](/2026/09/running-virtual-machines-in-containers/) for a number of platforms and [use them with *netlab*](https://netlab.tools/labs/clab/#clab-vrnetlab).
* GNS3 is always an option for GUI enthusiasts.

### Release History

2026-09-13
: Cleaned up obsolete information, added more links/details

2022-02-15
: [*netsim-tools* release 1.1.3](https://netlab.tools/release/1.1/#new-functionality-in-release-1-1-3) added build recipes for Cisco CSR and Juniper vSRX.