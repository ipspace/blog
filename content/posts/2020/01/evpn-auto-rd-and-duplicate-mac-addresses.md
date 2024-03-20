---
date: 2020-01-15 07:56:00+01:00
evpn_tag: details
tags:
- EVPN
title: EVPN Auto-Rd and Duplicate MAC Addresses
url: /2020/01/evpn-auto-rd-and-duplicate-mac-addresses.html
---
Another [EVPN reader question](https://blog.ipspace.net/2019/12/evpn-route-targets-route-distinguishers.html), this time focusing on auto-RD functionality and how it works with duplicate MAC addresses:

> If set to *Auto*, the RD generated for the same VNI across the EVPN switches will be different. If the same route (MAC/IP) is present under different leaves of the same L2VNI, there is no best path selection (since the RD is different), and both will be considered. This is a misconfiguration and shouldn't be allowed. How will the BGP deal with this?

{{<note>}}
If the above sentence sounded like Latin, go through the short EVPN terminology first (and I would suggest watching the [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar).
{{</note>}}
<!--more-->
Let's start with an interesting fact: while we usually had to specify VRF RD values in MPLS/VPN, EVPN standard defined a procedure where RD would be auto-generated from a PE IP address and VLAN ID. That means that *the same MAC address* would appear as two distinct EVPN Type-2 prefixes when coming from two different PE devices. BGP will happily process the two prefixes and tag them for inclusion into the local MAC table... and that's where it gets interesting:

- If an EVPN PE device figures out it has learned the same MAC address locally (through dynamic MAC learning) and through an EVPN BGP update, the observed MAC address duplication might have been caused by a MAC (VM) move. [MAC mobility](https://tools.ietf.org/html/rfc7432#section-15) procedures kick in, and eventually, we're left with a single MAC address.
- In case of true misconfiguration, the MAC mobility procedure goes into an endless loop, and EVPN RFC addresses that [with a duplicate-MAC timer](https://tools.ietf.org/html/rfc7432#section-15.1).

Long story short: BGP has nothing to do with duplicate MAC addresses; it just passes prefixes around the network. The EVPN devices discover duplicate MAC addresses when importing Type-2 EVPN routes into local MAC-VRF tables and try to rectify the situation using MAC mobility procedures defined in RFC 7432.

For more details, watch our [EVPN Technical Deep Dive](https://www.ipspace.net/EVPN_Technical_Deep_Dive) webinar or [go straight to the source](https://tools.ietf.org/html/rfc7432) (RFC 7432).
