---
title: "VXLAN Virtual Labs Have Never Been Easier"
date: 2024-02-27 13:00:00+0100
tags: [ netlab, VXLAN ]
netlab_tag: use
---
I stumbled upon an "*I want to dive deep into VXLAN and plan to build a virtual lab*" discussion on LinkedIn[^TL]. Of course, I suggested using *netlab*. After all, you have to build an IP core and VLAN access networks and connect a few clients to those access networks before you can start playing with VXLAN, and those things tend to be excruciatingly dull.

[^TL]: One of those rare cases where a post suggested by LinkedIn wasn't a Thought Leader&trade; self-promotion.

Now imagine you decide to use _[netlab](https://netlab.tools/)_. Out of the box, you get [topology management](https://netlab.tools/topology-overview/), lab orchestration, [IPAM](https://netlab.tools/example/addressing-tutorial/), routing protocol design ([OSPF](https://netlab.tools/module/ospf/), [BGP](https://netlab.tools/module/bgp/), and [IS-IS](https://netlab.tools/module/isis/)), and device configurations, including IP routing and VLANs.
<!--more-->
{{<figure src="/2024/02/handcrafting-configs.jpg" caption="Networking engineer handcrafting VXLAN lab (by Microsoft Copilot)">}}
OK, I ignored the royal pain of preparing the vendor-specific virtual machine images, but even there, things are continuously getting better:

* With zero hassle, you can download Cumulus Linux, FRR, Juniper vPTX, Nokia SR Linux, and VyOS. You must build a Vagrant box from the vPTX disk image, but it's a breeze. All others are available as download-and-deploy containers.
* Downloading Cisco Nexus 9300v and Arista EOS requires registration, but there are no further obstacles. Installing the Arista cEOS container is easy, and the box-building instructions for Arista vEOS and Nexus 9300v are included with _netlab_ (some assembly required).

That already gives you a half-dozen platforms to play with, and _netlab_ will [configure OSPF, BGP, and VLANs](https://netlab.tools/platforms/#platform-routing-support) on all of them for you. Even better, if you want to explore VXLAN before learning to configure it, _netlab_ does it for you on all those platforms apart from Juniper vPTX[^PRA].

Let's go further: you want to add EVPN to VXLAN. No biggie, _netlab_ will configure BGP for you on over a dozen platforms and throw EVPN in for free on Arista EOS, Aruba CX, Cisco Nexus OS, Cumulus Linux, Dell OS10, FRR, Nokia SR Linux, Nokia SR OS, and Vyos. It can even implement ~~crappy~~ creative designs like running IBGP EVPN AF over EBGP IPv4 AF.

[^PRA]: If anyone feels like creating a configuration template needed to deploy VXLAN on Junos, please submit a pull request.

So, what's stopping you from [downloading *netlab*](https://netlab.tools/install/) and discovering VXLAN and EVPN? If you're willing to deal with Linux networking inside FRR or Cumulus Linux containers, you could run a decent lab on an AWS **t3a.small** instance; you could also try to squeeze it into the [Always Free Oracle Cloud](https://www.oracle.com/cloud/free/#free-cloud-trial) instance. You'd need a bit more memory to run Arista cEOS containers, but even there, a **t3a.medium** should be good enough.