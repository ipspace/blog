---
date: 2020-10-14 07:42:00+00:00
ospf_tag: read
series_title: Redistributing Full BGP Feed into OSPF
tags:
- BGP
- OSPF
title: 'Must Read: Redistributing Full BGP Feed into OSPF'
---
The idea of redistributing the full Internet routing table (840.000 routes at this moment) into OSPF sounds as ridiculous as it is, but when fat fingers strike, it should be relatively easy to recover, right? Just turn off redistribution (assuming you can still log into the offending device) and move on.

Wrong. As [Dmytro Shypovalov](https://www.linkedin.com/in/dmytro-shypovalov-573aab58/) explained in an [extensive blog post](https://routingcraft.net/what-happens-if-you-redistribute-bgp-full-view-into-ospf/), you might have to restart all routers in your OSPF domain to recover.

And that, my friends, is why OSPF is a single [failure domain](/2019/12/disaster-recover-and-failure-domains/), and why you should [never run OSPF between your data center fabric and servers or VM appliances](/2013/08/virtual-appliance-routing-network/).
