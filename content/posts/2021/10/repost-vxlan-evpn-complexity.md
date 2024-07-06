---
date: 2021-10-27 07:15:00+00:00
evpn_tag: rant
tags:
- VXLAN
- EVPN
title: EVPN/VXLAN Complexity
---
_We have school holidays this week, so I'm reposting wonderful comments that would otherwise be lost somewhere in the page margins. Today: Minh Ha on [complexity of emulating layer-2 networks with VXLAN and EVPN](/2021/10/worth-reading-arp-problems-evpn.html#801)_.

---

Dmytro Shypovalov is a master networker who has a sophisticated grasp of some of the most advanced topics in networking. He doesn't write often, but when he does, he writes exceptional content, both deep and broad. Have to say I agree with him 300% on "_If an L2 network doesn’t scale, design a proper L3 network. But if people want to step on rakes, why discourage them._" 
<!--more-->
Hierarchical networking -- L3 routed network being an example – is the right way to scale. That L2 addressing was flat, created as a workaround from the start, and never meant to be a long-term solution, means all attempts to scale L2-based networks are attempts to make pigs fly, and therefore, by necessity, have to add a lot of moving parts, which increase complexity quickly.

Over-optimization is a dumb process, and overclocking a L2-based network is a prime example of that. Due to the unscalable nature of L2 networking, kludges like VXLAN multihoming’s BUM flooding trick, have to be implemented, significantly complicating the network. If one adds another kludge, MLAG (mentioned in his linked post On Duplicates), on top of that, the whole thing quickly spirals out of control. With this kind of state explosion, how can anyone intuitively visualize the network and the data flow? Worse, how many combinations of error can show up, some already mentioned in his posts? Even without MLAG, the VXLAN BUM trick can get nasty proportional to the size and the degree of multi-homing in a network. And L2 network being unscalable is again clearly on display when one looks at asymmetric Inter-VXLAN routing, the way it works. Once again state explosion. So they have to come up with the symmetric IRB trick -- essentially back to routing and hierarchy -- to reduce state and scale. Now how is all this complexity realized in the hardware FIB, and what kind of additional resources and latency it imposes? Is that why VXLAN in theory can scale to 2^24 segments, but not in actual hardware? I’d like to see the forwarding pipeline on a VTEP.

The sheer complexity of EVPN and particularly of EVPN over VXLAN, creates a lot of subtlety. How many people have any hope of understanding all this, let alone applying the knowledge to efficiently design and build a big network? What happens if you have to troubleshoot this complex matrix of feature interaction, in a large network? The thing is, networking and networking devices are already very complex to begin with -- the ARP problem in async-routed network is complicated enough on its own -- so the goal should be more simplicity, less complexity. With EVPN over VXLAN, it's the other way around because there're more moving parts being added. And look at the nested encapsulation of VXLAN. Layering is harmful due to possible inter-layer dependency and added processing, and VXLAN just takes it to a class of its own.

All of these dirty tricks, trying to make pigs fly, trying to scale the unscalable L2, come from people lacking a understanding of how addressing works, and how inadequate our current addressing model is (missing half of the structure), hence the creation of abominations like VXLAN and IPv6. Done correctly, and all of these become unnecessary.

---

For more details on network addressing, and layer-2 and layer-3 fundamentals, watch the *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar. Parts of that webinar are already available with [Free ipSpace.net subscription](https://www.ipspace.net/Subscription/Free). You need [Standard or Expert ipSpace.net Subscription](https://www.ipspace.net/Subscription/Individual) to watch the whole webinar or attend the live sessions.
