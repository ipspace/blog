---
date: 2022-01-31 07:36:00+00:00
lastmod: 2022-01-31 19:26:00
netlab_tag: use
tags:
- traffic engineering
- MPLS
- netlab
title: 'Sample Lab: SR-MPLS on Junos and SR Linux'
---
Last week I [published](/2022/01/netsim-example-rsvp-te-junos/) a link to [Pete Crocker](https://blog.petecrocker.com/about/)'s [RSVP-TE lab](https://github.com/ipspace/netlab-examples/tree/master/routing/rsvp-mpls-vsrx), but there's more: he [created another lab](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-isis-te-vsrx) using the same topology that uses SR-MPLS with IS-IS to get the job done.

[Jeroen Van Bemmel](https://www.linkedin.com/in/jeroenvbemmel/) did something similar for SR Linux: [his lab topology](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-mpls-bgp-srlinux) has fewer devices (plus SR Linux runs in containers), so it's easily deployable on machines without humongous amount of memory.
<!--more-->
---

SR Linux, Cumulus VX, and Extreme Virtual EXOS are the only network operating systems I'm aware of that you can download in a ready-for-use format without registration. Anything else? Please write a comment.

Even better, SR Linux and Cumulus VX are available as ready-to-run containers; Cumulus VX is also available as *libvirt* and *VirtualBox* Vagrant box. All you have to do to get the lab up and running is:

* Install the prerequisite software (docker, containerlab, netsim-tools)
* Copy topology.yml into an empty directory
* Execute **netlab up**

Downloading device images from most other vendors requires registration followed by arcane incantations to build a Vagrant box or container image.

---

Want even more platform options? Here's [another topology](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-mpls-bgp) using Cisco CSR and Arista vEOS.

The beauty of all these solutions: SR-MPLS is one of the [standard netsim-tools modules](https://netlab.tools/module-reference/), and getting it configured in your lab is as easy as adding **sr** to the **module** list.

### Release History

2022-01-31
: Images for Extreme Virtual EXOS are available on GitHub
