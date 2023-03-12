---
cdate: 2022-07-09
comment: 'In January 2014 I took another look at what the Open Networking Foundation
  founding members managed to achieve between March 2011 (the [beginning of OpenFlow/SDN
  hype](/2011/03/open-networking-foundation-fabric.html)) and early 2014. The only
  one that made significant progress on the “centralized control plane” front was
  Google.


  Since I wrote this blog post:


  * Facebook launched their own switch operating system, which is just another classical
  network operating system running on Linux.

  * Deutsche Telekom killed the Terastream pilot

  * BGP in the data center is the next big thing, and some hype scalers use it to
  disseminate forwarding information from the controller to traditional BGP routers.

  * Big Switch was acquired by Arista, and I''ve never met anyone using it in a production
  network.

  * Cisco Nexus 1000v died, and IBM virtual switch never got far beyond marketing
  materials.

  '
date: 2014-01-21 07:31:00+01:00
sdn_hype_tag: back
series:
- sdn_hype
tags:
- SDN
- OpenFlow
title: Control and Data Plane Separation – Three Years Later
url: /2014/01/control-and-data-plane-separation-three.html
---
Almost three years ago the [OpenFlow/SDN hype exploded](https://blog.ipspace.net/2011/03/open-networking-foundation-fabric.html) and the [Open Networking Foundation started promoting the concept of physically separate control and data planes](http://blog.ipspace.net/2014/01/what-exactly-is-sdn-and-does-it-make.html). Let's see how far its founding members got in the meantime:
<!--more-->
-   Google [implemented their inter-DC WAN network](https://blog.ipspace.net/2012/05/openflow-google-brilliant-but-not.html) with switches that use OpenFlow within a switching fabric and BGP/IS-IS and something akin to PCEP between sites. So far they haven\'t made their software available to the outside world.
-   Facebook is working on the networking platform for their [Open Compute Project](http://www.opencompute.org/projects/networking/). It seems they've got to [switch hardware specs](http://www.opencompute.org/assets/Uploads/Open-Compute-Project-BRCM-Open-1-0-Leaf-Spine-Switch-Specification-110813-2smallpdf.com.pdf); I haven't heard about software running on those switches yet ... or maybe they'll go down the same path as Google (We got cheap switches, and we have our own software. Goodbye and thank you!)
-   Yahoo! was talking about custom changes to standard networking protocols. Haven't heard about their progress since the first OpenFlow Symposium; the [April 2012 presentation from Igor Gashinsky](http://www.opennetsummit.org/archives/apr12/1030%20Tuesday%20Igor%20Gashinsky.pdf) still concluded with "Where's My Pony?"
-   Deutsche Telekom is still using [traditional routers](https://blog.ipspace.net/2013/11/deutsche-telekom-terastream-designed.html) and a [great NFV platform](http://blog.ipspace.net/2013/11/terastream-part-2-lightweight-4over6.html).
-   Microsoft [implemented SDN using BGP](https://blog.ipspace.net/2013/10/exception-routing-with-bgp-sdn-done.html), using a central controller, but not a centralized control plane.
-   I have no idea what Verizon is doing.

In the (physical) networking vendor world, NEC seems to be the only company with a mature commercial product that matches the ONF definition of SDN, and one might argue that Plexxi does something similar. Cisco has just shipped the initial version of their controller, as did HP, and those products seem pretty limited at the moment.

{{<note>}}Wondering why I didn't include [Big Switch Networks](http://www.bigswitch.com) in the above list? My definition of *shipping* includes publicly available product documentation, or (at the very minimum) something resembling a data sheet with feature description, system requirements and maximum limits. I couldn't find either on Big Switch web site.{{</note>}}

On the other hand, the virtual networking world was always full of solutions with separate control and data planes, starting with the venerable VMware\'s standard vSwitch and Distributed vSwitch and Nexus 1000V, and continuing with newer entrants, from Hyper-V extensible switch and VMware NSX to Juniper Contrail and IBM's 5000V and DOVE. Some of these solutions were used years before the explosion of OpenFlow/SDN hype (only we didn't know we should call them SDN).
