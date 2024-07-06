---
date: 2016-03-01 12:10:00+01:00
tags:
- bridging
- data center
- fabric
title: Spanning Tree Protocol (STP) and Bridging Loops
url: /2016/03/spanning-tree-protocol-stp-and-bridging.html
---
Continuing our [bridging loops](/2016/02/vlans-and-failure-domains-revisited.html) discussion [Christoph Jaggi](http://uebermeister.com/about.html) sent me another question:

> Theoretically STP should avoid bridging loops, and yet you claim they cause data center meltdowns. What am I missing?

In theory, STP avoids bridging loops. In practice, there are numerous reasons STP got a bad name.
<!--more-->
**Blocked alternate paths**. That's a design choice you have to accept if you want to have plug-and-pray networking instead of proper routing protocols. Not much we can do here.

{{<note info>}}It doesn't matter if you're doing routing on layer-2 (TRILL, SPB) or on layer-3 (IP) -- you need a proper routing protocol to use alternate paths.{{</note>}}

**Forward-on-failure** **behavior**. This is the only real grudge I have against STP as protocol -- all links forward traffic until BPDUs cause some of them to be blocked.

If you insert a device that drops BPDUs in the forwarding path, or if a [switch loses its control plane](/2014/07/is-stp-really-evil.html) (for example, due to a memory leak), a forwarding loop is almost guaranteed.

A unidirectional link (due to bad transceiver or cable) could also result in a forwarding loop when the bridge that should have put the link in blocking state doesn't receive the BPDUs (thanks to Antonio Ojea for pointing this out).

**Slow link establishment**. Vanilla STP waits 30 seconds before it starts forwarding traffic onto a link, and vendors ignorant of how networks work [start sending their precious traffic](/2014/08/stp-and-expert-beginners.html) as soon as they see layer-1 carrier on a server NIC, forcing networking vendors to implement all sorts of kludges like **portfast** and **bpduguard**.

**The kludges implemented by networking vendors are not reliable**. For example, [BPDU Guard kicks in after the first BPDU is received](/2012/04/stp-loops-strike-again.html), potentially resulting in a temporary forwarding loop before the first BPDU reaches the switch.

**Too many kludges cause configuration errors**. Understanding all possible kludges vendors implemented around STP and the relationship between them is hard, and even [the big guys sometimes get it wrong](/2015/06/another-spectacular-layer-2-failure.html).

**Virtualization vendors drop BPDU frames**. What could possibly go wrong if someone configures bridging between two VM NICs? It's definitely better to pretend it's someone else's problem and blame the network instead of explaining to the sysadmin why his VM was kicked off the virtual switch after he made a stupid configuration error.

**Some** **fabric** **vendors ignore(d)** **STP** and [propagate(d) BPDUs across the fabric](/2011/05/ignoring-stp-be-careful-be-very-careful.html), dramatically increasing the blast radius of any misconfiguration.

### Want to Know More?

[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work), [Data Center Infrastructure for Networking Engineers](https://www.ipspace.net/Data_Center_Infrastructure_for_Networking_Engineers) and [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinars discuss large-scale bridging and routing on layer-2, including SPB, TRILL, VXLAn and EVPN.