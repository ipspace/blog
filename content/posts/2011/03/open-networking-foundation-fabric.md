---
cdate: 2022-07-06
comment: 'In March 2011, industry media quickly picked up the buzz created by the
  Open Networking Foundation (ONF) press releases and started exaggerating the already
  extravagant claims made by ONF, prompting me to write the following blog post.


  Not surprisingly, most of the hype was just that, and in the intervening years ONF
  dropped OpenFlow like a hot potato, while most everyone refocused on things that
  really matter like network automation.

  '
date: 2011-03-31 06:40:00.003000+02:00
sdn_hype_tag: initial
series:
- sdn_hype
tags:
- data center
- OpenFlow
title: Open Networking Foundation – Fabric Craziness Reaches New Heights
url: /2011/03/open-networking-foundation-fabric/
---
Some of the biggest buyers of the networking gear have decided to squeeze some extra discount out of the networking vendors and threatened them with open-source alternative, hoping to repeat the Linux/Apache/MySQL/PHP saga that made it possible to build server farms out of low-cost commodity gear with almost zero licensing costs. They [formed the *Open Networking Foundation*](https://opennetworking.org/news-and-events/press-releases/onf-formed-to-speed-network-innovation/), found a convenient technology (OpenFlow) and launched another major entrant in the Buzzword Bingo -- Software-Defined Networking (SDN).

Networking vendors, either trying to protect their margins by stalling the progress of this initiative, or stampeding into another Wild West Gold Rush (hoping to unseat their bigger competitors with low-cost standard-based alternatives) have joined the foundation in hordes; the list of initial members (see the press release for details) reads like Who's Who in Networking.
<!--more-->
Now, let's try to figure out what SDN might be all about. The ONF Mission Statement[^LG] says "*SDN allows owners and operators of networks to control and manage their networks to best serve their needs.*" Are the founding members of ONF trying to tell us they have no control over their networks and lack network management systems? It must be something else. How about this one (from the same paragraph): "*OpenFlow seeks to increase network functionality while lowering the cost associated with operating networks.*" Now we're getting somewhere -- I told you it was all about reducing costs (starting with the networking vendors' margins).

[^LG]: Long gone. Unfortunately I wasn't able to find the correct page on archive.org, so you'll have to trust my copy/paste skills.
 
(Some of) the industry media happily joined the craze, parroting meaningless phrases from various press releases. Consider, for example, [this article from IT World Canada](http://www.itworldcanada.com/news/the-next-revolution-in-networking-is-months-away/142810).

"*SDN would give network operators the ability to virtualize network resources, being able to dynamically improve latency or security on demand*" If you want to do it, you can do it today, using dynamic routing protocols or QoS (latency), vShield/VSG (on-demand security) or a number of virtualized networking appliances.

Also, protocols like RSVP to signal per-session bandwidth needs have been around for more than a decade, but somehow never caught on. Must be the fault of those stupid networking vendors.

"*Sites like Facebook, Google or Yahoo would be able to tailor their networks so searches would be blindingly fast*" I never realized the main search problem was network bandwidth. I always somehow thought it was related to large datasets, CPU, database indices \... Anyhow, if the network bandwidth is the bottleneck, why don't they upgrade to the next-generation Ethernet (10G/40G). Ah, yes, it might be expensive. How about deploying Clos network architecture? Ouch, might be a nightmare to configure and manage. How exactly will SDN solve this problem?

"*Stock exchanges could assure brokerage customers on the other side of the globe they'd get financial data as fast as a dealer beside the exchange.*" Will SDN manage to flatten & shrink the earth, will it change the speed of light, or will it use large-scale quantum entanglement?

"*It could be programmed to order certain routers to be powered down during off-peak power periods.*" What stops you from doing that today?

Don't get me wrong -- OpenFlow might be a good idea and it will probably lead to interesting new opportunities (assuming they can solve the scalability and resilience issues) \... and I'm absolutely looking forward to the podcast we're recording later today.

However, there are plenty of open standards in the networking industry (including XML-based network configuration and management) waiting to be used. There are also (existing, standard) technologies that you can use to solve most of the problems these people are complaining about. The problem is that these standards and technologies are not used by operating systems or applications (when was the last time you've deployed a server running OSPF to have seamless multihoming?)

The main problems we're facing today arise primarily from *non-scalable application architectures* and [*broken TCP/IP stack*](/2009/08/what-went-wrong-tcpip-lacks-session/). In a world with scale-out applications you don't need fancy combinations of routing, bridging and whatever-else; you just need fast L3 transport between endpoints. In an Internet with decent session layer or a multipath transport layer (be it SCTP, Multipath TCP or something else) you don't need load balancers, BGP sessions with end-customers to support multihoming, or LISP. All these kludges were invented to support OS/App people firmly believing in [fallacies of distributed computing](http://en.wikipedia.org/wiki/Fallacies_of_Distributed_Computing). How is SDN supposed to change that? I'm anxiously waiting to see an answer beyond marketing/positioning/negotiating bullshit bingo.

### Prefer to Hear about Real-Life Technologies and Products?

If you want to learn more about [real-life SDN](https://www.ipspace.net/SDN) or [network automation](https://www.ipspace.net/Roadmap/Network_Automation_webinars), check out the [related ipSpace.net webinars](https://www.ipspace.net/Webinar_roadmaps).

For more information on Data Center architectures, watch [Data Center 3.0 for Networking Engineers](https://www.ipspace.net/DC30), [Leaf-and-Spine Fabric Architectures](https://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures), and [Data Center Fabric Architectures](https://www.ipspace.net/Data_Center_Fabrics) webinars.

All ipSpace.net webinars are available with [standard subscription](https://www.ipspace.net/Subscription).
