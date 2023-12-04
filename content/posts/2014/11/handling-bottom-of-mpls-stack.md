---
date: 2014-11-10 08:48:00.003000+01:00
tags:
- MPLS
- MPLS VPN
title: Handling the Bottom of MPLS Stack
url: /2014/11/handling-bottom-of-mpls-stack.html
---
MPLS bottom-of-stack bit confused one of my readers. In particular, he had a problem with the part where the egress MPLS Label Switch Router (LSR) should go from labeled (MPLS) to unlabeled (IPv4, IPv6) packets and had to figure out what was in the packet.
<!--more-->
### What Is the Bottom-of-Stack Bit?

A labeled packet might have more than one label (functionality heavily used in MPLS/VPN, MPLS TE, FRR, and EoMPLS/VPN), but there's no *stack length* in the MPLS header -- the last label in the stack has a Bottom-of-Stack bit set to indicate there's no further label beneath (behind) it.

An LSR swapping labels or pushing additional labels onto the MPLS label stack can safely ignore the BoS bit; all it has to do is copy the existing BoS value to the swapped label (or to the bottom label of the label stack when it swaps a single label for a label stack -- the situation commonly encountered in MPLS/TE environments).

An LSR popping a label from the stack MUST check the BoS bit. If the BoS bit is not set, there's another label behind the popped one, and the LSR is free to forward the labeled packet toward MPLS next hop.

When an LSR pops a label with BoS set, there's no further label behind it -- the outgoing packet is no longer a labeled packet, and has to be forwarded as IPv4/IPv6/AppleTalk... packet (which includes changing the Ethertype from 0x8847 to 0x0800, 0x86DD, 0x809B or whatever else). And now for the crucial question: how does the egress LSR know what's hiding in the labeled packet?

[RFC 3032](http://tools.ietf.org/html/rfc3032) has this to say on the topic:

> When the last label is popped from a packet\'s label stack (resulting in the stack being emptied), further processing of the packet is based on the packet\'s network layer header. The LSR which pops the last label off the stack must therefore be able to identify the packet\'s network layer protocol. However, the label stack does not contain any field which explicitly identifies the network layer protocol. This means that the identity of the network layer protocol must be inferable from the value of the label which is popped from the bottom of the stack, possibly along with the contents of the network layer header itself.

### How Does It Actually Work?

The wording of RFC 3032 might sound like magic until one remembers the labels in MPLS have local significance. The egress LSR popping the label does that because its Label Forwarding Information Base (LFIB) maps the incoming label *that it has assigned* to a *pop label* action.

One would hope that the LSR assigning a label and advertising the label to its neighbors knows what it's doing and what address family the label was assigned to, in which case it's trivial to figure out what the payload of the labeled packet is.

For example, if the egress LSR assigned the label found in the incoming label to an entry in the IPv4 FIB, it's obvious that the payload of the packet is an IPv4 packet (it doesn't hurt to check that the *version* field of the IP datagram is actually set to 4).

Likewise, if the label was assigned to an IPv6 prefix (in 6PE environment) or IPv6 VRF (in MPLS/VPN environment with per-VRF label allocation mode), the payload MUST be an IPv6 packet.

### More Information

My [MPLS/VPN books](http://www.ipspace.net/Books) are still not a bad option (even though they're over a decade old), I'm describing the label swapping and popping behavior in the [Enterprise MPLS/VPN webinar](http://www.ipspace.net/Enterprise_MPLS_VPN_Deployment), and there are several free MPLS-related videos in the [MPLS Essentials](https://www.ipspace.net/MPLS_Essentials) webinar.
