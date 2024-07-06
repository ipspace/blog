---
date: 2015-06-16 07:56:00+02:00
distributed-systems_tag: openflow
series:
- distributed-systems
tags:
- SDN
- OpenFlow
title: Centralized Control Is Not Centralized Control Plane
url: /2015/06/centralized-control-is-not-centralized.html
---
Every other week I stumble upon a high-level SDN article that repeats the misleading *SDN is centralized control plane* mantra (often copied verbatim from the [Wikipedia article on SDN](https://en.wikipedia.org/wiki/Software-defined_networking), sometimes forgetting to quote the source).

Yesterday, I had enough and decided to respond.
<!--more-->
{{<note>}}The original response is in quotes; I wrote additional explanations so I'll be able to quote this blog post in future.{{</note>}}

> Would everyone **please** get the terminology right? Central controller (or centralized visibility or central policy engine) is **not** centralized control plane.

Control plane in network devices (or distributed systems) is a well-defined concept that implements not only routing protocols (as is commonly understood), but also real-time protocols like spanning tree BPDU, LACP, link failure detection mechanisms like BFD and UDLD and even host-to-network protocols like ARP. More details in:

-   [Management, Control and Data Planes in Network Devices and Systems](/2013/08/management-control-and-data-planes-in.html)
-   [What Exactly Is the Control Plane?](/2013/10/what-exactly-is-control-plane.html)
-   [Control Plane in OpenFlow Networks](/2013/12/control-plane-in-openflow-networks.html)
-   [Implementing Control-Plane Protocols with OpenFlow](/2013/06/implementing-control-plane-protocols.html)

> The former makes perfect sense, particularly when combined with business-as-usual distributed forwarding to augment its behavior, the latter makes absolutely no sense in real world, no matter what its proponents claim.

Centralized control, be it configuration or policy management, traffic engineering or exception routing (aka PBR) significantly simplifies hard-to-solve problems that benefit from centralized visibility. Controller-based networks (or orchestration systems if you prefer that terminology) have a bright future. They also have a long history -- there are numerous home grown or commercial products that implemented some variant of centralized control for decades (example: Cariden MATE or service provisioning systems).

Centralized control plane (implementing a reasonably complete set of control-plane protocols, including host-to-network protocols and fast failure discovery) cannot scale, as every implementer of a commercial OpenFlow-based product had to admit sooner or later. Let me just list a few examples:

-   NEC pushed the envelope the furthest with their ProgrammableFlow controller, but only because they decided not to implement most control-plane protocols;
-   Nicira was using OpenFlow in their Network Virtualization Platform (NVP), but [deviated from it the moment they had to implement layer-3 forwarding and ARP](/2013/11/layer-2-and-layer-3-switching-in-vmware.html). Subsequent Linux networking software from the Nicira team (Open Virtual Networking) used a combination of centralized policy and forwarding information distribution with local intelligence (on-host agent);
-   Big Switch Networks got a scalable product only when they [deviated from the pure concepts of OpenFlow and centralized control plane](/2015/02/big-cloud-fabric-scaling-openflow-fabric.html), and implemented control-plane protocols locally;
-   HP decided to [use OpenFlow to augment traditional distributed forwarding](/2015/05/openflow-in-hp-campus-solutions-on.html), not replace it, because (in their own words) that's the only architecture that makes sense;
-   Even Google (in its OpenFlow-based WAN network) [used centralized control plane within a single WAN edge node](/2012/05/openflow-google-brilliant-but-not.html) (a tightly-coupled leaf-and-spine fabric), while relying on traditional routing protocols between WAN edge nodes.

At this point it's worth noting that all traditional centralized networks (Frame Relay, SDH/SONET, even SNA) always contained some local intelligence, *because that's the only approach that scales*.

{{<note>}}Please note that this argument has nothing to do with OpenFlow. Any system with centralized control plane failed to scale, starting with Ipsilon Networks and Cisco's Multi Layer Switching.{{</note>}}

### Further Reading

-   [Is Controller-Based Networking More Reliable than Traditional Networking?](/2015/01/is-controller-based-networking-more.html)
-   [Control and Data Plane Separation -- Three Years Later](/2014/01/control-and-data-plane-separation-three.html)
-   [What Exactly Is SDN -- and Does It Make Sense?](/2014/01/what-exactly-is-sdn-and-does-it-make.html)
-   [The Four Paths to SDN](/2014/09/the-four-paths-to-sdn.html)
-   [OpenFlow Fabric Controllers Are Light-Years Away From Wireless Ones](/2013/09/openflow-fabric-controllers-are-light.html)

Product-specific blog posts:

-   [Big Cloud Fabric: Scaling an OpenFlow Fabric](/2015/02/big-cloud-fabric-scaling-openflow-fabric.html)
-   [Layer-2 and Layer-3 Switching in VMware NSX](/2013/11/layer-2-and-layer-3-switching-in-vmware.html)
-   [There's a Difference Between Scaling and not Being Stupid](/2015/04/theres-difference-between-scaling-and.html)
-   [OpenFlow in HP Campus Solutions](/2015/05/openflow-in-hp-campus-solutions-on.html)
-   [OpenFlow @ Google: Brilliant but not Revolutionary](/2012/05/openflow-google-brilliant-but-not.html)

You might also want to explore my other [SDN](/tag/sdn.html)- and [OpenFlow](/tag/openflow.html)-related blog posts.

For even more details, explore my [SDN webinars and other SDN resources](http://www.ipspace.net/SDN):

-   Start with the free [Introduction to SDN](http://www.ipspace.net/Introduction_to_SDN) pack;
-   Explore [SDN architectures](http://www.ipspace.net/SDN_Architectures_and_Deployment_Considerations) and their scalability challenges;
-   Find out all the [details of the OpenFlow protocol](http://www.ipspace.net/OpenFlow_Deep_Dive);
-   Get 20+ hours of SDN and network automation content with [Advanced SDN training](http://www.ipspace.net/Advanced_SDN_Training).
