---
date: 2018-04-11 10:11:00+02:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
title: 'The Next Chapter in IPv6 Multihoming Saga'
url: /2018/04/new-in-ipv6-next-chapter-in-ipv6/
---
Remember the IPv6 elephant in the room -- the [inability to do small-site multihoming](/2010/12/small-site-multihoming-in-ipv6-mission/) without [NAT (well, NPT66)](/2011/12/we-just-might-need-nat66/)? IPv6 is old enough to buy its own beer, but the elephant is still hogging the room. Tons of ideas have been thrown around in IETF (mostly based on source address selection tricks), but none of that spaghetti [stuck to the wall](https://archive.psg.com/051000.sigcomm-ivtf.pdf).
<!--more-->
A new draft by [Jen Linkova and Massimiliano Stucchi](https://tools.ietf.org/html/draft-ietf-v6ops-conditional-ras-02) tries to solve at least some aspects of this problem with conditional RA functionality: the lifetime of a PA IPv6 prefix is adjusted based on the status of the corresponding uplink.

Interestingly, I was [musing along those same lines in 2010](/2010/12/small-site-multihoming-in-ipv6-mission/) but had to conclude the approach is impractical due to inability to deprecate an IPv6 prefix through RA. The new draft (if widely implemented in routers and hosts, which could take years) could solve that problem, finally resulting in reasonable IPv6 multihoming options.

### New to IPv6?

The [IPv6 webinars on ipSpace.net](http://www.ipspace.net/IPv6) are still pretty relevant (yeah, nothing much has changed in the meantime).
