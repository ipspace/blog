---
date: 2021-05-05 07:21:00+00:00
series:
- unnumbered-interfaces
tags:
- IP routing
- bridging
- networking fundamentals
title: 'Back to Basics: Do We Need Interface Addresses?'
short_summary: |
  In the world of ubiquitous Ethernet and IP, it's common to think that one needs addresses in packet headers in every layer of the protocol stack. However, that's just one option and not exactly the best one in many scenarios.
---
In the world of ubiquitous Ethernet and IP, it's common to think that one needs addresses in packet headers in every layer of the protocol stack. We have MAC addresses, IP addresses, and TCP/UDP port numbers... and low-level addresses are assigned to individual interfaces, not nodes.

Turns out that's just one option... and not exactly the best one in many scenarios. You could have interfaces with no addresses, and you could have addresses associated with nodes, not interfaces.
<!--more-->
### Unnumbered Interfaces

Imagine you're in a crowded ballroom and you want to do a random chat with Alice, Bob, or Charlie. It makes perfect sense to prepend your sentence with "*Bob, what do you think about...*" if you want to chat with Bob, right? Likewise, you need link-layer addresses on multi-access links (shared Ethernet, WiFi), and you need network addresses in networks having more than two nodes.

What about sitting in a quiet room with Bob seated across the table from you? Does it make sense to preface everything you're saying with "*Hey, Bob!*" Obviously not. 

Similarly, you don't need link-layer addresses on point-to-point links, and yet we almost always use them for historical reasons:

* SDLC, the grandfather of most serial-line protocols (including HDLC and PPP), supported multidrop -- the ability to connect more than two nodes to a single modem link -- and thus needed link-layer addresses. 

{{<figure src="/2021/05/Addr-Multidrop.png" caption="Multidrop is still used on cable and PON networks">}}

* All derivations of SDLC retained them because it was easier to reuse the existing hardware devices than to persuade the hardware manufacturers to do something else.

{{<figure src="/2021/05/Addr-PPP-Frame.png" caption="Every PPP frame includes an unnecessary _broadcast_ destination address">}}

* Ethernet was designed to be a multi-access network. Also, Ethernet switching pretends that point-to-point segments between the end nodes and switches belong to a [giant virtual multi-access cable](/2015/02/lets-get-rid-of-thick-yellow-cable/), and thus you cannot get rid of MAC addresses. However, when we started using Ethernet for router-to-router links[^1], we could reduce the size of the Ethernet header. Still, it was more convenient to reuse existing hardware than to work hard to save the 14 bytes of every frame.

[^1]: Or switch-to-switch links if you're of [marketing persuasion](/2011/02/how-did-we-ever-get-into-this-switching/).

A few protocols got it right, though:

* [SLIP](https://en.wikipedia.org/wiki/Serial_Line_Internet_Protocol) was designed to carry IP packets over dial-up links. Adding another layer of addresses was unnecessary, and as they started from scratch and used existing character-mode hardware, they could get away with it.
* [PPPoE](https://en.wikipedia.org/wiki/Point-to-Point_Protocol_over_Ethernet) dropped the HDLC addresses used in PPP frames and started the PPP payload with protocol ID.
* Fibre Channel (FC) designers realized you don't need layer-2 and layer-3 addresses in a single-protocol network and decided to use layer-3 addresses everywhere. That decision confused some FC practitioners to the point where they claimed [FC is switching, not routing](/2011/07/is-fibre-channel-switching-bridging-or/) (whatever the difference is), even though the standard documents are unambiguous.

### Interface and Node Addresses

Now you know why you need link-layer addresses on multi-access links, but do we need network-layer addresses on each interface?

Coming back to the ballroom example: Bob has two ears, but when you want to chat with Bob, you start with "Hey, Bob..."  not with "Hey, Bob's left ear...", or as [@odecentralize put it](https://twitter.com/ODecentralize/status/1389951805757575170): 

> Assigning IP addresses to interfaces is like having people address you by a different name depending on which door they used entering the building.

To reach a node, you need a unique network address per node, not per node's interface, and yet the IP designers went the other way. We'll explore their reasoning in the second part of this series.

{{<figure src="/2021/05/Addr-ifaddr.png" caption="An IP node has to use a different IP address on every interface">}}

{{<figure src="/2021/05/Addr-CLNS.png" caption="A CLNS node has a single address, regardless of how many interfaces it has">}}

It's worth noting that the "address-per-node" paradigm is not gone even in the world of IP/Ethernet. You'll find it in Ethernet bridging (bridges have a single node-wide MAC address), and we commonly use loopback IP interfaces when we want to make an IP address of a multi-interface IP device (often known as a router) stable.

### More to Explore

If you find this blog post interesting (or you wouldn't get this far), you might like the [Network Addressing](https://my.ipspace.net/bin/list?id=Net101#ADDR) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.

### Revision History

2021-05-05
: Added a tweet by @odecentralize
