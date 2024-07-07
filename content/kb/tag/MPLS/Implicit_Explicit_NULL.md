---
kb_section: MPLS
minimal_sidebar: true
title: Implicit and Explicit Null Label in MPLS networks
url: /kb/tag/MPLS/Implicit_Explicit_NULL/
tags: [ MPLS ]
---
The [MPLS Label Stack Encoding](http://tools.ietf.org/html/rfc3032) (RFC 3032) specifies two reserved values (among others) that are useful in the last hop of a Label Switched Path (LSP):

-   0: explicit NULL. Can be used in signaling protocols as well as label headers.
-   3: implicit NULL. Used in signaling protocols only. It should never appear in the label stack. Its use in a signaling protocol indicates that the upstream router should perform *penultimate hop popping* (PHP; remove the top label on the stack).

The *implicit NULL* should be used whenever possible, as the PHP reduces the amount of lookup required on the last hop of an LSP (sometimes that could mean the difference between hardware and software lookup).

With *implicit NULL*, the penultimate router performs a simple label lookup, pops the label, and sends an IP packet to the egress router. The egress router performs a simple IP lookup.

{{<figure src="/kb/tag/MPLS/Label_Implicit_Null.png" caption="Penultimate hop popping with implicit NULL">}}

When using the *implicit NULL*, there is no label on the last link in the MPLS network. QoS actions on that link are thus based on the IP packet DSCP value.

{{<figure src="/kb/tag/MPLS/MPLS_QoS_Implicit_Null.png" caption="MPLS QoS with implicit NULL">}}

With *explicit NULL*, the penultimate router swaps an MPLS label with a NULL label, and sends a labeled packet to the egress router. The egress router performs an MPLS label lookup and finds a NULL label which triggers another lookup in IP routing table.

{{<figure src="/kb/tag/MPLS/MPLS_Label_Explicit_Null.png" caption="End-to-end LSP with explicit NULL">}}

*Explicit NULL* could be used in environments where you want to use MPLS QoS values that are different from IP DSCP/IP Precedence values.

When the egress router signals an *explicit NULL*, a packet traversing the last link in the MPLS network carries a NULL label, the EXP bits in the label stack are preserved throughout the MPLS network, and the QoS actions performed by the penultimate router can be based on MPLS EXP bits.

{{<figure src="/kb/tag/MPLS/MPLS_QoS_Explicit_Null.png" caption="End-to-end MPLS QoS with explicit NULL">}}

By default, Cisco IOS routers advertise *implicit NULL* with LDP. To change this behavior, use the **mpls ldp explicit-null** global configuration command.
