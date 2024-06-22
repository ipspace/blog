---
title: "netlab 1.8.4: vrnetlab Containers, Catalyst 8000v"
series_title: "vrnetlab Containers, Catalyst 8000v (Release 1.8.4)"
date: 2024-06-24 07:43:00+02:00
tags: [ netlab ]
netlab_tag: release
---
I don't think I ever created two _netlab_ releases in a week, but last week, I stumbled upon a motherlode of goodies, and it would be a shame not to make them available.

Someone tried to use *netlab* with *[vrnetlab](https://containerlab.dev/manual/vrnetlab/)* containers for CSR 1000v and Nexus 9300v. We got it to work, but when I started integrating his changes into the development branch, I wanted to test them, so I installed *[vrnetlab](https://github.com/hellt/vrnetlab)* to create my own container images. *vrnetlab* is an excellent tool, and building containers is a breeze ([running them is a different story](https://netlab.tools/labs/clab/#using-vrnetlab-containers)), so I added [support for *vrnetlab* containers](https://netlab.tools/labs/clab/#container-images) for every device supported by that tool and *netlab* for which I happened to have a disk image.
<!--more-->
During that process, I also cleaned up the half-dozen "_let's wait for the VM to start_" ad-hoc solutions, replacing them with a unified script, and added extra "_are you really ready?_" checks for vPTX and Nexus OS (they both start the SSH server long before they realize they have the data-plane interfaces). Running those tests was a bit cumbersome, so I [added the `--ready` option to the **netlab initial** command](https://netlab.tools/netlab/initial/#wait-for-devices-to-become-ready). You can use that option to ensure the lab devices are ready without configuring them.

Speaking of disk images: after getting a Catalyst 8000v image, I couldn't resist [adding it to _netlab_](https://netlab.tools/platforms/). It was a breeze, as Catalyst 8000v is very close to CSR 1000v (unless it isn't; someone couldn't decide how to configure VLANs), and most features available with CSR 1000v are also configurable on Catalyst 8000v. CSR 1000v VXLAN configuration was accepted but didn't work, so I temporarily turned off VXLAN support for Catalyst 8000v. I also didn't test whether MPLS/VPN works.

Last but not least, I had to interrupt the **netlab initial** configuration process a few times while testing the "_are you ready?_" *vrnetlab* container scripts. I got annoyed by the resulting stack trace, so I implemented the `KeyboardInterrupt` handler for all long-running **netlab** commands.

For more details, [read the release notes](https://netlab.tools/release/1.8/#release-1-8-4).
<!--more-->
### Upgrading or Starting from Scratch

* To upgrade, execute `pip3 install --upgrade networklab`.
* New to *netlab*? Start with the [Getting Started document](https://netlab.tools/tutorials/) and the [installation guide](https://netlab.tools/install/).
* Need help? Open a [discussion](https://github.com/ipspace/netlab/discussions) or an [issue](https://github.com/ipspace/netlab/issues) in [netlab GitHub repository](https://github.com/ipspace/netlab).
