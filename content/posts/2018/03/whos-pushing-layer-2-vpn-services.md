---
date: 2018-03-07 10:38:00+01:00
tags:
- VPN
- service providers
title: Who’s Pushing Layer-2 VPN Services?
url: /2018/03/whos-pushing-layer-2-vpn-services.html
---
Here's another great point [Tiziano Tofoni](https://www.linkedin.com/in/tiziano-tofoni-1361759/) raised in his comment to my [EVPN in small data center fabrics](https://blog.ipspace.net/2018/02/using-evpn-in-very-small-data-center.html) blog post:

> I cannot understand the usefulness of L2 services. I think that the preference for L2 services has its origin in the enterprise world (pushed by well known \$vendors) while ISPs tend to work at Layer 3 (L3) only, even if they are urged to offer L2 services by their customers.

Some (but not all) ISPs are really good at offering IP transport services with fixed endpoints. Some Service Providers are good at offering per-tenant IP routing services required by MPLS/VPN, but unfortunately many of them simply don't have the skills needed to integrate with enterprise routing environments.
<!--more-->
For example: I've seen MPLS/VPN providers who force the customers to accept external OSPF routes because the provider wants to own the CE-router and is not willing to do BGP-to-OSPF redistribution in a way that would preserve the OSPF route attributes the way they were meant to be preserved in MPLS/VPN architecture.

{{<note info>}}More about this can of worms in the [Choose the Optimal VPN Service](http://www.ipspace.net/Choose_the_Optimal_VPN_Service) webinar and [Integrating DMVPN-based Internet VPN with MPLS/VPN WAN](https://www.ipspace.net/Integrating_Internet_VPN_with_MPLS_VPN_WAN) case study.{{</note>}}

**Long story short**: I always believed in greatness of MPLS/VPN architecture, but when the theory meets reality things often get ugly. As much as it hurts me, I'd prefer buying layer-2 services or IP transport services from a service provider because I know they can't mess them up too much, and I'd still own the end-to-end routing.

I would then use the layer-2 transport service to build my own routed core, or use IP transport service with a tunnel VPN on top of it. You could also use SD-WAN if you're happy to deal with GUI-driven undocumented technologies.
