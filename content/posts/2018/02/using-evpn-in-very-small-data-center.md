---
date: 2018-02-06 09:01:00+01:00
evpn_tag: design
tags:
- design
- data center
- fabric
- EVPN
title: Using EVPN in Very Small Data Center Fabrics
url: /2018/02/using-evpn-in-very-small-data-center.html
---
I had an interesting "*how do you build a small fabric without throwing every technology in the mix*" discussion with [Nicola Modena](http://www.ipspace.net/Expert:Nicola_Modena) and mentioned that I don't see a reason to use EVPN in fabrics with just a few switches. He disagreed and gave me a few good scenarios where EVPN might be handy. Before discussing them let's establish a baseline.

### The Setup

Assume you're building two small data center fabrics (small because you have only a few hundred VMs and two because of redundancy and IT auditors).
<!--more-->
You don't need more than two switches in each data center, and because the bandwidth requirements are usually reasonably small and long-distance links are expensive, you could connect them like this:

{{<figure src="/2018/02/s1600-SmallFabric.png">}}

Furthermore (because we're dealing with an Enterprise design), let's assume you have to support end-to-end layer-2 connectivity across this fabric.

{{<note warn>}}As you know, I would never recommend a customer to do that, but sometimes you have more important battles to fight in a limited amount of time.{{</note>}}

To keep things simple, we'll assume everyone involved wants to have the simplest possible fabric design, so we won't be using port channels between servers and switches but rely on active/standby links or whatever other load distribution mechanism the servers (or hypervisors) provide.

{{<figure src="/2018/02/s1600-SmallFabric-Servers.png">}}

### Let's Do It the Old Way First

In my simplistic design, I'd use VXLAN encapsulation with ingress replication based on static flood lists:

-   I'd use pure IP routing within the fabric;
-   Switches would use VXLAN encapsulation to transport Ethernet traffic across IP fabric;
-   Ingress replication would be used instead of IP multicast to implement VXLAN flooding of BUM frames;
-   Dynamic MAC learning relying on BUM flooding would be used to populate MAC-to-VTEP tables;
-   Instead of using a control-plane protocol to build the list of remote VTEPs to which the traffic needs to be flooded, I'd use a static list of remote VTEPs configured on every switch.

{{<figure src="/2018/02/s1600-SmallFabric-IngressVXLAN.png">}}

Admittedly, you'd have to tweak the configuration every time you add a switch to my fabric design. However, it would be trivial[^HVT] to write a simple Ansible playbook to generate the switch configuration. If you want to learn how to do that, check out the [Ansible for Networking Engineers](http://www.ipspace.net/Ansible_for_Networking_Engineers) online course.

[^HVT]: For some not-so-small value of "trivial" ;)

### Now Add EVPN to the Mix

Instead of manually configuring VTEP flood lists, you could use an EVPN control plane between the four switches. I would use a full mesh of IBGP sessions to keep the design as simple as possible (remembering I'd have to go for route reflectors if the fabric grows).

{{<figure src="/2018/02/s1600-SmallFabric-EVPN-Basic.png">}}

EVPN would automatically build the flood lists (removing the need for manual configuration) and propagate customer MAC addresses using BGP.

So far, there's very little advantage of using EVPN, and a disadvantage of using a pretty complex piece of technology; things get a bit more interesting when you want to implement MLAG or layer-3 forwarding.

EVPN does reduce configuration complexity in fast-growing environments that can't spell *automation*. On some devices, you have to configure static flood lists per VNI, whereas you only have to configure EVPN IBGP neighbors once.

### Want to Know More?

If you're building a small fabric with just a few switches, you might get a good design [following recipes you find on the Internet](http://www.ipspace.net/Optimize_Data_Center_Infrastructure)... but when you start building larger fabrics, your designs will be better if you understand the underlying technology and its tradeoffs. You'll discover those in the [Data Center webinars](http://www.ipspace.net/Roadmap/Data_center_webinars) and [Designing and Building Data Center Fabrics self-paced online course](http://www.ipspace.net/Designing_and_Building_Data_Center_Fabrics).

Some of you will have to design more than just the transport fabric. You'll find all the material from the data center fabrics course and more details on compute, virtualization, storage, and network services in the [Building Next-Generation Data Center](http://www.ipspace.net/Building_Next-Generation_Data_Center) instructor-led online course.

Finally, to learn more about EVPN technology, check out the [EVPN Technical Deep Dive](http://www.ipspace.net/EVPN) webinar.
