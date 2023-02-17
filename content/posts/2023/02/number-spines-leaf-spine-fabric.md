---
title: "How Many Spines Should a Leaf-and-Spine Fabric Have?"
date: 2023-02-23 07:18:00
tags: [ fabric, design ]
---
One of my readers sent me a question along these lines:

> How do we determine the number of spines needed in a leaf-and-spine fabric? It's easy to calculate the number of leaf nodes from the required number of server ports, and two spines give you the redundancy. Does it make sense to have more spines if two are good enough from the capacity perspective?

There are at least two factors to consider:
<!--more-->
* Required number of ports (based on the number of leaf switches)
* Required level of redundancy (two spines or more than two spines)

For example, assuming you have four uplinks per leaf switch (a typical configuration), you could have two, three, or four spines. Assuming you have 32 ports on a spine switch (yet again, a pretty typical configuration), you could connect up to 16 leafs to 2 spines (connecting two leaf switch uplinks to each spine), beyond that you need four spines. You could also use three spines if you're OK with an unused uplink and the resulting somewhat higher oversubscription ratio.

However, more than two spines give you better redundancy. With two spines you’re always at a risk of one spine crashing while you’re working on the other -- any change requires a maintenance window outside of business hours. With more than two spines, you can do changes or software upgrades on spine switches during the regular business hours. Your life will be even easier if you buy spine switches that support graceful shutdown and maintenance mode.

Finally, in the good old days it was recommended to have two or four spines based on equal-cost multipathing (ECMP) implementations. With the modern ASICs that support 64-way ECMP (or better) it’s perfectly OK to have three spines if that works for you.

For more details, watch the [physical fabric design](https://my.ipspace.net/bin/list?id=Clos#PHY_TOPOLOGY) part of [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar, and the [advanced routing protocol topics](https://my.ipspace.net/bin/list?id=Net101#ADV_ROUTING) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.
