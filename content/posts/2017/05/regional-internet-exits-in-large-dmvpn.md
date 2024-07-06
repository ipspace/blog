---
date: 2017-05-17 14:39:00+02:00
dmvpn_tag: design
tags:
- design
- DMVPN
title: Regional Internet Exits in Large DMVPN Deployment
url: /2017/05/regional-internet-exits-in-large-dmvpn.html
---
One of my readers wanted to implement a large DMVPN cloud with regional Internet exit points:

> We need to deploy a regional Internet exits and I'd like to centralize them.  Each location with a local Internet exit will be in a region and that location will advertise a default-route into the DMVPN domain to only those spokes in that particular region.

He wasn't particularly happy with the idea of deploying access and core DMVPN clouds:
<!--more-->
> Looking at various design documents, they lead you to a hierarchical setup but I would like to look at your webinar if it discusses DMVPN setup in a similar manner.

The easy answer first: no, my [DMVPN webinars](http://www.ipspace.net/DMVPN_trilogy) don't discuss such a setup. It's a routing challenge and has nothing to do with DMVPN. It does help though if you [understand](/2008/09/knowledge-or-recipes.html) how DMVPN works and how you should use routing protocols across DMVPN, and that is definitely covered in the DMVPN webinars.

Now for the interesting part.

Assuming the regional locations are DMVPN hub routers you could use (at least) two designs to get the desired traffic flow:

**Multiple DMVPN access clouds** (one per region) with another DMVPN cloud linking the hub routers. Hub routers would advertise default route into their region, but not between hubs. Alternatively you could exchange default routes between hubs for inter-hub redundancy.

{{<figure src="/2017/05/s550-DMVPN_Exit_Access_Subnets.jpg">}}

{{<note warn>}}The diagram is highly simplified. In real life you'd have at least two hub routers in ever region, and two DMVPN access networks (one over Internet, one over MPLS/VPN, or using two different ISPs) for redundancy.{{</note>}}

The "only" drawback of this setup is suboptimal inter-region spoke-to-spoke traffic flow. Without special tricks (NHRP shortcuts across multiple DMVPN clouds) the traffic would flow through two hub routers to reach a spoke in another region.

{{<figure src="/2017/05/s550-DMVPN_Exit_Access_Traffic.jpg">}}

**Routing tricks** -- while using a single DMVPN subnet the hub routers advertise default route to in-region spokes but not to other spokes (or low-cost default route to in-region spokes and high-cost default route to other spokes). This is clearly impossible to do with OSPF, and pretty hard to do with EIGRP. BGP would be my preferred routing protocol in this case.

{{<figure src="/2017/05/s550-DMVPN_Exit_Single_Routing.jpeg">}}

Finally a note for SD-WAN aficionados: before you tell me how much easier this would be with your preferred SD-WAN solution, do remember that an SD-WAN controller is functionally equivalent to a BGP route reflector. It's just that the route propagation functionality is [hidden behind a GUI façade](/2015/06/software-defined-wanwell-orchestrated.html).
