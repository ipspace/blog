---
date: 2012-02-24 06:41:00+01:00
tags:
- SDN
- OpenFlow
- virtualization
title: Embrace the Change ... Resistance Is Futile ;)
url: /2012/02/embrace-change-resistance-is-futile.html
---
After all the [laws-of-physics-are-changing hype](/2011/03/open-networking-foundation-fabric.html) it must have been anticlimactic for a lot of people to realize what Nicira is doing (although [I've been telling you that for months](/2011/10/what-is-nicira-really-up-to.html)). Not surprisingly, there were the usual complaints and twitterbursts:
<!--more-->
-   It's just an overlay solution;
-   It's yet another tunneling protocol;
-   It doesn't have end-to-end QoS;
-   It's a simple solution using too-complex technology;
-   Why are they playing at the edge instead of solving the whole problem?

All of these complaints have merits \... and I've heard them at least three or four times:

-   When we started encapsulating SNA in TCP/IP using RSRB and later DLSw;
-   When we started replacing voice switches with VoIP and transporting voice over IP networks;
-   When we replaced Frame Relay and ATM switches with MPLS/VPN.

{{<note>}}Interestingly I don't remember a huge outcry when we started using IPsec to build private networks over the Internet \... maybe the immediate cost savings made everyone forget we were actually building tunnels with no QoS.{{</note>}}

Anyhow, we've proven time and again in the last 20+ years that the only way to scale a networking solution is to [push the complexity to the edge](/2011/05/complexity-belongs-to-network-edge.html) and to decouple edge from the core (in case of virtual networks, [decouple them from the physical ones](/2011/12/decouple-virtual-networking-from.html)).

Assuming one could design the whole protocol stack from scratch, one could do a proper job of eliminating all the redundancies. Given the fact that the only ubiquitous transport we have today is IP, and that you can't expect the equipment vendors to invest into anything else but Ethernet+IP in the foreseeable future, the only logical conclusion is to use IP as the transport for your virtual networking data \... like any other application is doing these days. It obviously works well enough for Amazon.

You have to use transport over IP if you want the solution to scale \... or a completely revamped layer-2 forwarding paradigm, which is not impossible, merely impractical in a reasonable timeframe \... but of course OpenFlow will bring us there ;)

I'm not saying Nicira's solution is the right one. I'm not saying GRE or VXLAN or NVGRE or something else is the right tunneling protocol. I'm not saying transporting Ethernet frames in IP tunnels is a good decision -- I would prefer to have full IP routing in the hypervisors and transport IP datagrams, not L2 frames, between hypervisor hosts. I'm also not saying IP is the right transport protocol, it's just the only scalable one we have today.

However, I'm positive that the only way to build scalable virtual networks is to:

-   [Split hypervisor host addressing (which is visible in the core) from VM addressing](http://networkheresy.wordpress.com/2012/01/15/networking-needs-a-vmware-part-1-address-virtualization/) (which is only visible to hypervisors);
-   Use simple routed core transport which allows the edge (hypervisor) addresses to be aggregated for scalability;
-   Remove all VM-related state from the transport core;
-   Use [proper control plane](/2011/12/vxlan-ip-multicast-openflow-and-control.html) that will minimize the impact of stupidities we have to deal with if we have to build L2 virtual networks.

But, as always, this is just my personal opinion, and I\'m known to be biased toward things that [work in reality not in PowerPoint](/2011/09/long-distance-irf-fabric-works-best-in.html).
