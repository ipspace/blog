---
date: 2020-02-05 08:37:00+01:00
dcbgp_tag: rant
evpn_tag: rant
series:
- dcbgp
tags:
- design
- BGP
- EVPN
title: The EVPN/EBGP Saga Continues
url: /2020/02/the-evpnbgp-saga-continues.html
---
[Aldrin](http://aldrinisaac.blogspot.com/) wrote a well-thought-out comment to my *[EVPN Dilemma](https://blog.ipspace.net/2019/11/the-evpn-dilemma.html)* blog post explaining why he thinks it makes sense to use [Juniper's IBGP (EVPN) over EBGP (underlay) design](https://www.ipspace.net/Data_Center_BGP/BGP_in_EVPN-Based_Data_Center_Fabrics#IBGP-Based_EVPN_on_Top_of_EBGP-Based_Fabric_Routing). The only problem I have is that I forcefully disagree with many of his assumptions.

He started with an in-depth explanation of why EBGP over directly-connected interfaces makes little sense:
<!--more-->
> Following [blog](https://blog.noc.grnet.gr/2016/09/28/lab-on-evpn-vxlan-on-juniper-qfx5100-switches-3/) captures in detail EVPN over EBGP using Junos dating back to 2016. You can see the multi-hop EBGP sessions for EVPN required to set the loopback as the VTEP IP (i.e. BGP protocol next-hop). \[More about BGP next hop handling in the [original comment](https://blog.ipspace.net/2019/11/the-evpn-dilemma.html?showComment=1575861244172#c3854070778949161857)\].

I agree with Aldrin that the best way to get the desired BGP next hop *in Junos EVPN implementation* is to use a BGP session between loopback interfaces (to be more precise, you have to use the same loopback interface for BGP session and VTEP IP)... but that's just because *they decided not to set the correct BGP next hop when inserting the local EVPN route into the local BGP table*.

Setting BGP next hop to a specific value when originating a BGP route is not a novel idea - it took me about 30 seconds to [find it in RFC 1403](https://tools.ietf.org/html/rfc1403#page-14) (OK, I'm old enough to know where to look). Assuming an EVPN device wants to receive VXLAN packets with a specific destination IP address, I can't figure out a good reason why it wouldn't set that IP address as the BGP next hop *when originating the route*. Asking the network operator to run BGP sessions between loopback interfaces just so the BGP next hop would be set to the right value is stupid.

{{<note>}}There might be something in Junos EVPN implementation that prevents them from setting the BGP next hop on route origination, but if that's the case please [document that limitation and move on](https://blog.ipspace.net/2019/04/dont-sugarcoat-challenges-you-have.html). Trying to persuade me why I should consider a workaround a sane design won't work.{{</note>}}

Moving on, Aldrin mentioned BGP next hop handling on EBGP sessions:

> Hopefully folks also know that when using EBGP with EVPN, it's important that intermediate EBGP hops do not rewrite the protocol next-hop set by the egress PE since we need the VXLAN tunnels to be addressed to the correct egress PE and not somewhere short of that.

Please make your mind up. Your product marketing could either promote EBGP as the intra-domain routing protocol, and your engineering could support that by implementing sane defaults supporting that assumption, or you could tell people to stick with more traditional IGP+IBGP design and get rid of all the complexities.

For example, FRRouting implementation decided to go all-in, and uses **next-hop-unchanged** as default behavior on EBGP EVPN sessions (which nicely matches Cumulus' EBGP-only design). Most other vendors behave like deer in headlights.

> All considered, IMO it's more straight-forward to use IBGP with RRs for EVPN, rather than to force-fit EVPN into hop-by-hop EBGP route propagation.

If you want to use the same defaults you used for the last 30 years, then YES, please use IBGP... but also stick to the designs we've been using during those 30 years, like running IBGP over OSPF or IS-IS. Those designs were good enough for largest ISPs on this planet... and now all of a sudden they're not [good enough for enterprise data centers with a few dozen switches](https://blog.ipspace.net/2017/11/bgp-as-better-igp-when-and-where.html)? Could someone please stop this lemming run before everyone hits the cliff?

> Anyway it has been a long-standing convention to use IBGP for overlays within an instance of a transport domain.

And it has been a long-standing convention to use OSPF or IS-IS as the underlying routing protocol in said transport domain. Unfortunately most data center switching vendors [think they need to be hip](https://blog.ipspace.net/2018/05/is-ospf-or-is-is-good-enough-for-my.html), and try to persuade us how well star-shaped pegs fit into round holes (hint: they do if you have a big-enough hammer).

> FYI, Junos leans toward being explicit about configuration leaving it to automation to simplify management of network.

The best reply to this line of reasoning is a comment I got from an attendee of my recent *[VMware NSX, Cisco ACI or Standard-Based EVPN](https://www.ipspace.net/VMware_NSX,_Cisco_ACI_or_Standard-Based_EVPN)* workshop:

> For medium businesses (IT dept of 5-10 people) who have never heard of BGP, VNID, multicast... EVPN is simply scary as hell. If they have to choose they go for ACI - presented as single point of management and magically solves world hunger and is "anywhere" versus BGP EVPN being marketed as being complex (people don't want hear that they need to configure 70 lines of code per VXLAN per switch in the fabric versus a few clicks on ACI).

I would understand why someone within Cisco would have a vested interest to make EVPN configurations complex, but I fail to see why Arista and Juniper are playing along.

**Long story short**: I've seen two simple and successful ways of deploying EVPN in non-hyperscale VXLAN-based data center fabrics - running IBGP over OSPF/IS-IS, or running EBGP between directly-connected interfaces with sane BGP next-hop defaults on BGP route origination and propagation. Everything else is just piles of unnecessary complexity that scares people away from what is otherwise the best technology to use if you really want to build layer-2 fabrics (and your vendor doesn't believe in SPB).

**Final note**: Want to get beyond vendor arguments and marketing? You might want to watch our [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar - over 10 hours of (mostly) vendor-neutral fact-based material.
