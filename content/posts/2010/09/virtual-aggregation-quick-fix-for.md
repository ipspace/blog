---
date: 2010-09-03 06:53:00.001000+02:00
tags:
- switching
- IP routing
title: 'Virtual Aggregation: A Quick Fix for FIB/TCAM Overflow'
url: /2010/09/virtual-aggregation-quick-fix-for/
series: vagg
vagg_tag: vagg
---
**Quick summary for the [differently-attentive](/2010/03/qppb-in-mpls-vpn/#comments)**: virtual aggregation solves TCAM overflow problems ([high-level description of how it works](http://searchtelecom.techtarget.com/tip/0,289483,sid103_gci1517081,00.html)).

During the [Big Hot and Heavy Switches podcast](http://packetpushers.net/show-16-big-hot-heavy-part-1/), [Dan Hughes](http://blog.olorin.co.uk/) complained that the Nexus 7000 switch cannot take the full BGP table. The reason is simple: it's TCAM (FIB) has only 56.000 entries and the [BGP table has almost 350.000 routes](http://bgp.potaroo.net/).

Nexus 7000 is a Data Center switch, so the TCAM size is not really a limitation (it would usually have a default route toward the WAN core), but the same problem is experienced by Service Providers all over the world -- the TCAM/FIB size of their high-speed routers is limited.
<!--more-->
It's usually easy (and comparatively cheap) to upgrade router's main memory which holds the BGP table and the IP routing table. Upgrading SRAM or TCAM that holds the FIB is either expensive or mission-impossible ([the difference between IP routing table (RIB) and IP forwarding table (FIB) is explained in my RIB/FIB blog post](/2010/09/ribs-and-fibs/)), resulting in premature forced retirement of the high-speed gear.

Faced with this problem, [some very smart researchers proposed virtual aggregation](http://www.cs.cornell.edu/people/francis/va-wp.pdf) (and named it *ViAggre*), a technique that allows you to reduce FIB/TCAM requirements while still having the full BGP table in your router. For an [overview of virtual aggregation, read my SearchTelecom article](http://searchtelecom.techtarget.com/tip/0,289483,sid103_gci1517081,00.html), for more details, [read their paper](http://conferences.sigcomm.org/hotnets/2008/papers/19.pdf).
