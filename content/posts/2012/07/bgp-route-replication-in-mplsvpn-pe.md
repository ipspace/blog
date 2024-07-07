---
date: 2012-07-19 06:58:00+02:00
tags:
- BGP
- load balancing
- MPLS VPN
title: BGP Route Replication in MPLS/VPN PE-routers
url: /2012/07/bgp-route-replication-in-mplsvpn-pe/
---
Whenever I'm explaining MPLS/VPN technology, I recommend using the same route targets (RT) and route distinguishers (RD) in all VRFs belonging to the same simple VPN. The *Single RD per VPN* recommendation [doesn't work well for multi-homed sites](/2011/02/load-balancing-in-mplsvpn-networks-with/), so one might wonder whether it would be better to use a different RD in every VRF. The RD-per-VRF design also works, but results in significantly increased memory usage on PE-routers.
<!--more-->
### Sample Network

I'll illustrate the problem using the same network I used in [MPLS/VPN load balancing post](/2011/02/load-balancing-in-mplsvpn-networks-with/):

{{<figure src="/2012/07/s1600-MPLSVPN_MH.png" caption="Sample network">}}

Yet again, CE-A and CE-B are advertising BGP default route to PE-A and PE-B, but this time, PE-A, PE-B and PE-C use different route distinguishers in their VRF configurations:

VRF configuration on PE-A

``` {.code}
ip vrf Customer
 rd 65000:101
 route-target export 65000:101
 route-target import 65000:101
```

VRF configuration on PE-B

``` {.code}
ip vrf Customer
 rd 65000:1101
 route-target export 65000:101
 route-target import 65000:101
```

VRF and BGP configuration on PE-C

``` {.code}
ip vrf Customer
 rd 65000:102
 route-target export 65000:101
 route-target import 65000:101
!
router bgp 65000
 !
 address-family ipv4 vrf Customer
  no synchronization
  maximum-paths ibgp  4 import 4
 exit-address-family
```

### The Results

When the network reaches a stable state, PE-C should have two default routes in its BGP table, one from PE-A (with RD 65000:101) and one from PE-B (with RD 65000:1101).

