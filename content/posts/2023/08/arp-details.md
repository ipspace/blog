---
title: "ARP Details Behind the Scenes"
date: 2023-08-28 06:25:00
tags: [ ARP ]
---
When figuring out how [unnumbered IPv4 interfaces](/series/unnumbered-interfaces.html) work, Daniel Dib asked an interesting question: How does ARP work when the source and destination IPv4 address are not in the same segment (as is usually the case when using unnumbered interfaces)?

{{<figure src="/2023/08/ARP-Q.png">}}
  
**TL&DR:** ARP doesn't care about subnets. If the TCP/IP stack needs to find a MAC address of a node it thinks is adjacent, ARP does its best, no matter what.
<!--more-->
Before going into the details, it's worth revisiting the "_Why do we need ARP?_" fundamentals:

-   IP nodes sending IP packets over Ethernet must build an Ethernet frame for every IP packet[^OLAN].
-   That Ethernet frame must have a source MAC address[^HK] and a destination MAC address.
-   You could statically configure destination MAC addresses for adjacent IP hosts[^SA]; in most cases, the local IPv4 stack uses ARP to find the MAC address of an IP address the local node thinks is directly connected.[^6ND]

[^OLAN]: I know the same rules apply to all other LAN networks, including Token Ring and FDDI. The latter two would fall under the IEEE 802 ARP hardware type; it's just that I haven't seen them in decades

[^HK]: Hopefully known to the node or its Ethernet interface card

[^SA]: That functionality is called *static ARP*

[^6ND]: IPv6 stack uses neighbor discovery

ARP might be a bit underspecified[^GOD], but the rules listed in RFC 826 are pretty simple:

[^GOD]: RFC 826 comes from the days when everyone developing IP stacks knew each other

-   If an IPv4 node needs the MAC address of an adjacent IPv4 node, it stuffs the desired values[^DV] in an ARP packet and broadcasts it. There's no mention of "nodes being on the same subnet" -- ARP runs within a subnet, and it's assumed the higher-level routines (IPv4 forwarding code) know what they're doing.
-   Replying to ARP packets is also trivial: if the local node's IPv4 address is the *target protocol address*, the receiver swaps sender/receiver addresses in the incoming ARP packet, inserts its MAC address in the proper place, and sends an ARP reply.

A few other things are pretty obvious (even though they might not be mentioned in the RFC):

-   The receiver should reply with its own MAC address. I'm positive some vendors are doing crazy stuff, the least of it being the way first-hop gateway resolution protocols share a MAC address across multiple nodes.
-   Receiver does not check for "nodes being on the same subnet" -- if someone manages to send me an ARP request, it's polite to reply to them. This behavior is configurable in some devices (at least on Linux with `arp_ignore` *sysctl* parameter).
-   Finally, note that ARP is a non-routable protocol. The sender and the receiver must be in the same data-link-layer (usually Ethernet or WiFi) segment.

[^DV]: Source IPv4 address, source MAC address, and destination IPv4 address

Now for the gray areas:

-   RFC 826 does not specify whether the "*Am I the target protocol address?*" condition checks the IP address of the incoming interface or whether it could match any IP address on the node. I'm guessing this bit might be implementation-dependent; it could explain why some devices reply to ARP queries for their other IP addresses even when there's no proxy ARP configured on the incoming interface. The behavior is configurable on Linux with `arp_filter` and `arp_ignore` *sysctl* parameters; I don't remember seeing similar configuration options on any other network device, but maybe I just didn't look hard enough.
-   As already mentioned[^ST], RFC 826 also does not specify that the source and destination IP addresses have to be in the same subnet. An ARP implementation will send out any query the higher layers of the IP stack want to have answered and will report the answer if it ever comes back (unless the behavior is configurable -- see `arp_ignore` on Linux).

[^ST]: Several times

That brings us to another interesting case. Imagine that for whatever reason the sender thinks an IP address is directly connected, but the receiver of an ARP request does not have the target IP address but knows how to reach it.

In that case, the receiver might reply with its MAC address, effectively saying, "*Sure, send me the packets; I know how to get there.*" We usually call that functionality *proxy ARP*. Proxy ARP is a great but also pretty dangerous tool (but that's a story for another blog post).

Finally, it's worth noting that while we usually think proxy ARP can be used to reach hosts beyond a router, it's heavily used *within a subnet* in WiFi and PVLAN environments. You might want to read [RFC 3069](https://www.rfc-editor.org/rfc/rfc3069.html) for the PVLAN details. Brave souls are also [using proxy ARP to stretch local subnets into the cloud](/2019/11/stretched-layer-2-subnets-in-azure.html), forgetting that *because you can does not mean that you should*.

### Revision History

2023-08-28
: * Added Linux sysctl parameters based on a comment by Erik Auerswald
: * Added proxy ARP use cases

{{<next-in-series page="/posts/2023/08/arp-static-routes.html">}}**Coming up next**: ARP and static routes{{</next-in-series>}}
