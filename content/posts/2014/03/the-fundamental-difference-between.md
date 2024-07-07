---
date: 2014-03-11 07:43:00+01:00
dmvpn_tag: basics
series_weight: 200
tags:
- DMVPN
title: The Fundamental Difference between Phase 2 and Phase 3 DMVPN
url: /2014/03/the-fundamental-difference-between/
---
DMVPN networks still confuse some engineers, particularly the true differences between Phase 2 and Phase 3 DMVPN. Here's the explanation that worked for an engineer that sent me a question along these lines.
<!--more-->
[**Phase 2 DMVPN**](/2011/01/dmvpn-phase-2-fundamentals/) **forwarding** relies exclusively on IP routing table (RIB). Whatever IP next hop is in the routing table (as computed by the routing protocol) is [copied into forwarding table (FIB)](/2010/09/ribs-and-fibs/) and used for packet forwarding.

In **Phase 3 DMVPN**, there\'s the NHRP redirect cache below the forwarding table. FIB entries are copied from the routing table, but the next hop in the FIB table doesn't necessarily reflect the actual next hop (which might be overridden by a dynamic NHRP entry). This functionality allows direct spoke-to-spoke traffic even if the only route spokes have is a default route toward the hub router.

In both cases, the next hop router that appears in the FIB table or NHRP cache isn't used unless there's an already-established IPsec session with that router. Otherwise, the packet is sent [toward the *best* hub router](/2013/04/the-impact-of-changed-nhrp-behavior-in/) (for whatever value of *best*).

For more details, check the [ipSpace.net DMVPN webinars](http://www.ipspace.net/DMVPN_trilogy).
