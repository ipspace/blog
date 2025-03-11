---
date: 2022-09-07 07:05:00+00:00
series:
- if_port
tags:
- switching
- IP routing
- networking fundamentals
title: How Routers Became Bridges
short_summary: |
  Network terminology was easy in the 1980s: bridges forwarded frames between Ethernet segments based on MAC addresses, and routers forwarded network layer packets between network segments. That nirvana couldn't last long; eventually, a big enough customer told Cisco: "_I don't want to buy another box if I already have your too-expensive router. I want your router to be a bridge._"
---
Network terminology was easy in the 1980s: bridges forwarded frames between Ethernet segments based on MAC addresses, and routers forwarded network layer packets between network segments. That nirvana couldn't last long; eventually, a big enough customer told Cisco: "_I don't want to buy another box if I already have your too-expensive router. I want your router to be a bridge._"

Turning a router into a bridge is easier than going the other way round[^RB]: add MAC table and dynamic MAC learning, and spend an evening implementing STP.
<!--more-->
[^RB]: As many bridge vendors discovered when they tried to build routers to compete with Cisco (and failed), resulting in ridiculous concoctions like brouters.

Next step: a configuration mechanism. While bridge vendors tried to keep things as simple as possible (usually using the plug-and-pray approach), routers always had to be configured. To enable bridging on a Cisco router, you had to create bridge groups and assign interfaces to them.

[^SW]: Even when they were called layer-2 switches

That leaves just one tricky question: what happens when someone wants to configure routing and bridging on the same interface? My memory is hazy on this point (comments appreciated), but I have a vague recollection of having to decide what to do. You could configure IP/IPX/AppleTalk/... addresses on an interface or place the interface into a bridge group, but not both. The input packet processing was thus exceedingly simple:

* Did we receive a packet on an interface within a bridge group? Extract the destination MAC address and forward the packet using the corresponding MAC table.
* Did we receive a packet on any other interface? Use the Ethernet protocol type to figure out the network layer protocol. Do a lookup in the corresponding forwarding table to forward the packet.

{{<figure src="/2022/09/isolated-routing-bridging.jpg" caption="A router performing independent routing and bridging">}}

That simple world didn't last long. Someone inevitably figured out that it was easy to renumber IPX hosts (because IPX always used a SLAAC-like mechanism[^SLAAC]) but impossible to renumber IP hosts (because DHCP hadn't been invented yet). Splitting a large IPX segment into two was a no-brainer; splitting an IP subnet was Mission Impossible.

[^SLAAC]: You didn't think IPv6 designers invented everything from scratch, did you?

But what if we could route IPX and keep the IP subnet intact by bridging IP[^LAM]? Welcome to _Concurrent Routing and Bridging_: we'll route some protocols and bridge others[^CRB]. The change to the packet forwarding code was minimal:

* Look at the Ethernet protocol type.
* Use the protocol-specific forwarding table if the protocol type is a known network-layer protocol, and the router should route it.
* Bridge the packet in all other cases (a bridged network-layer protocol or an unknown protocol).

{{<figure src="/2022/09/concurrent-routing-bridging.jpg" caption="Protocol-based Concurrent Routing and Bridging (CRB)">}}

[^LAM]: The correct solution would be to use IP routing based on host addresses, but _Local Area Mobility_ hasn't been invented yet. Decades later, we're going through the same conundrum -- another clear win for RFC 1925.

[^CRB]: You could try configuring IP addresses on individual interfaces in the bridge group and bridge IP simultaneously, but it usually didn't end well.

OK, so we could route one protocol (example: IPX) across a set of interfaces and bridge another (example: IP) across the same interfaces, but how could you connect the bridged segment to the outside world? Use a loopback cable to connect the bridged interfaces with another routed interface. Yeah, we loved that as much as the younger engineers loved using external cables to connect M-series linecards to F-series linecards on Nexus 7000.

Final solution: _Integrated Routing and Bridging_: Route traffic sent to router's MAC address, and bridge everything else[^IPMC].

To get there, one has to use the same MAC address (usually an extra MAC address not belonging to any physical interface) on all physical interfaces belonging to the same bridge group[^ER]. You also need a way to specify the IP address belonging to the shared MAC address, and as you usually configure the IP address on an interface, you need an extra (virtual) interface. And that's how we got Bridge Virtual Interface (BVI) on Cisco IOS -- the granddaddy of VLAN interfaces we're using on layer-3 switches.

{{<figure src="/2022/09/integrated-routing-bridging.jpg" caption="Integrated Routing and Bridging (IRB)">}}

Wonder how we got from BVI interfaces to VLAN interfaces? We must take a detour through the VLAN Forest of Despair to get there. Stay tuned.

[^IPMC]: Ignoring IP multicast -- that's a juicy can of worms I'm not going to touch anytime soon.

[^ER]: The proof is left as an exercise for the reader

{{<next-in-series page="/posts/2022/09/vlan-interfaces.md" />}}
