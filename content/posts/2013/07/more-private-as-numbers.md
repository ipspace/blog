---
date: 2013-07-30 06:53:00+02:00
dmvpn_tag: routing
tags:
- DMVPN
- BGP
- MPLS VPN
title: More Private AS Numbers
url: /2013/07/more-private-as-numbers.html
---
Have you ever tried to implement a large-scale DMVPN or MPLS/VPN network using BGP as the routing protocol? If you tried to stitch more than \~1000 sites together you're well aware of all the pain caused by a [small range of private AS numbers defined in RFC 1930](http://tools.ietf.org/html/rfc1930). We can kludge our way around the limitation by reusing the same AS number on multiple sites (and using **allowas-in** when we need full routing information on every site), but such a design clearly sucks.
<!--more-->
RFC 6996 (published a few days ago) neatly solves the problem: it adds a new range of 32-bit private AS numbers from 4200000000 to 4294967294. I'm positive I won't be able to remember the number of zeroes in the first number, but fortunately we can still use *asdot* notation (even though it's been [discouraged by RFC 5396](http://www.ietf.org/rfc/rfc5396.txt)), where the private AS numbers go from 64086.59904 to 65535.65534. For all practical purposes, you could use 65000.1 through 65500.65500 and have enough AS numbers to address all your future DMVPN-connected sites throughout the solar system.

And finally, a few warnings:

-   Your CE-routers obviously have to support 4-byte AS numbers, which means you need reasonably new Cisco IOS (or IOS XE).
-   The BGP code dealing with private AS numbers (example: **neighbor remove-private-as** functionality) might not recognize the 32-bit private AS numbers. As always, it might be worthwhile testing stuff in a lab before a production deployment.
