---
date: 2012-01-17 07:03:00+01:00
dmvpn_tag: design
ospf_tag: dmvpn
tags:
- DMVPN
- OSPF
title: Redundant DMVPN designs, Part 1 (The Basics)
url: /2012/01/redundant-dmvpn-designs-part-1-basics/
---
Most of the DMVPN-related questions I get are a variant of the "*how many tunnels/hubs/interfaces/areas do I need for a redundant DMVPN design?*" As always, the right answer is "_it depends_", but here's what I've learned so far.

### Single Router/Single Uplink on Spoke Site

This blog post focuses on the simplest possible design -- each spoke site has a single router and a single uplink. There's no redundancy at the spokes, which might be an acceptable tradeoff (or you could use 3G connection as a backup for DMVPN).

You'd probably want to have two hub routers (preferably with independent uplinks), which brings us to the fundamental question: "*do we need one or two DMVPN clouds?*"
<!--more-->
### Design\#1 -- One Hub per DMVPN Tunnel

In this design, each hub router controls its own DMVPN subnet, and spoke routers have multiple tunnel interfaces (one per hub). Each hub router is the NHRP server for the subnet it controls, and propagates routing information between spokes.

{{<figure src="/2012/01/s1600-DMVPN_1S2I2H.png" caption="Two DMVPN tunnels, single hub per tunnel">}}

This design is by far the simplest, cleanest, and easiest to understand/troubleshoot -- it has no intricate dependencies between routing protocols and NHRP. You can also [easily deploy primary/backup hub router scenarios](/2011/01/sometimes-you-need-to-step-back-and/) by increasing the interface cost of one tunnel interface, or you could load-share the traffic between both hub routers.

{{<figure src="/2012/01/s1600-DMVPN_2TP1.png" caption="Load sharing across hub routers">}}

And now for the drawbacks:

-   Multiple IPsec sessions could be established between a pair of spoke routers in [DMVPN Phase 2 deployments](/2011/01/dmvpn-phase-2-fundamentals/) (one over each tunnel interface);

{{<figure src="/2012/01/s1600-DMVPN_2TP2.png" caption="You might get two IPsec sessions between a pair of spoke routers (one per tunnel)">}}

-   GRE keys are mandatory in Phase 2 deployments (otherwise the spokes cannot decipher which tunnel the other spoke router was using), causing performance degradation if the hub routers don't support GRE keys in hardware (Catalyst 6500 doesn't)
-   This design does not work with large-scale Phase 3 DMVPNs where you want each spoke to connect to a subset of hubs (you cannot establish Phase 2/3 shortcuts across DMVPN tunnels, only within a tunnel).

### Design\#2 -- Multiple Hubs in a Single DMVPN Tunnel

In this design, you connect all hub routers to the same DMVPN tunnel. All hub routers act as NHRP servers, and propagate routing information between the spokes (if you [use OSPF, one of the hub routers would become a DR, another one a BDR](/2011/01/configuring-ospf-in-phase-2-dmvpn/)).

{{<figure src="/2012/01/s1600-DMVPN_1S2H1T.png" caption="Single DMVPN tunnel, two hubs per tunnel">}}

You cannot use [Phase 1 DMVPN](/2011/01/dmvpn-phase-1-fundamentals/) with multiple hub routers -- Phase 1 DMVPN uses P2P GRE tunnels on the spoke routers with tunnel destination set to hub router's outside IP address.

[Phase 2/3 DMVPN](/2011/01/dmvpn-phase-2-fundamentals/) designs with multiple hub routers per tunnel could experience severe convergence issues -- [detecting failure of a hub router could take as long as three minutes](/2011/05/nhrp-convergence-issues-in-multi-hub/). On the *benefits* side, this design does not require GRE keys (which is good news if your hub router is a Catalyst 6500) or multiple IPsec sessions between spoke routers.

{{<figure src="/2012/01/s1600-DMVPN_1TP2.png" caption="Spoke-to-spoke session established across a Phase2/3 DMVPN tunnel">}}

### Summary

-   One hub router per DMVPN subnet is the ideal design for Phase 2 DMVPN deployments \... unless you have Catalyst 6500 as your hub router, in which case you must use one DMVPN subnet due to lack of hardware GRE key support. That's also the only design you can use with Phase 1 DMVPN.
-   One DMVPN subnet is probably the best design for Phase 3 DMVPN and it's mandatory if you have partial spoke-to-hub NHRP connectivity.

Coming next: [spoke routers with multiple uplinks and spoke sites with redundant routers](redundant-dmvpn-designs-part-2-multiple/).
