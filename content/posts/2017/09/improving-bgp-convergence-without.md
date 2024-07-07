---
date: 2017-09-19 08:44:00+02:00
dcbgp_tag: design
series:
- dcbgp
series_weight: 750
tags:
- BGP
title: Improving BGP Convergence without Tweaking BGP Timers
url: /2017/09/improving-bgp-convergence-without/
---
One of the perks of my [online courses](http://www.ipspace.net/Courses) is the lifetime access to course Slack team, and you'd amazed by the variety of questions asked there. Not so long ago I got one on BGP timers:

> The BGP timers I'm using in my network are 5 and 15 seconds, and I am not sure if it\'s a good practice to reduce them even more.

You should always ask yourself this set of questions before tweaking a nerd knob:
<!--more-->
-   What problem am I trying to solve?
-   Are there better ways to solve the problem?
-   What's the worst thing that could happen if I twiddle that knob?
-   Why would twiddling the nerd knob break things and what can I do to alleviate that (assuming I still feel it makes sense to twiddle it)?

Keep in mind that every nerd knob you start using increases the complexity of your network, which potentially increases the cost of operating it. Using vendor-specific nerd knobs is also a great way to get locked into a single-vendor solutions.

Still interested? In this blog post we'll address the first two questions.

### What Problem Am I Trying to Solve?

There's only one good reason (I found so far) to reduce the BGP timers below their ridiculously large (at least on Cisco IOS) default values: you're trying to improve convergence by reducing the time it takes for a BGP router to discover a failed neighbor.

### Are There Better Ways to Detect Neighbor Failure?

If you're running BGP between directly-connected IP addresses most decent implementations detect BGP neighbor loss as soon as the interface goes down.

You can use BFD on most platforms to detect byzantine failures of EBGP neighbors (interface or transmission path failure without carrier/light loss). BFD is a very lightweight protocol, so you should usually prefer it over routing protocol timers.

{{<note>}}BFD is another reason why it makes sense to run EBGP in data center fabrics.{{</note>}}

Some platforms support BFD for directly-connected IBGP neighbors (because they implement single-hop BFD), some support BFD for all IBGP neighbors (using multihop BFD).

Speaking of IBGP, it doesn't really matter if you lose IBGP session or two as long as the next hop (where you're supposed to send the traffic to) is reachable. Platforms that have *BGP next hop tracking* solve that problem quite nicely as they tie BGP route selection to (usually IGP-derived) next hop reachability in main IP routing table.

Assuming your platform supports next-hop tracking, and you're running IBGP between loopback interfaces, and use loopback interface addresses as BGP next hops, your (I)BGP routing table converges as fast as the IGP you're using in your AS.

### Still Feeling the Urge to Tweak the BGP Timers?

We'll figure out what could possibly go wrong in a [follow-up blog post](/2017/10/to-bfd-or-not-to-bfd/).
