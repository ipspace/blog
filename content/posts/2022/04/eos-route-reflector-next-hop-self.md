---
title: "Next Hops of BGP Routes Reflected by Arista EOS"
date: 2022-04-07 06:09:00
tags: [ BGP ]
pre_scroll: True
---
Imagine a suboptimal design in which: 

* A BGP route reflector also servers as an AS edge (PE) router[^SD];
* You want to use **next-hop-self** on AS edge routers.

Being exposed to Cisco IOS for decades, I considered that to be a no-brainer. After all, [section 10 of RFC 4456](https://datatracker.ietf.org/doc/html/rfc4456#section-10) is pretty specific:

> In addition, when a RR reflects a route, it SHOULD NOT modify the following path attributes: NEXT_HOP, AS_PATH, LOCAL_PREF, and MED.

Arista EOS is different -- a route reflector happily modifies NEXT_HOP on reflected routes (but then, did you notice the "[SHOULD NOT](https://www.ietf.org/rfc/rfc2119.txt)" wording?[^RSN])
<!--more-->
[^SD]: Because you ran out of budget, or because you forgot you needed a route reflector in your BGP network, and then randomly chose one of the routers to do that.

[^RSN]: Maybe that should be upgraded to [REALLY SHOULD NOT](https://datatracker.ietf.org/doc/html/rfc6919#section-3)?

{{<note info>}}Arista EOS has two sets of routing daemons configured as *ribd* or *multi-agent* model. This blog post is describing the behavior of *multi-agent* model.{{</note>}}

The behavior is easy to reproduce in a 4-router lab with the following BGP topology:

{{<figure src="/2022/04/BGP-RR-next-hop-self-topology.png">}}

I configured BGP on RR the way I would have done it on Cisco IOS:

{{<cc>}}BGP configuration on route reflector{{</cc>}}
```
router bgp 65000
   router-id 10.0.0.1
   bgp cluster-id 10.0.0.1
   bgp advertise-inactive
   neighbor 10.0.0.2 remote-as 65000
   neighbor 10.0.0.2 next-hop-self
   neighbor 10.0.0.2 update-source Loopback0
   neighbor 10.0.0.2 description e1
   neighbor 10.0.0.2 route-reflector-client
   neighbor 10.0.0.2 send-community standard extended
   neighbor 10.0.0.3 remote-as 65000
   neighbor 10.0.0.3 next-hop-self
   neighbor 10.0.0.3 update-source Loopback0
   neighbor 10.0.0.3 description e2
   neighbor 10.0.0.3 route-reflector-client
   neighbor 10.0.0.3 send-community standard extended
   neighbor 10.1.0.10 remote-as 65100
   neighbor 10.1.0.10 description x1
   neighbor 10.1.0.10 send-community standard
   !
   address-family ipv4
      neighbor 10.0.0.2 activate
      neighbor 10.0.0.3 activate
      neighbor 10.1.0.10 activate
```

The only difference I noticed when comparing Arista EOS configuration with Cisco IOS one was the need to specify **route-reflector-client** and **next-hop-self** per-neighbor and not within an address family. That might be a good choice: it makes little sense to have some neighbors as RR clients in one address family but not in another one, and having attributes specified per neighbor not per-AF-per-neighbor ensures you're not making stupid mistakes.

The BGP table on E1 was a shocker: prefix 10.0.0.3/32 (reflected route from E2) has RR as the next hop. The *originator-id* is set to 10.0.0.3, proving the route was originated by E2, but the *next-hop* is set to *cluster-id* (10.0.0.1), proving the next hop was changed by RR when reflecting the route.

{{<cc>}}BGP table on E1{{</cc>}}
```
e1#sh ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            10.0.0.1              0       -          100     0       i
 * >      10.0.0.2/32            -                     -       -          -       0       i
 * >      10.0.0.3/32            10.0.0.1              0       -          100     0       i Or-ID: 10.0.0.3 C-LST: 10.0.0.1
 * >      10.0.0.4/32            10.0.0.1              0       -          100     0       65100 i
```

I almost made a perfect mess creating a route map to change next hops on external BGP routes (but not on internal ones) when I noticed the nerd knob I needed to get Arista EOS behavior more in line with the recommendation of RFC 4456: **‌bgp route-reflector preserve-attributes**. All of a sudden, the BGP table changed to what I expected to see:

{{<cc>}}BGP table on E1 after RR reconfiguration{{</cc>}}
```
e1#sh ip bgp | begin Network
          Network                Next Hop              Metric  AIGP       LocPref Weight  Path
 * >      10.0.0.1/32            10.0.0.1              0       -          100     0       i
 * >      10.0.0.2/32            -                     -       -          -       0       i
 * >      10.0.0.3/32            10.0.0.3              0       -          100     0       i Or-ID: 10.0.0.3 C-LST: 10.0.0.1
 * >      10.0.0.4/32            10.0.0.1              0       -          100     0       65100 i
```

### Reproducibility Is the Key

You'll find the [lab topology and configuration files on GitHub](https://github.com/ipspace/netlab-examples/tree/master/BGP/RR-next-hop-self). The *tar* archives contain device configurations  ([initial](https://github.com/ipspace/netlab-examples/raw/master/BGP/RR-next-hop-self/eos-rr-next-hop-self.tar.gz) and [fixed](https://github.com/ipspace/netlab-examples/raw/master/BGP/RR-next-hop-self/eos-rr-next-hop-self-fixed.tar.gz)) and *containerlab* configuration needed to set up the lab[^SAS]. 

[^SAS]: Some Assembly Required: you'll have to install Docker, *containerlab* and Arista EOS container on a Linux host.

Alternatively, you can use *[netlab](https://netlab.tools/)* to set up the lab:

* [Install *netlab*](https://netlab.tools/install/) and your preferred lab environment
* Copy *topology.yml* file into an empty directory
* Execute **netlab up**

You can [specify virtualization provider or default device type](https://netlab.tools/netlab/up/) with **netlab up**, making it easy to test the route reflector behavior on a [dozen devices supported by *netlab*](https://netlab.tools/platforms/#supported-configuration-modules).