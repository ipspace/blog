---
date: 2008-01-30 07:22:00+01:00
tags:
- BGP
- IP routing
title: Redistributing Customer Routes into BGP
url: /2008/01/redistributing-customer-routes-into-bgp/
---
I\'m often [promoting the idea of separating customer routing from core routing](http://searchtelecom.techtarget.com/tip/0,289483,sid103_gci1289458,00.html) in the design articles I write. The only viable solution (unless you want to implement MPLS VPN and migrate customer routing into VPNv4) is to carry customer routes in BGP, redistributing them into BGP from other routing sources. On the other hand, I'm telling you that [you should advertise only static IP prefixes into the public Internet](/2008/01/bgp-essentials-advertising-public-ip/). Obviously there's a seeming disconnect between the two advices.

However, the dilemma is easily solved with the **no-export** BGP community that prevents an IP prefix from being advertised over EBGP sessions. Whenever you redistribute customer routes into BGP, you should attach the **no-export** community to them, ensuring that only the statically advertised IP prefixes will be propagated outside of your AS boundaries.
<!--more-->
**Important:** for this design to work, you have to configure BGP community propagation with the **neighbor send-community** router configuration command on all IBGP sessions in your network, [preferably with a peer template](/2008/01/bgp-essentials-peer-session-templates/). Otherwise, the BGP communities will be lost on IBGP updates and the IP prefixes will leak to your EBGP neighbors.

For example, if you use static routing with your customers and want to redistribute the static routes into BGP, use the following configuration (I've used **tag 123** to tag static routes that should get inserted into BGP).

``` {.code}
router bgp 65001
 redistribute static route-map StaticToBGP
!
route-map StaticToBGP permit 10
 match tag 123
 set community no-export additive
```

When you configure a static route toward the IP subnet 10.1.2.0/24 ...

``` {.code}
ip route 10.1.2.0 255.255.255.0 Null0 tag 123
```

... it's automatically inserted in the BGP table and marked with the **no-export** community.