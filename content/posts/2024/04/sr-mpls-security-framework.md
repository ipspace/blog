---
title: "SR/MPLS Security Framework"
date: 2024-04-09 09:10:00+0200
tags: [ segment routing, MPLS, security ]
---
A long-time friend sent me this question:

> I would like your advice or a reference to a security framework I must consider when building a green field backbone in SR/MPLS.

Before going into the details, keep in mind that the core SR/MPLS functionality is not much different than the traditional MPLS:
<!--more-->
* The data plane is the same. Ingress nodes add a stack of MPLS labels to each incoming layer-3 packet, and the rest of the network uses those labels for packet forwarding.
* You still need a functioning IP network core, so you need a set of routing protocols to propagate end-user prefixes and next hops.

The only significant difference between traditional MPLS and SR/MPLS is the [label allocation process](/2019/04/why-is-mpls-segment-routing-better-than.html):

* Traditional MPLS uses locally-significant labels, whereas SR/MPLS uses network-wide [Segment Identifiers](/2021/05/segment-routing-ids-mpls-labels.html).
* Traditional MPLS uses LDP to assign labels to entries in the IP forwarding table. In contrast, SR/MPLS attaches node- or adjacency segment identifiers to routing protocol data structures, eliminating an extra control-plane protocol and synchronizing MPLS forwarding with IP forwarding.

{{<note info>}}You can use network-wide labels in novel solutions like TI-LFA, but that's a topic for another day.{{</note>}}

The security recommendations for an SR/MPLS backbone thus don't differ from those I would make for a traditional MPLS backbone:

* Make sure it’s impossible to enable core routing protocols or form routing protocol adjacencies on customer-facing interfaces.
* Whenever someone breaks into the transport backbone, it’s game over. You could use encryption (but it has to be below MPLS encapsulation) to make the intruder’s life a bit more miserable (keeping in mind that the key distribution tends to be the most vulnerable bit).
* Someone could attach a third-party device to a transport link, so you’d better use routing protocol authentication.
* Finally, use the usual hardening practices on the PE- and P-devices. It doesn’t help if you do everything right just to have someone do a password recovery on one of your boxes.

Want more details? You can find them in the _[Security Framework for MPLS and GMPLS Networks](https://www.rfc-editor.org/rfc/rfc5920.html)_ (RFC 5920), or you can read the relevant chapter in the _MPLS and VPN Architectures, Volume II_ book.
