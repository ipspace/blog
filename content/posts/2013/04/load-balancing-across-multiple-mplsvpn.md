---
date: 2013-04-11 07:17:00+02:00
tags:
- BGP
- load balancing
- MPLS VPN
title: Load Balancing Across Multiple MPLS/VPN Providers
url: /2013/04/load-balancing-across-multiple-mplsvpn/
---
Arnold sent me an interesting challenge: he's using two MPLS/VPN providers, with most sites being connected to both providers. He'd like to load balance the inter-site traffic across all PE-CE links -- an easy task if you're using RIP, OSPF or EIGRP as the PE-CE routing protocol, but he happens to be using BGP.
<!--more-->
{{<figure src="/2013/04/s1600-BGP+Multipath+Relax.JPG" caption="The network diagram Arnold sent me">}}

Cisco IOS implementation of BGP supports load balancing, both across multiple EBGP or IBGP paths (and even a combination of VPNv4 IBGP path and VRF EBGP paths), but it's pretty picky -- the BGP paths have to be almost identical, including the contents of the AS path list. BGP will not use alternate paths if they're not passing through the same autonomous systems.

The default behavior usually makes sense. AS path length is a very coarse indicator of distance and often doesn't relate well to expected performance.

You can use the (still undocumented) **bgp bestpath as-path multipath-relax** router configuration command to relax the path selection rules. After entering this command, the router compares the AS path lengths (they still have to be the same), not the actual content of the AS path attribute.

### Caveats

-   Make sure the uplinks have equal bandwidth and the upstream networks have comparable performance characteristics. Equal-cost load balancing across two unequal links or networks results in twice the performance of the worst-performing component.
-   BGP routing process will consider only almost identical paths (same AS path length, local preference, origin code, MED, IGP metric).
-   You cannot load-balance between an IBGP and an EBGP path (you might get forwarding loops). In the above diagram you cannot load balance between the edge routers in the regional office; IBGP-based load balancing has to be configured on core switches.
-   You won't see the effects of the **bgp bestpath as-path multipath-relax** command in the BGP table. BGP still selects one best path, but is willing to copy more than one path into the IP routing table (where you should see multiple entries for the same prefix).
-   A BGP route reflector will not advertise more than one best path to its clients (unless you use [BGP Add Paths functionality](http://tools.ietf.org/html/draft-ietf-idr-add-paths) available in [IOS XE 3.7S and IOS 15.3(1)T](http://www.cisco.com/en/US/docs/ios-xml/ios/iproute_bgp/configuration/xe-3s/irg-additional-paths.html)).
