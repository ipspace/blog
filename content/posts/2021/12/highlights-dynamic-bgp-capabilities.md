---
title: "Highlights: Dynamic Negotiation of BGP Capabilities"
date: 2021-12-15 06:48:00
tags: [ BGP ]
---
The _[Dynamic Negotiation of BGP Capabilities](https://blog.ipspace.net/2021/11/bgp-dynamic-capability.html)_ blog post generated almost no comments, apart from the #facepalm realization that a [certain network operating system resets IBGP sessions when the sole EBGP session goes down](https://blog.ipspace.net/2021/11/bgp-dynamic-capability.html#891), but there were a few interesting comments on LinkedIn and Twitter.

While most engineers easily relate to the [awkwardness of bringing down a BGP session](https://twitter.com/alex_saroyan/status/1465849573293707273) to enable new functionality (_Tearing down BGP session, as a solution reminds me rebooting a host, as a solution._), it's not as easy as it looks. As [Adam Chappell put it](https://twitter.com/packetsource/status/1465598502671732741) "_Dynamic capability renegotiation does tend to sound a bit like changing the tyres while still moving. Very neat if you can pull it off but so much to go wrong..._"
<!--more-->
Jeff Tantsura succinctly summarized the tradeoffs as "_noone wants bugs in BGP_":

> As per RFC5492, dealing with capabilities negotiation is pretty straightforward and done once in the session lifetime. Making it dynamic creates quite some complexity (think amount of code, error handling, etc).
>
> On another side - how often do we introduce new BGP capabilities without code upgrade/not in maintenance windows/unplanned? The trade-off is really - complexity(and potential bugs(and noone wants bugs in BGP) ;-)) vs ability to introduce new functionality in a non disruptive way.

Dr. Tony Przygienda was even more succint:

> Let's put it that way, some things are easy to renogotiate, some will be very painful & some you probably shouldn't even [...try...] ;-) since you probably run multiple sessions to do it.

A few examples I could easily think of:

* Negotiating address families on demand should be a no-brainer. Adding an address family cannot hurt you (you can always reject the idea), and dropping an address family is equivalent to reseting the BGP session.
* Turning *[BGP Additional Paths](https://blog.ipspace.net/2021/12/bgp-multipath-addpath.html)* on without clearing the BGP table first would be interesting. What Path ID do you assign to the entries already in the receiver's RIB? Do you resend the same paths, but with Path ID? When can the receiver clean up the old paths?

[Adam Chappell](https://twitter.com/packetsource/status/1465641402918969353) pointed out that (as is often the case) good design helps. For example, you could deploy a separate set of route reflectors per address family -- adding an address family on a PE router would never tear down an existing BGP session. 

If your network is not big enough to justify a pair of devices per address family, you might want to cheat with per-address-family loopback interfaces. Unfortunately that doesn't work. BGP uses a session collision detection mechanism that allows a single BGP session between a pair of router IDs[^HACK], unless someone implemented [Multisession BGP draft](https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgp-multisession-07), another document that has been gathering dust for almost a decade.

[^HACK]: I'm pretty positive there must be boxes out there that allow you to set router ID per neighbor or per address family, similar to what [Cisco IOS XE does per VRF](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/configuration/xe-16/irg-xe-16-book/per-vrf-assignment-of-bgp-router-id.html).