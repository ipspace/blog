---
date: 2021-06-22 07:16:00+00:00
ospf_tag: mp
tags:
- IP routing
- OSPF
- BGP
title: Unexpected Interactions Between OSPF and BGP
---
It started with an interesting question [tweeted by @pilgrimdave81](https://twitter.com/pilgrimdave81/status/1400718236409380864)

> I've seen on Cisco NX-OS that it's preferring a (ospf->bgp) locally redistributed route over a learned EBGP route, until/unless you clear the route, then it correctly prefers the learned BGP one. Seems to be just ooo but don't remember this being an issue?

Ignoring the "_why would you get the same route over OSPF and EBGP, and why would you redistribute an alternate copy of a route you're getting over EBGP into BGP_" aspect, [Peter Palúch](https://twitter.com/Peter_Paluch) wrote a detailed explanation of what's going on and allowed me to copy into a blog post to make it more permanent:
<!--more-->
{{<long-quote>}}
I suspect that this may be a race condition. To BGP, a locally originated (includes locally redistributed) route is preferred to an eBGP-learned route. This is because locally originated BGP routes have the weight of 32768 while all others use weight 0 by default.

With this in mind, there are two possible scenarios:

1. RIB already contains the OSPF-learned route and BGP redistributes it before it learns the eBGP route. Then, even with the eBGP-learned route, BGP bestpath picks the locally originated one, so the OSPF route stays.

2. RIB does not contain the OSPF-learned route before BGP learns the eBGP route. Then the BGP bestpath picks the eBGP route (since there's no alternative) and installs it into RIB with AD=20. Even if OSPF tries to offer its route to RIB later, it will fail due to AD=110. (3/4) 

So based on the initial state (the OSPF-learned route being or not being in the RIB), we have two possible outcomes under otherwise identical configuration and conditions - hence, a race condition. Note that this would also happen with other IGPs redistributed into BGP.
{{</long-quote>}}

Of course Peter was right, but [pilgrimdave81 kept wondering](https://twitter.com/pilgrimdave81/status/1400742176728961024) about the underlying reasons for that behavior:

> Yes, this is exactly what happens, and changing timing changes it, however I'd have thought it would work out that the "locally originated" bgp route actually came from an inferior source protocol and corrected itself?

Here's Peter with another detailed explanation:

{{<long-quote>}}
Assuming there is an "inferior source protocol" is the mistake here:

1. OSPF has its route in RIB
2. BGP redistributes it
3. BGP decides the locally originated route is the best
4. hence, no eBGP route can beat it based on BGP bestpath rules

BGP does not think speculatively: "If the route to redistribute would not be there, the eBGP route would win, and then it would win even over the OSPF route to redistribute since the AD is lower". This kind of what-if decision making does not exist in routing protocols.

There are three moving parts here: BGP, OSPF, and RIB. Each one of them acts based on the momentary state. OSPF is really unperturbed -- its SPF always produces the same result, regardless of what's going on in BGP and RIB. At worst, its routes won't be picked as best by RIB.

BGP, on the other hand, is the destination of the redistribution, and so its bestpath results depend on what routes are there to choose from. By default, in presence of a locally injected route, any other path will lose. The type of the chosen path also determines its AD.

And here's the trick: If the timing allows to install an eBGP route in the RIB by BGP, then OSPF has no chance of beating it, so the BGP won't ever see that there is another option for that route to consider. Essentially, from this point of view, BGP locks itself out.

The concept of an "inferior source protocol" is based on the AD, but neither OSPF nor BGP are in business of comparing ADs, ever. In the case of redistribution taking place, it's actually BGP deciding that the OSPF route redistributed into BGP is better, due to weight.

AD of the routes offered to RIB by BGP is the result of the best path selection, not an input to it. If BGP decides that an iBGP variant is the best, then it'll offer it to RIB with AD=200; if eBGP variant is the best, then with AD=20. AD comes as a consequence.

And as a universal rule, a protocol that redistributed into itself a route from another protocol won't attempt to install that very same route back into RIB - because it could change its origin protocol, so the redistribution would no longer apply to it. It'd flap wildly.
{{</long-quote>}}

Lesson learned: having too many moving parts results in interesting and hard-to-grasp behavior... more so when the details are implementation-specific as [Jeff Tantsura detailed in a follow-up tweet](https://twitter.com/jtantsura/status/1401248088988164099):

> Junos doesn’t differentiate (AD wise) between eBGP and iBGP routes, both have AD of 170 (OSPF 10/150), so IGP always wins (predictably). EOS, while supporting weight, doesn’t set it to higher value for redistributed routes.

In other words: a perfect scenario to troubleshoot when your network is down on a Sunday night. Don't try to fix it by [using BGP as the universal answer to life, the Universe and everything](/2021/06/use-best-tool-for-job/). Having a sane and simple design is a much better alternative.
