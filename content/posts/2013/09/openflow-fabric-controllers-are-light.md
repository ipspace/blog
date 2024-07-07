---
date: 2013-09-09 14:25:00+02:00
distributed-systems_tag: openflow
series:
- distributed-systems
tags:
- SDN
- data center
- OpenFlow
title: OpenFlow Fabric Controllers Are Light-years Away from Wireless Ones
url: /2013/09/openflow-fabric-controllers-are-light/
---
When talking about OpenFlow and the whole idea of controller-based networking, people usually say "well, it's nothing radically new, we've been using wireless controllers for years and they work well, so the OpenFlow ones will work as well."

Unfortunately, the comparison is totally misleading.
<!--more-->
While OpenFlow-based data center fabrics and wireless controller-based networks look very similar on a high-level PowerPoint diagram, in reality they're light-years apart. Here are just a few dissimilarities that make OpenFlow-based fabrics so much more complex than the wireless controllers.

### Topology Management

Wireless controllers work with the devices on the network edge. A typical wireless access point has two interfaces: a wireless interface and an Ethernet uplink, and the wireless controller isn't managing the Ethernet interface or any control-plane protocols that interface might have to run. The wireless access point communicates with the controller through an IP tunnel and expects someone else to provide IP connectivity, routing and failure recovery. The underlying physical topology of the network is thus totally abstracted and invisible to the wireless controller.

Data center fabrics are built from high-speed switches with tens of 10/40GE ports, and the OpenFlow controller must manage topology discovery, topology calculation, flow placement, failure detection and fast rerouting. There are zillions of things you have to do in data center fabrics that you never see in a controller-based wireless network.

### Traffic Flow

In traditional wireless networks all traffic flows through the controller (there are [some exceptions](http://www.insearchoftech.com/2013/07/21/another-controller-less-wi-fi-solution/), but let's ignore them for the moment). The hub-and-spoke tunnels between the controller and the individual access points carry all the user traffic and the controller is doing all the smart forwarding decisions.

In an OpenFlow-based fabric the controller should do a minimal amount of data-plane decisions (ideally: none) because every time you have to [punt packets to the controller](/2013/03/controller-based-packet-forwarding-in/), you reduce the overall network performance (not to mention the dismal capabilities of today's switches when they have to do CPU-based packet forwarding across an SSL session).

### Amount of Traffic

Wireless access points handle megabits of traffic, making a hub-and-spoke controller-based forwarding a viable alternative.

Data center fabrics are usually multi-terabit structures (every single pizza-box ToR switch has over a terabit of forwarding capacity) -- three to four orders of magnitude faster than the wireless network we're comparing them with. Controller-based forwarding is totally unrealistic.

### Forwarding Information

In a traditional controller-based wireless network, the access point forwarding is totally stupid -- the access points forward the data between directly connected clients (if allowed to do so) or send the data received from them into the IP tunnel established with the controller (and vice versa). There's no forwarding state to distribute; all an access point needs to know are the MAC addresses of the wireless clients.

In an OpenFlow-based fabric the controller must distribute as much forwarding, filtering and rewriting (example: decrease TTL) information as possible to the OpenFlow-enabled switches to minimize the amount of traffic flowing through the controller.

Furthermore, smart OpenFlow controllers build forwarding information in a way that allows the switches to cope with the link failures (the controller has to install backup entries with lower matching priority); you wouldn't want to have an overloaded controller and burnt-out switch CPU every time a link goes down, network topology is lost, and the switch (in deep panic) forwards all the traffic to the controller.

The functionality of a good OpenFlow controller that proactively pre-programs backup forwarding entries (example: NEC ProgrammableFlow) is very similar to MPLS Traffic Engineering with Fast Reroute; you cannot expect its complexity to be significantly lower than that.

### Real-time Events

User roaming is the only real-time event in a controller-based wireless network (remember: access point uplink failure is not handled by the controller). Access points do most of the work on their own (the expected behavior is specified in IEEE standards anyway), and the controller just updates the MAC forwarding information. The worst thing that can happen if the controller is too slow is a slight delay experienced by the user (noticeable only on voice calls and by players of WoW sessions running around large buildings).

The other near-real-time wireless event is user authentication, which often takes seconds (or my wireless network is severely misconfigured). Yet again, nothing critical; the controller can take its time.

In data center fabrics, you have to react to a failure in milliseconds and reprogram the forwarding entries on tens of switches (unless you know what you're doing and already installed the pre-computed backup entries -- see above).

### Frequency of Real-Time Events

Wireless controllers probably handle between tens and few hundreds real-time events per second (unless you had a power glitch and every user wants to log into the network at the same time).

OpenFlow controllers that implement flow-based forwarding (flow entries are downloaded into the switches for each individual TCP/UDP session -- a patently bad idea if I ever saw one) are designed to handle millions of flow setups per second (not that the physical switches could take that load).

### Summary

As you can see, wireless controllers have nothing to do with OpenFlow controllers; they aren't even remotely similar in requirements or complexity (the only exception being OpenFlow controllers that program just the network edge, like VMware NSX-T when used with Open vSwitch on Linux hosts).

Comparing the two is misleading and hides the real scope of the problem; no wonder some people would love you to believe otherwise because that makes selling the controller-based fabrics easier. In reality, an OpenFlow controller managing a physical data center fabric is a complex piece of real-time software, as anyone who tried to build a high-end switch or router has learned the hard way.
