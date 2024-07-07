---
date: 2022-01-26 08:03:00+00:00
dcbgp_tag: details
series:
- dcbgp
tags:
- BGP
title: Three Dimensions of BGP Address Family Nerd Knobs
---
Got into an interesting BGP discussion a few days ago, resulting in a wild chase through recent SRv6 and BGP drafts and RFCs. You might find the results mildly interesting ;)

BGP has three dimensions of address family configurability:

* **Transport sessions**. Most vendors implement BGP over TCP over IPv4 and IPv6. I'm sure there's someone out there running BGP over CLNS[^CLNS], and there are already drafts proposing running BGP over QUIC[^QUIC].
* **Address families** enabled on individual transport sessions, more precisely a combination of [Address Family Identifier](https://www.iana.org/assignments/address-family-numbers/address-family-numbers.xhtml) (AFI) and [Subsequent Address Family Identifier](https://www.iana.org/assignments/safi-namespace/safi-namespace.xhtml).
* **Next hops address family** for enabled address families.
<!--more-->
Let's start with a few well-known AFI/SAFI combinations:

* 1/1 stands for IPv4 (1) unicast (1)
* 1/2 is IPv4 (1) multicast (2)
* 2/1 is IPv6 (2) unicast (1)
* 2/2 is ... ;)
* 1/4 is IPv4 (1) with MPLS labels (4 = MPLS-labeled prefix)
* 1/128 is IPv4 MPLS VPN (128 = MPLS-labeled VPN address)
* 2/128 is IPv6 MPLS VPN
* 25/70 is EVPN (25 = L2VPN, 70 = EVPN)

AFI/SAFI combinations are negotiated between adjacent BGP neighbors in BGP capabilities exchange, [bringing down the BGP transport session](/2021/11/bgp-dynamic-capability/) every time you change AFI/SAFI set on that session unless your vendor implemented [Multisession BGP](https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgp-multisession) which opens a new transport session for every AFI/SAFI combination.

In Ye Olde Days they made a sane[^SANE] assumption that the next hop for an address family would belong to the same address family (AFI):

* IPv4 unicast and multicast had IPv4 next hops
* IPv6 unicast and multicast had IPv6 next hops

It was perfectly possible from the day Multiprotocol Extensions for BGP ([RFC 4760](https://datatracker.ietf.org/doc/html/rfc4760)) were implemented to run IPv4 unicast (1/1) address family over IPv6 session (or vice versa). After all, BGP updates are just application data, and you could theoretically use avian carries to transport them around. There's just the tiny little detail of next hop processing: whenever a router doesn't have a usable next hop handy, it takes its transport address as the next hop. 

The results of running IPv4 AF over IPv6 transport session or vice versa are usually hilarious; you need some serious route-map-fu to make it work (set next hop by hand unless it's already set), and the results are usually not worth the effort[^NH].

[^SANE]: The assumption is still sane, it's the networking industry that got insane turning BGP into an eventually consistent policy-aware kitchen sink.

[^QUIC]: A while ago, everything was better with Bluetooth. These days, everything is better with QUIC.

[^CLNS]: Cisco implement CLNS address family, but it has to run over IPv4 transport session.

[^NH]: Not sure whether I wrote a blog post about this, I know it's covered in _[Building Large IPv6 Networks](https://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks)_ webinar.

The *prefixes and next hops belong to the same address family* assumption started to break down the moment someone decided to use BGP to propagate VPNv4 prefix information. As is so often the case they ended with a Quick-and-Dirty Solution (QDS):

* [VPNv4 (MPLS VPN)](https://datatracker.ietf.org/doc/html/rfc4364) had VPNv4 next hops that were really IPv4 next hops encoded as L3VPN address with RD set to zero.
* [VPNv6](https://datatracker.ietf.org/doc/html/rfc4659) could have IPv4 or IPv6 next hops -- IPv6 next hops are VPNv6 addresses with RD set to zero, IPv4 next hops are specified as IPv4-mapped IPv6 addresses with RD set to zero.

Labeled unicast (BGP-LU -- RFC 8277) is another tweak: let's pretend the prefix (NLRI) is a bit longer than usual and contains the label, but the next hop still belongs to the same address family.

Then there's EVPN. [EVPN with MPLS](https://datatracker.ietf.org/doc/html/rfc7432) can use IPv4 or IPv6 next hops (because we just need a label toward the next hop anyway), [EVPN with VXLAN](https://datatracker.ietf.org/doc/html/rfc8365) usually needs IPv4 next hop. I don't have enough time to dig out the how that works; the details are left as an exercise for an overzealous reader.

The list goes on and on and on and on... and every time you open another RFC you realize how much you don't know.

But wait, there's more. [RFC 5549](https://datatracker.ietf.org/doc/html/rfc5549) (used to implement [Cumulus unnumbered EBGP feature](/2015/02/bgp-configuration-made-simple-with/)) and its successor [RFC 8950](https://datatracker.ietf.org/doc/html/rfc8950) describe how to use IPv6 next hops for IPv4 prefixes. That obviously doesn't make much sense until you throw some serious ARP glue at the problem ([this RIPE presentation](https://ripe65.ripe.net/presentations/101-RIPE65.pdf) does a decent job of explaining the details)... unless you believe in the Power of SRv6.

SRv6 can be used to implement numerous [BGP-based overlay services](https://datatracker.ietf.org/doc/html/draft-ietf-bess-srv6-services-05), including global IPv4 and IPv6, and VPN IPv4 and IPv6 -- SRv6 proponents reinvented most everything we did in the MPLS world, the only difference being much higher overhead and more complex hardware required by SRv6[^CUST].

[^CUST]: ... which is awesome for everyone involved but the customers.

Anyways, if you want to run IPv4 over SRv6, you have to send IPv4 traffic to a SRv6 SID, which is an IPv6 address, thus the need for IPv6 next hops on IPv4 unicast BGP address family, which is usually transported over an IPv6 TCP session. 

A careful reader might wonder how we're going to negotiate the plethora of options. Welcome to the *[Extended Next Hop Encoding Capability](https://www.iana.org/assignments/capability-codes/capability-codes.xhtml)* defined in RFC 8950. Capability value is a set of triplets specifying AFI/SAFI/Nexthop AFI, enabling you to tell your neighbors "I want to run IPv4 (AFI) VPN Unicast (SAFI) over IPv6 next hop (NH-AFI)". Cluedo anyone?

Finally: is it possible to run IPv4 AF with IPv6 next hops over IPv4 transport session? Sure, I just hope no-one implemented it.

