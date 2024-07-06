---
anycast_tag: design
date: 2021-02-24 07:48:00+00:00
series:
- anycast
tags:
- switching
- design
title: Routing in Stretched VLAN Designs
---
One of my readers was "blessed" with the *stretched VLANs* requirement combined with the need for inter-VLAN routing and sub-par equipment from a vendor not exactly known for their data center switching products. Before going on, you might want to [read his description of the challenge he's facing](/2011/09/long-distance-irf-fabric-works-best-in.html#380) and what I had to say about the [idea of building stackable switches across multiple locations](/2011/09/long-distance-irf-fabric-works-best-in.html).

{{<note>}}Of course it's possible that my reader failed to explain the challenge in enough details to get good advice from the vendor SE, or that he had to deal with a clueless SE, or that he's using ancient gear or that the stars just weren't aligned... but I don't think anyone should ever be painted into the corner he found himself in.{{</note>}}

Here's an overview diagram of what my reader was facing. The core switches in each location work as a single device (virtual chassis), and there's MLAG between core and edge switches. The early 2000s just called and they were [proud of the design](/2020/03/should-i-go-with-vxlan-or-mlag-with-stp.html) (but to be honest, sometimes one has to work with the tools his boss bought, so...).
<!--more-->
{{<figure src="sr-overview.png" caption="Overview diagram">}}

To make it even more interesting, the whole network is a set of giant VLANs potentially stretching across all edge and core switches. Of course that makes it a [single failure domain](/2012/05/layer-2-network-is-single-failure.html), but that's the least of my reader's worries.

When my reader wanted to implement inter-VLAN routing he faced the usual challenge: where should the first-hop router be? The "traditional" designs (remember: early 2000s are still on the line enjoying the show) would run some first-hop redundancy protocol between the two core switch clusters and select one of the clusters (or even one of the boxes within one of the clusters) as the active router:

{{<figure src="sr-single-router.png" caption="Single core switch is an active router">}}

Most networking vendors "discovered" years ago what the correct solution is: anycast gateway, either properly implemented ([Arista](/2013/05/optimal-l3-forwarding-with-varp-and.html) and [Enterasys](/2013/08/optimal-layer-3-forwarding-with.html) had it years before anyone else) or faked with dirty tricks like HSRP filtering.

{{<figure src="sr-anycast-gateway.png" caption="All core switches are active first-hop routers">}}

{{<note info>}}Of course it would be even better to have anycast gateways on edge (ToR) switches, and VXLAN running in the fabric core, but that's a different story.{{</note>}}

The solution my reader implemented was something completely different: let's stretch the virtual chassis across both data centers (ignoring that one data center will be dead if the DCI link ever fails)... because then the first packet (in a flow? between a pair of IP addresses?) would go through the master switch (that also acts like a router), but then the master switch would install a flow entry in all other switches, and the rest of the traffic would use that shortcut.

{{<figure src="sr-stretched-chassis.png" caption="Stretched stackable switch with conversational learning">}}

At that point, 1990s joined the call with fond memories of early Catalyst 5000 multi-layer switching implemented with a router sitting on top of that switch, or as RFC 1925 says...

> Every old idea will be proposed again with a different name and a different presentation, regardless of whether it works.

**Long story short:**

* Try to avoid broken designs (VLANs stretched across multiple locations). There might be a better option; [Building Active-Active Data Centers](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar has some more details.
* Figure out what problem you're solving (inter-VLAN routing) and what's the best way to solve it (anycast first-hop gateway). Our [Leaf-and-Spine Fabrics](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar might help.
* Use the tools that solve the problem the right way. I know that's impossible in some environments, but in that case it's time to start polishing your resume. As Ethan Banks pointed out in a recent blog post, more organizations are amenable to remote work than ever.