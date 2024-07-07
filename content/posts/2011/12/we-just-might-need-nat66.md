---
date: 2011-12-06 07:12:00+01:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
- NAT
- LISP
title: We Just Might Need NAT66/NPT66 (and Not LISP)
url: /2011/12/we-just-might-need-nat66/
---
My friend Tom Hollingsworth has written another [NAT66-is-evil](http://networkingnerd.net/2011/12/01/whats-the-point-of-nat66/) blog post. While I agree with him in principle, and most everyone agrees NAT as we know it from IPv4 world is plain stupid in IPv6 world (NAPT more so than NAT), we just might need NPT66 ([Network Prefix Translation; RFC 6296](http://www.rfc-editor.org/rfc/rfc6296.txt)) to support [small-site multihoming](/2009/05/small-site-multihoming-tutorial/) \... and yet again, it seems that many leading IPv6 experts grudgingly agree with me.
<!--more-->
### The Problem

There's plenty of multihoming going on in the current Internet without anyone being aware of it. Anyone using Internet for mission-critical applications (or business-grade cloud access) can get two Internet connections from two upstream providers and [use pretty simple NAT tricks to use those connections](/2009/05/small-site-multihoming-tutorial/) in either active-standby or active-active mode. I'm personally aware of a few large multinational organizations using similar designs for remote office or retail access.

{{<figure src="/2009/05/SOHO_Multihoming_Addressing.png" caption="Simple small site multihoming">}}

Using currently available low-end routers and existing IPv6 host stacks (with [TCP stack without a session layer](/2009/08/what-went-wrong-tcpip-lacks-session/) and [broken socket API](/2009/08/what-went-wrong-socket-api/)) you can solve the same problem in one of two ways in the IPv6 world:

**BGP-based multihoming**. Get a large chunk of provider-independent (PI) address space and an AS number, assign a /48 to every location, and run BGP with two upstream ISPs from every location.

{{<note info>}}With a few routing tricks you don't need more than one AS number; you can use default routing or **allowas-in** to get connectivity between your sites.{{</note>}}

With this approach anyone in Elbonia who's willing to pay ASN and PI prefix tax (a few tens or hundreds € or \$ per year) and a business-grade ISP connection to two Service Providers gets the chance to pollute routing and forwarding tables in every router in the default-free zone \... worldwide. Not something I'm looking forward to.

**VPN-based multihoming.** You use your own address space within the remote office site; the public address space assigned by the ISPs is used only to address tunnel endpoints. This design does not allow *local Internet exit* (all Internet traffic has to be shuffled over a VPN tunnel to a central hub site) -- often a showstopper for companies that have widespread remote offices.

**NPT66-based multihoming.** Works in exactly the same way as NAT-based multihoming in IPv4, but translates only on the upper 64 bits of the IPv6 prefix. It's NAT (so it's evil), but at least it's stateless.

### Unicorn Tears and Other Solutions

There are a number of other solutions we could use, but they all require changes to the host IPv6 stack, so it's not likely we'll see them implemented any time soon.

[SCTP](http://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol) and [Shim6](http://en.wikipedia.org/wiki/Shim6) are pretty old and well-known. SCTP requires application-level changes (due to broken socket API), Shim6 requires changes in the IPv6 stack.

[IPv6 multihoming without IPv6 NAT](http://ietfreport.isoc.org/idref/draft-ietf-v6ops-ipv6-multihoming-without-ipv6nat/) is one of the emerging IETF drafts that try to address the problem (you should read at least the first few sections, where they admit you need NPT66) \... but yet again requires changes to the host IPv6 stack to work properly (but only in the source IP address selection policy code).

[LISP](http://en.wikipedia.org/wiki/Locator/Identifier_Separation_Protocol) would replace BGP-based multihoming with LISP-based multihoming (moving the customer prefixes into the LISP+ALT topology, which yet again uses BGP). This approach will probably work well once everyone deploys LISP (like: never?). In the meantime, you'll need proxy-ITR/ETR routers (6to4 relays anyone?), resulting in suboptimal traffic flows and central choke points.

### Summary

As much as I hate to admit it, NPT66 seems to be the most flexible solution for the small-site IPv6 multihoming problem we have today. I would love to see the host IPv6 stacks fixed, but I've learned a sad lesson from the history of NAT: once the networking McGyvers fix other people's problems with layers of duct tape, everyone starts pretending the problem is gone and goes off chasing another squirrel.

### More information

-   [*Enterprise IPv6 -- the first steps*](http://www.ipspace.net/Enterprise_IPv6_-_the_First_Steps) webinar gives you an overview of IPv6 technologies, 4-to-6 migration alternatives and design recommendations.
-   [*Service Provider IPv6 Introduction*](http://www.ipspace.net/Service_Provider_IPv6_Introduction) is an introductory-level webinar targeting ISP environments.
-   [*Building Ipv6 Service Provider Core*](http://www.ipspace.net/Building_IPv6_Service_Provider_Core) webinar describes access- and core-layer technologies and designs.

All three webinars (and numerous others) are part of the [yearly subscription](http://www.ipspace.net/Subscription).
