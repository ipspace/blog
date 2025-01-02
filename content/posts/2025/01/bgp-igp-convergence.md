---
title: "Comparing IGP and BGP Data Center Convergence"
date: 2025-01-15 07:01:00+0100
tags: [ design, data center ]
---
A Thought Leader[^TL] recently published a LinkedIn article comparing IGP and BGP convergence in data center fabrics[^DH]. In it, they[^TH] claimed that:

> iBGP designs would require route reflectors and additional processing, which could result in slightly slower convergence.

Let's see whether that claim makes any sense.

**TL&DR**: No. If you're building a simple leaf-and-spine fabric, the choice of the routing protocol does not matter (but you already knew that if you read this blog).
<!--more-->
[^TL]: Who else would publish an introductory article on LinkedIn?

[^DH]: We've inspected the corpse of that horse way too many times, but some people still keep beating it. Anyway, I'm digressing.

[^TH]: Making this gender-neutral to protect the "innocent". After all, one cannot be blamed for regurgitating marketing fantasies, right?

As I discussed in the [Fast Failover](https://blog.ipspace.net/series/fast-failover/) series, the overall convergence time has these components:

1. A failure has to be detected.
2. The node detecting the failure has to report a change in network topology.
3. The change must be propagated across the network
4. Other nodes must recompute the best paths based on the new network topology
5. The new best paths must be installed in the forwarding tables.

In a fine-tuned network, steps #1 and #5 could take longer than steps #2..#4, making our discussion as relevant as the famous [angels-on-pinhead](https://en.wikipedia.org/wiki/How_many_angels_can_dance_on_the_head_of_a_pin%3F) one. Out of the box, most routing protocol implementations suck because they're still using defaults from the 1980s[^UI].

[^UI]: Using the default settings, IBGP might work better than EBGP because the IBGP *update interval* is usually set to zero, whereas the EBGP value is often non-zero.

Finally, we must differentiate between *endpoint topology changes* (carried in IBGP and EBGP) and *core topology changes* (carried in IGP or EBGP). As IBGP is not involved in the core topology changes, the impact of route reflectors is *zero*, and the potential differences in the core network convergence depend solely on how fine-tuned your IGP or EBGP timers are.

BGP deals with the *endpoint topology changes* in the same way regardless of whether you use IBGP route reflectors or EBGP-only design:

* An edge node detects a topology change and sends a BGP UPDATE message describing it.
* A spine switch or a route reflector (intermediate node) receives the BGP UPDATE message and modifies its BGP table accordingly.
* The intermediate node selects the new best BGP path and reports the change in another BGP update to its neighbors. The BGP update is usually sent immediately over IBGP sessions and might be delayed on EBGP sessions due to the default value of the *update interval*[^UI2].
* The process continues until the change notification reaches all the edge nodes.

[^UI2]: Network operating systems designed for data center BGP environments often set the EBGP update interval to zero. More generic implementations might use non-zero values.

Interestingly, in a multi-stage leaf-and-spine fabric[^BF], an EBGP-only implementation might be *slower* (not faster) than an IBGP implementation with centralized route reflectors due to the multihop update propagation process.

[^BF]: If you do build multi-stage fabrics, I sincerely hope you're not taking design advice from random bloggers and thought leaders.
