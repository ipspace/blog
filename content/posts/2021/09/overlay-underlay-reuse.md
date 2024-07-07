---
title: "Reusing Underlay Network for Infrastructure Services"
date: 2021-09-30 06:32:00
lastmod: 2021-09-30 16:19:00
tags: [ overlay networks, design ]
---
Boris Lazarov [sent me an excellent question](/2018/05/what-is-evpn/#691):

> Does it make sense and are there any inherent problems from design perspective to use the *underlay* not only for transport of *overlay* packets, but also for some services. For example: VMWare cluster, vMotion, VXLAN traffic, and some basic infrastructure services that are prerequisite for the rest (DNS).

Before answering it, let's define some terminology which will inevitably lead us to the *it's tunnels all the way down* endstate.
<!--more-->
One of the most common ways of implementing a complex service on top of a simple transport network is to use *tunnels*. We could endlessly argue whether [MPLS labels or virtual circuits are tunnels](/2011/10/mpls-is-not-tunneling/) (or whether [seven or nine angels can dance on the head of a pin](https://en.wikipedia.org/wiki/How_many_angels_can_dance_on_the_head_of_a_pin%3F)), but let's not go there.

In every network using tunnels (or some such technology) you have the *transport* part of the network -- called *underlay* -- that the edge nodes use to send tunnel-encapsulated user traffic to other edge nodes to implement *customer* (or *services*) network called *overlay*.

Let's take VMware NSX-T as an example. The vSphere hypervisors use the IP connectivity provided by the physical data center fabric to exchange Geneve-encapsulated user traffic. Virtual networks are clearly the *overlay*, physical data center fabric is the *underlay*.

Unfortunately, VMware [never mastered the art of using simple transport networks](/2020/02/do-we-need-complex-data-center-switches/), they [love to push the complexity onto others](/2019/10/the-cost-of-disruptiveness-and/) (and then blame them for being [overly complex](/2013/04/this-is-what-makes-networking-so-complex/)). In the NSX-V and NSX-T case, a redundantly connected vSphere server requires a single IP subnet spanning all ToR switches it's connected to (usually a pair of switches)[^S1]. It also sends traffic belonging to multiple security domains -- administration, storage, vMotion, customer -- and VMware recommended designs rightfully suggest implement four different forwarding domains in the physical network.

[^S1]: When a server uplink fails, vSwitch activates a backup interface for the virtual switch the overlay kernel interface is attached to. Unchanged underlay tunnel IP address thus appears on another server uplink, and if that uplink happens to be connected to a different ToR switch, you need the same subnet spanning multiple switches ([more details](/2020/02/do-we-need-complex-data-center-switches/)). That does NOT mean you need a VLAN spanning those switches, you could use tricks like host routing. [More details...](/kb/Layer3Fabrics/)

What's the easiest way to implement multiple forwarding domains in a modern data center fabric? Ask any vendor and they'll immediately reply EVPN with VXLAN (not a bad answer, I might skip the EVPN part but that's just me). The *underlay* network used by VMware NSX servers all of a sudden becomes an *overlay* fabric network that has to be implemented with another *underlay* network -- simple IP connectivity within the data center fabric. Does that mean you'll be running Geneve over VXLAN?[^1] Of course. Welcome to the modern world of infinite abstractions where bandwidth and CPU cycles seem to be free... or at least someone else is paying for them (hint: that would be you).

Could we bypass that second layer of abstraction and connect all servers straight to the physical IP fabric? Be extremely careful. VXLAN and Geneve are simple data-plane encapsulation schemes that [have absolutely no security](/2018/11/omg-vxlan-is-still-insecure/)[^2]. The moment someone gains access to the underlay network, they can inject any traffic into any overlay network[^3].

## To Recap

You should always start your design with "_What problem am I trying to solve?_" followed by "_What is the best tool for the job?_" Sometimes a stack of tunnels happens to be the least horrible option.

For more details, you might want to watch _[Overlay Virtual Networking](https://www.ipspace.net/Overlay_Virtual_Networking)_, _[VMware NSX Technical Deep Dive](https://www.ipspace.net/VMware_NSX_Technical_Deep_Dive)_, _[EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive)_ and _[Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)_ webinars.

## Revision History

2021-09-30
: Added a detailed explanation for the need of a single IP subnet spanning multiple ToR switches.

[^1]: To be precise, it will be Geneve-over-UDP-over-IP-over-Ethernet-over-VXLAN-over-UDP-over-IP.

[^2]: A fact promoted as an astonishing discovery to bedazzled attendees of security conferences... even though it's clearly stated in VXLAN RFC.

[^3]: Most tunneling mechanisms (apart from IPsec for obvious reasons) have the same limitations. MPLS is no better.
