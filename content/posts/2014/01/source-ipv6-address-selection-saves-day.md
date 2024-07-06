---
date: 2014-01-14 07:31:00+01:00
tags:
- IPv6
title: Source IPv6 Address Selection Saves the Day
url: /2014/01/source-ipv6-address-selection-saves-day.html
---
My recommendation to use [ULA addresses for internal communications](/2014/01/i-say-ula-you-hear-nat.html) within [organizations that don't have their own provider-independent address space](/2013/09/to-ula-or-not-to-ula-thats-question.html) resulted in the following comment:

> \[...\] Having ULA for internal company communication and global IPv6 addresses for communication with the Internet will cause lots of issues with application guys since now application has to bind to specific IPv6 address for internal communications and another IPv6 address to go to the Internet.

Numerous aspects of IPv6 [may still be broken](/2011/12/ipv6-multihoming-without-nat-problem.html), but fortunately this is not one of them.

{{<note warn>}}
I missed a crucial detail: because RFC 6724 prefers IPv4 addresses over ULA addresses, [impossible to use ULA addresses](/2022/05/ipv6-ula-made-useless.html) in dual-stack networks. Even this aspect of IPv6 is broken :(
{{</note>}}
<!--more-->
### Client-Side Behavior

Every major IPv6 protocol stack includes *source IPv6 address selection* functionality specified in [RFC 6724](http://tools.ietf.org/html/rfc6724) (or its predecessor, [RFC 3484](http://tools.ietf.org/html/rfc3484)). These rules select source IPv6 address of an outgoing TCP session or UDP packet in instances when the application doesn't specify it.

{{<note>}}Things were simpler in the IPv4 world as most hosts had a single IPv4 address on each interface. Every IPv6 host able to communicate beyond the local subnet has at least two operational IPv6 addresses, one of them being link-local address.{{</note>}}

The default source IPv6 address selection rules solve the ULA/global address selection challenge. These rules result in the following behavior:

{{<note warn>}}This is a good-enough oversimplified description. Read the [RFC 6724](http://tools.ietf.org/html/rfc6724) for details.{{</note>}}

-   If the destination IPv6 address is ULA, and the source host has an ULA address, the ULA source address is used;
-   If the destination IPv6 address is a global address, and the source host has a global IPv6 address, the global source IPv6 address is used;
-   If the destination IPv6 address is ULA, and the source host doesn't have an ULA address, it uses whatever other IPv6 address is available (preferring global IPv6 addresses over alternatives);
-   If the destination IPv6 address is a global IPv6 address and the source host has an ULA address but no global IPv6 address, it tries to use the ULA source IPv6 address (and might reach the destination or not).

**Summary:** no problem on the client side. No additional administrative burden (read: default address selection policies built into major operating systems work just fine) if you use ULA+global addresses.

### Server-Side Behavior

Many applications bind themselves to a wildcard socket address -- they accept incoming connections addressed to any IPv4/IPv6 address available on the destination host. These applications would accept incoming connections addressed to global or ULA addresses configured on a server. Is that a problem? Usually it isn't (but of course it all depends).

**Security aspects**: You might want to block incoming connections to global IPv6 address configured on the server. No problem, use a host firewall available in every major operating system, or an ACL on the first-hop layer-3 switch. Security by obscurity (using internal addresses only) or partial reachability has never been a good idea anyway.

**Service reachability aspects**: Even though a server accepts incoming connections to its ULA and global IPv6 addresses doesn't mean the clients will use them. If the internal DNS contains ULA addresses of internal servers, most clients won't use servers' global IPv6 addresses anyway. If you're worried about potential intruders, read the preceding paragraph.

Finally, **do we need global IPv6 addresses on** **internal** **servers**? It depends on whether the servers have to reach the global Internet. You might decide to use only ULA addresses on these servers and connect the public-facing servers to the global Internet through a load balancer (a stateful NAT66 implementation with no religious connotations).

**Summary**: a combination of global IPv6+ULA addresses on the servers does not introduce new problems (but might expose shoddy practices used in the past).

### Need More IPv6 Information?

My [IPv6 webinars](http://www.ipspace.net/Roadmap/IPv6_webinars) and [public presentations](http://www.ipspace.net/Presentations#IPv6) will help you plan, design and deploy IPv6 in your network.