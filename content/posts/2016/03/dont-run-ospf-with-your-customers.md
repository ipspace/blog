---
date: 2016-03-14 10:05:00+01:00
dcbgp_tag: server
ospf_tag: trust
series:
- dcbgp
series_weight: 750
tags:
- OSPF
- data center
- BGP
- IP routing
title: Don’t Run OSPF with Your Customers
url: /2016/03/dont-run-ospf-with-your-customers/
---
Salman left an interesting comment on my [*Running BGP on Servers*](/2016/02/running-bgp-on-servers/) blog post:

> My prior counterparts thought running OSPF on Mainframes was a good idea. Then we had a routing blackhole due to misconfiguration on the server. Twice! The main issue was the Mainframe admins lack of networking/OSPF knowledge.

Well, there's a reason OSPF is called *Interior Routing Protocol*.
<!--more-->
{{<note>}}Honestly, mainframe administrators have no other options: IBM, in their infinite wisdom, implemented only RIP and OSPF, and OSPF seems to be the lesser evil.{{</note>}}

However, even some networking engineers didn't get the memo. A long time ago, I encountered a service provider who [ran OSPF with their customers](/2009/08/do-not-ever-run-ospf-or-is-is-with-your/), and all customers happily shared area 0 with the provider... until a customer accidentally managed to create an intra-area default route (don't ask me how), which was preferred over provider's external default route. And so, an early attempt at plug-and-pray networking (because it's oh-so-much-easier to run OSPF with your customers than to configure static routes) failed miserably.

### 30K Foot View

Ignoring the technicalities, the main difference between OSPF (which I would never run on a host) and BGP (which I'd recommended in some cases) is the intended use:

-   OSPF is an [*Interior Routing Protocol*](https://en.wikipedia.org/wiki/Interior_gateway_protocol) designed to exchange information *within* an autonomous system.
-   BGP is an *Exterior Routing Protocol* with enough safeguards to be used *between* autonomous systems.

You might claim that the mainframe Salman mentioned belongs to the same autonomous system as the data center switches. However, even the early definitions of AS (going all the way back to [RFC 1654](https://tools.ietf.org/html/rfc1654)) don't talk about physical proximity:

> The classic definition of an Autonomous System is a set of routers under a single technical administration...

Obviously, the mainframe team and the networking team weren't a *single technical administration*.

### Technical Differences

The intended use cases heavily influenced the design and behavior of OSPF (or IS-IS) and BGP:

-   BGP uses a pretty conservative approach to information propagation: receive → filter → evaluate → filter → propagate best information.
-   OSPF is focused on speed-of-convergence and uses a radically different approach: receive → flood everything → evaluate.

In other words, anyone who's part of an OSPF domain can insert any stupidity they wish into the domain, and **there's nothing anyone else can do to stop the propagation of that stupidity** within an area, **and it stays in the area for at least half an hour**. There are (as expected) vendor-specific kludges one can use between areas, but within area flooding rules (and external routes get flooded across area boundaries unless you use NSSA areas).

### To Summarize

As I [wrote 2.5 years ago](/2013/08/virtual-appliance-routing-network/): Don't ever run OSPF with a third party, even if that third party happens to be your friendly server administrator. It's not that you wouldn't trust him, it's just that you don't need so many additional sources of semi-reliable information plugged straight into the heart of your network.

Finally, to learn more about running BGP between servers and ToR switches, watch the [Leaf-and-Spine Fabric Designs](http://www.ipspace.net/Leaf-and-Spine_Fabric_Designs) webinar.