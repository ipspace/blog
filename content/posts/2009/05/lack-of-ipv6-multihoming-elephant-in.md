---
cdate: 2023-03-10
comment: 'This blog post was written in 2009 when IPv6 traffic in the Internet couldn''t
  be seen on a traffic graph without using logarithmic scale. The situation hasn''t
  improved a bit in more than a decade, and I''m not aware of a single shim6 production-grade
  deployment.

  '
date: 2009-05-12 06:46:00.002000+02:00
high-availability_tag: multihoming
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
- high availability
title: 'Lack of IPv6 Multihoming: the Elephant in the Room?'
url: /2009/05/lack-of-ipv6-multihoming-elephant-in/
---
I have to admit I have no hands-on Service Provider IPv6 experience (but then there are not too many people that can claim they do) and I don't attend RIPE meetings, so I might have a completely wrong impression, but here it is: Is it just my perception or do we really lack any production-grade means of end-user multihoming in IPv6?
<!--more-->
Just to make sure we're on the same page: businesses that care about their continuous presence on the Internet (somewhat close to 100% of large enterprises, I would dare to guess) and use Internet as one of their sales/delivery/support channels usually decide to connect to multiple (at least two) Internet Service Providers. Due to the current state of protocols above layer 3, an end-user that wants true multihoming needs their own chunk of publicly routable IP address space that is advertised to the world via BGP, which would make IPv6 routing tables as bad as their IPv4 counterparts.

The proposed solution to this issue ([shim6](http://www.shim6.org/)) uses unique host identifiers over multiple IPv6 addresses, allowing the end-to-end communication to continue even if IPv6 endpoints change. Great idea, but the [shim6 working group](http://www.ietf.org/html.charters/shim6-charter.html) has not managed to publish a single RFC yet and it looks like [there are no production-grade implementations](http://www.shim6.org/).

I would be delighted if someone could tell me that I've missed something, but from my current perspective, we are years away from being able to deploy high-availability IPv6 public networks that we take for granted in the today's IPv4 Internet.
