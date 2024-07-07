---
date: 2019-05-08 07:43:00+02:00
dr_tag: fail
high-availability_tag: dr
series:
- dr
tags:
- design
- bridging
- data center
- high availability
title: Real-Life Data Center Meltdown
url: /2019/05/real-life-data-center-meltdown/
---
A good friend of mine who prefers to stay A. Nonymous for obvious reasons sent me his "*how I lost my data center to a broadcast storm*" story. Enjoy!

---

Small-ish data center with several hundred racks. Row of racks supported by an end-of-row stack. Each stack with 2 x L2 EtherChannels, one EC to each of 2 core switches. The inter-switch link details don't matter other than to highlight "sprawling L2 domains.\"

VLAN pruning was used to limit L2 scope, but a few VLANs went everywhere, including the management VLAN.
<!--more-->
On the fateful day, a switch crashed. The crash condition resulted in a repeated sequence of frames being sent at full wire speed. The repeated frames included broadcast traffic in the management VLAN, so every control-plane CPU had to process them.

Network infrastructure CPUs at 100% all over the data center including core switches, routing adjacencies down, etc. The entire facility could not process for \~3.5 hours. No stretched L2, so damage was contained to a single site.

This was a reasonably well-managed site, but had some dumb design choices. Highly bridged networks don't tolerate dumb design choices.

I don't remember what the "official\" story was we issued to customers. Standard operating procedure was to spin the truth. Point being that there are doubtless DC-down stories we never hear. And if we do hear them, the truth is obscured by spin. Probably similar to how most security breaches are handled.

This story is perhaps too old to be relevant... but as I reflect on it, the technology we were using then was fairly simple. Carefully managed rapid spanning-tree. Etherchannels. Diligent VLAN pruning. What have we got today in L2 that would update such an environment? Myriad stacking & MLAG options. TRILL & SPB (that almost no one bought). BGP EVPN (not really L2 anymore).

Can any of the stacking / MLAG technologies be LESS prone to failure, considering their complexity? I remember kicking early Cisco 6500 VSS out the door because it was hopelessly unstable. Nexus VPCs seemed stable in my experience, but had the benefit of being limited in scope compared to shared control-plane stacking technologies.

Coincidentally, I've been on hand for my share of L3 related outages, but in almost every case, the issues were caused by human error, bad design, or a combination of both where an unintentional (human screw up) or unforeseen (topological, circuit down) change to the network toppled a house of cards. I don't see that as a problem inherent to L3, because in every case a design change could resolve the problem. (I.e. replace the house of cards with a proper house.) L2 issues...not so much.

I tend to think of large bridging domains as inherently risky in a way that is not possible to engineer away. Storm-control and fancy STP add-ons help when properly applied, but have limits. Sort of like when the containment shell of a nuclear facility fails during a runaway reaction.

---

Want to know the real difference between routing and bridging? It will be one of the first topics I'll cover in the upcoming [*How Networks Really Work*](https://www.ipspace.net/How_Networks_Really_Work) webinar. On a more practical note, you might want to explore various DCI design options with the [*Data Center Interconnects*](https://www.ipspace.net/Data_Center_Interconnects) webinar, or figure out how to build scalable multi-data-center solutions with [*Designing Active-Active and Disaster Recovery Data Centers*](https://www.ipspace.net/Designing_Active-Active_and_Disaster_Recovery_Data_Centers) webinar.

Finally, there's also the [*Building Next-Generation Data Center*](https://www.ipspace.net/Building_Next-Generation_Data_Center) online course -- hundreds of [data center architects and designers](https://www.linkedin.com/school/ipspace-building-next-generation-data-center-course/) found it highly relevant and useful.
