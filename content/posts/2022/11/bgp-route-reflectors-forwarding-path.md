---
title: "BGP Route Reflectors in the Forwarding Path"
date: 2022-11-10 07:31:00
tags: [ BGP ]
---
Bela Varkonyi left [two intriguing comments](/2022/10/bgp-route-reflector-next-hops.html#1481) on my _[Leave BGP Next Hops Unchanged on Reflected Routes](/2022/10/bgp-route-reflector-next-hops.html)_ blog post. Let's start with:

> The original RR design has a lot of limitations. For usual enterprise networks I always suggested to follow the topology with RRs (every interim node is an RR), since this would become the most robust configuration where a link failure would have the less impact.

He's talking about the extreme case of hierarchical route reflectors, a concept I first encountered when designing a large service provider network. Here's a simplified conceptual diagram (lines between boxes are physical links as well as IBGP sessions between loopback interfaces):
<!--more-->
{{<ascii>}}
┌──────┐         ┌──────┐     ┌──────┐
│      ├─────────┤      ├─────┤      │
│  C1  │         │  P1  │     │  A1  │
│      ├──┐ ┌────┤      ├─┐ ┌─┤      │
└──────┘  │ │    └──────┘ │ │ └──────┘
          │ │             │ │
          └─┼─────┐       └─┼────┐
            │     │         │    │
┌──────┐    │    ┌┴─────┐   │ ┌──┴───┐
│      ├────┘    │      ├───┘ │      │                          
│  C2  │         │  P2  │     │  A2  │
│      ├─────────┤      ├─────┤      │
└──────┘         └──────┘     └──────┘
{{</ascii>}}

* A1 and A2 are access routers
* P1 and P2 are POP aggregation routers. They are route reflectors, and A1 and A2 are their clients.
* P1 and P2 have IBGP sessions with C1 and C2, but have no idea that they are not participating in the IBGP full mesh
* C1 and C2 are route reflectors. P1 and P2 are their clients.

Taken to the extreme, every router in the network is a route reflector, and all its IBGP neighbors are its route reflector clients.

Does that work? When I asked a friend in Cisco TAC whether such a setup would work in 1990s the best answer I could get was "_looking at the code I couldn't see why it wouldn't work_." He was right, hierarchical route reflectors work surprisingly well, we used them numerous times (but without any next-hop magic), and they are pretty common in large networks.

Obviously this design only makes sense when the intermediate routers have to know the prefixes advertised by the edge routers. Using it with MPLS/VPN or EVPN is a waste of CPU cycles and memory[^LS].

[^LS]: Running BGP route reflectors for EVPN address family on spine switches is still OK -- you have to run them somewhere.

Interestingly, if your IBGP sessions follow the physical topology, then it's OK to change the BGP next hop on reflected routes[^VRFC]. Back to Bela:

[^VRFC]: That would go against the SHOULD NOT in [section 10 of RFC 4456](https://www.rfc-editor.org/rfc/rfc4456.html#section-10), but that never stopped vendors trying to win a deal or network engineers throwing kludges at a badly broken design.

> If you implement a native RR topology following the physical topology, then changing the next hop might be meaningful, since the RR is always in the user data plane path and shares the fate of user data packets. BTW, this is the original IP networking concept. The routing protocol shall follow the same path as the user data plane.

While I agree with him that [routing should rely on shared fate](/2014/08/fate-sharing-in-ip-networks.html), we usually use IGP to meet that requirement. In ye olden days we redistributed BGP into IGP, and believed a BGP prefix is reachable if IGP brought it to the other edge of the autonomous system. In the meantime, the global BGP table exploded, and the best we can do is to configure the routers to accept only loopback prefixes as the BGP next hops (as opposed to default route or aggregated prefixes). In the MPLS world, one could go a step further and consider a BGP next hop valid only when the ingress router has a valid LSP to the next hop.

An irrelevant aside: if you run IBGP sessions over the physical links, and change BGP next hops on every IBGP session, you managed to implement "_BGP as a better IGP_" design paradigm with IBGP. Congratulations, you saved an incredible amount of memory shortening the AS-path, and created a design that will keep you employed (and on pager duty) for decades.

Finally, Bela compared centralized BGP route reflectors with SDN controllers:

> Ivan loves criticizing the centralized SDN controller design. The centralized RR design has almost the same issues... :-) I know people still prefer doing that, but this was not the original intention of RR. It is a misuse of the original RR concept.

For the record: I did not criticize the idea of centralized SDN controllers, but the stupid idea of centralized control plane. It's well known[^WK] that [some problems](/2013/01/edge-and-core-openflow-and-why-mpls-is.html) (example: [optimal bandwidth reservations](/2018/02/machine-learning-and-network-traffic.html)) cannot be solved with a distributed system of autonomous agents.

[^WK]: A wonderful [handwaving](https://wiki.c2.com/?HandWaving) phrase used when you're too lazy to find supporting evidence.

As for the "original intention of route reflectors" (as I happened to be around at that time): route reflectors were designed to be a more scalable replacement for IBGP full mesh, not a mechanism to implement shared fate in IBGP. See the Introduction section of [RFC 1966](https://datatracker.ietf.org/doc/html/rfc1966) for more details. How we use them today and what we think is the right way of using them is a different story ;)
