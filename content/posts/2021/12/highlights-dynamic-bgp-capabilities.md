---
date: 2021-12-15 06:48:00+00:00
dcbgp_tag: details
lastmod: 2021-12-20 18:44:00
series:
- bgp-cap
- dcbgp
tags:
- BGP
title: 'Highlights: Dynamic Negotiation of BGP Capabilities'
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

If your network is not big enough to justify a pair of devices per address family, you might want to cheat with per-address-family loopback interfaces. Doing that is a bit tricky[^DS] as you have to establish BGP sessions between distinct *pairs of IP addresses*[^EVPN]. More about that in another blog post;[here's the lab setup](https://github.com/ipspace/netlab-examples/tree/master/BGP/Multi-Loopback) in case you want to try it out yourself -- you'll need *[netlab](https://netlab.tools/)* to set it up.

[^DS]: Thanks a million to [Dmytro Shypovalov](https://routingcraft.net/contact/) for setting me straight -- I claimed it cannot be done.

[^EVPN]: Similar to how some people [run IBGP over EBGP](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics) when [trying to implement BGP-only data center](https://blog.ipspace.net/2020/02/the-evpnbgp-saga-continues.html) with devices that [were not designed to run EVPN over EBGP](https://blog.ipspace.net/2019/04/dont-sugarcoat-challenges-you-have.html).

Your life becomes much easier if your vendor implemented [Multisession BGP draft](https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgp-multisession-07), another interesting idea that has been stuck in _draft_ limbo for almost a decade for no apparent reason. Topic for yet another blog post.

## Revision History

2021-12-20
: You can run multiple sessions between a pair of BGP routers *as long as they are using distinct endpoints on both ends*.
