---
date: 2018-10-08 09:53:00+02:00
evpn_tag: design
tags:
- VXLAN
- data center
- EVPN
- overlay networks
- virtualization
title: VXLAN and EVPN on Hypervisor Hosts
url: /2018/10/vxlan-and-evpn-on-hypervisor-hosts.html
---
One of my readers sent me a series of questions regarding a new cloud deployment where the cloud implementers want to run VXLAN and EVPN on the hypervisor hosts:

> I am currently working on a leaf-and-spine VXLAN+ EVPN PoC. At the same time, the systems team in my company is working on building a Cloudstack platform and are insisting on using VXLAN on the compute node even to the point of using BGP for inter-VXLAN traffic on the nodes.

Using VXLAN (or GRE) encap/decap on the hypervisor hosts is nothing new. That's how NSX and many OpenStack implementations work.
<!--more-->
The "*BGP for Inter-VXLAN traffic*" bit sounds too sketchy -- at the very minimum one should know:

-   What they plan to use BGP for;
-   How they plan to propagate MAC-to-VTEP mapping information (that's one of the things we use EVPN for);
-   How they plan to integrate virtual with physical network;
-   What control-plane stack they plan to use.

If they plan to use Juniper Contrail (or however it's called today), then the whole thing has a good chance of working. Free Range Routing is another reasonable option, although I'm not sure how well it works with VXLAN tunnels on Linux hosts, and a [recent post by Attilla de Groot](https://cumulusnetworks.com/blog/evpn-host/) indicates the whole idea might not be ready for production deployment. Anyone with real-life experience is most welcome to write a comment.

> I am a little worried about this as we network folks will have no visibility as to how they are going to implement it and with what ramifications.

Maybe it's time you start [acting like a service provider](https://blog.ipspace.net/2016/08/networking-is-infrastructure-get-used.html), and provide them with end-to-end connectivity that they can use in any way they wish. You might still have to use VXLAN to implement VLANs stretched across multiple ToR switches unless you use either host routing or routing on host designs, but stop worrying about things you have no influence upon.

Just make sure all the decisions made in the design phase and integration/service points are well documented and understood by the management level where the two teams meet. "*Sign on the dotted line that you accept the risk*" sometimes does wonders when there's lack of communication between teams.

> Do you think it's a good idea to offload the VXLAN traffic from the hardware switch to the compute nodes?

As I wrote many times, it's the right architecture, and all scalable solutions (whether visible to the outside world, or hidden in the misty fog of the public clouds) use this approach. In case you missed those blog posts, start with:

-   [Complexity belongs to the network edge](https://blog.ipspace.net/2011/05/complexity-belongs-to-network-edge.html);
-   [Decouple virtual networking from the physical world](https://blog.ipspace.net/2011/12/decouple-virtual-networking-from.html);
-   [Network virtualization and spaghetti wall](https://blog.ipspace.net/2013/06/network-virtualization-and-spaghetti.html);
-   [Virtual networks: the Skype analogy](https://blog.ipspace.net/2012/05/virtual-networks-skype-analogy.html);
-   [Smart fabrics versus overlay virtual networks](https://blog.ipspace.net/2013/07/smart-fabrics-versus-overlay-virtual.html).

[ipSpace.net subscribers](https://www.ipspace.net/Subscription) can find more details in [*Networking in Private and Public Clouds*](https://www.ipspace.net/Networking_in_Private_and_Public_Clouds) and [*Overlay Virtual Networking*](https://www.ipspace.net/Overlay_Virtual_Networking) webinars.

> Would this not affect the performance of the hardware Nics on those servers?

Well-implemented VXLAN encapsulation/decapsulation never had significant performance problems. Unfortunately, the [open-source world is full of less-than-optimal solutions](https://blog.ipspace.net/2014/11/open-vswitch-performance-revisited.html).

> What other arguments can we the network engineers present to challenge this approach if it helps the company in the right direction

Without having more details, the only thing I can say is that their approach is architecturally correct even though you might not like it, or doubt that the other team is able to pull it off.
