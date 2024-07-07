---
cdate: 2023-03-10
comment: |
  While Cisco uses LISP in their SDA products, LISP never became more than solution-in-search-of-a-problem when it comes to global IPv6 connectivity. Also, global (DFZ) IPv6 routing table is still a fraction of the global IPv4 routing table a decade after this blog post has been written. 
date: 2012-03-01 11:57:00+01:00
multihoming_tag: ipv6
series:
- multihoming
- LISP
tags:
- IPv6
title: Anyone Can Get IPv6 PI Space – Buy More RAM and TCAM?
url: /2012/03/anyone-can-get-ipv6-pi-space-buy-more/
---
Till a few weeks ago, you could get provider-independent (PI) IPv6 address space in RIPE region only if you "demonstrated that you'll be multihomed", which usually required having nothing more than an AS number. With the recent policy change, [anyone can get PI address space](http://www.ripe.net/ripe/policies/proposals/2011-02) (and this is [why you should get it](http://etherealmind.com/importance-provider-independent-ipv6-addresses/)) as long as they [have a sponsoring LIR](http://www.ripe.net/ripe/docs/ripe-452), and the [yearly fee for an independent resource (RIPE-to-LIR) is €50](http://www.ripe.net/ripe/docs/ripe-499).
<!--more-->
Having PI address space is definitely a good idea if you're an enterprise customer, but you do realize that someone will have to keep track of those prefixes, right? Unless LISP really takes off and everyone implements it, that "someone" would be most core routers (unless you go for [BGP-free MPLS core](/2012/01/bgp-free-service-provider-core-in/), in which case only the edge routers will have to hold all prefixes).

Reasonably high-end routers have around 1M TCAM/FIB-based IPv6 routes. How long do you think that will last once enterprises realize IPv4 addresses are truly gone and start jumping on the IPv6 bandwagon? Yeah, we really wrecked the opportunity to design a proper protocol with 15 years of ignorance and neglect.

{{<figure src="/2012/03/s1600-DoubleFacepalm.jpg" caption="When will they realize [you need a session layer](/2009/08/what-went-wrong-tcpip-lacks-session/)?">}}
