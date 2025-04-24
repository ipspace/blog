---
title: "Worth Reading: BGP Unnumbered in 2025"
series_title: "BGP Unnumbered in 2025"
date: 2025-04-24 08:06:00+0200
tags: [ BGP, worth reading ]
---
Gabriel sent me a pointer to a blog post by [Rudolph Bott](https://blog.bott.im/about/) describing the [details of BGP Unnumbered implementations on Nokia, Juniper, and Bird](https://blog.bott.im/bgp-unnumbered-in-2025-same-idea-different-implementations/).

Even more interestingly, Rudolph points out the elephant I [completely missed](https://blog.ipspace.net/2022/11/bgp-unnumbered-duct-tape/): [RFC 8950](https://www.rfc-editor.org/rfc/rfc8950.html) refers to [RFC 2545](https://www.rfc-editor.org/rfc/rfc2545#section-3), which requires a GUA IPv6 next hop in BGP updates (well, it uses the SHALL wording, which usually means "troubles ahead"). What do you do if you're running EBGP on an interface with no global IPv6 addresses? As expected, vendors do different things, resulting in another [fun interoperability exercise](/2025/04/evpn-symmetric-irb-arp/).

Finally, there's [RFC 7404](https://datatracker.ietf.org/doc/html/rfc7404) that advocates LLA-only infrastructure links, so we might find the answer there. Nope; it doesn't even acknowledge the problem in the Caveats section.

For even more information, read the [Unnumbered IPv4 Interfaces](/series/unnumbered-interfaces/) and [BGP in Data Center Fabrics](/series/dcbgp/) blog posts.
