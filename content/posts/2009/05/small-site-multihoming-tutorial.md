---
date: 2009-05-15 06:39:00.003000+02:00
lastmod: 2020-11-20 07:00:00
multihoming_tag: site
series:
- multihoming
tags:
- NAT
- IP routing
title: Small Site Multihoming Tutorial
url: /2009/05/small-site-multihoming-tutorial.html
---
In 2007 and 2008 I wrote several articles covering small-site multihoming (a site connected to two ISPs without having its own public address space or running BGP).

### Basics

A multihomed site is a customer site connected with (at least) two uplinks to one or more Internet Service Providers (ISP). Traditionally, a multihomed site needs its own provider independent (PI) public IP address space, has to run BGP with the upstream ISP and thus needs its own BGP autonomous system (AS) number.
<!--more-->
These requirements are viable for central sites of enterprise networks or high-availability e-commerce solutions, but completely unrealistic if you want to multi-home a small site (or numerous remote sites of a single enterprise network).

### Single-Router Small-Site Multihoming

Connecting a small site to multiple service providers can be extremely easy – you get two upstream links and two provider-assigned (PA) IP addresses (either static or dynamically assigned). Since each ISP will give you only a single IP address, you have to use private IP addresses on the LAN side of the router and perform Network Address Translation (NAT) on the gateway router.

{{<figure src="SOHO_Multihoming_Addressing.png" caption="IP addressing in a multihomed small site">}}

As most ISPs will not be willing to run a dynamic routing protocol with small sites, you have to configure static default routing on your end. Reliable static routing (static routes tied to IP SLA measurements) should be used to ensure failure detection of any component between your router and the core of the Service Provider network.

{{<figure src="SOHO_Multihoming_Routing.png" caption="Static routing in a multihomed small site">}}

{{<jump>}}[Read more](https://learning.nil.com/tips-and-tricks/technical-articles/show/small-site-multi-homing/){{</jump>}}

### Redundant Small-Site Multihoming

A redundant remote site is even simpler to implement. The addressing and routing requirements do not change (NAT from private to PA address space is performed on both gateway routers), but the routing becomes simpler: each gateway router has a single reliable static route and redistributes it into an intra-site dynamic routing protocol.

OSPF should be used as the intra-site routing protocol as its default route origination mechanisms require no route redistribution.

{{<figure src="SOHO_Redundant_Routing.png" caption="Default routing in a redundant multihomed site">}}

{{<jump>}}[Read more](https://learning.nil.com/tips-and-tricks/technical-articles/show/redundant-small-site-multi-homing/){{</jump>}}

### Servers in Multihomed Small Site

If you want to deploy high-availability public servers within your network, you should implement proper multi-homing solution including BGP routing with the Service Providers. In most other cases, it’s better to use a decent hosting service.

However, if you want to deploy local mail server within your LAN or you have a special application that simply cannot be hosted anywhere else and you’re willing to accept less-than-perfect reliability and complex design, it’s possible to deploy servers in a small-site multihoming environment.

{{<figure src="SOHO_Servers.png" caption="Servers in multi homed small site">}}

{{<jump>}}[Read more](https://learning.nil.com/tips-and-tricks/technical-articles/show/servers-in-small-site-multi-homing/){{</jump>}}

{{<note update>}}The following paragraph has been added when I updated the article in November 2020{{</note>}}

### From IPv4 to IPv6

Implementing a similar architecture in IPv6 is still a Mission Impossible, and although there have been many promises how wonderful new architectures (like [Homenet](https://datatracker.ietf.org/wg/homenet/about/)) will solve the problem, [not much has been done in more than a decade](/2015/11/theres-problem-with-ipv6-multihoming.html); the only viable solution is still Network Prefix Translation. For more details, read these blog posts:

* [Lack of IPv6 multihoming: the elephant in the room?](/2009/05/lack-of-ipv6-multihoming-elephant-in.html)
* [Small-site multihoming in IPv6: mission impossible?](/2010/12/small-site-multihoming-in-ipv6-mission.html)
* [IPv6 multihoming without NAT: the problem](/2011/12/ipv6-multihoming-without-nat-problem.html)
* [We just might need NAT66](/2011/12/we-just-might-need-nat66.html)
* [New in IPv6: The Next Chapter in IPv6 Multihoming Saga](/2018/04/new-in-ipv6-next-chapter-in-ipv6.html)
* [Are Provider-Independent IPv6 prefixes really global?](/2012/01/are-provider-independent-ipv6-prefixes.html)
* [IPv6 addressing: how wrong can you get it?](/2010/11/ipv6-addressing-how-wrong-can-you-get.html)




