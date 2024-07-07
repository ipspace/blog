---
title: "The BGP Origin Attribute"
date: 2023-12-04 07:02:00
tags: [ BGP ]
---
[Kristijan Taskovski](https://www.linkedin.com/in/kristijan-taskovski/) asked an interesting question related to my [BGP AS-prepending lab](https://bgplabs.net/policy/7-prepend/): 

> I've never personally done this on the net but....wouldn't the BGP origin code also work with moving one's ingress traffic similarly to AS PATH?

**TL&DR**: Sort of, but not exactly. Also, just because you can climb up ropes using shoelaces instead of [jumars](https://en.wikipedia.org/wiki/Ascender_(climbing)) doesn't mean you should.

Let's deal with the *moving traffic* bit first.
<!--more-->
According to [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271.html#section-9.1.2.2), the length of the AS path is compared before the origin code, which makes AS path length a more decisive metric. It's pretty rare for an adjacent autonomous system to have different paths to your network with the same AS path length unless you have parallel links into that AS, in which case you could [easily use MED](/2023/11/bgp-labs-multi-exit-discriminator/).

Origin attribute does have an advantage over the MED attribute, though: it's a mandatory attribute (and thus always present), avoiding the *[how should we compare missing values](/2023/11/bgp-med-saga/)* drama. Its disadvantage: it only has three values.

### A Bit of History

Now for the fun part: what exactly is the ORIGIN attribute?

In the times of [The Two Napkins](https://computerhistory.org/blog/the-two-napkin-protocol/), [BGP](https://www.rfc-editor.org/rfc/rfc1105) had to interact with its predecessor -- the [Exterior Gateway Protocol (EGP)](https://datatracker.ietf.org/doc/html/rfc827) -- and exchange routing information with it (today we'd call that two-way route redistribution). Using two routing protocols to perform the same functionality is always a big mess, and BGP tried to address the *quality of routing information* part of it with the ORIGIN attribute that has these values:

* **IGP** (best) -- prefix is interior to the originating AS.  Routers usually set the ORIGIN to IGP when originating prefixes configured with **network** statements (as in: we know what we're doing).
* **EGP** -- prefix came from EGP. That's not as good as an interior prefix, but it's still OK. However, if you see EGP origin in the global BGP table today, that's probably someone being too creative.
* **INCOMPLETE** (worst) -- we have no idea how the prefix appeared in the BGP table. Routers usually set INCOMPLETE origin on prefixes redistributed from other routing protocols unless you apply a route-map setting **origin** to **igp** to the **redistribute** command.

**Long story short**: BGP ORIGIN is like junk DNA. It's there but leave it alone unless the '?' at the end of the AS path bothers you. If it does, use a route map when redistributing routes into BGP[^PL].

[^PL]: ... and if you decide to do that, do yourself a favor and add a prefix list to the route map to ensure only the expected routes get into the BGP table.
