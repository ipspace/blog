---
date: 2011-02-01 07:02:00+01:00
multihoming_tag: ipv6
series:
- multihoming
tags:
- IPv6
title: IPv6 Provider Independent Addresses
url: /2011/02/ipv6-provider-independent-addresses.html
---
If you want your network to remain multihomed when the Internet migrates to IPv6, you need your own Provider Independent (PI) IPv6 prefix. That's old news (I was [writing about the multihoming elephant almost two years ago](/2009/05/lack-of-ipv6-multihoming-elephant-in.html)), but most of the IT industry managed to look the other way pretending the problem does not exist. It was always very clear that the lack of other multihoming mechanisms will result in explosion of global IPv6 routing tables (attendees of my [Upcoming Internet Challenges](https://www.ipspace.net/InternetChallenges) webinar probably remember the topic very well, as it was one of my focal points) and yet nothing was done about it (apart from the LISP development efforts, which will still take a while before being globally deployed).

To make matters worse, some Service Providers behave like the model citizens in the IPv6 world and filter prefixes longer than /32 when they belong to the Provider Assigned (PA) address space, which means that you cannot implement reliable multihoming at all if you don't get a chunk of PI address space.
<!--more-->
I was always focusing on the technical aspects of the problem; Greg Ferro added the business aspects in his [The Importance of Provider Independent IPv6 Addressing](http://etherealmind.com/importance-provider-independent-ipv6-addresses/) post. Characteristically, he was unable to resist another Service Provider-focused rant, triggering a knee-jerk response from Russell Heilling (which resulted in [another great post on the same topic](http://perlmonkey.blogspot.com/2011/01/fear-and-loathing-in-ipv6.html), this time from the Service Provider perspective).

Anyhow, things are not as easy as Greg would like them to be. You have to satisfy certain requirements to get PI IPv6 prefix and while I'm positive Greg's customer will always be in that group, smaller organizations that used NAT-based multihoming today [will be left in the dark in the IPv6 world](/2010/12/small-site-multihoming-in-ipv6-mission.html)... and there is no good answer we could give them apart from "Use ULA addresses internally to reduce the eventual renumbering pain."

{{<note warn>}}Due to changes to source IPv6 address selection algorithms made after this blog post was written in 2011, it's [impossible to use ULA addresses](/2022/05/ipv6-ula-made-useless.html) in dual-stack networks.{{</note>}}

### More Information

To learn more about early IPv6 pitfalls and the first steps you have to take to prepare for the brave new world, watch the [Enteprise IPv6 -- the First Steps](https://www.ipspace.net/EnterpriseIPv6) webinar.

### Revision History

2023-03-10
: Added a note about ULA uselessness
