---
date: 2016-02-17 11:32:00+01:00
dcbgp_tag: server
series:
- dcbgp
series_weight: 900
tags:
- data center
- BGP
- high availability
- Cumulus Linux
title: Running BGP on Servers
url: /2016/02/running-bgp-on-servers.html
---
Mr. A. Anonymous left this comment on my [BGP in the data centers](http://blog.ipspace.net/2016/02/using-bgp-in-data-center-fabrics.html) blog post:

> BGP is starting to penetrate into servers as well. What are your thoughts on having BGP running from the servers themselves?

Finally some people got it. Also, welcome back to the \'90s (see also RFC 1925 section 2.11).
<!--more-->
Running a routing protocol on servers (or IBM mainframes) is nothing new -- we've been doing that 30 years ago, using either RIP or OSPFv2 -- and it's one of the best ways to achieve path redundancy.

{{<note warn>}}
I've also heard of a network design that was one link failure away from IBM mainframe becoming the core router. If you run routing protocols on servers make sure they cannot become transit nodes.
{{</note>}}

Later it became unfashionable to have any communication between the server silo and the network silo, resulting in the unhealthy mess we have today where everyone expects the other team to solve the problem. Unfortunately, the [brown substance tends to flow down the stack](http://blog.ipspace.net/2013/04/this-is-what-makes-networking-so-complex.html).

However, even though the [mainstream *best practices*](https://twitter.com/SpotifyEng/status/698196447922147328) focused on link bonding, MLAG and similar kludges, I know people who were running BGP on their servers (with good results) for years if not decades.

The old ideas resurfaced in the mainstream networking as [means of connecting the virtual (overlay) world with the physical world](http://blog.ipspace.net/2013/06/dynamic-routing-with-virtual-appliances.html), first with routing protocol support on VMware NSX Edge Services Router (ESR), later with BGP support in Hyper-V gateways... and I was really glad VMware decided to [implement BGP on ESR](http://blog.ipspace.net/2013/08/routing-protocols-on-nsx-edge-services.html) because [BGP establishes a clean separation](http://blog.ipspace.net/2013/08/virtual-appliance-routing-network.html) between two administrative domains (virtual and physical).

{{<note info>}}
Juniper Contrail and Nuage VSP use BGP to [connect to the outside world](http://blog.ipspace.net/2014/01/interfacing-overlay-virtual-networks.html), but not from end-hosts, so they're out of the scope of this article.
{{<note>}}

Lately, I've seen very smart full-stack engineers (read: sysadmins who understand networking) use recent versions of Quagga (with [Cumulus Networks patches](http://blog.ipspace.net/2015/02/bgp-configuration-made-simple-with.html)) to run BGP across [unnumbered links](http://blog.ipspace.net/2014/06/unnumbered-ospf-interfaces-in-quagga.html) between servers and ToR switches totally simplifying both BGP configurations as well as deployment procedures (not to mention turning the whole fabric into pure L3 fabric with no VLANs on ToR switches).

Want to know more? Dinesh Dutt described the idea in the [Leaf-and-Spine Fabric Architectures](http://www.ipspace.net/Leaf-and-Spine_Fabric_Architectures) webinar.
