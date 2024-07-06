---
date: 2018-04-19 09:21:00+02:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
- Internet
title: Why Can’t We All Use Provider-Independent IPv6 Addresses?
url: /2018/04/why-cant-we-all-use-provider.html
---
Here's another back-to-the-fundamentals question I received a while ago when [discussing IPv6 multihoming](/2018/04/new-in-ipv6-next-chapter-in-ipv6.html) challenges:

> I was wondering why enterprise can't have dedicated block of IPv6 address and ISPs route the traffic to it. Enterprise shall select the ISP\'s based on the routing and preferences configured?

Let's try to analyze where the problem might be. First the no-brainers:
<!--more-->
-   A consumer device with high-availability requirements: use two independent uplinks (WiFi + 5G). As long as the traffic from both uplinks doesn't merge before being sent to upstream ISPs you don't have a problem (the proof is left as an exercise for the reader);
-   An organization with a single uplink to a single ISP: no problem. Use provider-assigned IPv6 address (ideally delegated via DHCPv6 IA_PD) and put all your services into a cloud, or use dynamic DNS if you want to save \$10/month.

{{<note info>}}I described the customer- and provider side of this setup in the [Building Large IPv6 Networks](http://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks) webinar.{{</note>}}

-   A large single-site organization with one or more Internet uplinks: get your own IPv6 address space and use BGP to advertise your prefix(es) to upstream ISPs. The same approach works for an enterprise with multiple large sites.

{{<note info>}}It's worth noting at this point that an Internet service that includes provider-independent address space advertised by BGP tends to be an order of magnitude more expensive than a residential service with the same speed... just because customers with such requirements are willing to pay more.{{</note>}}

Now for the trickier use case: small office of a large enterprise. Even if they'd be willing to pay for enterprise-grade Internet access for every 3-person sales office in the middle of nowhere, do you really think that the [global Internet would survive](/2012/03/anyone-can-get-ipv6-pi-space-buy-more.html) carrying [provider-independent /48 prefixes](/2011/02/ipv6-provider-independent-addresses.html) for every single small office of every rich-enough organization out there?

A similar one: [small organization with two uplinks](/2018/04/new-in-ipv6-next-chapter-in-ipv6.html). They won't pay for enterprise-grade Internet service, and won't get provider-independent IPv6 address space because it's too expensive. IETF has been tackling various aspects of [this elephant](/2010/12/small-site-multihoming-in-ipv6-mission.html) for a decade and still hasn't got anywhere close to solving it.

You might wonder how many small sites really need two uplinks. Lots of SOHO offices or remote workers do -- one the uplinks is a site-to-site VPN with the mothership. You could solve 95% of this problem with host-based IPsec VPN or SSL VPN (in both cases you don't care about the transport IP address of the client) or with [SSL proxy](/2018/03/before-commenting-on-someone-mentioning.html), but there's always the problem of remote printers and IP phones. Johannes Weber described the challenges of using VPNs with dynamic IPv6 prefixes in his [Troopers 2018 presentation](https://www.troopers.de/troopers18/agenda/9grrde/)... and it's not a pretty picture.

Anything else I've missed? Please write a comment.

### Revision History

2018-04-21
: Updated based on feedback from Dan Wing. Thank you!
