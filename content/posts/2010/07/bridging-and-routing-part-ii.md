---
date: 2010-07-22 07:23:00.003000+02:00
tags:
- bridging
- data center
- workshop
- IP routing
- TRILL
title: Bridging and Routing, Part II
url: /2010/07/bridging-and-routing-part-ii/
---
Based on the readers' comments on my "[*Bridging and Routing: is there a difference?*](/2010/07/bridging-and-routing-is-there/)*"* post (thanks you!), here are a few more differences between bridging and routing:

**Cost.** Layer-2 switches are almost always cheaper than layer-3 (usually combined layer-2/3) switches. There are numerous reasons for the cost difference, including:
<!--more-->
-   Mass-market low-end switches are usually simple bridges. Low-cost high-speed bridging silicon is thus readily available.
-   MAC address lookup is simpler than IP table lookup and easier to implement in silicon. You need simple CAM ([Content Addressable Memory](http://en.wikipedia.org/wiki/Content-addressable_memory)) to perform MAC address lookup and TCAM] (Ternary CAM) with additional output logic to perform longest-IP-prefix matching.
-   Layer-3 switches are expected to perform IP packet filtering. Implementing access lists in hardware (usually with even larger TCAM) is expensive.

**Zero configuration.** In their simplest incarnation, the bridges are plug-and-play devices (magically [transforming themselves into plug-and-pray devices as the network grows](/2009/12/ten-steps-of-small-lan-design/)); it's quite easy to find a perfectly working switch named *Switch* with no non-default configuration in a badly managed network. Routers always require configuration (at the very minimum, you have to configure IP subnets and IP routing protocols).

However, as soon as VLANs are introduced into the network or you need to fine-tune STP, the zero-configuration benefits are gone.

**Equal-cost multipath.** Routers can load-balance traffic between equal-cost paths across the network. Bridges can load-balance traffic between parallel bonded links (port channel). Redundant paths in bridged networks are disabled to prevent forwarding loops.

Enhancements to port channel technology (VSS and vPC) allow links connected to multiple switches to be bonded. TRILL (and similar technologies) solves the problem, allowing unrestricted equal-cost multipath.

**Security.** Packet filters between IP subnets are a standard feature of every decent router, allowing the network designer to segment the network into security zones.

Some layer-2 switches have similar functionality (port ACL), which turns a L2 switch into a layer-3-aware L2 device, increasing configuration and troubleshooting complexity.

**Predictability.** L3 forwarding tables are modified only by the [control plane](/2013/08/management-control-and-data-planes-in/) (routing) protocols based on messages exchanged by the routers, not by the data traffic flow. L2 forwarding tables are modified on-the-fly by the data plane snooping functionality based on source MAC addresses in the frames forwarded by the switch.

**Troubleshooting.** It's impossible to troubleshoot a bridged network from an end-host; the network is designed to be invisible. The error reporting mechanisms built into most L3 protocols allow an end-host to trace a path across the network, giving the network operator at least an initial snapshot of the network conditions and a troubleshooting starting point.

**End-host mobility.** The source MAC address snooping (which makes the bridged networks less predictable) allows instant host mobility -- as soon as the host is attached to another network segment and sends a broadcast (a gratuitous ARP is a perfect candidate), all bridges readjust their L2 forwarding tables.

You can implement seamless host mobility in a routed network, but the delay is much higher, as the dissemination of changed information is done by the routing protocol.

**Impact of link failure.** Link failure in a routed network results in temporary loss of traffic forwarded over that link (until routing protocol convergence). Link failure in a bridged network running STP can impact unrelated parts of the network.

TRILL uses a routing protocol (IS-IS); a network built with TRILL RBridges behaves like a routed network.

**Impact of** **physical errors.** Most layer-3 routing protocols detect unidirectional links and wiring errors (which usually result in subnet mismatch errors). The same conditions can easily result in a forwarding loop in a bridged network, unless you use [UDLD and bridge assurance](http://www.netcordia.com/community/blogs/terrys_blog/archive/2010/01/06/what-is-bridge-assurance.aspx).

TRILL and other similar technologies no longer have this problem, as they use a routing protocol inside the network.

**Impact of network overload.** When a L2 switch is overloaded to the point where it stops sending STP packets (for example, due to data plane overload impacting control plane functionality), remote switches might unblock their ports, resulting in a forwarding loop and a total network meltdown.

When a router stops sending routing protocol hello packets, other routers detect a dead neighbor and recomputed the network topology (not necessarily resulting in a working network, but at least they're not aggravating the problem).

Bridge assurance solves this issue, as does TRILL.

**Size of fault domain.** Whole bridged network is a single fault domain (a fault anywhere in the network can impact the rest of it). A fault domain in a routed network is a single subnet.

The *fault domain* issue is usually related to the behavior of STP, but extends to the forwarding plane as well. A [single misbehaving host attached to a bridged network can affect the whole network](/2012/05/layer-2-network-is-single-failure/).

**Anything else?** Have I still missed something? Leave a comment!

You'll find an even more comprehensive discussion of this topic in *[Switching, Routing and Bridging](https://my.ipspace.net/bin/list?id=Net101#SWITCH)* part of *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar.
