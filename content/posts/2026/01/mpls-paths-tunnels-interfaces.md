---
title: "On MPLS Paths, Tunnels and Interfaces"
date: 2026-01-20 07:29:00+0100
tags: [ networking fundamentals, MPLS, GRE ]
---
One of my readers attempted to implement a multi-vendor multicast VPN over MPLS but failed. As a good network engineer, he tried various [duct tapes](https://blog.ipspace.net/2015/06/software-defined-wanwell-orchestrated/) but found that the only working one was a GRE tunnel within a VRF, resulting in considerable frustration. In his own words:

> How is a GRE tunnel different compared to an MPLS LSP? I feel like conceptually, they kind of do the same thing. They just tunnel traffic by wrapping it with another header (one being IP/GRE, the other being MPLS).

Instead of going down the "how many angels are dancing on this pin" rabbit hole (also known as "[Is MPLS tunneling?](https://packetpushers.net/podcasts/heavy-networking/hn102-a-layer-of-indirection-is-mpls-tunneling/)"), let's focus on the fundamental differences between GRE/IPsec/VXLAN tunnels and MPLS paths.
<!--more-->
* Tunnels (IP-over-IP, IPv6-over-IPv4, GRE, IPsec, VXLAN...) were designed to connect discontiguous bits of an overlay network across an underlay network *without the underlay network ever seeing the packets*
* MPLS paths were designed to be a better *packet forwarding mechanism inside the same network*.

Because we're using tunnels to connect segments of a larger network, we must exchange reachability information between those segments. Cisco once tried to do that without the tunnel interfaces (*crypto maps* anyone?), but fortunately quickly came to their senses (VTI interfaces). Running a routing protocol over tunnel interfaces (while trying to avoid the recursive routing blowbacks) remains the best way to build an overlay network.

You were not supposed to run routing protocols over MPLS paths (don't get me started on the *MPLS TE tunnel adjacency* nightmare). The network was supposed to figure out where things are using regular routing protocols, use the results of those calculations to set up MPLS paths (LDP), and then map the forwarding equivalence classes (prefixes) onto MPLS paths.

{{<long-quote>}}
Every now and then, I bump into someone claiming that Tag Switching[^TS] was about traffic engineering or VPNs. That's simply not true; the initial use case was improved forwarding performance (in particular, using ATM switches in IP network).

Straight from [RFC 2105](https://datatracker.ietf.org/doc/html/rfc2105):

> Tag switching blends the flexibility and rich functionality provided by Network Layer routing with the simplicity provided by the label swapping forwarding paradigm.  The simplicity of the tag switching forwarding paradigm (label swapping) enables improved forwarding performance, while maintaining competitive price/performance.

[^TS]: Cisco's technology that went through the [racing-horse-to-camel transformation](https://en.wikipedia.org/wiki/Design_by_committee) within the IETF and became MPLS.
{{</long-quote>}}

The MPLS paths used to implement IP forwarding were always created on demand based on the contents of the IP routing table. Creating dynamic interfaces to map MPLS paths into would be an interesting exercise in futility. The ability to merge multiple MPLS paths to the same egress device anywhere in the network[^MP] would make the implementation of that idea even more _interesting_.

[^MP]: If you like digging into the gory details, you'll love the *[Label Merging](https://datatracker.ietf.org/doc/html/rfc3031#section-3.26)* section of the [Multiprotocol Label Switching Architecture](https://datatracker.ietf.org/doc/html/rfc3031) RFC (RFC 3031).

On the other hand, I was a bit surprised when the MPLS TE *tunnel* interfaces turned out to be unidirectional constructs[^TEL]. Preventing recursive routing and providing network designers with as much flexibility as possible[^UDT] likely outweighed any potential drawbacks.

[^TEL]: Apart from the RSVP reservations, the tail-end LSR has no idea it's the egress point of an MPLS TE tunnel.

[^UDT]: The traffic engineering tunnels are unidirectional, allowing you to have different paths in each direction. That minor detail derailed ITU to the point where they wanted to build their own version of MPLS and then [settled on MPLS-TP](https://blog.ipspace.net/2010/11/what-is-mpls-tp-and-is-it-relevant/).

Finally, you'll find even more details in the [MPLS is not tunneling](/2011/10/mpls-is-not-tunneling/) blog post from 2011.
