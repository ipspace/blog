---
title: "SR Linux Containers Run on Apple Silicon"
date: 2024-09-25 08:38:00+0200
lastmod: 2024-12-11 09:39:00+0100
tags: [ netlab ]
netlab_tag: use
---
When looking for the [latest SR Linux container image](https://github.com/nokia/srlinux-container-image/pkgs/container/srlinux), I noticed images with **-arm-preview** tags and wondered whether they would run on Apple Silicon.

**TL&DR:** YES, IT WORKS 🎉 🎉

{{<note update>}}**Update 2024-12-11:** Starting with 24.10.1 and 23.10.6 images, the SR Linux container manifest contains AMD and ARM images, making running SR Linux on ARM trivial. This blog post has been updated accordingly.{{</note>}}

Here's what you have to do to make SR Linux work with *netlab* running on a Ubuntu VM on Apple silicon:
<!--more-->
* Follow the instructions from the [Running netlab and BGP Labs on Apple Silicon](/2024/03/netlab-bgp-apple-silicon/) blog post. Make sure to increase disk size to at least 10 GB, memory size to 8 GB, and to let the virtual machine use four CPU cores.
* Copy the following lab topology into an empty directory:

```
provider: clab
defaults.device: srlinux
defaults.devices.srlinux.clab.image: ghcr.io/nokia/srlinux:24.10.1

nodes: [ r1,r2 ]
links: [ r1-r2 ]
module: [ ospf ]
```

* Execute **netlab up** and have fun.

{{<note info>}}SR Linux release 24.10.1 will be the default SR Linux image in _netlab_ release 1.9.3. Until then, you must change the image name, either in the lab topology or in the system defaults ([more details](https://netlab.tools/example/release/#tutorial-release)).{{</note>}}

Once you verify that the SR Linux containers run on your Apple silicon, have fun [using them](https://bgplabs.net/1-setup/#select-the-network-devices-you-will-work-with) in the [BGP labs](https://bgplabs.net/).