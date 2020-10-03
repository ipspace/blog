---
title: "Must Read: Redistributing Full BGP Feed into OSPF"
date: 2020-10-07 07:42:00
tags: [ BGP, OSPF ]
---
The idea of redistributing the full Internet routing table (840.000 routes at this moment) into OSPF sound as ridiculous as it is, but when fat fingers strike it should be relatively easy to recover, right? Just disable redistribution (assuming you can still log into the offending device) and move on.

Wrong. As [Dmytro Shypovalov](https://www.linkedin.com/in/dmytro-shypovalov-573aab58/) explained in an [extensive blog post](https://routingcraft.net/what-happens-if-you-redistribute-bgp-full-view-into-ospf/), you might have to restart all routers in your OSPF domain to recover.

And that, my friends, is why OSPF is a single [failure domain](https://blog.ipspace.net/2019/12/disaster-recover-and-failure-domains.html), and why you should [never run OSPF between your data center fabric and servers or VM appliances](https://blog.ipspace.net/2013/08/virtual-appliance-routing-network.html).
