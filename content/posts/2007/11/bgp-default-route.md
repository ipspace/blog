---
url: /2007/11/bgp-default-route/
title: "Use BGP Default Route to Replace Static Routing"
date: "2007-11-15T06:23:00.004+01:00"
tags: [ BGP ]
series: bgp-essentials
---
Martin Kluge sent me an interesting BGP question: he has two upstream links and runs BGP on both. Since his router is low on RAM, he cannot accept full routing, so he's just announcing his IP prefix and using static default routing toward upstream ISPs.

{{<figure src="/2007/11/bgp_1.jpg" caption="Static default routing toward upstream ISP">}}
<!--more-->
The relevant configuration on the GW router is somewhat similar to the configuration I've used as a staring point in my lab:

``` code
interface Serial1/0
 ip address 10.0.1.1 255.255.255.252
!
interface Serial1/1
 ip address 10.0.1.5 255.255.255.252
!
router bgp 65100
 neighbor 10.0.1.2 remote-as 65001
 neighbor 10.0.1.6 remote-as 65002
!
ip route 0.0.0.0 0.0.0.0 10.0.1.2
ip route 0.0.0.0 0.0.0.0 10.0.1.6 250
```

I'm sure the long-time readers of my blog immediately figured out where the catch is: if the upstream router dies, but the interface stays up, the outbound traffic is blackholed. [Reliable static routing](/2007/02/reliable-static-routing/) might be a solution, but his router is running an old IOS version. Obviously it's time for yet another rarely known BGP feature: the BGP default route.

If you've [mastered default routes in other routing protocols](/2007/06/inserting-default-route-into-ospf/), forget about what you know … BGP is different:

-   Default route already in the BGP table is advertised to BGP neighbors like any other route.
-   To announce a default route to a BGP neighbor without having a default route yourself, configure **neighbor default-originate**.
-   Once you've configured default route advertising with the **neighbor default-originate**, it's announced to the neighbor even if the router doesn't have the default route itself.
-   The default route advertised to a BGP neighbor with the **neighbor default-originate** does not pass through BGP output filters, so you cannot filter it.

For even more details, read [_Default Routes in BGP_](/kb/tag/BGP/Default_Route/).

To solve Martin's problem, you'd have to reconfigure BGP on E1 and E2 as follows (the **ip as-path** access list just ensures nothing else is sent to the customer router; obviously you could use a **route-map** instead):

``` code
router bgp 65002
 neighbor 10.0.1.5 remote-as 65100
 neighbor 10.0.1.5 default-originate
 neighbor 10.0.1.5 filter-list 1 out
!
ip as-path access-list 1 deny .*
```

Now that the default route is advertised via BGP, there is no need for a static default, and the default route will be removed (and replaced with the backup one) if the BGP neighbor disappears.

### More Details

* [Default Routes in BGP](/kb/tag/BGP/Default_Route/)
* [Responsible generation of BGP default route](/2011/09/responsible-generation-of-bgp-default/)
