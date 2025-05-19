---
title: "Response: True Unnumbered Interfaces"
date: 2025-05-21 07:55:00+0200
series:
- unnumbered-interfaces
tags:
- IP routing
- networking fundamentals
short_summary: |
  Is it possible to route IPv4 or IPv6 over interfaces that have no IP addresses? In theory, it might be. In practice, IPv6 always uses link-local addresses, and it's much easier to borrow an IPv4 address from another interface.
---
Hendrik left an [interesting comment](https://blog.ipspace.net/2022/01/isis-unnumbered/#2628) on my [Running IS-IS over Unnumbered Ethernet Interfaces](/2022/01/isis-unnumbered/) blog post:

> FRRouting (Linux) with pure IS-IS, the only way it currently (10.3) works is to copy the loopback IPv4 address to the interfaces that you need to do IPv4 routing on. The OpenFabric (IS-IS "extension" draft) does support true unnumbered interfaces and routes IPv6.

Let's unpack this. There are (at least) four reasons a router needs an address associated with an interface[^CLNP]:
<!--more-->
[^CLNP]: We'll conveniently bypass the fact that bridges or protocols like CLNP use device-wide layer-2 or layer-3 addresses by assuming the same address is associated with all interfaces.

1. The device needs to put something in the *source address* part of the header when sending control-plane messages, including ICMP *TTL Exceeded* or *Fragmentation Needed* messages. Most routing protocols[^ISOF], traceroute, or path MTU discovery don't work without an interface having an IP address associated with it.
2. The adjacent devices need to know what next hop to use when building routing tables.
3. The adjacent devices have to map the routing table next hops (as derived from the routing protocols or static routes) into  layer-2 (MAC) addresses.
4. The device has to decide whether to accept packets from protocol X on interface Y. That decision is usually transformed into *Do we have an X-address on Y?*

[^ISOF]: IS-IS is an exception as it uses a bespoke Layer 3 protocol. OpenFabric is an extension of IS-IS.

CLNP and IS-IS (for CLNP) bypass all the above considerations by using device-wide addresses. IPv6 avoids the control-plane issues with link-local addresses (LLA). However, all of them still have to address the *Do we accept packets on interface Y?* question, and usually do that with an *enable X on Y* configuration command[^CIPv6E].

[^CIPv6E]: That's why you have to configure **ipv6 enable** on router interfaces. Linux-based systems often assume you want to accept IPv6 traffic on all interfaces and generate IPv6 LLA on all interfaces unless you tell them to turn it off with a configuration command or **sysctl** parameter.

OSPF runs on top of IPv4 and thus has no chance of working without IPv4 addresses associated with interfaces.

What about ISIS?

* It uses its own Layer 3 protocol and can run on any interface (bypassing #1 completely)
* IS-IS for IPv6 uses link-local addresses as next hops and thus works out of the box
* IS-IS for IPv4 must address the next-hop issues (#2 and #3)

Most IS-IS implementations require configuration commands to enable IS-IS for a particular layer-3 protocol, but still check IPv4 interface addresses before advertising that they can route IPv4 on a specific link. The adjacent routers also [require information about IPv4 addresses to use as the next hops in their routing tables](/2022/01/isis-unnumbered/).

[EBGP over unnumbered interfaces](/2022/11/bgp-unnumbered-duct-tape/) uses a bag of tricks:

* EBGP sessions are established between IPv6 LLAs (so it's not really running over *unnumbered* interfaces)
* IPv4 prefixes are advertised with IPv6 next hops
* The routers use implementation-dependent mechanisms to transform IPv6 LLA next hop into a MAC address that is then used to forward IPv4 traffic.

Although it would be possible to run IPv4 with EBGP-over-LLA over interfaces that have *no IPv4 address associated with them*, any implementation would still need to decide what IPv4 address to use for ICMP messages, and whether or not to accept IPv4 packets received on an interface.

Most implementations wisely choose the easy way out, borrow an IPv4 address from another interface (that's why you always need an interface name in the **ip unnumbered** configuration command), and assign it to the (not really) *unnumbered* interface. Linux has to be different; you have to implement the low-level mechanism usually hidden behind the **ip unnumbered** command and set the same IP address on multiple interfaces[^SAMI].

[^SAMI]: Having the same IP address on multiple interfaces is usually a configuration error. Most network operating systems would violently disagree with that; Linux loves to give you plenty of rope to hang yourself.

**Long story short:** There are no *True Unnumbered* interfaces in the IP world. The most we could achieve is a needlessly complex implementation using tricks to forward IPv4 traffic with the help of IPv6 link-local addresses.

**Finally:** Considering all of the above, saying "_X supports true unnumbered interfaces and routes IPv6_" makes no sense as every IPv6-enabled interface usually gets a link-local address[^LxLLA].

[^LxLLA]: Not surprisingly, Linux allows you to remove an IPv6 LLA from an interface. I don't want to know about any potential side effects.