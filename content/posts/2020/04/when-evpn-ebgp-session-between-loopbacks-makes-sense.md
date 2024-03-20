---
date: 2020-04-29 07:12:00+00:00
dcbgp_tag: design
evpn_tag: design
series:
- dcbgp
series_weight: 550
tags:
- EVPN
- BGP
- design
title: When EVPN EBGP Session between Loopbacks Makes Sense
---
One of the attendees of our [Building Next-Generation Data Center](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course submitted a picture-perfect solution to scalable layer-2 fabric design challenge:

* VXLAN/EVPN based data center fabric;
* IGP within the fabric;
* EBGP with the WAN edge routers because they’re run by a totally different team and they want to have a policy enforcement point between the two;
* EVPN over IBGP within the fabric;
* EVPN over EBGP between the fabric and WAN edge routers.

The only seemingly weird decision he made: he decided to run the EVPN EBGP session between loopback interfaces of core switches (used as BGP route reflectors) and WAN edge routers.
<!--more-->
{{<figure src="/2020/04/EVPN-EBGP-Loopback-Design.jpg" caption="EBGP EVPN session between loopback interfaces" >}}

Regular readers of my blog probably know [how I feel about that solution](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics), and so I politely asked him what made him do that. He came back with an interesting explanation:

* At the moment there’s a single link between a core switch and a WAN edge router, but they might have to go to parallel links when the traffic increases;
* He could use MLAG or routed interfaces between core switches and WAN edge routers;
* With MLAG he’d have a single routed interface, and it would make sense to run EVPN address family between directly connected IP addresses… but then he’d have to deal with micro-BFD implementations (LACP short timers weren’t good enough);
* Running EVPN address family on routed interfaces between adjacent nodes would result in larger BGP table (there would be at least two alternate paths for every prefix) and potentially slower convergence (every link up/down event would result in a full BGP table refresh). Running EVPN AF between loopback interfaces and having stable EBGP sessions seemed like a better approach.

If you feel a bit lost at this point, the following diagram might help. I would also suggest to watch [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) and [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinars.

{{<figure src="/2020/04/EVPN-EBGP-Multilink-Options.jpg" caption="Design options for parallel links between EBGP neighbors" >}}

He was absolutely right (also proving that there’s an exception to every *best practice*) – like in traditional IP designs, it might make sense to run EBGP between loopback interfaces when you have parallel routed links between EBGP nodes. The only question is whether you’d use an isolated copy of IGP between the two nodes (like we did 20 years ago to get load balancing on EBGP sessions), or run EBGP between them to propagate loopback IP addresses.

I'm positive that some proponents of indiscriminate use of EBGP-between-loopbacks design feel the urge to tell me “*I told you so*”, but please consider these minor details:

* This design only makes sense if you have multiple parallel links between a pair of adjacent nodes;
* When you have a single link between two nodes (like in a typical data center fabric design) it’s irrelevant whether you run the EVPN EBGP session between directly connected IP addresses or between loopback interfaces (unless the boxes you're using have interesting implementation limitations)… but one of the two options is simpler to configure;
