---
title: "Again: What Exactly Is MPLS?"
date: 2024-07-11 07:26:00+0200
tags: [ MPLS ]
---
Brad Casemore published an interesting analysis [explaining why Cisco should accept being a mature company with mature products](https://crepuscular-circus.ghost.io/cisco-cant-party-like-its-1999-but-the-end-is-not-near/) (yeah, you have to subscribe to view it). I always loved reading his articles, but unfortunately, this time, he briefly ventured into the "_I don't think this word means what you think it means_" territory:

> MPLS worked – and it still works – but it provided optimal value in an earlier time when the center of gravity was not the cloud. The cloud challenged the efficacy of MPLS, and it wasn’t long before SD-WAN, cloud connects, and interconnects [...] represented an implacable threat to a status quo that had once seemed unassailable.

The second part of the paragraph is (almost) true, but it had nothing to do with MPLS.
<!--more-->
MPLS is nothing more than a [data-plane encapsulation backed with one or more control-plane protocols](https://datatracker.ietf.org/doc/html/rfc3031) that provides virtual circuits across a transport network. Even some cloud providers use it internally when sending traffic along paths that cannot be implemented with the hop-by-hop forwarding paradigm (for example, Egress Peer Engineering between proxy servers and WAN edge routers).

MPLS can also be used to provide *services*, be it flying unicorns (Segment Routing), traffic engineering, L2VPNs (VPLS or EVPN), or L3VPNs (lovingly known as MPLS/VPN, but also EVPN).

Alas, when industry analysts write _MPLS_, they usually think the acronym means _MPLS/VPN services offered by service providers_. I know I am a Terminology Nazi[^SWI], but words do have meanings, and those meanings matter.

[^SWI]: And this is a [Duty Calls](https://xkcd.com/386/) blog post

Anyway, what really killed the MPLS/VPN services was not the shifting center of gravity, but [good enough (and cheaper) public Internet](https://blog.ipspace.net/2015/07/reliability-of-sd-wan-and-hybrid-wan/)[^CD]. I was [writing about that a decade ago](https://blog.ipspace.net/2014/07/could-you-replace-mplsvpn-with-ipsec/), and we were building IPsec VPNs in parallel with the MPLS/VPN services long before the [SD-WAN acronym](https://blog.ipspace.net/tag/sd-wan/) was invented. However, the lemming run started when someone figured out they could squeeze some money out of venture capitalists if only they'd [dress a bunch of old ideas in software-defined clothes](https://blog.ipspace.net/2015/06/software-defined-wanwell-orchestrated/)[^BTC].

[^CD]: The [complex deployments](https://blog.ipspace.net/2022/03/mpls-vpn-too-complex/) trying to cope with every possible customer stupidity didn't help either.

[^BTC]: Adding a sprinkle of *this is so much better than Cisco* to spice it up.
