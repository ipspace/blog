---
title: "Building a Small Data Center Fabric with Four Switches"
date: 2021-09-23 06:37:00
tags: [ data center, fabric, design ]
---
One of my subscribers has to build a small data center fabric that's just a tad too big for [two switch design](https://www.ipspace.net/Optimize_Data_Center_Infrastructure/Build_an_Optimized_Fabric).

> For my datacenter I would need two 48 ports 10GBASE-T switches and two 48 port 10/25G fibber switches. So I was watching the *[Small Fabrics and Lower-Speed Interfaces](https://my.ipspace.net/bin/get/Clos/2.1%20-%20Small%20Fabrics%20and%20Lower-Speed%20Interfaces.mp4?doccode=Clos)* part of *[Physical Fabric Design](https://my.ipspace.net/bin/list?id=Clos#PHY_TOPOLOGY)* to make up my mind. There you talk about the possibility to do a leaf and spine with 4 switches and connect servers to the spine.

A picture is worth a thousand words, so here's the diagram of what I had in mind:
<!--more-->
{{<figure src="/2021/09/4-switch-fabric.png" caption="Four Switch Fabric">}}

Although a four-switch fabric does look like a leaf-and-spine fabric if you squint hard enough it's not. It's just four switches with a full mesh of links between them, and although [full mesh does happen to be the worst possible fabric architecture](/2012/04/full-mesh-is-worst-possible-fabric.html) it's good enough for this particular use case assuming the traffic requirements aren't too high.

Talking about traffic requirements -- my subscriber also wondered if it's worth optimizing server connectivity:

> Wouldn't it be better to connect all servers to all switches (with four uplinks) in such a way that we reduce the distance between servers?

I think that’s over-complicating the design. Most small fabrics won’t have traffic- or latency requirements that would justify that kind of connectivity. Also, assuming you really needed four switches in the first place, you'd run out of switch ports.

For more details, watch the _[Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures)_ webinar.
