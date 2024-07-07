---
date: 2012-11-21 07:11:00+01:00
tags:
- IPv6
- security
title: IPv6 Router Advertisements Deep Dive
url: /2012/11/ipv6-router-advertisements-deep-dive/
---
I'm constantly getting questions about the intricate interworking of various flags present in IPv6 Router Advertisement messages. Here's a (hopefully comprehensive) summary taken primarily from [RFC 4861](http://tools.ietf.org/html/rfc4861).
<!--more-->
### A Bit of the Theory

Router advertisement (RA) message include numerous flags. The M and O flags are [always present](http://tools.ietf.org/html/rfc4861#section-4.4):

-   **M -- Managed Address Configuration**. DHCPv6 is available for IPv6 address allocation.
-   **O -- Other Configuration**. Other configuration information (ex: DNS server IPv6 address) is available through DHCPv6.

RA messages may include [prefix information](http://tools.ietf.org/html/rfc4861#section-4.6.2). Each prefix has L and A flags:

-   **L -- On-Link Flag**. The prefix can be used for [on-link determination](http://tools.ietf.org/html/rfc5942) (IPv6 addresses within that prefix are on the same L2 subnet).
-   **A -- Address Configuration Flag**. The prefix can be used for [stateless address configuration (SLAAC)](http://tools.ietf.org/html/rfc4862).

### Default Behavior: SLAAC

The most common IPv6 address allocation mechanism is SLAAC. If you want the hosts to use SLAAC, the routers MUST include one or more prefixes with A flag set in their RA messages.

The RA messages SHOULD have the O flag set to prompt the end hosts to use DHCPv6 to get DNS server IPv6 address, or you have to use RA RDNSS option ([RFC 6106](http://tools.ietf.org/html/rfc6106) -- [check whether it's supported on your operating system](https://en.wikipedia.org/wiki/Comparison_of_IPv6_support_in_operating_systems)).

### Enforcing DHCPv6-only Address Assignment

Setting the M flag in RA messages is not enough to enforce IPv6 address assignment through DHCPv6. Some hosts (example: Windows 7) will use DHCPv6 to get an IPv6 address, but also create a pseudo-random IPv6 address using [SLAAC privacy extensions (RFC 4941)](http://tools.ietf.org/html/rfc4941), and prefer the SLAAC-generated address.

You MUST clear the A flag in the prefixes advertised by the router to enforce DHCPv6-only address assignment.

{{<note warn>}}Removing the on-link prefix from the RA messages will stop SLAAC, but also enforce PVLAN-like traffic flow.{{</note>}}

### Enforcing PVLAN-like Traffic Flow

You can use the [on-link determination functionality](http://tools.ietf.org/html/rfc5942) to force local host-to-host traffic through the first-hop router. IPv6 hosts use RA messages to discover on-link prefixes: all prefixes advertised in RA messages with L bit set are in the same layer-2 domain.

{{<note info>}}Advertising multiple IPv6 prefixes with the L bit set can also be used to send direct traffic between IPv6 hosts in different IPv6 subnets configured on the same layer-2 segment.{{</note>}}

To force the local host-to-host traffic through the first-hop router, clear the L flag or remove the on-link prefix from RA messages. Hosts can still use SLAAC (if the A flag is set) or DHCPv6 (if the M flag is set); the L flag affects the traffic flow, not the address assignment process.

{{<note warn>}}The L flag is not a security measure; hosts can use local IPv6 configuration to bypass the information sent in the RA messages.{{</note>}}

### More RA/SLAAC/DHCPv6 Gotchas (Courtesy of Tore Anderson):

Tore Anderson listed numerous other gotchas in his comment (thank you!). The italicized comments are mine.

-   The O flag is meaningless if the M flag is set, as the O flag is basically a subset of the M flag (*broken OS stack might require both though*);
-   When it comes to DNS server assignment, there are OS-es that only support DHCPv6 (for example, many Windows versions), and there are some that only support the RDNSS Option (for example, Mac OS X 10.6.x). Therefore, for maximum host compatibility, I recommend using both simultaneously (*assuming your switch/router supports RDNSS*).
-   A prefix information option with both A and L flags unset is meaningless and might as well be removed.
-   SLAAC can only occur for prefixes with a length of 64, so setting the A flag for other prefix lengths is meaningless. The L flag, on the other hand, works for any prefix length.
-   DHCPv6 does not carry prefix length information, so a prefix information option with L=1 is the **only** way a host may acquire an on-link route.
-   Receipt of a RA (with lifetime \> 0) will cause the host to install a default route to the RA's source address. This is the **only** way to advertise a default route in IPv6 (on Ethernet at least), as DHCPv6 cannot carry this information. Furthermore, the RA is guaranteed to come from a link-local address (within fe80::/64), which is crucial in making off-link prefixes work.

### Revision History

2012-11-21
: Reworded some sections based on feedback from Tore Anderson and copied his list of gotchas into the blog post.

### More information

You'll find detailed description of RA and DHCPv6 functionality, design recommendations and router configurations in the [Building Large IPv6 Service Provider Networks](http://www.ipspace.net/Building_Large_IPv6_Service_Provider_Networks) webinar (part of [yearly subscription](http://www.ipspace.net/Subscription)).
