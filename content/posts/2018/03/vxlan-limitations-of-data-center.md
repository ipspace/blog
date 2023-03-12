---
date: 2018-03-29 08:25:00+02:00
tags:
- VXLAN
- switching
- data center
title: VXLAN Limitations of Data Center Switches
url: /2018/03/vxlan-limitations-of-data-center.html
---
One of my readers found a Culumus Networks article that explains why you can't have more than a few hundred VXLAN-based VLAN segments on every port of 48-port Trident-2 data center switch. That article has unfortunately disappeared in the meantime, and even the Wayback Machine doesn't have a copy.

{{<note warn>}}Expect to see similar limitations in most other chipsets. There's a huge gap between *millions of segments* enabled by 24-bit VXLAN Network Identifier and reality of switching silicon. Most switching hardware is also limited to 4K VLANs.{{</note>}}
<!--more-->
Based on that document he became concerned whether merchant silicon switches might be a good choice for his small data center:

> I've had impression that in small data center environments (two sites, a few ToR, \~1000 VMs & max 20 ESX hosts) all Broadcom chipsets should be "good enough" for us even without support for single-pass VXLAN routing. Is it really so? Those limits could hurt even our small DC.

Realistically, what that document is saying is \"*if you\'re careless enough to have all VLANs configured on all ports, you won\'t be able to have more than 300 VLANs on every port of a 48-port 10GE switch*\". Honestly, I would be scared of having 300 VLANs on every server-facing switch port no matter what the chipset limitations might be\... and why would you need 300 VLANs for 1000 VMs anyway?

If you need more than a few dozen segments, you should either use a hypervisor-based virtual networking solution (example: NSX), an orchestration system that synchronizes the needs of physical and virtual switches, or a [single-image data center fabric](https://blog.ipspace.net/2018/02/single-image-systems-or-automated.html) that does that behind the scenes.

{{<note info>}}One of them is [architecturally correct](https://blog.ipspace.net/2011/05/complexity-belongs-to-network-edge.html), the other one preferred by networking vendors telling you how you [should keep supporting legacy infrastructure for the next millennium](http://blog.ipspace.net/2013/06/network-virtualization-and-spaghetti.html).{{</note>}}

Numerous vendors have edge VLAN pruning solutions that try to pull information out of vCenter (VM Tracer, VM Tracker\...); you'll find them described in [*Data Center Fabric Architectures*](http://www.ipspace.net/Data_Center_Fabrics) webinar. The same vendors usually integrate with other orchestration systems like OpenStack.

However, what you should do as the starting point is what I\'ve explained in the [*Networking in Private and Public Clouds*](http://www.ipspace.net/Networking_in_Private_and_Public_Clouds)*,* [*Designing Cloud Infrastructure*](http://www.ipspace.net/Designing_Private_Cloud_Infrastructure)*,* and [*NSX, ACI or EVPN*](http://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN) webinars. Figure out:

-   Who the data center infrastructure customers are (hint: application developers);
-   What they really need (as opposed to what they\'re asking for);
-   And finally, what problem you're trying to solve.

You'll probably find that those limitations aren't as bad as they sound.

#### Notes

-   All webinars mentioned in this blog post are included in [Standard ipSpace.net Webinar Subscription](http://www.ipspace.net/Subscription);
-   For even more data center goodies check out the [Building Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) online course.
