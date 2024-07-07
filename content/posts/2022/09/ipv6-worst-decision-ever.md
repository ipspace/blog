---
title: "Was IPv6 Really the Worst Decision Ever?"
date: 2022-09-06 07:17:00
tags: [ IPv6, networking fundamentals ]
---
A few weeks ago, Daniel Dib tweeted a slide from Radia Perlman's presentation in which she claimed IPv6 was the worst decision ever as we could have adopted CLNP in 1992. I had similar thoughts on the topic a few years ago, and over tons of discussions, blog posts, and creating the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar slowly realized it wouldn't have mattered.

{{<figure src="/2022/09/ipv6-worst-decision-ever.png">}}
<!--more-->
Could we use CLNP as the next-generation IP? Of course, and we could have saved a few years -- [CLNP](/tag/clnp/) was already a mature protocol. Sadly, it turned out even IETF wasn't pragmatic enough to acknowledge superior technology from what some considered their arch-enemy. You'll find a few juicy details in [The Elements of Networking Style](https://www.amazon.com/Elements-Networking-Style-Animadversions-Intercomputer/dp/0595088791) by Michael A. Padlipsky.

Regardless of that not-so-brilliant episode in IETF history, I inevitably get upset when CLNP aficionados use bogus arguments to justify their gripes. The "Worst Decision Ever" slide contains a bunch of them, starting with these:

**CLNP wouldn't need ARP**. There is absolutely no way around having a protocol mapping layer-3 addresses into layer-2 addresses unless you're building your network with point-to-point links that don't need layer-2 addresses by definition.

CLNP just used a different approach than IP. Instead of a demand-driven ARP (ask when you need the information), CLNP uses ES-IS (periodic hellos). We could spend way too much time discussing whether one is better than the other, and it doesn't matter in the days of 4-core 2GHz CPUs. Just don't claim that CLNP is better than IP because it doesn't need ARP.

**CLNP wouldn't need Ethernet**. The real reason Ethernet and other shared-media LAN solutions became popular was lower cost. You need two interfaces per link in any switched or routed solution. You only need one when you're attaching endpoints to a shared medium. The situation becomes even more ridiculous when the endpoints require high bandwidth consumed in bursts, keeping the average endpoint interface utilization low.

What mattered in 1980s obviously still matters in 2020s: when every data center switching ASIC includes line-speed layer-3 forwarding, the service providers are still building Passive Optical Networks (PON) instead of switched Ethernet or routed IP networks.

Another reason for the explosion of bridged solutions was the simplicity of the protocol stack. You had to implement STP -- which could easily fit into the 64 KB address space of an 8-bit CPU -- instead of a dozen network layer protocols and a bunch of associated routing protocols[^NLP].

**Long story short**: Using CLNP instead of IPv6 would not change a thing. We would still want to use lower-cost connectivity solutions (Ethernet), and vendors trying to implement a networking stack with minimum investment would still [create crappy bridges](/2019/10/the-cost-of-disruptiveness-and/) or [spaghetti mess of static routes and NAT](/2020/08/docker-swarm-services/).

[^NLP]: If you're old enough to remember the IPX, DECnet, CLNP, AppleTalk, Banyan Vines, XNS, Apollo Domain... you probably know what I'm talking about.