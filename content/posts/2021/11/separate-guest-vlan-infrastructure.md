---
title: "Building a Separate Infrastructure for Guest Access"
date: 2021-11-10 06:50:00
tags: [ security ]
---
One of my readers sent me an age-old question:

> I have my current guest network built on top of my production network. The separation between guest- and corporate network is done using a VLAN -- once you connect to the wireless guest network, you're in guest VLAN that forwards your packets to a guest router and off toward the Internet.
>
> Our security team claims that this design is not secure enough. They claim a user would be able to attach somehow to the switch and jump between VLANs, suggesting that it would be better to run guest access over a separate physical network.

Decades ago, VLAN implementations were buggy, and it was possible (using a carefully crafted stack of VLAN tags) to insert packets from one VLAN to another (see also: [VLAN hopping](https://en.wikipedia.org/wiki/VLAN_hopping)).
<!--more-->
I haven't heard of VLAN hopping exploits[^1] in ages, and I've never heard of bidirectional communication enabled by VLAN hopping, but maybe inserting a single packet is good enough -- the Slammer worm needed a single UDP packet to spread. Anyway, the myths of VLAN hopping (and the myths of hypervisor escapes) refuse to die.

[^1]: Apart from the obvious misconfigurations pointed out in the Wikipedia article.

Just to cover all bases: a layer-2 switch that crashes and loses its configuration might wake up in a state where all ports are in the native VLAN (VLAN 1), but it’s easy to mitigate that — use VLAN trunking without a native VLAN on the uplink, and while everyone might be in the same VLAN on the switch, they won’t get anywhere else.

Finally, I'm positive there are ultra-high-security environments  where separate infrastructure for guest access is a must[^2], but I'm guessing that engineers working in those environments don't expect to get security-related advice from a random blogger.

[^2]: I don't think PCI compliance counts. It's well understood that anyone thinking about guest access in PCI environment is asking for horrendous auditing headaches.

Anyway, how could one deal with an overzealous security team? Be polite. For example, "_looking from the networking perspective, and considering industry best practices, I can’t see what you’re so worried about. Could you please help me by pointing out the actual problem in our infrastructure (after all, you’re the security experts) and we’ll fix it_." 

In the ideal case, they'd hire a third party to prove you wrong, and while I would be surprised to see someone hop out of a VLAN, expect a decent pen tester to find a bunch of real-life security vulnerabilities well worth fixing. Not sure about that? Maybe you should listen to a few episodes of the [Darknet Diaries](https://darknetdiaries.com/) podcast ;)

