---
date: 2013-02-13 07:40:00+01:00
tags:
- Internet
- BGP
- MPLS VPN
title: Internet-in-a-VRF and LFIB Explosion
url: /2013/02/internet-in-vrf-and-lfib-explosion/
comment: |
  This blog post is over a decade old. I hope the only time you'll see a Catalyst 6500 is in a computer museum (although I've heard some organizations still run them in production networks), and the full BGP table has almost a million entries. However, the underlying dilemma is as relevant as it was in those days; we still don't have infinite forwarding tables.
---
[Matthew Stone](http://twitter.com/bigmstone) encountered another unintended consequence of [full Internet routing in a VRF](/2012/07/is-it-safe-to-run-internet-in-vrf/) design: the TCAM on his 6500 was 80% utilized even though he has the new Sup modules with one million IPv4 routes.

A closer look revealed the first clue: L3 forwarding resources on a Cat6500 are shared between IPv4 routes and MPLS labels (I don't know about you, but I was not aware of that), and half the entries were consumed by MPLS labels:
<!--more-->
```
L3 Forwarding Resources
   FIB TCAM usage:                     Total        Used       %Used
       72 bits (IPv4, MPLS, EoM)     1048576      843727         80%
       144 bits (IP mcast, IPv6)      524288       11654          2%
       288 bits (IPv6 mcast)          262144           3          1%

   detail:      Protocol                    Used       %Used
                IPv4                      433781         41%
                MPLS                      409945         39%
                EoM                            1          1%

                IPv6                       11639          2%
                IPv4 mcast                    15          1%
                IPv6 mcast                     3          1%
```

### What's Up?

There's a fundamental difference in the way MPLS assigns labels to BGP routes in different routing tables:

* MPLS labels are not assigned to BGP routes in the global routing table. When the router [copies BGP routes from RIB into FIB](/2010/09/ribs-and-fibs/), it uses the labels its downstream neighbor allocated to the BGP next hop. All BGP routes advertised by the same BGP next hop thus get the same label.
* A unique MPLS label is assigned to every VRF route when it's imported into the VPNv4 address family. In the Internet-in-the-VRF design, the Internet edge PE-routers receive Internet routing through EBGP sessions running in a VRF, and those routes automatically appear in the VPNv4 address family (and get their labels) even if they are never propagated to other PE-routers.

Net result: if you have plenty of BGP routes in the global routing table (for example, around 450.000), your router allocates a local MPLS label for each BGP next hop. If those routes move to a VRF, your router allocates a local MPLS label for each route.

### Why All the Fuss?

To make a long story short, the creators of the MPLS architecture wanted to minimize forwarding hardware requirements. Thus, they created a solution that ensures LSRs (including PE-routers) forward packets (both IPv4 and labeled packets) with a single lookup in a single table.

The proof is left as an exercise for the reader. I know a really good one, but it wouldn't fit in the sidebar of this blog post.

### Can We Fix It? Yes, We Can!

Wherever there's a challenge, there's a kludge. In this particular case, the magic command is **mpls label mode vrf Internet protocol all-afs per-vrf**. This command changes the label allocation mechanism from one-label-per-prefix to one-label-per-VRF.

With the changed label allocation model, the incoming label no longer uniquely identifies the outgoing interface and IP next hop. The egress PE-router thus has to perform two lookups: label lookup to identify the next lookup table (VRF FIB) and IPv4 destination address lookup in the VRF FIB.

The performance hit on the Cat 6500 seems to be minimal (at least [the documentation](http://www.cisco.com/en/US/docs/ios/mpls/configuration/guide/mp_vpn_per_vrf_lbl.pdf) claims so), but you lose the ability to do EIBGP multipathing (IPv4 lookup in the egress PE-router could lead to forwarding loops) and Carrier's Carrier functionality (IPv4 lookup in the egress PE-router breaks the end-to-end LSP between CE-routers) in the VRFs for which you've configured per-VRF label allocation.

{{<next-in-series page="/posts/2024/10/mpls-vpn-prefix-vrf-labels.md" />}}