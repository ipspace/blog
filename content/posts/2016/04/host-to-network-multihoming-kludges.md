---
date: 2016-04-12 08:49:00+02:00
dcbgp_tag: server
high-availability_tag: multihoming
multihoming_tag: server
series:
- dcbgp
- multihoming
series_weight: 650
tags:
- data center
- BGP
- IP routing
- high availability
title: Host-to-Network Multihoming Kludges
url: /2016/04/host-to-network-multihoming-kludges.html
---
Continuing our [routing-on-hosts](/2016/03/sysadmins-shouldnt-be-involved-with.html) discussions, [Enno Rey](https://twitter.com/Enno_Insinuator) (of the [Troopers](https://www.troopers.de/troopers16/) and [IPv6 security](https://www.insinuator.net/tag/ipv6/) fame) made another interesting remark "*years ago we were so happy when we finally got rid of gated on Solaris*" and I countered with "*there are still people who fondly remember the days of running gated on Solaris*" because it's a nice solution to host-to-network multihoming problem.

{{<note info>}}Quoting RFC1925, "*It's easier to move a problem around than to solve it*" and people have been extremely good at moving this particular problem around for decades.{{</note>}}
<!--more-->
To set the context: imagine a host connected to two or more network edge devices (example: server connected to two ToR switches) and offering a service that has to be reachable from the outside. How do you make it work?

The correct solution is obvious (in hindsight):

-   Assign a different IP address to each interface to get small layer-2 domains (IP subnet is assigned to a single switch) and layer-3 scalability through address summarization;
-   Use session layer to establish a mapping between service names and transport/network addresses.

Unfortunately, this solution was deemed religiously incorrect and so TCP/IP stack still doesn't have a proper session layer.

{{<note info>}}Multipath TCP is a step in the right direction. Unfortunately, while it does provide seamless multipathing it doesn't solve the multihomed service problem.{{</note>}}

Some people decided to solve the problem in the application layer. New age solutions use scale-out application architecture where you don't care about a particular service instance service availability (and subsequently don't need host-to-network multihoming) because there are always multiple instances of the same service. You could also use a nasty kludge like happy eyeballs and simply try all service endpoints advertised via DNS in parallel.

The traditional way of "solving" this problem was to [push it down the stack until it landed in the networking land](/2013/04/this-is-what-makes-networking-so-complex.html), and because people writing server operating systems could get link bonding to work with a hub sitting at their desktop (I'm obviously exaggerating but you get the idea) they expected the same behavior from the network regardless of its underlying topology.

End result: VLANs spanning at least two switches, sometimes even [whole data centers](/2012/05/layer-2-network-is-single-failure.html) (to support VM mobility), resulting in expensive and brittle kludges like layer-2 fabrics or [multi-chassis link aggregation](/2010/10/multi-chassis-link-aggregation-basics.html).

Now imagine you'd use some service advertisement protocol to allow the host to advertise its services even in legacy environments where a service is tied to a fixed IP address.

{{<note>}}Yeah, I know we had that in Novell IPX, and no, don't get me started on SAP chattiness. Too bad the IPv6 people took only the address autoconfiguration idea from IPX and not the other goodies it had.{{</note>}}

Actually, we do have the solution for years - the DNS SRV records. Too bad the application and middleware developers never heard about them.

Trying to solve the problem in the network layer, you could invent a whole new protocol to get the job done, or you could use BGP (because it's widely available and usually works) to [advertise server loopback address to the network](/2016/02/running-bgp-on-servers.html). You could even go a step further and run the latest version of FRR on the Linux server and use unnumbered physical interfaces with adjacent Cumulus Linux switch for truly scalable plug-and-play networking, like Dinesh Dutt described in the [Leaf-and-Spine Fabric Designs](http://www.ipspace.net/Leaf-and-Spine_Fabric_Designs) webinar.

{{<note info>}}Before you write a comment -- I'm well aware I just described ES-IS, another great idea that was deemed religiously incorrect because it was invented by the wrong standards body.{{</note>}}
