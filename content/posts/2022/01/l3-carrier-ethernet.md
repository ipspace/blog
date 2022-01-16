---
title: "Layer-3 Carrier Ethernet"
date: 2022-01-18 07:49:00
tags: [ VPN ]
---
One of ipSpace.net subscribers asked for my opinion about *Adaptive IP*, a concept promoted by one of the optical connectivity vendors. As he put it:

> My interest in Carrier Ethernet moving up to Layer 3 is to see if it would be something to account for in the future. 

A quick search resulted in a marketecture using Segment Routing (of course) and an SDN controller (what else could one be using today) using Path Computation Element Protocol (PCEP) to program the network devices... and then I hit a regwall. They wanted to collect my personal details to grace me with their whitepaper, and I couldn't find even a link to the product documentation. 
<!--more-->
I can't figure out why anyone would want to consider a company that thinks their documentation is not good enough for public scrutiny in a world where most networking vendors make their design documents and product documentation publicly available, but let's keep going.

First step: fix the terminology used by my reader. There is no such thing as *layer-3 Carrier Ethernet* -- a network can forward packets based on layer-2 addresses or layer-3 addresses. If a network forwards packets based on Ethernet MAC addresses and meets certain other criteria you can claim it offers *Carrier Ethernet* services. If a network forwards packets based on IPv4 or IPv6 addresses, then it offers L3VPN services.

It's no wonder that Carrier Ethernet vendors want to enter adjacent markets (after all, Flip, cable modems, and set-top boxes worked so well for Cisco), but if you want to move from Carrier Ethernet to full-blown L3VPN services you will need a decent layer-3 control plane, and you'll have to master tons of intricacies trying to integrate snowflake customer environments into your core network. It took traditional router vendors decades to get there… probably because they’re so clumsy and stupid ;))

Let's imagine for a moment that the Carrier Ethernet vendor manages to pull off that trick. Next step: they have to persuade their traditional customers (services providers) to use the new technology. That shouldn't be too hard; after all, most service providers want nothing more than increased ARPU (Average Revenue Per User), and tried all sorts of desperate tricks to do that, including building public clouds (hint: in many cases that didn't end well).

However, once a service provider known for its Carrier Ethernet service starts pushing L3VPN (or SD-WAN) services you have to ask yourself "_am I willing to believe that they can handle the complexities of L3VPN and outsource my network core?_" I know a lot of customers unwilling to make that leap of faith. For example, they remained on Frame Relay (for a very good reason) even when their service providers started offering MPLS/VPN services, or bought IP connectivity without ever running a routing protocol with the service provider, and built their own core with IP tunnels on top of that (if that doesn't sound like SD-WAN I don't know what does ;).

### Keep Going

* For a one-hour version of a "_know your customers_" rant, watch the *[Address the Business Challenges First](https://my.ipspace.net/bin/list?id=NetBiz#BF)* part of _[Business Aspects of Networking Technologies](https://www.ipspace.net/Business_Aspects_of_Networking_Technologies)_ webinar (you'll need [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free) to watch it)
* You'll find a longer version of "_should you trust your service provider_" rant in *[Managed SD-WAN Services](https://my.ipspace.net/bin/list?id=NetBiz#SDWAN)* part of the same webinar (that part still requires [Standard ipSpace.net Subscription](https://www.ipspace.net/Subscription/Individual)).
* I did an overview of VPN services landscape (including _which one should I use_ guidelines) in _[Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service)_ webinar.
* Finally, if you're interested in Segment Routing, PCE, or SD-WAN we have you covered: watch _[Segment Routing Introduction](https://www.ipspace.net/Segment_Routing_Introduction)_ (part of standard subscription), _[PCEP and BGP-LS Deep Dive](https://www.ipspace.net/PCEP_and_BGP-LS_Deep_Dive)_ (free) or _[SD-WAN Overview](https://www.ipspace.net/SD-WAN_Overview)_ (free).
