---
date: 2008-05-17 07:23:00+02:00
tags:
- DNS
- IP routing
- training
title: Using IP Prefixes, AS Numbers and Domain Names in Examples
url: /2008/05/private-domain-names.html
lastmod: 2020-12-28 07:47:00
---
**Keep in mind**: Use private IP addresses, AS numbers and domain names in all technical documentation you\'re producing (unless, of course, you\'re describing an actual network). If you\'re forced to use public addresses or AS numbers (for example, to illustrate how the neighbor remote-private-as command works), you should clearly state that they are imaginary.

You can safely use:

* [IPv4 prefixes reserved for private use by RFC 1918](http://tools.ietf.org/html/rfc1918)
* IPv6 prefix 2001:DB8::/32 [reserved for documentation in RFC 3849](https://tools.ietf.org/html/rfc3849)
* 2-byte AS numbers [reserved for private use in RFC 1930](http://tools.ietf.org/html/rfc1930)
* 4-byte AS numbers [reserved for private use in RFC 6996](http://tools.ietf.org/html/rfc6996)
* [Reserved domain names documented in RFC 2606](http://tools.ietf.org/html/rfc2606) including **example.com**
