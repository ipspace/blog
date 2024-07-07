---
title: "Relationships between Layer-2 (VLAN) and Layer-3 (Subnet) Segments"
date: 2023-01-19 07:23:00
tags: [ networking fundamentals ]
---
Sometimes it takes me years to answer interesting questions, like the one [I got in a tweet in 2021](https://twitter.com/webernetz/status/1450559574927364097):

> Do you have a good article describing the one-to-one relation of layer-2 and layer-3 networks? Why should every VLAN contain one single L3 segment?

There is no mandatory relationship between multi-access layer-2 networks and layer-3 segments, and secondary IP addresses (and subnets) were available in Cisco IOS in early 1990s. The rules-of-thumb[^BCP] claiming there should be a 1:1 relationship usually derive from the oft-forgotten underlying requirements. Let's start with those.
<!--more-->
### The Basics

When you have a layer-3 host attached to a multi-access layer-2 network, that host has to:
[^BCP]: Often called _best current practices_

* Figure out which other layer-3 nodes are connected to the same segment so it can send the packets to them directly without going through an intermediate device.
* Find out the layer-2 addresses of directly connected layer-3 nodes so it knows what to use as the destination layer-2 address in outgoing layer-2 frames.
* Have a mechanism to find the next hop for destinations that are not directly connected.

Numerous solutions to these challenges have been developed in the past, including:

{{<explain term="CLNS">}}
* Nodes have a [single layer-3 address](/2010/12/clnp-and-multihoming-myths/) (NSAP).
* There are no [interface layer-3 addresses](/2015/10/was-clnp-really-broken/) or subnets.
* Directly connected nodes are discovered through end-system hellos (ESH) and intermediate-system hellos (ISH).
* NSAP-to-layer-2 mappings are built from ESH/ISH information.
* Routers advertise their presence with ISHs, hosts use one of the directly-attached routers to forward traffic to all nodes that are not directly connected (the host received no ESH from that node)
{{</explain>}}
{{<explain term="IPv4">}}
* Interfaces have IPv4 addresses and subnet masks.
* Interface IPv4 address and subnet mask are used to figure out whether a destination IPv4 address is directly connected. Do a bitwise AND of subnet mask and source/destination IPv4 addresses. Destination is in the same subnet if the results are the same.
* You can configure static routes pointing to an interface (without the next hop) to fake further directly-connected subnets. Some of us were stupid enough to [do that with a default route](/2009/10/my-stupid-moments-interface-default/), making the whole Internet directly connected. [What could possibly go wrong](/2009/10/follow-up-interface-default-route/)?
* Once the host decides a destination IPv4 address is directly connected, it uses ARP to find its MAC address.
* Static routes (manually configured or derived from DHCP) are used for off-subnet forwarding. There is no standard mechanism to find the first-hop router.
{{</explain>}}
{{<explain term="IPv6">}}
* Interfaces have IPv6 addresses and prefix lengths. Prefix length is assumed to be /64; it can be changed via RA messages or static configuration.
* Like in IPv4, IPv6 addresses and prefix lengths of statically configured interface addresses are used to figure out whether a destination IPv6 address is directly connected.
* Prefixes included in IPv6 Router Advertisement messages are [considered to be directly connected](/2012/11/ipv6-on-link-determination-what-is-it/) only if they have the on-link flag set.
* IPv6 Neighbor Discovery is used to find the layer-2 address of directly-connected IPv6 nodes.
* Router advertisement messages are [used to find the first-hop router](/2011/02/dhcpv6slaacra-dhcpv4/).

**Notes**
* It's [perfectly possible to tell a host to create an auto-configured IPv6 address in an IPv6 subnet that has no other directly-connected nodes](/2012/11/ipv6-router-advertisements-deep-dive/) -- set the A flag to one and L flag to zero.
* I'm positive I missed at least one intricate mechanism hidden deep inside DHCPv6 options. Your comments would be highly appreciated.
{{</explain>}}

For even more information, watch the [network addressing videos](https://my.ipspace.net/bin/list?id=Net101#ADDR) from _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar (available with [free subscription](https://www.ipspace.net/Subscription/Free)).

### Back to Best Practices

Now that you know what's going on behind the scenes, it's easy to figure out the reason for the 1:1 subnet-to-VLAN "_best practice_":

* If you have a single subnet stretched across multiple VLANs, hosts can't reach each other because ARP/ND messages don't cross VLAN boundaries. Obviously you can fix this one with proxy ARP/ND[^JS] or LISP[^LISP].
* If you have multiple subnets on a single VLAN, then (in the IPv4 world) the hosts have to send traffic to other hosts on the same VLAN through a router. Not a big deal if the router happens to be the core switch with linerate hardware L3 forwarding, but a major nuisance if the router is an overwhelmed underpowered device attached to the edge of the VLAN.

Having multiple IPv6 subnets per VLAN is easier. You can fix suboptimal packet forwarding with carefully-crafted RA messages, but as you probably won't have more than a gazillion hosts per subnet[^64], it might be a better idea to keep things simple.

[^JS]: ... resulting in eternal appreciation of your coworkers who have to troubleshoot that monstrosity, and a permanent job security unless someone is smart enough to fire you before you manage to implement it.

[^LISP]: There's absolutely nothing you cannot fix with LISP (or NAT). SRv6 supposedly has similar magic properties.

[^64]: 18446744073709551614 if you want to be more precise.