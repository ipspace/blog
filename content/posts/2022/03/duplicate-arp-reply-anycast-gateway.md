---
anycast_tag: fabric
date: 2022-03-30 07:11:00+00:00
evpn_tag: details
series:
- anycast
tags:
- ARP
- EVPN
- bridging
title: Duplicate ARP Replies with Anycast Gateways
---
A reader sent me the following intriguing question:

> I'm trying to understand the ARP behavior with SVI interface configured with anycast gateways of leaf switches, and with distributed anycast gateways configured across the leaf nodes in VXLAN scenario.

Without going into too many details, the core dilemma is: will the ARP request get flooded, and will we get multiple ARP replies. As always, the correct answer is "_it depends_" 🤷‍♂️
<!--more-->
### MLAG with Active-Active FHRP

Let's start with a pair of leaf switches in an MLAG pair. You might configure anycast gateway on them (using, for example, [Arista's Virtual ARP](/2013/06/arista-eos-virtual-arp-varp-behind/)) or use an active/active implementation of first-hop redundancy protocol like HSRP or VRRP.

{{<figure src="/2022/03/MLAG-architecture.jpg">}}

The scenario seems simple enough: the ARP request (broadcast) is sent over a single link in the LAG group, and whichever router gets the request will reply to it. For example, A sends the ARP request for gateway IP address to S2, and S2 replies to it. Mission accomplished.

Reality is more complex than that. All broadcasts have to be propagated over the MLAG peer link because they might have to be sent to orphan nodes connected to the other switch in the MLAG pair. For example, A might have sent an ARP request for X to S2, and S2 must propagate it over the peer link to S1 so that it eventually reaches X.

The ARP request for the shared IP address is thus always delivered to the second switch over the peer link. Whether the second switch replies with a second ARP reply or trust that the switch receiving the original ARP request did its job is an implementation detail.

Finally, if you configured a VLAN stretched across more than two leaf switches, the behavior depends on whether your devices *bridge if they can and route if they must* or *route if they can and bridge if they must*.

### VXLAN/EVPN with Proxy ARP

VXLAN/EVPN with Proxy ARP on leaf switches is the cleanest scenario. Most data center switches configured with proxy ARP behave in *route if you can* mode, intercept all ARP requests, and reply to them *on behalf of other hosts attached to the same segment* (thus *proxy ARP*) based on the information received in EVPN updates.

{{<figure src="/2022/03/EVPN-anycast-leaf.jpg">}}

### Stretched VLANs

Most other stretched VLAN implementations (including traditional  bridging, TRILL/SPB, some VXLAN designs) behave in *route if you must* mode, so you'd expect the ARP requests to be flooded to everyone, and potentially answered by multiple anycast gateways[^GARP].

[^GARP]: According to Dmytro Shypovalov, Arista's Virtual ARP sends out gratuitous ARPs every 30 seconds anyway, so the impact of multiple ARP replies shouldn't matter -- once a host learns the virtual gateway MAC address, GARPs will ensure that address stays in the host ARP cache. Please note that the *Virtual ARP* feature is not the same thing as *Anycast EVPN Gateway*. Arista EOS does not send GARPs from EVPN anycast gateways.

An interested reader might be tempted to ask the question along the lines of "_but can't we filter the ARP request for the anycast gateway and not flood it?_", and she would be perfectly right. Unfortunately, most TCAMs cannot look that far into an ARP request[^FG], which brings us into a totally unpredictable[^LT] territory:

* An implementation might decide it's preferable that the end hosts deal with duplicate ARP replies, floods ARP in hardware, and delivers them to multiple anycast gateways.
* A smarter implementation might decide it makes sense to deliver all ARP requests to the CPU first (because a copy of the ARP request will be delivered to the CPU anyway), and then make a smart decision whether to reply to the request, proxy it, or flood it further.

### Known Implementations

As with so many things in networking, we're in the "_it depends on the implementation details_" territory, and this is what I got so far:

* ARPs get delivered to the CPU on Arista EOS if you configure EVPN and SVI (source: [Dmytro Shypovalov](https://www.linkedin.com/in/dmytro-shypovalov-573aab58/?originalSubdomain=ua)).

Please leave a comment if you're familiar with related behavior on other platforms.

### Thank You!

Finally, a huge THANK YOU to Dmytro -- he was kind enough to help me figure out some of the details described in this blog post.

[^LT]: ... without doing an actual lab test

[^FG]: Not to mention the ND morass, in particular when Fernando Gont comes along and [throws a few extension headers around just for fun](https://www.rfc-editor.org/rfc/rfc7113.html).
