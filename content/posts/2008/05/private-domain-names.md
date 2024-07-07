---
date: 2008-05-17 07:23:00+02:00
tags:
- DNS
- IP routing
- training
title: Using IP Prefixes, AS Numbers and Domain Names in Examples
url: /2008/05/private-domain-names/
lastmod: 2021-01-05 07:47:00
---
**Keep in mind**: Use private IP addresses, AS numbers and domain names in all technical documentation you\'re producing (unless, of course, you\'re describing an actual network). If you\'re forced to use public addresses or AS numbers (for example, to illustrate how the neighbor remote-private-as command works), you should clearly state that they are imaginary.

You can safely use:
<!--more-->

**IPv4**
* [IPv4 prefixes reserved for private use by RFC 1918](http://tools.ietf.org/html/rfc1918)
* [Documentation IPv4 prefixes reserved in RFC 5737](https://tools.ietf.org/html/rfc5737)\
(192.0.2.0/24, 198.51.100.0/24 and 203.0.113.0/24)

**IPv6**
* IPv6 prefix 2001:DB8::/32 [reserved for documentation in RFC 3849](https://tools.ietf.org/html/rfc3849)

**2-byte ASN**
* 2-byte AS numbers [reserved for documentation in RFC 5398](https://tools.ietf.org/html/rfc5398) (64496 -- 64511)
* 2-byte AS numbers [reserved for private use in RFC 1930](http://tools.ietf.org/html/rfc1930)

**4-byte ASN**
* 4-byte AS numbers [reserved for documentation in RFC 5398](https://tools.ietf.org/html/rfc5398) (65536 - 65551)
* 4-byte AS numbers [reserved for private use in RFC 6996](http://tools.ietf.org/html/rfc6996)

**Domain names**
* [Reserved domain names documented in RFC 2606](http://tools.ietf.org/html/rfc2606) including **example.com**

### Revision History

2020-12-28
: Cleaned up the blog post as part of winter 2020 cleaning. Added IP IPv6 documentation prefix.

2021-01-05
: Added documentation IPv4 prefixes, 2-byte ASN and 4-byte ASN (RFC 5737, RFC 5398) suggested in comment by Charles Monson.