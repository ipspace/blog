---
date: 2023-02-28 07:21:00+00:00
multihoming_tag: bgp
series:
- multihoming
tags:
- BGP
- design
title: Alternatives to IBGP within Multihomed Sites
---
Two weeks ago I explained why you might want to run IBGP between CE-routers on a multihomed site. One of the blog readers [didn't like my ideas](https://blog.ipspace.net/2023/02/ce-ibgp-multihomed-site.html#1669):

> In such a small deployment I assume that both ISPs offer transit, so that both CEs would get a default route from their upstream.
>
> In this case I would not iBGP the CEs together but have HSRP running on the two CEs and track the uplink (interface and/of BGP session) to determine the active gateway.

Let's see what could possibly go wrong with that design.
<!--more-->
{{<figure src="/2023/02/ce-ibgp-l2.png" caption="Network topology">}}

### To IBGP Or Not to IBGP

Assuming both PE-routers advertise only the default route, a CE-router know where to propagate a packet it receives through the LAN interface if:

* The PE-CE link is up
* The PE-CE BGP session is operational
* PE-router advertised a default route over the PE-CE BGP session.

It's easy to adjust HSRP/VRRP priority based on uplink status. I never tried to do it based on a state of a BGP session, and it's interesting to try to do it based on the presence of a specific prefix in RIB.

Some network operating systems can adjust HSRP/VRRP priority based on a complex tracked object, and on some network operating systems it's possible (with enough effort) to have the BGP default route as that tracked object[^EEM]. However, it might be simpler to have that IBGP session in place.

{{<note>}}Please note that I'm not saying "*you don't need FHRP on the LAN interfaces of the CE-routers*" (that's a completely different discussion) but "_you can't rely on FHRP priority to get LAN packets to the router that knows how to forward them_."{{</note>}}

[^EEM]: If nothing else, you could develop some crazy EEM magic on Cisco IOS -- read some [ancient blog posts](https://blog.ipspace.net/tag/eem.html) on this site if you're interested in that particular strain of job security.

I also received an interesting comment on [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7031529539725877248/) saying:

> You need a static default route pointing towards the second CE with a metric [sic] inferior to the route installed by EBGP for failover purpose.

{{<note>}}Obviously you'd need a static route with higher admin distance (or whatever your preferred implementation calls it); one usually cannot compare metrics between different routing sources. HT: [A Random Guy](https://blog.ipspace.net/2023/02/multihomed-ibgp-details.html#1689).{{</note>}}

That would also work. I still think IBGP session is simpler, and it helps ensure that all (BGP) routers in an autonomous system have the same view of the network.

Another commenter on LinkedIn wanted to demonstrate his BGP prowess and wrote a lengthy treatise on BGP next hop processing (spoiler alert: [here's a better version](https://blog.ipspace.net/2011/08/bgp-next-hop-processing.html)) including the recommendation to set the next hop on IBGP session to the loopback interface. Interestingly, although that's the recommended _best practice_, you don't need the loopback interface or IGP if you have only two directly-connected routers in an autonomous system -- [the road to hell is often paved with best practices](https://blog.ipspace.net/2011/08/road-to-complex-designs-is-paved-with.html).

To recap:

* I would still use an IBGP session between the CE-routers
* I would establish that IBGP session between IP addresses assigned to LAN interfaces -- assuming the CE-routers have a single LAN interface (or a port channel) and the site does not have any intermediate routers.

### Default Route or More Specifics?

The original comment continued along the lines of _we don't need more than the default route_:

> And if you wanted to IBGP them anyway, I would put a route-map on it to only exchange the default route from the upstreams, so that both CEs have a 0/0 route with different distance. The only thing I don't understand is in which failure scenario traffic would end up on a CE without an active BGP uplink.

Using just the default route makes sense if:

* You're using the uplinks in pure active/backup setup or
* You want to do ECMP load balancing between two uplinks connected to the same ISP[^N2].

In any case, if you decide to go with the default route, it might be better to filter BGP updates on the PE-CE EBGP session, not on the CE-CE IBGP session. Why would you accept a default route and the full DFZ table, spend CPU cycles to process all the updates (all of them having the same BGP next hop) and pass just the default route to the IBGP peer?

[^N2]: Trying to do ECMP load balancing across links connected to different ISPs is usually a bad idea. The proof is left as an exercise for the reader; if you decide to go down that path, you might find some of the older blog posts useful.

While two default routes might work well for a content _consumer_ (because it's hard to influence incoming traffic anyway), if you happen to be content *provider* (there's more traffic going out than coming in), you might want to optimize WAN link utilization. For example, you might want to use the direct uplink for prefixes belonging to ISPs and their customers, or you could do a [traffic flow analysis combining NetFlow with BGP data](https://blog.ipspace.net/2015/01/sdn-router-spotify-on-software-gone-wild.html), and [accept prefixes that represent large percentage of your traffic](https://blog.ipspace.net/2015/10/sdn-internet-router-is-in-production-on.html) ([even more details](https://blog.ipspace.net/2022/05/living-small-forwarding-tables.html)).

### More Details

We discussed whether to use just the default route, a subset of prefixes, or a locally-generated default route in [September 2022](https://my.ipspace.net/bin/list?id=Design#2022_09) session of _[ipSpace.net Design Clinic](https://www.ipspace.net/IpSpace.net_Design_Clinic)_. You might also want to watch the _[Surviving the Internet Default Free Zone](https://www.ipspace.net/Surviving_the_Internet_Default_Free_Zone)_ webinar.

### Revision History

2023-03-01
: Added a "you might need FHRP on LAN interfaces" note based on a comment from Mr. Anonymous.
