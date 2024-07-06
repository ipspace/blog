---
date: 2012-11-27 06:38:00+01:00
tags:
- IPv6
title: IPv6 On-Link Determination
subtitle: What Is It And Why Do We Need It?
url: /2012/11/ipv6-on-link-determination-what-is-it.html
---
When an IPv4/IPv6 host wants to send a packet to another host, it has to answer the following simple questions:

-   Can I reach the destination IP address directly (is the destination on the same LAN/subnet)?
-   If not, who will help me forward the packet (who is the first-hop router)?

In IPv4 world, the host can get all the information it needs through DHCP. In IPv6 world, things are way more complex (but also way more *correct* if you're a theoretician).
<!--more-->
{{<note>}}This post is a follow-up to the [IPv6 Router Advertisement Deep Dive](/2012/11/ipv6-router-advertisements-deep-dive.html) post.{{</note>}}

### The Magic of the Subnet Mask

In the IPv4 world, the host gets the answer to the first question with a simple logical AND operation. To figure out if the destination address is in the same subnet, the IPv4 host ANDs its own and the destination IP address with the subnet mask. If (SourceAddr & SubnetMask == DestinationAddr & SubnetMask), the host can send the packet directly to the destination address (assuming it has the destination's MAC address in its ARP cache).

{{<note>}}We'll ignore all the complexities introduced by having multiple interfaces and multiple IP addresses per interface; it's important you get the generic idea.{{</note>}}

If the destination IPv4 address is not in the same subnet, the IPv4 host sends the packet to the first-hop router (sometimes called *default gateway* for historical reasons).

An IPv4 host thus needs two parameters: subnet mask and first-hop router's IPv4 address. Both can be configured manually or passed to the host through DHCP.

Situation is a bit different when an IPv4 host uses PPP. PPP connection assumes subnet mask of 255.255.255.255 (no other host is on the same subnet); the default gateway is replaced with an interface default route (a static route without an IPv4 next hop pointing to an interface).

### The Many Wonders of the IPv6 World

In the IPv6 world, IPv6 hosts have to listen to *router advertisement* (RA) messages sent by the adjacent routers to get the required parameters:

-   Source IPv6 address of an RA message is assumed to be a router. If the lifetime advertised in the RA message is not zero, that router can be used as the first-hop router, and the IPv6 host installs a default route to that IPv6 address.

{{<note>}}Source IPv6 address of an RA message is always a link-local address; the next hop of a default route is thus always a link-local address.{{</note>}}

-   The prefix length of IPv6 prefixes is advertised by the routers in [*prefix information*](http://tools.ietf.org/html/rfc4861#section-4.6.2) option of RA messages.

{{<note warn>}}An IPv6 host MUST listen to RA messages even if it got its IPv6 address through DHCPv6. DHCPv6 cannot be used to send the prefix length or first-hop router information to IPv6 hosts.{{</note>}}

Every router might advertise numerous prefixes in RA messages (IPv6 works perfectly well with numerous IPv6 prefixes on the same LAN/L2 subnet), but only those that have the L bit set can be used for on-link determination.

In the end, an IPv6 host could have information about numerous *on-link* IPv6 prefixes (prefixes that are present on the same LAN/link as the IPv6 host). When a host wants to figure out whether it can send an IPv6 packet directly to the destination address, it has to go through the list of all IPv6 prefixes known to be on the outgoing interface and check whether the destination IPv6 address belongs to one of them. If it does, the packet can be sent directly, otherwise the packet is sent toward the link-local address of one of the routers.

{{<note>}}The host behavior in environments with multiple first-hop routers is "somewhat" undefined and depends on the host's TCP stack.{{</note>}}

### More information

If you want to know more, you MUST read [RFC 5942](http://tools.ietf.org/html/rfc5942) (IPv6 Subnet Model: The Relationship between Links and Subnet Prefixes) and you SHOULD read [RFC 4943](http://tools.ietf.org/html/rfc4943). You might also be interested in how things work in mobile world, in which case read [RFC 6459](http://tools.ietf.org/html/rfc6459) (IPv6 in 3GPP EPS) and [RFC 7066](https://datatracker.ietf.org/doc/html/rfc7066) (IPv6 for 3GPP Cellular Hosts).

Finally (you know I have to mention that) you can watch the [Building Large IPv6 Service Provider Networks](http://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks) webinar (available with [yearly subscription](http://www.ipspace.net/Subscription)).
