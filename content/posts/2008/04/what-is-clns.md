---
date: 2008-04-27 07:54:00.003000+02:00
tags:
- IP routing
- CLNP
title: What Is CLNS?
url: /2008/04/what-is-clns/
---
According to the results of my recent *Do you use CLNS* poll, around 10% of my readers use CLNS in their network, while 36% of them wonder what that acronym stands for.

{{<figure src="/2008/04/CLNSresults.jpg">}}

Let\'s start with the acronyms. CLNS (Connection-Less Network Service) in combination with CLNP (Connection-Less Network Protocol) is the ISO (International Standards Organization) equivalent to IP.
<!--more-->
{{<note>}}ISO makes a fine semantic distinction between the service offered to higher layers (CLNS) and the protocol used to implement it (CLNP). There is no such distinction in the IP world.{{</note>}}

CLNS (and CLNP) uses long variable-length addresses, making it a viable successor to IPv4. At the time when the IETF community started to design the next-generation IP (before IPv6 appeared on the drawing board), the [proposals to use CLNS](http://tools.ietf.org/html/rfc1561) were taken pretty seriously even though they used interesting acronyms like TUBA ([TCP and UDP over Big Addresses](http://tools.ietf.org/html/rfc1347)) and FOOBAR ([FTP Operation Over Big Address Records](http://tools.ietf.org/html/rfc1639)).

In the end, IETF decided to invent yet another protocol (IPv6), effectively quadrupling the IPv4 address size while retaining most of the benefits and drawbacks of IPv4. If I remember correctly, the technical explanation for this decision was the variable-length of the CLNS addresses (which make the hardware implementation of layer 3 forwarding pretty complex), while one of the real reasons was probably also the \"not-invented-here\" syndrome (and the lack of total control over a new protocol inherited from another organization).

CLNS was widely used in early large IP networks primarily due to the multi-protocol implementation of [IS-IS](http://en.wikipedia.org/wiki/IS-IS) (the CLNS routing protocol that is roughly equivalent to OSPF), which came from DECnet phase V(anyone remember DEC, the maker of great minicomputers and probably the best operating system ever written?). Several very large networks used IS-IS at that time, forcing Cisco to optimize IS-IS code before they managed to fix the OSPF code. This led to an interesting phenomenon: the best-performing IP routing protocol was a protocol endorsed by ISO that was never designed (initially) to carry IP prefixes.

When network engineers claim that they use CLNS in their networks, they usually want to say that they use IS-IS, which uses CLNS addresses to identify routers (similar to IPv4 addresses used by OSPF as the Router ID). The actual forwarding of CLNP datagrams (what I would consider the real usage of CLNS) is very rare today; the last time I\'ve seen it, CLNP was used in the management networks to manage Sonet/SDH devices. Most of these devices support IP as the transport protocol today, making CLNP mostly obsolete.
