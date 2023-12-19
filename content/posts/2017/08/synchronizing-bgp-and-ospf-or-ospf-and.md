---
date: 2017-08-29 09:01:00+02:00
ospf_tag: mp
tags:
- MPLS
- OSPF
- BGP
- IP routing
- segment routing
title: Synchronizing BGP and OSPF (or OSPF and LDP)
url: /2017/08/synchronizing-bgp-and-ospf-or-ospf-and.html
---
Rich sent me a question about temporary traffic blackholing in networks where every router is running IGP (OSPF or IS-IS) and iBGP.

He started with a very simple network diagram:
<!--more-->
{{<ascii>}}
            +------+    +------+
    +-------+  C1  +----+  C2  +-------+
    |       +------+    +------+       |
+------+                            +------+
|  E1  |                            |  E2  |
+------+                            +------+
    |       +------+    +------+       |
    +-------+  C3  +----+  C4  +-------+
            +------+    +------+
{{</ascii>}}

The routers are configured as follows:

-   The network does not have a default route;
-   All routers run OSPF and iBGP;
-   iBGP sessions are established between loopback interfaces;
-   E1 and E2 insert external prefixes into iBGP;
-   BGP next hop is not changed across the autonomous system;
-   There's a full mesh of iBGP sessions between the routers, or a route reflector somewhere -- doesn't really matter;

Now imagine C1 crashes. No problem. IGP detects the topology change and changes the IP routing tables accordingly. The BGP next hop is unchanged, so there's no need for BGP convergence. Life is good.

A few minutes later, C1 recovers. IGP establishes adjacencies between C1 and its neighbors. BGP sessions are established only after IGP already changed the routing tables (C1's loopback was not reachable prior to that), and it takes a while for C1 to populate its BGP table and copy its contents into its routing table.

In the meantime, E1 sees two equal-cost paths toward E2. It starts sending traffic toward external destinations to C1, which immediately drops it, resulting in a temporary traffic black hole until C1 receives all the BGP updates and installs BGP prefixes into its IP routing and forwarding tables.

You'll experience the same problem any time you're trying to use functionality (IP forwarding) that relies on information supplied by two independent eventually-consistent systems (OSPF and BGP). [MPLS forwarding using LDP exhibits very similar behavior](https://blog.ipspace.net/2011/11/ldp-igp-synchronization-in-mpls.html); see also [this blog post](http://blog.ipspace.net/2008/02/use-slow-igp-startup-in-ldp-only-mpls.html).

Rich's question: how can I fix that?

As always, it depends. The "canonical" answer (probably expected in the CCIE lab) is **max-metric router-lsa on-startup wait-for-bgp** OSPF router configuration command (there's a similar command for IS-IS).

The **max-metric router-lsa** command makes a router advertise its Type-1 (router) LSA with maximum metric allowed by OSPF, making paths through it less preferred than anything else. The **on-startup** option tells the router to do that *after reload* (instead of immediately) and the next parameter tells the router how long it should advertise the maximum metric -- you can specify it in seconds or tell the OSPF routing process to wait for BGP to converge (or at most 10 minutes).

The interesting question at this point should be: *how does the router know when the BGP routing process has converged?* The Cisco IOS XE documentation is totally mum on the topic, but I remember seeing something along the lines of *we assume BGP has converged when we receive a BGP keepalive message from all peers (which means they have nothing more to tell us*). Modern implementations most likely use the BGP End-of-RIB marker introduced with the [Graceful Restart](https://blog.ipspace.net/2021/09/graceful-restart.html) functionality.

And now for the fun alternatives:

-   Turn the BGP+OSPF synchronization challenge into a LDP+OSPF synchronization challenge by deploying MPLS forwarding in BGP-free core. See also RFC 1925 rule 6.
-   Build a BGP-only network. Not necessarily a good idea if you care about convergence times and your network is not highly symmetrical. The proof is left as an exercise for the reader.
-   Use BGP-free core with MPLS forwarding based on segment routing instead of LDP.
