---
date: 2010-10-18 06:39:00.003000+02:00
mlag_tag: implement
series:
- mlag
tags:
- link aggregation
- data center
title: 'Multi-chassis Link Aggregation: Stacking on Steroids'
url: /2010/10/multi-chassis-link-aggregation-stacking.html
---
In the [*Multi-chassis Link Aggregation* *(MLAG)* *Basics*](/2010/10/multi-chassis-link-aggregation-basics.html) post I've described how you can use (usually vendor-proprietary) technologies to bundle links connected to two upstream switches into a single logical channel, bypassing the Spanning Tree Protocol (STP) port blocking. While every vendor takes a different approach to MLAG, there are only a few architectures that you'll see. Let's start with the most obvious one: *stacking on steroids*.
<!--more-->
### The Basics

Low-end devices have provided multi-chassis link aggregation for a long time and nobody realized it's a big deal. After all, a *stackable switch* is just a stackable *switch*; in opinion of many networking engineers that's not necessarily a sin, but neither is it something to be very proud about.

When the vendors decided to introduce the same mentality to the core Data Center switches, they couldn't say "_well, we just made our core switches stackable_"; their marketing department had to invent a fancy name for the technology, be it _Virtual Switching System_ (Cisco) or _Intelligent Resilient Framework_ (HP).

Regardless of the branding efforts, the architecture of VSS/IRF solution still looks and feels like a stackable switch: you take X independent boxes (X = 2 in VSS case) and turn all but one brain (= control plane) off. Distributed switching subsystems add some spice (= complexity) to the mix. For example, in a VSS system, the SUP blade in the secondary chassis still controls its switching fabrics.

{{<figure src="/2010/10/s400-vss1.png" caption="VSS Architecture Overview">}}

With all the control planes but one gone into self-induced coma (vendors prefer the term *standby*), it's easy to implement link aggregation. After all, the primary control plane receives all control packets (including LACP and STP messages) and directly or indirectly (through standby control planes) controls the switching fabrics in the whole system.

The traffic flow across the whole stacked system is usually optimal. Consider, for example, the following diagram:

{{<figure src="/2010/10/s320-vss2.png" caption="Typical VSS deployment">}}

When server A sends a packet to server B through the Primary switch, the Primary switch automatically updates its own MAC address table and the MAC address table on the Standby switch (both entries for MAC address A point to local links in the port channel with server A). When server B sends a subsequent packet to server A it uses the optimal path and does not traverse the inter-switch link.

{{<figure src="/2010/10/s320-vss3.png" caption="MAC table synchronization in VSS cluster">}}

### Schizophrenia

The worst scenario in any stackable solution is a split-brain failure -- the link between the primary switch and standby switches is lost while the access links remain operational.

In a pure layer-2 solution, split-brain failure is not necessarily a disaster. The standby switch discovers the primary switch is gone, becomes independent (causing, among other things, STP topology change) and tries to renegotiate port channels (Cisco's name for *link aggregation groups* -- LAG) with a different switch ID, which causes a port channel failure. Depending on how the connected switches implement port channels, they could split the port channel in two independent links (and STP would block one of them) or shut down half of the links in the port channel.

Layer-3 split brain event is a cataclysm. All of a sudden you have two routers with the same set of IP addresses and same router IDs in your network. Try to imagine what that does to your ARP caches and routing protocol and how long the post-traumatic effects will linger after you manage to shut down one of the switches (in case of OSPF, up to one hour).

{{<figure src="/2010/10/s400-vss4.png" caption="Layer-3 split brain is a disaster">}}

### Read the Smallprint

If a vendor tells you virtual device partitioning is not a problem, run away... or ask them how they handle layer-3 problems, grab some popcorn, lean back, and enjoy the show.

The methods vendors use to deal with detecting and recovering from device partitioning tells you a lot about their commitment to the stability of your network. Don't be dazzled by the flamboyant approaches like "_this can never happen_"; personally I prefer to see someone who thought seriously about the problem and tried hard to detect it and recover from it (even though we agree it should never happen).

Consider, for example, [design recommendations and dual-active detection technologies used by Cisco's VSS](https://web.archive.org/web/20111102151821/http://www.cisco.com/en/US/docs/solutions/Enterprise/Data_Center/DC_3_0/DC-3_0_IPInfra.html) (a stack of Catalyst 6500s):

-   You should use multiple physical links bundled into a channel for the Virtual-Switch Link (VSL);
-   Apart from VSL, there should be an independent keepalive link between the switches.
-   BFD is run on the keepalive link to distinguish between switch failure and VSL failure;
-   If you have Cisco's switches connected to the VSS complex, you can run Enhanced Port Aggregation Protocol (EPagP) across some port channels to allow the VSS switches to communicate across access switches.

As for what happens when the dual-active condition is detected, Cisco is yet again quite honest: the primary switch is immediately restarted (assuming the standby switch has already transitioned into an active role).
