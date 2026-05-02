---
date: 2022-01-31 07:36:00+00:00
lastmod: 2022-01-31 19:26:00
netlab_tag: mpls
tags:
- traffic engineering
- MPLS
- netlab
- SR-MPLS
sr-mpls_tag: lab
sr-mpls_title: 'Traffic Engineering with SR-MPLS on Junos and SR Linux'
title: 'Sample Lab: Traffic Engineering with SR-MPLS on Junos and SR Linux'
---
Last week I [published](/2022/01/netsim-example-rsvp-te-junos/) a link to [Pete Crocker](https://blog.petecrocker.com/about/)'s [RSVP-TE lab](https://github.com/ipspace/netlab-examples/tree/master/routing/rsvp-mpls-vsrx), but there's more: he [created another lab](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-isis-te-vsrx) using the same topology that uses SR-MPLS with IS-IS to get the job done.
<!--more-->
[Jeroen Van Bemmel](https://www.linkedin.com/in/jeroenvbemmel/) did something similar for SR Linux: [his lab topology](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-mpls-bgp-srlinux) has fewer devices (plus SR Linux runs in containers), so it's easily deployable on machines without a humongous amount of memory.

Want even more platform options? Here's [another topology](https://github.com/ipspace/netlab-examples/tree/master/routing/sr-mpls-bgp) using Cisco CSR and Arista vEOS.

The beauty of all these solutions: SR-MPLS is one of the [standard netsim-tools modules](https://netlab.tools/module-reference/), and getting it configured in your lab is as easy as adding **sr** to the **module** list.
