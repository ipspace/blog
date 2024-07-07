---
date: 2014-04-10 06:46:00+02:00
dmvpn_tag: routing
tags:
- DMVPN
- BGP
title: Changes in IBGP Next Hop Processing Drastically Improve BGP-based DMVPN Designs
url: /2014/04/changes-in-ibgp-next-hop-processing/
---
I always [recommended EBGP-based designs for DMVPN networks](/2014/03/scaling-bgp-based-dmvpn-networks/) due to the significant complexity of running IBGP without an underlying IGP. The **neighbor next-hop-self all** feature introduced in recent Cisco IOS releases has totally changed my perspective -- it makes IBGP-over-DMVPN the best design option unless you want to [use DMVPN network as a backup for MPLS/VPN network](http://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN).
<!--more-->
### What Was the Problem?

Imagine a simple DMVPN network with a hub router and two spoke routers. The hub router is further connected to WAN core, and all routers run IBGP (with DMVPN hub router being BGP route reflector for DMVPN spokes).

{{<ascii>}}
RA--+
    !
    +--hub—core
    !
RB--+
{{</ascii>}}

Let's assume the core router advertises BGP prefix 192.168.10.0/24 with BGP next hop 10.0.2.2.

``` code
Hub#show ip bgp 192.168.10.0
BGP routing table entry for 192.168.10.0/24, version 7
Paths: (1 available, best #1, table default)
  Advertised to update-groups:
     1         
  Refresh Epoch 1
  Local
    10.0.2.2 from 10.0.2.2 (10.11.12.6)
      Origin IGP, metric 0, localpref 100, valid, internal, best
```

When that update gets propagated to DMVPN spoke routers, they ignore the BGP prefix, as they cannot reach the BGP next hop (there's no IGP on the DMVPN subnet):

``` code
RA#show ip bgp 192.168.10.0
BGP routing table entry for 192.168.10.0/24, version 12
Paths: (1 available, no best path)
  Not advertised to any peer
  Refresh Epoch 1
  Local
    10.0.2.2 (inaccessible) from 10.0.0.3 (192.168.3.1)
      Origin IGP, metric 0, localpref 100, valid, internal
      Originator: 10.11.12.6, Cluster list: 192.168.3.1
```

We can fix that problem in a number of ways:

-   Run EBGP across DMVPN subnet, potentially reusing the same AS number across multiple sites (the solution I usually proposed so far);
-   Advertise BGP next hops in BGP. A bit messy, but it works in recent IOS releases;
-   Change the BGP next hop in inbound updates on spoke routers;
-   Change the BGP next hop on the hub router.

Let evaluate the last three options:

### Advertising IBGP Next Hops in IBGP

Each IBGP router in our autonomous system could advertise all its connected interfaces (effectively turning IBGP into a path vector IGP). Once the IBGP next hops appear in BGP table, the DMVPN spoke routers start using the IBGP prefixes advertised by routers beyond the DMVPN hub:

``` code
RA#show ip bgp
BGP table version is 14, local router ID is 192.168.1.1
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal, 
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter, 
              x best-external, a additional-path, c RIB-compressed, 
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>i 10.0.2.0/24      10.0.0.3                 0    100      0 i
 *>  192.168.1.0      0.0.0.0                  0         32768 i
 *>i 192.168.2.0      10.0.0.2                 0    100      0 i
 *>i 192.168.3.0      10.0.0.3                 0    100      0 i
 *>i 192.168.10.0     10.0.2.2                 0    100      0 i
RA#show ip bgp 192.168.10.0
BGP routing table entry for 192.168.10.0/24, version 14
Paths: (1 available, best #1, table default)
  Not advertised to any peer
  Refresh Epoch 1
  Local
    10.0.2.2 from 10.0.0.3 (192.168.3.1)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      Originator: 10.11.12.6, Cluster list: 192.168.3.1
```

There are at least two problems with this approach:

-   I remember having problems with IBGP routes using IBGP next hops (some versions of Cisco IOS refused to use them); either my memory is failing me or the behavior might have changed recently.
-   BGP doesn't change next hop on IBGP updates, resulting in ever-deeper next hop recursion (the proof is left as an exercise for the reader), which may eventually break the next hop evaluation process.

**Summary:** don't even try.

### Changing BGP Next Hop on Spoke Routers

You could use inbound route map on spoke routers to change BGP next hop of all received BGP prefixes to the IP address of the hub router. The **set ip next-hop peer-address** command makes this approach even more viable, as you don't have to specify the hub router's IP address in the route map.

You have to use slightly more complex route map in Phase 2 DMVPN networks -- the BGP next hop has to be changed only if it doesn't belong to the DMVPN subnet.

While this solution works, it requires additional configuration on all spoke routers. Not a problem unless you have thousands of spokes (and haven't heard of configuration automation yet).

**Summary:** use as a solution-of-last-resort.

### Changing BGP Next Hop on the Hub Router

Ideally, the hub router would set the BGP next hop to its own IP address on all outbound updates sent to DMVPN spokes. Unfortunately a [BGP route reflector doesn't change the attributes of reflected routes](/2011/08/bgp-next-hop-processing/), even when configured to do so with a route map or **neighbor next-hop-self**.

Recent IOS releases got a tweak on the **neighbor next-hop-self** command -- the **all** option changes BGP next hop on all routes, including reflected routes. Problem solved.

**Summary**: recommended solution if your hub router supports this feature.
