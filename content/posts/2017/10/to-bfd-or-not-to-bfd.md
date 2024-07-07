---
date: 2017-10-23 08:11:00+02:00
dcbgp_tag: design
series:
- dcbgp
series_weight: 700
tags:
- BGP
- IP routing
title: To BFD or Not to BFD?
url: /2017/10/to-bfd-or-not-to-bfd/
---
Omer asked a pretty common question about BFD on [one of my blog posts](/2017/10/routing-protocols-perfect-example-of/) (slightly reworded):

> Would you still use BFD even if you have a direct router-to-router physical link without L2 transport in the middle to detect if there is some kind of software failure on the other side?

Sander Steffann quickly replied:
<!--more-->
> Too many things can go wrong, even on a simple point-to-point link. The latest ones I have observed are a router not properly detecting when a link goes down and one of the SFPs on a DAC cable failing while keeping the link up towards the router.

We all know that the absolutely correct answer is "it depends" (even though, in this case, I would forgo that get-out-of-jail card and lean heavily toward YES). Let's try to quantify it using the same questions we used when [discussing BGP timers](/2017/09/improving-bgp-convergence-without/):

**What problem are we trying to solve?** We're trying to detect inter-router link failure faster than what would be feasible using routing protocol hellos or timeouts.

**Are there better ways to solve the problem?** You could detect link failure at:

-   Physical layer (carrier/light loss);
-   Data link layer (UDLD, LACP, Gigabit Ethernet signaling...)
-   Network layer (BFD, routing protocols)

Physical layer failure detection is the easiest one, assuming it's reasonably reliable... but it cannot detect anything else but physical medium failure (cable cut) or drastic transceiver failure (power loss or similar).

Data link layer mechanisms might be able to detect transceiver failures (although I'm still wondering where 10GE signaling is done -- pointers are highly appreciated). LACP introduces unnecessary complexity on point-to-point router links, and UDLD is vendor-specific. Furthermore, data link layer mechanisms cannot detect end-to-end failures across a layer-2 network.

BFD is perfectly positioned to solve the network path element failure detection challenge. It sits at the [waist of the protocol hourglass](https://www.iab.org/wp-content/IAB-uploads/2010/11/hourglass-london-ietf.pdf), is standardized, and is simple enough to be easy to implement.

**What's the worst thing that could happen if I use BFD?** Aggressive BFD timers might trigger false positives due to packet loss and bring down perfectly good links.

**Why would twiddling BFD timers break things?** Some platforms might implement BFD in hardware at the line rate. I'm probably not rich enough to be able to afford them (or [this car](http://auto.ferrari.com/en_US/sports-cars-models/car-range/laferrari-aperta/)).

Most other platforms implement BFD in software -- a major consideration on platforms that use the same general-purpose CPU for packet forwarding. If higher-priority processes use all the CPU, BFD starves and might be unable to send packets or process them fast enough.

{{<note info>}}The problem is not limited to routers and switches -- Booking.com [experienced it on their load balancers](https://blog.booking.com/troubleshooting-a-journey-into-the-unknown.html).{{</note>}}

You might think that the switches performing packet forwarding in hardware wouldn't be susceptible to the same problems. They are -- unless you protect your infrastructure with strict ACLs at all the edges, it's always possible to attack it with a DoS flood. A long while ago, I could hose a Catalyst 6500 using nothing more aggressive than ARP requests.

You can (and should) use Control Plane Protection (CoPP) to protect the central CPU of your network device. Just make sure CoPP can treat NNI traffic (BFD and routing protocols) differently than UNI traffic (ARP or ping).

Long story short: be moderate on BFD timers. Figure out what your real business needs are, not what everyone assumes they are, and choose the simplest possible approach that would meet them (see also what [Deutsche Telekom did to simplify their network](/2013/11/deutsche-telekom-terastream-designed/)).
