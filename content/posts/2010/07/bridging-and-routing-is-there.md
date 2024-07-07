---
date: 2010-07-14 07:10:00.011000+02:00
tags:
- bridging
- data center
- workshop
- IP routing
- TRILL
title: 'Bridging and Routing: Is There a Difference?'
url: /2010/07/bridging-and-routing-is-there/
---
In his comment to one of my TRILL posts, [Petr Lapukhov](http://www.ine.com/about-petr.htm) has asked *the* fundamental question: "how is bridging different from routing?". It's impossible to give a concise answer (let alone something as succinct as [42](https://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy#The_Answer_to_the_Ultimate_Question_of_Life,_the_Universe,_and_Everything_is_42)) as the various kludges and workarounds (including bridges and their [IBM variants](http://en.wikipedia.org/wiki/Source_route_bridging)) have totally muddied the waters. However, let's be pragmatic and compare Ethernet bridging with IP (or CLNS) routing. Throughout this article, *bridging* refers to *transparent bridging* as defined by the IEEE 802.1 series of standards.

**Design scope.** IP was designed to support global packet switching network infrastructure. Ethernet bridging was designed to emulate a single shared cable. Various design decisions made in IP or Ethernet bridging were always skewed by these perspectives: scalability versus transparency.
<!--more-->
**Forwarding.** IP routers forward IP datagrams according to their IP routing tables and never make multiple copies of the same datagram. They drop datagrams sent to unknown destinations and tell the sending hosts they did so. Bridges have to emulate a shared cable and thus forward frames sent to unknown destinations to all active ports but the one on which the frame was received (*flooding*). In short, routing is "forwarding based on presumption of knowledge", bridging is "forwarding by guessing".

**Loop detection.** IP (and most other layer-3 protocols) has a hop count in its header. Ethernet header does not have a hop count (neither do most other layer-2 protocols). Using hop count, loops can be detected even when they cannot be prevented (uRPF does a decent job of loop prevention in non-asymmetric networks, but that's a different story).

Even worse, the *forwarding by guessing* bridging paradigm can create multiple copies of a looped packet sent to unknown destination. The number of copies grows exponentially with each iteration of the loop, quickly resulting in a total network meltdown.

**Multicast.** Routers stop multicast or broadcast packets unless they are configured to forward them. Decent multicast implementations allow hosts to register to multicast streams and the routers deliver multicast packets only to those hosts or segments that actually need them.

Transparent bridges have to emulate a shared cable where every station can receive a broadcast or multicast frame. They are thus bound to flood multicast/broadcast frames.

Some layer-2 bridges support IGMP snooping and other mechanisms that should limit the amount of IP multicast propagated in unwanted directions. These measures work only for known (IP) multicast addresses; bridges still have to flood frames sent to unknown multicast destinations.

Most bridges can rate-limit the flooding process, reducing the chances of a single runaway host bringing the whole network to a standstill. Nonetheless, a determined intruder can use the rate-limiting mechanisms for an effective DoS attack where the bogus multicast traffic interferes with crucial protocols like ARP.

**Forwarding tables.** IP routing tables are built by routers exchanging (somewhat) authoritative information: their connected subnets and their static routes. Bridging tables are built by guessing -- by listening to the traffic and extracting source MAC addresses from the frames. The guessed information is never exchanged between the bridges (ESADI in TRILL is an exception, but even ESADI information is not authoritative).

**Addressing.** Layer-3 addresses are configurable and usually include some topology information, allowing the layer-3 routing to scale. Layer-2 addresses are supposed to be static (hardwired) and are (within a single network) randomly scattered around the network.

**Scalability.** All layer-3 protocols have some mechanism that aggregates forwarding information, allowing them to scale. The "desktop protocols" (Cisco's invention, not mine), including AppleTalk, IPX and Banyan Vines performed routing based on *networks* (*cable ranges* in Appletalk), which were very similar to fixed-prefix IP subnets. DECnet, CLNS and SNA have areas and perform host-based routing within an area, but still use only area addresses in "long-distance" (inter-area) routing to scale. Classless routing with IP prefixes allows you to build a multi-layer hierarchy.

Transparent bridging forwards frames to randomly scattered layer-2 addresses and thus cannot have a scaling mechanism.

Novel approaches to bridging (TRILL and 802.1ad) introduce a bridging hierarchy (or a bridging/routing hierarchy in case of TRILL), in which inner bridges (*provider bridges* in 802.1ad) know just the MAC address of edge bridges. VLANs deployed on edge bridges further limit the amount of information a single edge bridge must carry. Still, a single bridged domain cannot scale.

**Spoofing.** The "forwarding by learning" paradigm makes it extremely easy to spoof a bridged network: send frames with wrong source MAC address. Spoofing a routed network is somewhat harder; you have to hack the routing protocol.

Bridges reduce the risk of spoofing by implementing port security, dynamic ARP inspection and DHCP snooping; workaround measures trying to solve a problem that shouldn't have existed in the first place. You cannot secure an environment designed to emulate a single shared cable (at least not without breaking some eggs).

**Fragmentation.** IP was designed to span a multitude of physical media with different characteristics and supports datagram fragmentation and path MTU discovery. Bridging was designed to connect segments with uniform technology, which was fine as long as the maximum Ethernet MTU was constant. Introduction of jumbo frames has created a "somewhat more complex" environment, where bridging between Ethernet segments can fail spectacularly.

**Out-of-order packets.** Out-of-order packets are a fact of life in any multipath topology (including any layer-3 network). Layer-3 protocols were thus designed to deal with them, either rearranging them (TCP) or dropping them (most UDP applications).

Protocols that pretend the hosts communicate on a shared cable tend to ignore the out-of-order problems; some protocols might even terminate the session when receiving one. SNA was one of those protocols, forcing Cisco to implement FST, which dropped any out-of-order packets. The requirement to deliver packets in order significantly complicates any advanced bridging implementation (for example, TRILL).

**Mixed media.** IP can (by definition) be used on all data link layer technologies. You can mix-and-match various technologies as needed: Ethernet for access LAN, Gigabit Ethernet with large MTU for data center, HDLC, PPP, Frame Relay or ATM for WAN links. Datagram transport across all the media is always (close to) optimal.

Bridging forces you to use a single layer-2 technology (for example, Ethernet) everywhere and emulate the chosen layer-2 technology across all other media. This requirement leads to [baroque architecture used in DSL networks](/2009/03/adsl-overhead/) and emulation jumbles like LANE or VPLS.

**Anything else?** I\'ve listed some more differences between routing and bridging in the *[Bridging and Routing - Part II](/2010/07/bridging-and-routing-part-ii/)* post. If I have still missed something, please let me know in the comments.