{{<note info>}}We have to use different route distinguishers on PE-A and PE-B to allow the two routes to pass through the route reflector. [*Advertisement of Multiple Paths in BGP*](http://tools.ietf.org/html/draft-ietf-idr-add-paths) (BGP Add Paths) feature would solve that problem if your platform supports it for the VPNv4/VPNv6 address families.{{</note>}}

Now let's inspect the BGP table on PE-C:

{{<cc>}}VPNv4 BGP table on PE-C{{</cc>}}
``` {.code}
PE-C#show bgp vpnv4 unicast all
[...edited...]
   Network          Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 65000:101
*>i0.0.0.0          172.16.0.1               0    100      0 65100 i

Route Distinguisher: 65000:102 (default for vrf Customer)
* i0.0.0.0          172.16.0.2               0    100      0 65100 i
*>i                 172.16.0.1               0    100      0 65100 i

Route Distinguisher: 65000:1101
*>i0.0.0.0          172.16.0.2               0    100      0 65100 i
```

For whatever weird reason, the BGP table has *four* copies of the default route, not two. Let's inspect these four entries in more details:

{{<cc>}}VPNv4 BGP entries for default route on PE-C{{</cc>}}
``` {.code}
PE-C#show bgp vpnv4 unicast all 0.0.0.0                        
BGP routing table entry for 65000:101:0.0.0.0/0, version 70
Paths: (1 available, best #1, no table)
Flag: 0x820
  Not advertised to any peer
  65100
    172.16.0.1 (metric 129) from 172.16.0.5 (172.16.0.5)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      Extended Community: RT:65000:101
      Originator: 172.16.0.1, Cluster list: 172.16.0.5
      mpls labels in/out nolabel/37
BGP routing table entry for 65000:102:0.0.0.0/0, version 106
Paths: (2 available, best #2, table Customer)
Multipath: eBGP
Flag: 0x820
  Not advertised to any peer
  65100, imported path from 65000:1101:0.0.0.0/0
    172.16.0.2 (metric 129) from 172.16.0.5 (172.16.0.5)
      Origin IGP, metric 0, localpref 100, valid, internal, multipath
      Extended Community: RT:65000:101
      Originator: 172.16.0.2, Cluster list: 172.16.0.5
      mpls labels in/out nolabel/30
  65100, imported path from 65000:101:0.0.0.0/0
    172.16.0.1 (metric 129) from 172.16.0.5 (172.16.0.5)
      Origin IGP, metric 0, localpref 100, valid, internal, multipath, best
      Extended Community: RT:65000:101
      Originator: 172.16.0.1, Cluster list: 172.16.0.5
      mpls labels in/out nolabel/37
BGP routing table entry for 65000:1101:0.0.0.0/0, version 69
Paths: (1 available, best #1, no table)
Flag: 0x820
  Not advertised to any peer
  65100
    172.16.0.2 (metric 129) from 172.16.0.5 (172.16.0.5)
      Origin IGP, metric 0, localpref 100, valid, internal, best
      Extended Community: RT:65000:101
      Originator: 172.16.0.2, Cluster list: 172.16.0.5
      mpls labels in/out nolabel/30
```

On top of the two routes received from PE-A and PE-B, there are two almost identical routes with RD 65000:102 marked *imported path*. Weird, isn't it?

### What's Going On?

You probably know the basic principles of MPLS/VPN and BGP route selection ([read my MPLS/VPN books](/2007/06/using-mpls-vpn-books-to-study-for-ccip/) or watch my [Enterprise MPLS/VPN webinar](http://www.ipspace.net/Enterprise_MPLS_VPN_Deployment) if you need more details). Best MPLS/VPN routes are selected using (approximately) this algorithm:

1.  BGP routing process performs best path selection in the VPNv4 table using the [standard set of BGP path selection rules](http://www.cisco.com/en/US/tech/tk365/technologies_tech_note09186a0080094431.shtml).
2.  The IPv4 parts of the best-path VPNv4 prefixes with the route targets matching local VRFs are inserted into the VRF routing tables (where they compete with routes learned through per-VRF routing protocols based on their administrative distance);
3.  Per-VRF FIB is built from the VRF routing table (more details in [RIBs and FIBs](/2010/09/ribs-and-fibs/))

The first step in this process (BGP best path selection) cannot work correctly if the prefixes in VPNv4 table are not comparable. Remember: we have to compare the whole VPNv4 prefix as different customers might have overlapping address spaces.

The BGP process thus has to make local copies of those BGP paths that have RDs different from the local RD value to make them comparable to local BGP paths (for example, routes received from a CE-router through an EBGP session). The BGP paths received from other PE-routers are *imported* (BGP process creates a copy with the local value of the RD) and then used in the BGP best path selection process.

{{<note info>}}To be precise, step #2 in the above algorithm (copy from VPNv4 BGP table into VRF RIB) should read "... with the route targets *and route distinguishers* matching local VRFs ..."{{</note>}}

### Is This Bad?

As always, the answer is "It depends." If you have an occasional route distinguisher mismatch, you'll slightly increase your memory consumption. But if you'd go to the extreme and use a different VRF and RD for every site connected to a PE-router, the overhead of the *imported* BGP routes might become significant.

Let's continue with our example and add another VRF on PE-C with the same RT but a different RD:

{{<cc>}}Second VRF on PE-C{{</cc>}}
``` {.code}
ip vrf Site-B
 rd 65000:103
 route-target export 65000:101
 route-target import 65000:101
```

As expected, PE-C creates another copy of default routes received from PE-A and PE-B, further increasing BGP memory consumption:

{{<cc>}}Multiple copies of VPN default route on PE-C{{</cc>}}
``` {.code}
PE-C#show bgp vpnv4 unicast all
[...edited...]
   Network          Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 65000:101
*>i0.0.0.0          172.16.0.1               0    100      0 65100 i

Route Distinguisher: 65000:102 (default for vrf Customer)
* i0.0.0.0          172.16.0.2               0    100      0 65100 i
*>i                 172.16.0.1               0    100      0 65100 i

Route Distinguisher: 65000:103 (default for vrf Site-B)
* i0.0.0.0          172.16.0.2               0    100      0 65100 i
*>i                 172.16.0.1               0    100      0 65100 i

Route Distinguisher: 65000:1101
*>i0.0.0.0          172.16.0.2               0    100      0 65100 i
```

### Summary

If you offer a simple VPN service, the *use a single RD and RT value for a simple VPN* is still be best advice I can give you. If you plan to support [multipath load sharing](/2011/02/load-balancing-in-mplsvpn-networks-with/) or fast failover, the per-PE-per-VRF RD is one way to get it working, or you could use BGP Add Paths functionality if your platform supports it for VPNv4 prefixes.

{{<note info>}}*nosx* made an excellent suggestion: use RDs in the *global.ipv4.loopback.address:vpnid* format. The RDs will definitely be unique, and you might find the presence of PE router identifier (its loopback address) useful during troubleshooting.{{</note>}}

### Revision History

2012-07-24
: Updated the conclusions based on feedback from *nosx*

2023-01-18
: Point out the alternative: BGP Add Paths

### Need Help?

* The basics of MPLS/VPN technology are described in the [MPLS Essentials](https://www.ipspace.net/MPLS_Essentials) webinar (available with [free subscription](https://www.ipspace.net/Subscription/Free))
* MPLS/VPN enterprise use cases are described in the [Enterprise MPLS/VPN Deployments](http://www.ipspace.net/Enterprise_MPLS_VPN_Deployment) webinar (part of [standard subscription](http://www.ipspace.net/Subscription)).
* We discussed the impact of [using this trick with Internet in a VRF](https://my.ipspace.net/bin/get/Design/21.12.02%20-%20Internet%20in%20a%20VRF.mp4?doccode=Design) in [December 2021 Design Clinic](https://my.ipspace.net/bin/list?id=Design#2021_12).
