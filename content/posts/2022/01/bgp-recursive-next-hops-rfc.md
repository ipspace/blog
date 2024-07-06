---
title: "Recursive BGP Next Hops: an RFC 4271 Quirk"
date: 2022-01-05 07:41:00
tags: [ BGP ]
---
All BGP implementations I've seen so far use *recursive next hop lookup*:

* The next hop in the IP routing table is the BGP next hop advertised in the incoming update
* That next hop is resolved into the actual next hop using one or more recursive lookups into the IP routing table.

Furthermore, all BGP implementations I've seen used multiple recursive next hops (if available) to implement load balancing toward the BGP next hop -- that's how we made [EBGP load balancing work](/2009/03/ebgp-load-balancing-with-multihop-ebgp.html) in Stone Age of networking. 
<!--more-->
Life was good... until [Dmitry Perets](https://www.linkedin.com/in/dmitryperets/) sent me an email with a disturbing question: unless both of us can't read standards anymore, all those implementations violate RFC 4271.

Here's the weird part of Section [5.1.3 of RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271#section-5.1.3) (highlight mine):

> The immediate next-hop address is determined by performing a recursive route lookup operation for the IP address in the NEXT_HOP attribute, using the contents of the Routing Table, **selecting one entry** if multiple entries of equal cost exist.

Interestingly, nothing was said about recursive lookup in RFC 1771 or early drafts of RFC 4271. To make the whole thing even more mysterious, [interim draft versions](https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgp4-13#section-5.1.3) of RFC 4271 contained this text:

> The NEXT_HOP attribute is used by the BGP speaker to determine the actual outbound interface and immediate next-hop address that should be used to forward transit packets to the associated destinations. The immediate next-hop address is determined by performing a recursive route lookup operation for the IP address in the NEXT_HOP attribute using the contents of the Routing Table.

The final text of RFC 4271 first appears in [draft-ietf-idr-bgp4-18](https://datatracker.ietf.org/doc/html/draft-ietf-idr-bgp4-18#section-5.1.3) from October 2002.

Now a plea to my grumpy old readers: if anyone remembers why that change was made, please add a comment.
