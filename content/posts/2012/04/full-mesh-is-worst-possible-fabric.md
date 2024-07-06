---
date: 2012-04-16 07:35:00+02:00
tags:
- design
- data center
- fabric
title: Full Mesh Is the Worst Possible Fabric Architecture
url: /2012/04/full-mesh-is-worst-possible-fabric.html
---
One of the answers you get from some of the vendors selling you *data center fabrics* is "you can use any topology you wish" and then they start to rattle off an impressive list of buzzword-bingo-winning terms like *full mesh,* [*hypercube*](http://en.wikipedia.org/wiki/Hypercube) and *Clos fabric*. While *full mesh* sounds like a great idea (after all, what could possibly go wrong if every switch can talk directly to any other switch), it's actually the worst possible architecture (apart from the fully randomized [Monkey Design](/2012/04/monkey-design-still-doesnt-work-well.html)).

{{<note info>}}Before reading the rest of this post, you might want to visit [*Derick Winkworth's The Sad State of Data Center Networking*](http://packetpushers.net/the-sad-state-of-data-center-networking/) to get in the proper mood.{{</note>}}
<!--more-->
Imagine you just bought a bunch (let's say eight, to keep the math simple) of typical data center switches. Most of them [use the same chipset today](http://etherealmind.com/merchant-silicon-vendor-software-rise-lost-opportunity/), so you probably got 48x10GE ports and 4x40GE ports[^2020] that you can split into 16x10GE ports. Using the pretty standard 1:3 oversubscription, you dedicate 48 ports for server connections and 16 ports for intra-fabric connectivity ... and you wire them in a full mesh (next diagram), giving you 20 Gbps of bandwidth between any two switches.

[^2020]: ... or 48 x 25GE ports and 4 x 100GE ports if you're reading this is 2020s

{{<figure src="/2012/04/s1600-FM_Mesh.jpg" caption="Full mesh between leaf switches">}}

Guess what ... unless you have a perfectly symmetrical traffic pattern, you've just wasted most of the intra-fabric bandwidth. For example, if you're doing a lot of [vMotion](/2010/09/vmotion-elephant-in-data-center-room.html) between servers attached to switches A and B, the maximum throughput you can get is 20 Gbps (even though you have 160 Gbps of uplink bandwidth on every single switch).

{{<note>}}Remember that most routing protocols (and thus most data center fabric technologies) use *equal cost multipath*. You could try getting unequal-cost multipathing with LFA, MPLS or SR-MPLS traffic engineering. I wish you luck but will walk away before your design collapses under its own complexity.{{</note>}}

Now let's burn a bit more budget: buy two more switches with 40GE ports, and wire all ten of them in a Clos fabric. You'll get 80 Gbps of uplink bandwidth from each edge switch to each core switch.

{{<figure src="/2012/04/s1600-FM_Clos.jpg" caption="Clos fabric">}}

Have we gained anything (apart from some goodwill from our friendly vendor/system integrator)?

Actually we did -- using the Clos fabric you get a maximum of 160 Gbps between any pair of edge switches. Obviously the maximum amount of traffic any edge switch can send into the fabric or receive from it is still limited to 160 Gbps[^UBO], but we're no longer limiting our ability to use all available bandwidth.

[^UBO]: Unless you use [unicorn-based OpenFlow](/2011/03/open-networking-foundation-fabric.html)  powered by tachyons.

Now shake the whole thing a bit, let the edge switches "fall to the floor" and you have the traditional 2-tier data center network design. Maybe we weren't so stupid after all ...

{{<figure src="/2012/04/s1600-FM_2Tier.jpg" caption="Leaf-and-spine fabric">}}

## More Information

Since publishing this blog post I created a whole series of webinars on [data center fabrics](http://www.ipspace.net/Data_Center_Fabrics), [leaf-and-spine fabric architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures), and [EVPN](http://www.ipspace.net/EVPN_Technical_Deep_Dive).

## Revision History

2023-01-15
: Mentioned 25GE/100GE ports and cleaned up the wording.