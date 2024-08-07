---
date: 2017-02-16 09:12:00+01:00
ospf_tag: fa
tags:
- OSPF
title: More Thoughts on OSPF Forwarding Address
url: /2017/02/more-thoughts-on-ospf-forwarding-address/
---
[Angelos Vassiliou](https://leanpub.com/unofficialcciev51sg) sent me an interesting lengthy email after I published my OSPF Forwarding Address series ([part 1](/2017/01/ospf-forwarding-address-yet-another/), [part 2](/2017/01/ospf-forwarding-address-yak-take-2/), [part 3](/2017/02/why-ospf-needs-forwarding-address-with/), [part 4](/2017/02/the-unintended-consequences-of-nssa/)). I asked him whether it's OK to publish his email together with my responses as a blog post and he gracefully agreed, so here it is.
<!--more-->
He started with:

> You call the \"Forwarding Address\" of OSPF a kludge. I don\'t know what the definition of a kludge is, but the FA feature was implemented in OSPF for the same reasons that Areas, stub Areas, LSA throttling and many other convolutions were added to OSPF.

That one's easy ;) Kludge (noun): an ill-assorted collection of parts assembled to fulfil a particular purpose.

Here are the reasons Angelos listed:

> Low-end routers in 1998 had little memory, so Moy wanted to squeeze out all \"redundant\" and/or unnecessary information from within the LSDB

Somewhat agree, but I wouldn't necessarily use OSPF on low-end routers (see below).

In my opinion (that hasn't changed in the last 20+ years) people working on OSPF went too far too many times while trying to hammer their square peg into yet another round hole. One of the skills of an *engineer* should be to select the best tool for the job, not to try to make a single tool suitable for every job out there.

OSPF (or IS-IS) is a great tool if you need a fast-reacting IGP for the network core. BGP is the right tool if you have to carry many prefixes or have to implement routing policies. RIPv2 is ideal for remote sites with one or two uplinks. Trying to make OSPF fit all three scenarios resulted in complexity we have today.

On a tangential note: I've been telling people the same thing since at least mid-1990s as was everyone else with long enough experience in building scalable IP network. Other people tried to make their tool fit every single use case, or build country-wide networks using bridging-over-ATM (yes, it went down in flames) or extend ATM virtual circuits to the desktop (no, of course it didn't scale).

Unfortunately, nothing ever changes in IT. Today I see people trying to use LISP to solve every problem ever encountered by the mankind, or inventing ever-more-complex technologies to extend the virtual thick yellow cable across a continent.

> Links were much slower and more expensive (the main reason for Demand Circuit functionality) and the fewer LSAs were on the wire, the better.

No. Demand circuits appeared way later when we already had "reasonable" links. There were two reasons for introduction of demand circuits:

-   Dial-up lines (example: ISDN) where the call was kept active due to OSPF hello packets;
-   X.25 circuits where you were billed by the traffic, and OSPF hellos and periodic flooding racked up the bills.

We lived without demand circuits for years and had solutions (floating static routes, for example) that worked reasonably well. The real reason (in my biased opinion, then and now) was to try to adapt the tool-of-choice (OSPF) to environment it was not suited for (ISDN or X.25) instead of using the right tool for the job.

> The topology of the \"OSPF Forwarding Address: Yet another Kludge\" post is not \"the typical scenario for OSPF FA found on the Internet\", but rather it is the exact example from RFC 2328, page 141, Figure 16.

That is true. It is also the only scenario I could find on the Internet when searching for OSPF forwarding address, which tells you a lot about its usefulness.

> The case of having several routers on a shared segment is no longer typical.

It might not be typical in enterprise environment, but that's how most IXPs operate.

> The example that you presented in the \"OSPF Forwarding Address: Yet another Kludge\" post would actually come up if E1 is a router with much more memory and significantly more CPU than E2. In this case, the administrator may realize that either:
>
> -   X1 cannot (or the X1 administrator may not wish to) handle two BGP peerings with the same customer\'s routers.
> -   E2 cannot handle a BGP peering
>
> Then, the administrator would choose to only establish a single peering over the shared segment.

I would argue that in both cases we're still dealing with a broken design that has at least one single point of failure (E1), and that we shouldn't increase the complexity of everyone's life just to handle someone's broken designs (see also: prefix deaggregation in the global Internet).

> Since the restrictions that were present in 1998 are currently not valid, it makes sense that the solutions that were devised in 1998 to overcome such restrictions are no longer necessary in 2017. Actually, implementing solutions that were designed to solve a specific problem to solve another problem for which the solutions were not meant to solve will most probably fail.

While I conceptually agree with the first sentence, the second sentence totally expresses my sentiments about all the features that were bolted on to OSPF, including NSSA and Demand Circuits.

> Cisco decided to implement the FA feature differently than RFC 2328. In particular, Cisco IOS adds some extra requirements for using the next hop\'s FA: the interface used to \_reach\_ the nexthop should not be passive and not be point-to-point nor point-to-multipoint. The only RFC mandated requirement seems to be that the next hop IP address should be known throughout the OSPF domain as an intra-area or as an inter-area network (known via a type 1, 2 or type 3 LSA). I can\'t find this requirement in RFC 2328.

I had the same problem as Angelos -- if someone knows (A) why Cisco decided to implement Forwarding Address behavior the way they did or (B) if other vendors do the same thing, please write a comment.

> Not allowing the externally-facing interface to be configured as a passive interface is the single problem that breaks the design.

Agreed... but it would be really nice to know what made them go this way.

> If we were allowed to advertise the common segment into OSPF without sending out Hellos on our external interface, this would have been a simple problem, with no security concerns.

Disagree. It wouldn't be a security problem, but it would still be broken design. Whether you call that simple or not is debatable ;)

> For ECMP to work though, \_all\_ OSPF routers connected to the segment should run OSPF on the shared segment, most probably also forming adjacencies between themselves, and exchanging all of the OSPF domain\'s topology in clear text with the external router hearing everything. Now \_this\_ is a security concern!

To make it worse, it's quite hard to stop OSPF routers from forming adjacencies with anyone talking OSPF on that same segment (or continuously complaining about key mismatches). OSPF is simply the wrong tool to use on an external segment.

> Regarding the generation of identical type 5 LSAs by two routers, this is clearly stated in RFC 2328, page 141, where this is considered a \"duplication of effort\" and when suppressing an extra LSA into the OSPF domain, \"the size of the link state database would decrease\". Apparently, the duplication of effort was an issue to consider (due to CPU constrains in routers in the 90s) and since memory was at a premium, reducing the size of the LSDB was a priority over redundancy of information. I know that the LSAs were not exactly redundant as they would offer faster fail-over, but still. In the same page 141, RFC 2328 says: ... the LSA originated by the router having the highest OSPF Router ID is used. The router having the lower OSPF Router ID can then flush its LSA.

This is another one of the "using wrong tool for the job" scenarios. They had to implement this workaround due to some people dumping thousands of external routes into an OSPF domain with low-end routers (with too little memory to handle those duplicate LSAs) instead of using BGP to carry the external prefixes.

Also, at the time RFC 2328 was published it was well known how to do scalable network designs using a combination of IGP and BGP.

> Regarding your last post \"Why OSPF Needs Forwarding Address with NSSA Areas\", I have to say I agree with you, and so does Acee Lindem (IETF OSPF WG chair). [He wrote](http://www.ietf.org/mail-archive/web/ospf/current/msg08230.html) "If I were to be designing OSPFv4, I would most likely omit the forwarding address feature (along with virtual links)."

So nice to see it's not just me ;)

> My personal opinion: I believe that everyone should change their design guides to omit Areas, VLs, DC and FAs

Amen.
