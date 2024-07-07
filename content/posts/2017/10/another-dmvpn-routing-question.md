---
date: 2017-10-19 08:00:00+02:00
dmvpn_tag: routing
tags:
- DMVPN
- BGP
- IP routing
title: Another DMVPN Routing Question
url: /2017/10/another-dmvpn-routing-question/
---
One of my readers sent me an interesting DMVPN routing question. He has a design with a single DMVPN tunnel with two hubs (a primary and a backup hub), running BGP between hubs and spokes and IBGP session between hubs over a dedicated inter-hub link (he doesn't want the hub-to-hub traffic to go over DMVPN).

Here\'s (approximately) what he\'s trying to do:
<!--more-->
{{<figure src="/2017/10/s550-DMVPN_DualHub_EBGP_IBGP.jpg">}}

Furthermore he's "*...sending only default route from Hub to spokes, and using BGP local preference I made my Left Hub as primary one and the one in the right as secondary.*"

DMVPN Phase 3 should take care of optimal traffic flow:

> Everything is good and spoke to spoke communication go well as NHRP redirect is triggered every time the first packet crosses the primary HUB tunnel (IN from the Spoke-1 and out to the Spoke-2) for any spoke to spoke communication at the first time before the creation of the NHRP shortcut then direct Spoke to Spoke connection.

{{<note info>}}Need to know more about DMVPN? Check out the ipSpace.net [DMVPN webinars](http://www.ipspace.net/DMVPN_trilogy).{{</note>}}

Now for the fun part:

> Now let\'s imagine that the tunnel between Spoke-1 and the primary HUB broke down, hence Spoke-1 will use the default route from the Backup HUB to join Spoke-2 so HUB2 will generate a redirect NHRP and send it to Spoke-1 as the packet get in and out the same interface tunnel but when Spoke-2 will try to respond to Spoke-1,it will send the packet back through primary HUB and from the primary HUB to the second one via the IBGP peering then from the BACKUP HUB to destination so NHRP redirect will never be triggered and the Spoke to Spoke communication wont never come UP. Is this a normal situation or there is anything I miss?

Remember: the problem is that the traffic between hubs flows over the direct link, so it's effectively leaving DMVPN domain, going over to the other hub, and reentering DMVPN domain, breaking NHRP in the process.

You could get redirects to work with interesting NHRP tricks (NHRP works across multiple tunnel interfaces if they have the same NHRP ID and GRE key), or you could use BGP next hop processing to solve the problem -- after all, as the hub routers exchange spoke prefixes over BGP, they don't have to change the BGP next hop, so the real next hop always points to the other spoke, and NHRP should work.

However, there's a more fundamental decision you have to make: do you prefer *direct* traffic flow or do you prefer *reliable* traffic flow.

If you decide to go for *direct* traffic flow, make sure the hub routers don't change the BGP next hop. NHRP redirects for spoke-to-spoke traffic will work (because both hub routers know the destination is reachable via another spoke due to BGP next hop), but you might get traffic black holes if a hub router cannot reach a spoke router (for example, due to IPsec session failure).

If you decide to go for *reliable* traffic flow, change BGP next hops to *self* on every hop. The traffic will [flow over the same path as BGP path information data](/2014/08/fate-sharing-in-ip-networks/), but you might get suboptimal traffic flow that concerned my reader.

Want to discuss an interesting problem you're facing in your network? I'm usually available for [online consulting](http://www.ipspace.net/ExpertExpress).
