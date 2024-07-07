---
date: 2018-03-01 09:21:00+01:00
tags:
- SD-WAN
- IP routing
- SDN
- WAN
title: Lack of Fast Convergence in SD-WAN Products
url: /2018/03/lack-of-fast-convergence-in-sd-wan/
sd-wan_tag: myth
---
One of my readers sent me this question:

> I\'m in the process of researching SD-WAN solutions and have hit upon what I believe is a consistent deficiency across most of the current SD-WAN/SDx offerings. The standard \"best practice\" seems to be 60/180 BGP timers between the SD-WAN hub and the network core or WAN edge.

Needless to say, he wasn't able to find BFD in these products either.

Does that matter? My reader thinks it does:
<!--more-->
> When we consider that many companies will use these SD-WAN solutions to transport voice and real-time traffic, why is there a lack of focus on mechanisms which enable fast convergence at critical aggregation points?

He definitely has a point, even without voice and real-time traffic requirements. Waiting three minutes to figure out an adjacent box is down definitely feels like a call from '90s.

Or maybe we're missing something. The whole idea of SD-WAN was to take over the core WAN routing in your network. Tom Hollingsworth has an interesting story [in one of his blog posts](https://networkingnerd.net/2018/01/19/can-routing-be-oversimplified/):

> We turned off OSPF and now have a /16 route for the internal network and a default route to the Internet where a lot of our workloads were moved into the cloud.

We've seen similar claims in the past. Remember MPLS/VPN and the nirvana you'll reach once the Service Provider takes over your core routing? Yeah, it didn't turn out exactly that way, did it?

Anyway, assuming we give a proprietary black-box system total control of our core network should we care about the routing protocols at the edge of the black haze?

If you're deploying a single SD-WAN appliance per site, and it controls all uplinks, the answer is obviously NO. There's a single exit point (SD-WAN appliance) and it's either working or not.

{{<figure src="/2018/03/s600-Small+site.png" caption="Non-redundant SD-WAN site">}}

If you're deploying redundant SD-WAN appliances on a site that needs higher availability and these appliances work as a cluster, control all the uplinks, and use layer-2 tricks (usually VRRP) to give the impression of a single next-hop router to the site network, the answer is still NO. We're doing the same thing with static default routes pointing to a shared IP address of a firewall cluster today. I'm not saying it's a good idea, but some people would probably claim it's the best practice.

{{<figure src="/2018/03/s600-Redundant+layer-2+site.png" caption="Site with redundant SD-WAN connections">}}

Unfortunately some SD-WAN vendors believe they can use the same approach no matter what. Their appliances try to avoid routing protocols like black plague and use dirty tricks like VRRP between SD-WAN appliance and on-site router combined with static default routing to get the appearance of primary/backup behavior. How many times do we have to repeat the same mistakes?

{{<figure src="/2018/03/s600-Site+with+Redundant+Uplinks.png" caption="Site using a router in parallel with an SD-WAN appliance">}}

However, if you do run routing protocol between SD-WAN appliances and other routers on your site for whatever reason (failover, alternate uplinks...), then I guess we deserve a decent implementation of the said routing protocols. It's not like you couldn't get a routing protocol suite these days, either as open-source project or a commercial product.

{{<figure src="/2018/03/s600-Large+Site+with+Routing.png" caption="Site using a routing protocol to implement internal layer-3 redundancy">}}

Or maybe the SD-WAN vendors don't have to care because they're never asked about such mundane details. There must be plenty of customers believing in [magic powers of PowerPoint](/2011/09/long-distance-irf-fabric-works-best-in/) out there...

### Want to know more?

I covered the basics of SD-WAN in [Choose the Optimal VPN Service](http://www.ipspace.net/Choose_the_Optimal_VPN_Service) and [SDN Use Cases](http://www.ipspace.net/SDN_Use_Cases) webinars.

You might also want to watch the free [SDWAN 101](https://www.ipspace.net/SDWAN) and [Cisco SD-WAN Foundations and Design Aspects](https://www.ipspace.net/Cisco_SD-WAN_Foundations_and_Design_Aspects) webinars.
