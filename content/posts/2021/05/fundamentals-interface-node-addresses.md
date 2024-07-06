---
date: 2021-05-12 06:59:00+00:00
series:
- unnumbered-interfaces
tags:
- IP routing
- bridging
- networking fundamentals
title: 'Back to Basics: The History of IP Interface Addresses'
---
In the [previous blog post](/2021/05/fundamentals-need-interface-addresses.html) in [this series](/series/unnumbered-interfaces.html), we figured out that you might not need link-layer addresses on point-to-point links. We also started exploring whether you need network-layer addresses on individual interfaces but didn't get very far. We'll fix that today and discover the secrets behind IP address-per-interface design.

In the early days of computer networking, there were three common addressing paradigms:
<!--more-->
* Companies building large-scale networks connecting mainframes or minicomputers (IBM and DEC) realized you need a unique network-wide identifier per node, not per interface. After all, you want to connect to the services running on a node, and nobody (apart from the network administrator) cares about individual node interfaces.

{{<figure src="/2021/05/Addr-Nodes.png" caption="Assign network addresses to nodes, not links">}}

* Companies building LAN-based client-server networks (AppleTalk, Novell Netware...)[^2] didn't care about the distinction between node- and interface addresses. The devices connected to their networks had at most one interface anyway.[^1]

{{<figure src="/2021/05/Addr-Interfaces.png" caption="Keep things simple: assign network addresses to interfaces">}}

[^1]: Netware servers were an exception, but Novell engineers realized that too late and had to settle for the same loopback interface hack we use in IP networks today.

[^2]: Lovingly called *desktop protocols* by Cisco TAC.

* Anything mentally based on the phone network paradigm assigned addresses to switch ports, and the nodes attached to the network had to use the address of the connected switch port, or they wouldn't receive any traffic. You could say that the switches used static host routing, with a host route pointing to every edge port.

Where does IP fit into this picture, and how did we get to interface addresses where it would be much better for IP routers and multihomed hosts to use node addresses?

You have to remember that IP didn't start as a network protocol. IP stood for Internetworking Protocol and was designed by a bunch of academics trying to make sense of an underlying network built by BBN (see [BBN Report 1822](https://walden-family.com/impcode/BBN1822_Jan1976.pdf) for the details). IP addresses were statically assigned to the ports of the [Interface Message Processor](https://en.wikipedia.org/wiki/Interface_Message_Processor), with part of the original IP address being the IMP identifier and the second part being the port number on the IMP[^3].

[^3]: SAN geeks might realize that Fibre Channel still uses the same approach.

{{<figure src="/2021/05/IMP-Nutshell.png" caption="An IMP in a nutshell">}}

Deciding to use interface-scoped network addresses when designing a protocol to fit that environment was an obvious choice. After all, if a host connected to two IMP ports, it had to use two IP addresses, and who would want to burn two IMP ports anyway.

Eventually, the IP networks got extended to Ethernet segments. The gateways between the original BBN network and the LAN network had to use two IP addresses - one for the BBN part and another for the LAN part. When subnets were introduced to split LAN networks into smaller routable bits, the architecture was already cast in stone.

{{<figure src="/2021/05/Addr-Per-Link-Prefix.png" caption="Let's use per-link prefixes to make our lives simpler">}}

IPv6 was another missed opportunity. The difference between node-level addresses and interface-level network addresses was well understood at that time. DEC's experience with building large-scale WAN and LAN networks influenced the OSI CLNP protocol design; CLNP was consequently using node-level addresses. There were even ideas to [use CLNP as the basis for next-generation IP](/2010/09/ipv6-experts-strike-again.html). Still, following a grassroots revolt[^5], IAB decided to start from scratch. The "*we always did things this way*" mentality quickly kicked in together with a copious amount of [Second System Effect](https://en.wikipedia.org/wiki/Second-system_effect).

Does that mean that it would be better to use a CLNP-like design with node-level network addresses? Not necessarily:

* [Node-level network addresses are harder to summarize](/2015/10/was-clnp-really-broken.html). In IP networks, routers have to know about subnets and directly connected nodes. In CLNP networks, routers have to know about all nodes in an area.
* Regardless of what some academics claim, [node-level addresses wouldn't solve the multihoming problem](/2010/12/clnp-and-multihoming-myths.html). They would get rid of the loopback interface hack and resolve the [local multihoming issue](/2019/10/saved-tcp-is-most-expensive-part-of.html) (node connected to the network with two or more interfaces) for good... but it's impossible to solve the challenge of nodes connected to multiple networks (example: WiFi and LTE, or two upstream ISPs) without a [proper session-layer protocol](/2009/08/what-went-wrong-tcpip-lacks-session.html).

However, it still doesn't make sense to be forced to use an IP subnet for every point-to-point router-to-router[^4] link. Welcome to the mysterious world of unnumbered IP interfaces -- the topic of the next blog post in this series.

### More to Explore

Why don't you watch the [Network Addressing](https://my.ipspace.net/bin/list?id=Net101#ADDR) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar to get even more details?

[^4]: People believing in [vague marketese](/2011/02/how-did-we-ever-get-into-this-switching.html) are free to replace that with a switch-to-switch link.

[^5]: You might find a few hints about that event in the hilarious [Elements of Networking Style](https://www.amazon.com/Elements-Networking-Style-Animadversions-Intercomputer/dp/0595088791) book.
