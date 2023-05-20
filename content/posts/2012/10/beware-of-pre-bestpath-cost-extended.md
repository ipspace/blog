---
date: 2012-10-24 06:51:00+02:00
eigrp_tag: details
pre_scroll: true
tags:
- EIGRP
- BGP
- MPLS VPN
title: Beware of the Pre-Bestpath Cost Extended BGP Community
url: /2012/10/beware-of-pre-bestpath-cost-extended.html
---
One of my readers sent me an interesting problem a few days ago: the BGP process running on a PE-router in his MPLS/VPN network preferred an iBGP route received from another PE-router to a locally sourced (but otherwise identical) route. When I looked at the detailed printout, I spotted something "interesting" -- the *pre-bestpath cost* extended BGP community.
<!--more-->
``` code
PE2#sh ip bgp vpnv4 vrf XXX 0.0.0.0 
BGP routing table entry for 172.16.1.105:0:0.0.0.0/0, version 159367 

Paths: (2 available, best #1, table XXX) 
   Local, imported path from 100:0:0.0.0.0/0 
     172.16.1.104 (metric 11) from 172.16.1.104 (172.16.1.104) 
       Origin incomplete, metric 0, localpref 100, valid, internal, best 
       Extended Community: RT:100:0 Cost:pre-bestpath:129:25600 0x8800:0:0 
         0x8801:100:0 0x8802:65280:25600 0x8803:65281:1500 
         0x8804:1936:184188929 0x8805:9:0 0x8806:0:184188929
       mpls labels in/out nolabel/372
   Local 
     10.251.0.130 from 0.0.0.0 (172.16.1.105) 
       Origin incomplete, metric 0, localpref 100, weight 32768, valid, sourced 
       Extended Community: RT:100:0 
```

The [BGP cost community](http://tools.ietf.org/html/draft-retana-bgp-custom-decision-02) modifies the [BGP path selection process](http://21500.net/?p=336): if the cost community has ABSOLUTE_VALUE (displayed as pre-bestpath) point-of-insertion, it's considered before the "standard" BGP path selection attributes (yes, it's stronger than *weight*).

BGP paths without the *cost* community are assumed to have a pretty high cost value (2147483647, as [explained by Cisco's documentation](http://www.cisco.com/en/US/docs/ios/12_0s/feature/guide/s_bgpcc.html)), causing the iBGP route to be better than the local route (which had no cost community).

The *cost* extended BGP community is usually seen in [networks running EIGRP between PE-and CE-routers](https://blog.ipspace.net/2008/07/multihomed-eigrp-sites-in-mpls-vpn.html) that try to cope with multihomed customer sites. Although you could change it manually with the **set extcommunity cost** command in numerous places where a route-map can be used, it should not appear in my reader's network -- his default route was a simple static route redistributed into BGP without a route-map.

It turned out he stumbled upon a bug; he was using EIGRP in the same VRF, and removing and re-enabling EIGRP-to-BGP redistribution in the VRF address family removed the stray *cost* community from the default route. Obviously that fix isn't always applicable -- you can't simply bounce EIGRP redistribution every time a BGP prefix gets a weird set of communities -- but fortunately you can ignore the *cost* community with the **bgp bestpath cost-community ignore** router configuration command.
