---
date: 2011-12-20 07:01:00+01:00
tags:
- firewall
- security
- NAT
title: Is NAT a Security Feature?
url: /2011/12/is-nat-security-feature/
---
15 years after NAT was invented, I'm still getting questions along the lines of "is NAT a security feature?" **Short answer: NO!**

**Longer answer:** NAT has some side effects that resemble security mechanisms commonly used at the network edge. That does NOT make it a security feature, more so as there are so many variants of NAT.
<!--more-->
### Basic NAT

Basic NAT (as defined in [RFC 2663](http://tools.ietf.org/html/rfc2663)) performs just the IP address translation (one inside host to one IP address in the NAT pool). The moment the inside host starts a session through the NAT, it becomes fully exposed to the outside world.

When using static basic NAT (statically defined inside-to-outside IP address mapping), the inside host is exposed all the time.

**Summary:** Basic NAT provides no security.

### Stateless NAT

Some IPv6-to-IPv4 (or 4-to-6) NAT algorithms are *stateless* -- IPv6 address is calculated from the IPv4 using an algorithm (or device configuration). From the security standpoint, stateless NAT is no different from static basic NAT (read: useless).

### Network Address Port Translation (NAPT)

NAPT (also known as PAT) keeps a list of established sessions and uses that list to perform address and port translation of inbound and outbound packets. If an unknown packet arrives from the inside interface, a new entry is created, if an unknown packet arrives from the outside interface, it's dropped.

There is no "standard" NAPT behavior. [RFC 4787](http://tools.ietf.org/html/rfc4787) describes various NAPT parameters; the ones most important to the security-related discussion are the [*Address and Port Mapping* behaviors](http://tools.ietf.org/html/rfc4787#section-4.1).

With the *Endpoint independent mapping*, the NAT translation table contains just the inside IP address and TCP/UDP port (default behavior on most low-end devices). As soon as the inside host opens a session through NAT, anyone can send TCP or UDP packets to the source port used by that host.

Cisco IOS usually implements *Address and Port-Dependent Mapping* -- the NAT translation table contains full 5-tuple (source/destination address/port and the L4 protocol).

NAPT device using *address and port-dependent mapping* seems to behave like a stateful firewall, but does not inspect the contents of the TCP/UDP session and does not check the validity of TCP headers. Its behavior is almost identical to [reflexive ACL feature](http://www.cisco.com/en/US/docs/ios/sec_data_plane/configuration/guide/sec_cfg_ip_filter_ps10591_TSD_Products_Configuration_Guide_Chapter.html).

**Summary**: NAPT does provide some packet filtering functionality. Static NAPT is identical to a simple packet filter (whatever is translated by the static NAPT rules is permitted).

### Other Considerations

While we definitely need firewalls and/or packet filters at the network edge, most of today's attacks work on application-layer, using SQL injection or "Advanced Persistent Threats" like sending an Excel or PDF file with a 0-day exploit to a [click-happy user](http://packetpushers.net/the-clicky-clickety-click-ring-tone/).

Finally, I will not discuss the absurdity of the security-by-obscurity argument (*Let\'s secure the network by hiding internal addresses with NAT*). Please don't even mention it in the comments.
