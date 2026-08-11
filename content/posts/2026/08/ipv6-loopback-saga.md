---
title: "The Never-Ending IPv6 Loopback Prefix Saga"
date: 2026-08-17 08:02:00+0200
tags: [ IPv6 ]
---
Remember the sage advice to simplify your life and use the IPv6 /64 prefixes everywhere? Not only does it make your life simpler (and wastes immesuarably less address space than the crazy "let's assign /64 to [every device](https://blog.ipspace.net/2025/09/android-dhcpv6-prefix-delegation/)" stupidity), it also reduces the hardware requirements in your high-speed ~~routers~~ layer-3 switches. You see, doing lookups on 64 bits uses half the silicon it takes to do lookups on 128 bits.

Alas, some people never got the memo. OSPFv3 standard clearly states in one of the bullets in [section 4.4.3.9](https://datatracker.ietf.org/doc/html/rfc5340#section-4.4.3.9) that the loopback prefixes should always be advertised as /128s *regardless of what's configured on the interface*.
<!--more-->
We couldn't care less when loopbacks were used solely for control-plane connectivity (for example, as the endpoints of IBGP sessions). Today, we use them as VXLAN endpoints. High-speed forwarding toward loopback prefixes is thus a must.

One could square this circle in a few ways (none good, some awful):

* Most datacenter switch vendors support a limited number of IPv6 prefixes longer than /64. I have no idea what tricks they use; the worst they could do is burn the TCAM (the hardware that implements ACLs) to do pattern matching on the entire destination IPv6 address.
* While most vendors adhere to the OSPFv3 RFC and advertise the loopbacks as /128s, some (for example, Arista EOS) ignore it and advertise the loopback prefixes as configured. Want to know who else does that? Check the results of the _netlab_ **loopback prefix** [OSPFv3 integration test](https://release.netlab.tools/_html/coverage.ospfv3).
* Others refuse to accept anything but a /128 prefix on the system loopback (for example, Nokia SR OS).
* FRRouting used to behave like Arista EOS; now it advertises both -- the configured prefix and the /128 prefix. One can't be wrong that way, right?
* BIRD allows you to configure what you want to have advertised in OSPFv3 *even when the prefixes are not used on local interfaces*. Infinite flexibility is the best road to job security.
* Cisco IOS has a nerd knob that effectively says "ignore that bit of the RFC and advertise what's configured". It's called **ipv6 ospf network point-to-point** because that's the first thing one would think of when having a loopback prefix challenge.

In a nutshell, it's a mess, and the only way to get back to the saner grounds (if you believe in the /64-everywhere story, or if you're facing hardware limitations) seems to be to use either IS-IS or BGP as your IPv6 IGP. Oh, and don't get me started on the vendor (fortunately, I'm only aware of one) that still hasn't discovered multi-topology IS-IS in 2026 (probably because "nobody asked for it yet" 🤦‍♂️).
