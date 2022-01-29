---
title: "Sample Lab: SR-MPLS on Junos and SR Linux"
date: 2022-01-31 07:36:00
tags: [ traffic engineering, MPLS ]
series: netsim
netsim_tag: use
---
Last week I [published](https://blog.ipspace.net/2022/01/netsim-example-rsvp-te-junos.html) a link to [Pete Crocker](https://blog.petecrocker.com/about/)'s [RSVP-TE lab](https://github.com/ipspace/netsim-examples/tree/master/routing/rsvp-mpls-vsrx), but there's more: he [created another lab](https://github.com/ipspace/netsim-examples/tree/master/routing/sr-isis-te-vsrx) using the same topology that uses SR-MPLS with IS-IS to get the job done.

[Jeroen Van Bemmel](https://www.linkedin.com/in/jeroenvbemmel/) did something similar for SR Linux: [his lab topology](https://github.com/ipspace/netsim-examples/tree/master/routing/sr-mpls-bgp-srlinux) has fewer devices (plus SR Linux runs in containers), so it's easily deployable on machines without humongous amount of memory.
<!--more-->
---

SR Linux and Cumulus VX are still the only network operating systems I'm aware of that you can download in a ready-for-use format without registration. All you have to do to get the lab up and running is

* Install the prerequisite software (docker, containerlab, netsim-tools)
* Copy topology.yml into an empty directory
* Execute **netlab up**

Downloading device images from most other vendors requires registration followed by arcane incantations to build a Vagrant box or container image.

---

Want even more platform options? Here's [another topology](https://github.com/ipspace/netsim-examples/tree/master/routing/sr-mpls-bgp) using Cisco CSR and Arista vEOS.

The beauty of all these solutions: SR-MPLS is one of the [standard netsim-tools modules](https://netsim-tools.readthedocs.io/en/latest/module-reference.html), and getting it configured in your lab is as easy as adding **sr** to the **module** list.
