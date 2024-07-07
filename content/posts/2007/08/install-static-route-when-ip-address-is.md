---
date: 2007-08-23 08:07:00+02:00
tags:
- IP routing
- SLA
title: Install a Static Route When an IP Address Is NOT Reachable
url: /2007/08/install-static-route-when-ip-address-is/
---
One of my readers recently asked an interesting question: "*How do you install a static route when an IP address is not reachable?*"

Without going into the design reasons that prompted the question, you can actually track when IP SLA measurement fails with an obscure configuration syntax of the **track** objects that tracks when another *track* object fails.
<!--more-->
In my example, the route to 1.0.0.0/8 would be inserted in the IP routing table when the ping to 172.16.0.22 fails:

``` {.code}
!
! Define and start the IP SLA probe
!
ip sla 53
 icmp-echo 172.16.0.22
 timeout 500
 frequency 3
ip sla schedule 53 life forever start-time now
!
! Define an object that tracks the SLA probe
!
track 13 rtr 53 reachability
!
! Define another object that is the negation of the previous object
!
track 14 list boolean and
 object 13 not
!
! Insert a static route if the second object is UP (thus the 
! IP SLA probe failed)
!
ip route 1.0.0.0 255.0.0.0 Null0 track 14
```
