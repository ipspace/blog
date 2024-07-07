---
date: 2012-07-04 06:56:00+02:00
tags:
- SDN
- data center
- OpenFlow
title: Legacy Protocols in OpenFlow-Based Networks
url: /2012/07/legacy-protocols-in-openflow-based/
---
This post is probably a bit premature, but I'm positive your CIO will get a visit from a vendor offering clean-slate OpenFlow/SDN-based data center fabrics in not so distant future. At that moment, one of the first questions you should ask is "*how well does your new wonderland integrate with my existing network?*" or more specifically "*which L2 and L3 protocols do you support?*"
<!--more-->
At least one of the vendors offering OpenFlow controllers that manage physical switches has a simple answer: use static LAG to connect your existing gear with our OpenFlow-based network (because our controller doesn't support LACP), use static routes (because we don't run any routing protocols) and don't create any L2 loops in your network (because we also don't have STP). If you wonder how reliable that is, you obviously haven't implemented a redundant network with static routes before.

However, to be a bit more optimistic, the need for legacy protocol support depends primarily on how the new solution integrates with your network.

**Overlay solutions** (like Nicira's NVP) [don't interact with the existing network at all](/2012/02/embrace-change-resistance-is-futile/). A hypervisor running Open vSwitch and using [STT](/2012/03/do-we-really-need-stateless-transport/) or GRE appears as an IP host to the network, and uses existing Linux mechanisms (including NIC bonding and LACP) to solve the L2 connectivity issues.

[**Hybrid OpenFlow solutions**](/2011/11/openflow-deployment-models.html#of_ships) that only modify the behavior of the user-facing network edge (example: per-user access control) are also OK. You should closely inspect what the product does and ensure it doesn't modify the network device behavior you rely upon in your network, but in principle you should be fine. For example, the [XenServer vSwitch Controller](http://docs.vmd.citrix.com/XenServer/6.0.0/1.0/en_gb/dvs_controller.html) modifies just the VM-facing behavior, but not the behavior configured on uplink ports.

[**Rip-and-replace OpenFlow-based network fabrics**](/2012/02/necibm-enterprise-openflow-you-can/) are the truly interesting problem. You'll have to connect existing hosts to them, so you'd probably want to have LACP support ([unless you're a VMware-only shop](/2011/01/vmware-vswitch-does-not-support-lacp/)), and they'll have to integrate with the rest of the network, so you should ask for at least:

-   LACP, if you plan to connect anything but vSphere hosts to the fabric ... and you'll probably need a device to connect the OpenFlow-based part of the network to the outside world;
-   LLDP or CDP. If nothing else, they simplify troubleshooting, and they are implemented on almost everything including vSphere vSwitch.
-   STP unless the OpenFlow controller implements [split horizon bridging like vSphere's vSwitch](/2010/11/vmware-virtual-switch-no-need-for-stp/), but even then we need [basic things like BPDU guard](/2011/11/virtual-switches-need-bpdu-guard/).
-   A routing protocol if the OpenFlow-based solution supports L3 (OSPF comes to mind).

Call me a grumpy old man, but I wouldn't touch an OpenFlow controller (or an SD-WAN solution) that doesn't support the above-mentioned protocols. Worst case, if I would be forced to implement a network using such a controller, I would make sure it's totally isolated from the rest of my network. Even then a single point of failure wouldn't make much sense, so I would need two firewalls or routers and static routing in redundant scenarios breaks sooner or later. You get the picture.

To summarize: dynamic link status and routing protocols were created for a reason. Don't allow glitzy new-age solutions to daze you, or you just might experience a major headache down the road. For more details watch *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.