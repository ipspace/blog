---
date: 2013-04-16 06:51:00+02:00
high-availability_tag: fail
series_weight: 470
tags:
- security
- Internet
- high availability
title: This Is What Makes Networking So Complex
url: /2013/04/this-is-what-makes-networking-so-complex.html
---
The responses to my [*What did you do to get rid of manual VLAN provisioning post*](https://blog.ipspace.net/2013/03/what-did-you-do-to-get-rid-of-manual.html) were easy to predict: a few people sharing their best practices (thank you!), few musings on the future of SDN/networking, and the ubiquitous anonymous rant against stubbornness and stupidity of networking engineers and their OPEX.

I know one should never feed anonymous trolls, but this morsel is simply too juicy to pass, so here it is -- let's see what makes networking so complex.
<!--more-->
To start with, networking done properly was never complex, and it still isn't. Large IP networks (e.g. ISP networks) with reasonable convergence expectations and small subnets (with layer 2 domains limited to the approximate size of [original definition of layer 2](http://en.wikipedia.org/wiki/Data_link_layer)) are simple and stable. What makes some of them less simple is the featurism usually heaped onto them (including bogus bolt-ons like [QoS in public Internet](http://www.potaroo.net/ispcol/2012-06/noqos.html)), or the idea that you can transport anything (including ATM cells if the customer asks for that) over them.

So what causes the networking complexity? In most cases, it's the shortsightedness of everyone involved (from OS designers and application developers down to the networking engineers) and the usual way of dealing with it -- instead of fixing your own mistakes, it's so much simpler to push the \*\*\*\* down a layer, and so the accumulated heap lands in networking, [vastly increasing its complexity](https://blog.ipspace.net/2012/07/virtualized-squashed-complexity-sausage.html). The MacGyver-ish "I can fix the world [one kludge at a time](https://blog.ipspace.net/2009/10/my-stupid-moments-interface-default.html)" attitude practiced by many networking engineers doesn't help either.

{{<figure src="/2013/04/s1600-Career+-+the+real+pyramid.jpg" caption="Replace the labels: applications → servers → virtualization → networking">}}

Before writing a heated response telling me how I'll become extinct together with FEP programmers when point-and-click takes over, do me a favor and read the rest of the post. If you still disagree, please feel free to comment.

It would be so easy to start ranting about [virtualization vendors who used VLANs](https://blog.ipspace.net/2011/12/vmware-vswitch-baseline-of-simplicity.html) because [they couldn't figure out](https://blog.ipspace.net/2013/04/vlans-are-wrong-abstraction-for-virtual.html) a more appropriate abstraction, [storage vendors who require long-distance layer-2 domains](https://blog.ipspace.net/2013/03/does-dedicated-iscsi-infrastructure.html) because they were too lazy to implement iSCSI checksums, application architects who pretend [VMware HA](https://blog.ipspace.net/2011/08/high-availability-fallacies.html) or [stretched clusters](https://blog.ipspace.net/2011/06/stretched-clusters-almost-as-good-as.html) solve their [high-availability requirements](https://blog.ipspace.net/2011/02/what-exactly-makes-something-mission.html), virtualization consultants who [propose stretched VMware HA clusters](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) not because the [business needs justify them](https://blog.ipspace.net/2013/01/long-distance-vmotion-stretched-ha.html) but to make their lives easier (and shift the problem into another team), or [networking vendors selling snake oil](https://blog.ipspace.net/2011/09/trill-goes-to-wan-bridging-craze.html). Instead of that, let's focus on systemic problems.

#### Systemic problems

[**Socket API is broken**](https://blog.ipspace.net/2009/08/what-went-wrong-socket-api.html) to the point where it's impossible to add IPv6 support to the network without rewriting old applications. Let me reiterate that: you have to change your applications if you want to introduce a new network-layer protocol (IPv6) or transport-layer protocol (SCTP). How stupid is that?

I'm positive all the original Socket API designers needed was a short-term kludge, but we've been stuck with it for ages, and not much has been done to fix the situation.

**Major impacts:**

-   Resources are ultimately identified by their IP addresses, not service names, requiring load balancing solutions for scale-out architectures.
-   Disaster recovery solutions require complex network realignments (or large layer-2 domains) to avoid server renumbering (this would be a non-issue if the applications couldn't use IP addresses directly, or if all programmers finally figured out how to use [*getaddrinfo*](http://linux.die.net/man/3/getaddrinfo)).
-   The ability to work with network addresses on application layer resulted in applications embedding IP addresses in application data. We need application-level gateways in firewalls and address translators to deal with each application individually.

[**TCP stack lacks session layer**](https://blog.ipspace.net/2009/08/what-went-wrong-tcpip-lacks-session.html), bringing some very smart application designers to a point where they implemented a [zeroth-order approximation within the web browser](https://blog.ipspace.net/2013/03/happy-eyeballs-happiness-defined-by.html). [Alternatives have been available for years](https://blog.ipspace.net/2009/08/what-went-wrong-sctp.html), but never got properly implemented, because it was easier to push the problem down the stack.

**Major impacts:**

-   High availability requirements have to be solved with network-layer multihoming, resulting in exploding routing tables or added layers of complexity like LISP.
-   Session state has to be preserved across failures of stateful devices (firewalls, load balancers). BTW, the existence of stateful devices within the network is a kludge by itself.
-   Network-layer kludges within the host operating systems are used to implement IP mobility -- it would be so much easier if the session layer could consistently reconnect the application session after an IP address change.
-   VM mobility (where usual IP mobility techniques cannot be used because they require host stack support) requires large layer-2 domains or complex routing tricks.
-   Every RPC-like solution implements its own directory service that uses dynamic TCP ports in a way that's impossible to filter with simple packet filters.

In general, **security is an afterthought** and someone else's problem. If we'd have semi-secure operating systems and applications, applications using few well-known TCP/UDP ports instead of a hodgepodge of unknown dynamic ports, and \"securing my product is my responsibility\" attitude, we wouldn't need complex (and/or next-generation) firewalls.

**To summarize**: with properly architected TCP/IP stack (I doubt I'll live long enough to see it) we wouldn't need large layer-2 domains (and FabricPath, TRILL, SPB, EVB, VEPA \...), load balancers, application-level gateways, 500K entries in global BGP table (and in TCAM of every core router) or LISP. [TCP is really the most expensive part of your data center](https://rovingengineer.wordpress.com/2011/03/16/tcp-the-most-expensive-part-of-your-datacentre/).

Also note that I'm not blaming the original architects of TCP/IP. They were designing the TCP/IP stack more than 30 years ago for a totally different and less demanding environment, and they did a great job considering the compute and bandwidth constraints they were facing. I'm blaming everyone who pretended there was no problem (including the total absence of results of the [TCPng working group](https://datatracker.ietf.org/wg/tcpng/)), or who tried to benefit by exploiting the \*\*\*\*-shoveling activities (example: every networking vendor peddling long-distance layer-2 solutions).

Finally, if you happen to be a CIO getting the "network OPEX is too high" advices from your M-level consultants *and* reading my blog *and* you got this far (and I'm an eternal optimist, so I hope the intersection is a non-empty set) -- you might save more (in the long term) by helping the networking team simplify the network than by buying next-generation point-and-click tool that will hide ever-increasing complexity with another layer of eye candy.

After all, while it might be OK for the laptop support group to reformat your laptop when they can no longer cope with the increasing complexity of desktop operating systems, [reformatting the network](https://blog.ipspace.net/2012/03/knowledge-and-complexity.html) usually isn't an option.
