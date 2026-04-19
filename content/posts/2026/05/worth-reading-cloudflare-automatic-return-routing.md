---
title: "Hmmm: Cloudflare's Automatic Return Routing"
date: 2026-05-06 08:12:00+0200
tags: [ worth reading ]
---
A while ago, I found the [How Automatic Return Routing solves IP overlap](https://blog.cloudflare.com/automatic-return-routing-ip-overlap/) article on Cloudflare's blog. They evidently have a technology that addresses a pain point well worth solving (access to shared resources from clients using overlapping address ranges). I just hate how they're selling it. Go read the article first; I'll wait.

OK, here's what bothers me: the "VRFs and NAT are bad" claims, while they use the same technology in disguise.
<!--more--> 
Let's unravel what they're doing:

* They use session information to select the forwarding table (VPN tunnel) used for return traffic. We called those forwarding tables VRFs.
* Regardless of how smart they handle session setup, they will inevitably hit the case of two clients with the same source IP address *using the same source port*[^VR]. Handling that requires remapping (at least) the source port. You can call that remapping whatever you want; I call it NAT.

[^VR]: While that's admittedly very rare, I'm positive Cloudflare's engineers didn't just shrug and said "We believe in the magic powers of statistics." They're experienced enough to have encountered the [Birthday Paradox](https://en.wikipedia.org/wiki/Birthday_problem) more than once.

So what they really do is well-orchestrated inter-VRF NAT at scale. I'm positive it's a great solution that doesn't deserve the negative hype they're using to sell it.

Incidentally, they also proved that session-based forwarding works at scale. It would be nice to know how fast they can make it work and what CPU resources the solution consumes.
