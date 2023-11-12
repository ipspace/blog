---
date: 2013-07-18 07:40:00+02:00
tags:
- IPv6
- security
- LAN
title: First-Hop IPv6 Security Features in Cisco IOS
url: /2013/07/first-hop-ipv6-security-features-in.html
---
I wanted to figure out how to use IPv6 DAD proxy in PVLAN environments during my seaside vacations, and as I had no regular Internet access decided to download the whole set of IPv6 configuration guides while enjoying the morning cup of coffee in an Internet café. Opening the [IPv6 First-Hop Security Configuration Guide](http://www.cisco.com/en/US/docs/ios-xml/ios/ipv6_fhsec/configuration/xe-3s/ip6f-xe-3s-book.pdf) was one of the most pleasant (professional) surprises I had recently.

One word summary: Awesome.
<!--more-->
Cisco IOS has (at least) these IPv6 first-hop security features:

**IPv6 RA Guard** rejects fake RA messages coming from host (non-router) ports (not sure whether it handles all possible IPv6 header fragmentation attacks). Interestingly, it can also validate the contents of RA messages (configuration flags, list of prefixes) received through router-facing ports, potentially giving you a safeguard against an attack of fat fingers.

**DHCPv6 Guard** blocks DHCPv6 messages coming from unauthorized DHCPv6 servers and relays. Like IPv6 RA Guard it also validates the DHCPv6 replies coming from authorized DHCPv6 servers, potentially providing protection against DHCPv6 server misconfiguration.

**IPv6 Snooping and device tracking** builds a IPv6 First-Hop Security Binding Table (nicer name for ND table) by monitoring DHCPv6 and ND messages as well as regular IPv6 traffic. The binding table can be used to stop ND spoofing (in IPv4 world we'd call this feature DHCP Snooping and Dynamic ARP Inspection).

**IPv6 Source Guard** uses the IPv6 First-Hop Security Binding Table to drop traffic from unknown sources or bogus IPv6 addresses not in the binding table. The switch also tries to recover from lost address information, querying DHCPv6 server or using IPv6 neighbor discovery to verify the source IPv6 address after dropping the offending packet(s).

**IPv6 Prefix Guard** is denies illegal off-subnet traffic. It uses information gleaned from RA messages and IA_PD option of DHCPv6 replies (delegated prefixes) to build the table of valid prefixes.

IPv6 Prefix Guard is a layer-2 feature. You should use uRPF check on layer-3 interfaces.

**IPv6 Destination Guard** drops IPv6 traffic sent to directly connected destination addresses not in IPv6 First-Hop Security Binding Table, effectively stopping ND exhaustion attacks.

**Summary:** Cisco IOS seems to be the networking software with the most comprehensive set of IPv6 first-hop security features. As always, some features might not be available on some platforms -- use feature navigator to figure out which features your IPv6-capable switches support.

### Related Webinars

You'll find more about IPv6 first-hop security requirements and features in the [IPv6 Security](http://www.ipspace.net/IPv6_security) webinar (also available as part of the [yearly subscription](http://www.ipspace.net/Subscription)). In that webinar, Eric Vyncke described individual Cisco IOS security features. The videos of his presentation are freely available.