---
date: 2010-11-08 06:56:00.016000+01:00
tags:
- IPv6
- workshop
title: 'IPv6 Addressing: How Wrong Can You Get It?'
url: /2010/11/ipv6-addressing-how-wrong-can-you-get/
---
Mike was wondering whether his ISP is giving him what he needs to start an IPv6 pilot within his enterprise network. He wrote:

> So I got an IPv6 assignment with a /120 mask (basically our IPv4/24 network mapped to IPv6) and two smaller networks to use for links between our external router and the ISP.

{{<note>}}Believe it or not, I'm not making this up. I was as amazed as you probably are.{{</note>}}

Dear Mike's ISP: where were you when the rest of the world was preparing to deploy IPv6? Did you read [*IPv6 Unicast Address Assignment Considerations*](http://tools.ietf.org/html/rfc5375) (RFC 5375) or [*IPv6 Address Allocation and Assignment Policy*](http://www.ripe.net/docs/ipv6policy.html) from RIPE or your regional registry?
<!--more-->
Let's start with prefix lengths. RFC 5375 is very explicit (section 3):

> Using a subnet prefix length other than a /64 will break many features of IPv6, including Neighbor Discovery (ND), Secure Neighbor Discovery (SEND) \[RFC3971\], privacy extensions \[RFC4941\], parts of Mobile IPv6 \[RFC4866\], Protocol Independent Multicast - Sparse Mode (PIM-SM) with Embedded-RP \[RFC3956\], and Site Multihoming by IPv6 Intermediation (SHIM6) \[SHIM6\], among others.

It's therefore highly recommended to use a /64 prefix on every subnet. The use of longer prefixes on point-to-point inter-router links is debatable (some people recommend /126 or /127, others /112). Properly implemented network devices have no problem with shorter subnets; after all, IPv6 is classless. However, to ensure you won't get a hiccup from a just-good-enough-too-cheap-to-pass box someone will eventually connect to your network, be conservative and use /64 everywhere.

**Summary:** assigning someone a public /120 prefix is \... let's be diplomatic \... out of touch with reality.

So, Mike got a /120 and tried to make sense out of it. He needs to allocate IPv6 addresses to the whole network and somehow can't do that with a /120. Here is the next bit of wisdom passed to him by a helpful colleague (I'm not making this up either):

> I asked someone more familiar (but no hands-on-experience) about this, and got the answer that I should use a link-local or unique-local addresses beginning with fe08 or fd for all computers within the company, the same way we use RFC1918 addresses today, and then just NAT them to the /120 network I got assigned from the ISP.

We were all confused by the plethora of different types of IPv6 addresses ([Packet Pushers IPv6 podcast](http://packetpushers.net/show-21-ipv6-for-the-win-part-1/) has a lively debate on that topic), but they are really not that hard to grasp. Let's over-simplify them a bit:

-   Link-local addresses are a better solution for unnumbered interfaces and other communication needs before you get a real IPv6 address (for example, DHCPv6 request packets are sent from a link-local address);
-   Unique local addresses (ULA) can be used for intra-network connectivity (for example, for those hosts and servers that never communicate with the Internet). Your host could have an ULA and a global IPv6 address (or even more than one global address) and use one or the other as needed.
-   In most cases, your hosts should have a globally unique IPv6 address.

Regardless of whether you decide to use ULA or not, remember that there is no NAT in IPv6 (although some people are [seriously longing for NAT66](http://tools.ietf.org/html/rfc5902)). Let me repeat that: **there is no NAT in IPv6**.

{{<note>}}Of course that's not true. You need NAT for load balancing, and you need NPT66 for small site multihoming... but I'm digressing.{{</note>}}

Mike is thus stuck: he needs a /64 on every subnet in his network and got a meager /120 from the ISP. What's wrong? The ISP's IPv6 address allocation policy.

A minimum allocation an ISP has to give to a residential end-user is a /64. If a residential end-user needs multiple subnets, he should get a /56. Minimum end-site allocation is /48 (Mike should thus get a /48, not a /120). Minimum provider-independent allocation assigned by RIPE or ARIN is /48.

Mike could get 65000 /64 prefixes from the /48 prefix he should have got from the ISP, probably more than enough to number his entire network. If you have a larger network, it's not hard to get a larger allocation; you just have to provide the paperwork documenting your needs.

**Summary:** If you are an enterprise customer and your ISP is giving you anything less than a /48, it's time to consider changing the ISP.

For more information, check out [ipSpace.net IPv6 webinars](https://www.ipspace.net/IPv6).
