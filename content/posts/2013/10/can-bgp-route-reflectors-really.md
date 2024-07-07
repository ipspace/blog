---
date: 2013-10-08 07:48:00+02:00
tags:
- MPLS
- BGP
- IP routing
title: Can BGP Route Reflectors Really Generate Forwarding Loops?
url: /2013/10/can-bgp-route-reflectors-really/
---
TL&DR Summary: Yes (if you're clumsy enough).

A while ago I read [*Impact of Graceful IGP Operations on BGP*](http://inl.info.ucl.ac.be/system/files/igpmig_bgp_tr.pdf) -- an article that described how changes in IGP topology result in temporary (or sometimes even permanent) forwarding loops in networks using BGP route reflectors.

Is the problem real? Yes, it is. Could you generate a BGP RR topology that results in a permanent forwarding loop? Yes. It's not that hard.
<!--more-->
### I Think I Broke It

Here's a particularly broken topology (connections with arrows are BGP sessions, R1 and R2 are route reflectors, all other routers are their clients).

{{<figure src="/2013/10/s500-BGP_RR_Broken.png">}}

Assuming E1 and E2 advertise an identical external prefix (*IP-External*) over their IBGP sessions, this topology results in a permanent forwarding loop. Can you figure out why that's the case?

{{<note warn>}}
Although the above topology looks utterly silly, you might get dangerously close to it in a well-designed network after one or more IBGP session failures.
{{</note>}}

### Route Reflector Is Just a Router

A BGP route reflector is nothing more than a regular BGP router with [a few route propagation rules bolted onto the update generation code](/2008/08/bgp-route-reflector-details/). It still follows all the rules of BGP route processing:

-   Receive routes from BGP peers;
-   Install all (accepted) routes into BGP RIB;
-   For every IP prefix, select the best route from all RIB routes describing that prefix;
-   Advertise the best routes to BGP peers (and here's where a route reflector deviates from standard BGP behavior -- it [advertises best routes to its clients](/2009/04/bgp-route-reflector-update-groups/) regardless of how it got them).

### BGP Route Selection Rules Reexamined

Route reflectors in our diagram (R1 and R2) receive BGP routes for the *IP-External* prefix from E1 and E2. Assuming the updates are identical, R1 and [R2 select their best BGP route based on lowest IGP cost](http://www.cisco.com/en/US/tech/tk365/technologies_tech_note09186a0080094431.shtml) -- R1 will select the route advertised by E1; R2 will select the route advertised by E2.

### BGP Route Reflectors and Forwarding Topology

Next step in our forwarding loop creation: R1 advertises the best route to *IP-External* with E1 as the BGP next hop to all its clients (E1, E2 and C2). E1 and E2 ignore the update (they both have a better route), C2 uses it.

Similarly, R2 advertises its best route to *IP-External* with E2 as BGP next hop to E1, E2 and C1. C1 uses the advertised route.

Based on its BGP table (copied into IP routing table and FIB) C1 sends the traffic for *IP-External* toward BGP next hop E2. [Recursive next hop resolution](/2010/09/ribs-and-fibs/) results in C2 being the true next hop. Likewise, C2 sends the traffic for *IP-External* to C1. Bingo! A permanent forwarding loop.

Can you prevent the forwarding loop? You can avoid most of them with a good design -- make sure your BGP sessions don't deviate too much from the forwarding topology. Ideally, all BGP route reflectors in a cluster would have equal IGP cost to all BGP next hops.

Alternatively, if you're OK with a slightly slower convergence, you could establish IBGP sessions across physical links (so they're guaranteed to follow the forwarding topology) and turn every single router into a BGP route reflector \... effectively turning BGP into RIP.

### MPLS is the answer. What was the question?

OK, good design clearly helps. But can you **prevent** the forwarding loops? Sure -- MPLS is always the right answer (these days it might be LISP, but I'm digressing).

If you deploy LDP-based MPLS forwarding in your BGP network, the packets toward the BGP next hops always carry an LDP-generated label for the BGP next hop (not the external prefix) and thus get across your autonomous system without a single additional L3 lookup. Even if the forwarding tables derived from BGP information don't make much sense, the packets still get to some egress router (although they might take a suboptimal path).

{{<note info>}}You don't need to deploy a [BGP-free core](/2012/01/bgp-free-service-provider-core-in/) to make MPLS work. MPLS-based forwarding gets rid of forwarding loops even in traditional networks with BGP running on every router.{{</note>}}