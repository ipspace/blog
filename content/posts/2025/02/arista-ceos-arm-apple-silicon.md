---
title: "Arista cEOS Containers Run on Apple Silicon"
date: 2025-02-04 08:41:00+0200
tags: [ netlab ]
netlab_tag: use
---
A few days ago, someone mentioned Arista released a cEOS EFT image running on Arm. Of course, I had to test whether it would run on Apple Silicon.

**TL&DR:** YES 🎉 🎉

Here's what you have to do to make the Arista cEOS container work with *netlab* running on an Ubuntu VM on Apple silicon:
<!--more-->
* Follow the instructions from the [Running netlab and BGP Labs on Apple Silicon](/2024/03/netlab-bgp-apple-silicon/) blog post. Make sure to increase the disk size to at least 10 GB, memory size to 8 GB, and let the virtual machine use four CPU cores.
* [Download the Arista cEOS ARM container](https://www.arista.com/en/support/software-download).
* Use **multipass transfer** to copy the file into the Multipass instance.
* Follow the [cEOS installation instructions](https://netlab.tools/labs/ceos/)
* Copy the following lab topology into an empty directory. Change the cEOS image name if needed.

```
provider: clab
defaults.device: eos
defaults.devices.eos.clab.image: ceos:4.33.1F

nodes: [ r1,r2 ]
links: [ r1-r2 ]
module: [ ospf ]
```

* Execute **netlab up** and have fun.

Once you verify that the Arista cEOS containers run on your Apple silicon, have fun [using them](https://bgplabs.net/1-setup/#select-the-network-devices-you-will-work-with) in the [BGP](https://bgplabs.net/) and [IS-IS](https://isis.bgplabs.net/) labs.