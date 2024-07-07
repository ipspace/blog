---
title: "So-Called Modern VPNs: Marketing and Reality"
date: 2022-03-17 07:59:00
tags: [ VPN, LISP ]
---
Someone left a "killer" comment[^BB] after reading the _[Should We Use LISP](/2022/03/should-we-use-lisp/)_ blog post. It start with...

> I must sadly say that your view on what VPN is all about is pretty rusty and archaic :( Sorry! Modern VPNs are all pub-sub based and are already turning into NaaS.

Nothing new there. I've been called *old-school guru from an ivory tower* when claiming TRILL is the wrong direction and we should use good old layer-3-based design[^TRILL], but let's unpack the "pub-sub" bit.
<!--more-->
[^BB]: Assuming you're playing Buzzword Bingo

[^TRILL]: In the meantime, TRILL and SPBM are mostly dead, as are all proprietary fabric solutions like FabricPath, VCS Fabric, or Virtual Chassis Fabric. Everyone is building fabrics on top of layer-3 networks. Go figure...

[According to Wikipedia](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern), "_publish–subscribe is a messaging pattern where senders of messages, called publishers, do not program the messages to be sent directly to specific receivers, called subscribers, but instead categorize published messages into classes without knowledge of which subscribers, if any, there may be_". The author of that comment somehow failed to realize that's a perfect description of an L3VPN or EVPN design using BGP route reflectors and RT-based Outbound Route Filters. I already mentioned that in the [LISP blog post](/2022/03/should-we-use-lisp/), but it's obviously too much of a nuisance to read the whole article before writing a dismissive comment.

As for network-as-a-service, I'm old enough to remember industry pundits telling us how networking is dead because every endpoint will use mobile networks with LTE VPNs. More than a decade later, we're still slogging through the networking morass even though it [should be easier to build networks with no wires](https://dilbert.com/strip/2010-04-24). Also, according to the pundits, routing is dead because we have SD-WAN, and BGP and MPLS are obsolete. What's funny is that people having these opinions couldn't publish them without BGP and (oftentimes) MPLS doing their job in the background.

But wait, it gets better:

> VPN overlays starts at the end points compute or mobile device and seamlessly and dynamically interconnects endpoints.

Time to go back to taxonomy. There are endpoint VPNs that the author of this comment is so excited about, and infrastructure VPNs implemented in routers[^SDR], firewalls, or dedicated encryption boxes... All of them could be implemented as an overlay on top of another network[^IPSEC], and all of them need some sort of control plane or orchestration system.

[^SDR]: An SD-WAN device is a router regardless of what the vendor marketing is telling you. So are all boxes called _switches_ that happen to forward packets based on network-layer addresses.

[^IPSEC]: Ever heard of IPsec tunnel mode?

From the VPN traffic flow perspective, we have hub-and-spoke VPNs where all devices communicate through a set of central servers and peer-to-peer VPNs where the VPN devices can communicate directly. Traditional IPsec endpoint VPNs with VPN concentrators are a perfect example of hub-and-spoke VPN. Interestingly, BGP/MPLS L3VPN[^L3VPN] was one of the first peer-to-peer VPNs.

[^L3VPN]: The official name of this technology is (according to RFC 4364) BGP/MPLS IP Virtual Private Networks (VPNs). I will use L3VPN throughout this post to differentiate it from L2VPN.

It's also worth pointing out that endpoint peer-to-peer VPNs are nothing new. My kids were playing Minecraft using Hamachi ([released in 2004](https://en.wikipedia.org/wiki/LogMeIn_Hamachi)) a decade ago, and I'm positive Hamachi was not the first peer-to-peer VPN[^PA].

[^PA]: Pointers to "prior art" are most welcome.

Finally, there are customer-operated VPNs (DMVPN, SD-WAN...) and provider-operated VPNs (Carrier Ethernet, VPLS, BGP/MPLS L3VPN...). We even build VPNs within data centers to implement virtual networks (VXLAN/EVPN, Cisco ACI, VMware NSX, all public cloud infrastructure).

There are great use cases for any technology or product I mentioned above, and saying "_one of them sucks, you should only use the other one_" makes as much sense as saying "_Python and C/C++ are dead, you should use Swift or TypeScript_". There's a slight difference between a fanboy and an engineer -- an engineer considers the requirements and selects the optimal set of technologies that meet the requirements with minimum complexity.

We're not done yet. Next comes a jab at the service providers:

> Examples of VPNs are not EVPN or L3VPNs -- those are SP customer locking tools.

L3VPN is a lock-in tool *if you're gullible enough to believe marketing slides and outsource your core routing to a third party*. Numerous CxOs are in that category to the delights of various service providers. Smart customers use L2VPN and build their own networks on top of that, or use L3VPN as pure IP transport and build their own overlay on top of that transport (see also: SD-WAN).

EVPN is usually used to implement L2VPN (aka Carrier Ethernet) and if you manage to get locked into a single Carrier Ethernet... I'll stop right there.

For a more thorough overview of VPN technologies, their applicability, and associated gotchas (including lock-in considerations) watch the _[Choose the Optimal VPN Service](https://www.ipspace.net/Choose_the_Optimal_VPN_Service)_ webinar.

Now for the final bit of that wonderful comment:

> Real VPNs of current times are ZeroTier, TailScale etc.., LISP falls into the same modern camp.

ZeroTier and TailScale excel as endpoint VPNs, although both of them support gateway (relay) nodes[^TS]. If I had to implement an endpoint VPN these days, I would definitely consider them before thinking about IPsec clients and concentrators.

[^TS]: I've heard great things about TailScale coming from an environment that will definitely need gateway nodes.

LISP is a totally different story. While there are endpoint LISP implementations, the only products pushing LISP (that I'm aware of) use it to implement infrastructure VPNs. Furthermore, [based on the comments I got to recent blog posts](/2022/03/should-we-use-lisp/), it looks like LISP refocused from [cache-based forwarding](/2022/02/cache-based-forwarding/) towards a control plane that's functionally equivalent to EVPN or L3VPN control plane. 

To round up the VPN confusion: there are endpoint EVPN implementations (we discussed them in [December 2021 Design Clinic](https://my.ipspace.net/bin/list?id=Design#2021_12)), so what's the difference between _real VPNs_ and _SP customer locking tools_[^TOYS]? It's obviously not the technology, but the way it's used.

[^TOYS]: Apart from _I love shiny new toys and hate stuff that I had to work with in the past_
