---
title: "BGP-Free Network Core with SRv6"
date: 2026-10-07 07:27:00+0200
tags: [ SRv6 ]
srv6_tag: intro
---
The concept of a [BGP-free core](https://blog.ipspace.net/2012/01/bgp-free-service-provider-core-in/) is decades old:

* The network core routers (P routers in MPLS terminology) do not carry BGP routes; BGP routes are exchanged solely between network edge routers.
* The core routers thus cannot use the customer IP addresses in the packet forwarding process.
* The edge routers (PE routers in MPLS terminology) know how to reach BGP next hops using an encapsulation mechanism that makes IP packets opaque to the network core.

{{<note info>}}
Interestingly, the concept predates Cisco's Tag Switching (later MPLS) by at least a decade; that's how all ATM and Frame Relay networks worked (with ATM VPI/VCI or Frame Relay DLCI used as the in-network addresses).
{{</note>}}
<!--more-->
Regardless of that bit of historic trivia, we started talking about a BGP-free core in combination with MPLS encapsulation. It doesn't matter whether the MPLS labels for BGP next hops are distributed with a routing protocol ([Segment Routing with MPLS labels](https://blog.ipspace.net/2021/05/segment-routing-mpls-bgp-free-core/), [sample lab topology](https://blog.ipspace.net/2026/09/sr-mpls-bgp-free/)) or a separate control-plane protocol (LDP or RSVP/TE).

If SRv6 wants to be *[the one technology to bind them all](/tag/srv6)*, it has to have a solution for this scenario, and of course, it does -- layer-3 services with SRv6 next hops defined in [RFC 9252](https://www.rfc-editor.org/info/rfc9252/):

* The network core uses IPv6 addresses
* The core routing protocol is used to build IPv6 routing tables, which might include SRv6 locators.
* The edge routers have to establish BGP sessions over IPv6 (that's the only protocol used in the network core)
* The IPv4 address family has to be activated over the IPv6 transport session and use IPv6 next hops because the routers cannot know how to reach IPv4 next hops across an IPv6-only network.
* The IPv4 address family thus has to use *extended nexthop* BGP capability with [RFC 8950](https://www.rfc-editor.org/info/rfc8950/)-style IPv6 next hops.

However, that's not enough to carry customer IPv4 or IPv6 packets across an IPv6-only network when the network core doesn't know the customer routes. We could use VXLAN or GRE encapsulation to get customer IP packets across the core, but some vendors want us to believe SRv6 is the final answer to life, universe, and everything, so there you go 🤷🏻‍♂️

That brings us to the final detail: if an ingress PE router wants to use SRv6 encapsulation to send customer IP packets toward an egress PE router, the egress PE router MUST attach the SRv6 encapsulation information to the BGP updates using the Prefix SID optional transitive attribute defined in [RFC 8669](https://www.rfc-editor.org/info/rfc8669/) and extended with [layer-3 service TLVs](https://www.rfc-editor.org/info/rfc9252/#section-5) defined in [RFC 9252](https://www.rfc-editor.org/info/rfc9252/).

I might go into the details in a later blog post; here's a sample BGP update message[^CW]:

[^CW]: As shown in Wireshark 4.4.19 using [Edgeshark](https://netlab.tools/extool/edgeshark/) to capture traffic in a [netlab lab](https://github.com/ipspace/srv6-examples/tree/main/2-services/1-ipv4-islands).

{{<figure src="/2026/10/bgp-ipv4-island-update.png">}}

* A BGP Update message is carried in a TCP session between IPv6 endpoints;
* The message describes an IPv4 unicast (AFI/SAFI=1/1) prefix 172.16.1.0/24 with an IPv6 extended next hop
* There is a BGP Prefix-SID BGP attribute attached to the update with an SRv6 L3 Service TLV.

The BGP Prefix-SID is as complex as one could expect from a *Grand Unifying Technology*:

{{<figure src="/2026/10/bgp-srv6-prefix-sid.png">}}

If you want to understand all the noise down to the sub-sub-TLV level (that's four levels down from the BGP Update message), you're welcome to spend as much time as you want getting acquainted with RFC 9252. The practical part of that screenshot is the SRv6 SID Value (5f00:0:2:e000::), because that's what you'll see in the packet headers for traffic sent toward customer prefix 172.16.1.0/24:

{{<figure src="/2026/10/srv6-ipv4-island-icmp.png">}}

And now you know just enough about *[IPv4 Islands over SRv6](https://www.ietf.org/archive/id/draft-mishra-idr-v4-islands-v6-core-4pe-10.html)* to get into a nice mess once things don't work as expected.
