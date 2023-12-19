---
date: 2020-11-18 07:53:00+00:00
ospf_tag: details
tags:
- OSPF
- IP routing
- networking fundamentals
title: Why Is OSPF not Using TCP?
---
[A Network Artist](https://duckduckgo.com/?q=a+network+artist&sites=ipspace.net) sent me a long list of OSPF-related questions after watching the *[Routing Protocols](https://my.ipspace.net/bin/list?id=Net101#ROUTING)* section of our *[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)* webinar. Starting with an easy one:

> From historical perspective, any idea why OSPF guys invented their own transport protocol instead of just relying upon TCP?

I wasn't there when OSPF was designed, but I have a few possible explanations. Let's start with the _what functionality should the transport protocol provide_ reasons:
<!--more-->
**TCP has point-to-point sessions**. That's [more than good enough today](https://www.ipspace.net/Data_Center_BGP/) when everything is a ~~router~~ layer-3 switch, but in early days routers were expensive, and it was quite common to have numerous edge routers connected to a shared layer-2 segment. OSPF DR/BDR uses IP multicast to send the same information to all neighbors at once.

**TCP provides a single stream**, whereas OSPF has per-LSA retransmission capabilities. A dropped OSPF LSA does not prevent other LSAs from being sent to a neighbor, a dropped TCP packet stalls the TCP session.

**TCP provides a byte stream**, and expects a higher-layer protocol to provide message boundaries. That's also why a single dropped packet stalls a TCP session -- as there are no message boundaries in the TCP byte stream, TCP cannot deliver out-of-order packets to higher layers.

**Head-of-line blocking**. A corollary of _TCP provides a single stream_. TCP has a hard time delivering urgent messages ahead of the usual chatter. Yes, it has _urgent data_, but that functionality is "somewhat" limited. OSPF could transmit LSAs in any order it wishes (not that I would be aware of any implementation doing so, but at least the functionality is there).

{{<note>}}That's also one of the reasons QUIC replaced TCP in HTTP/3 ([some more details](https://blog.cloudflare.com/http-3-vs-http-2/)).{{</note>}}

There's also **neighbor discovery**: As Enrique Vallejo pointed out in the comments, you still need a multicast-based *hello protocol* to discover adjacent routers if you find it unacceptable to configure them. That doesn't mean you can't use TCP to establish the sessions once the neighbors are discovered -- LDP uses UDP-over-multicast to discover neighbors, and TCP to exchange labels.

Finally, there might have been other considerations, including:

**TCP was considered an overkill**. After all, TCP provided decent reliable end-to-end transport under a variety of conditions while all we needed in OSPF was a single-hop quick fix.

Straight from _OSPF: Anatomy of an Internet Routing Protocol_ by John T. Moy (quote provided by Paul Hare):

> We did not need the reliability of TCP; link-state routing protocols have their own reliability built into the flooding algorithms, and TCP would just get in the way. Also, the ease of applications in UNIX and other operation systems to sent and receive UDP packets was seen by some as a disadvantage; the necessity of gaining OS privileges was seen as providing some small amount of security. The additional small benefits of UDP encapsulation were outweighed by the extra 8 bytes of UDP header overhead that would appear in every protocol packet. So we decided to run OSPF directly over the IP network layer, and we received an assignment of IP protocol number 89 from the IANA

{{<note>}}UNIX applications had to run as _root_ user if they wanted to listen on TCP or UDP port numbers below 1024 for a very long time (since at least [BSD release 4.1c](https://utcc.utoronto.ca/~cks/space/blog/unix/BSDRcmdsAndPrivPorts) in [1981](http://gunkies.org/wiki/4.1_BSD), while [RFC 1247](https://tools.ietf.org/html/rfc1247) was published in July 1991), so I'm considering the security argument of not using UDP  a bit bogus.{{</note>}}

**TCP was considered to be a resource hog** by people writing networking code. I never understood this one, as it persisted long after WWW took off for real.

**CPU cycles were precious in early routers**, as they used the same CPU for control-plane activities and packet forwarding. Networking vendors cutting costs and using the cheapest CPU they could get away with didn't help either. Keep in mind that running an [O(|E| + |V|.log(|V|)) algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) on a graph with hundred nodes was considered to be a big deal in those days.

**Networking is special**. We couldn't simply reuse a protocol that works. We have to invent something _more optimal_ (leading to tons of protocols with unique binary encodings instead of everyone using the same markup language). [Lack of understanding of what _presentation layer_ should provide](https://blog.ipspace.net/2019/09/response-osi-model-is-lie.html) didn't help either (considering the alternative could be ASN.1 maybe I shouldn't complain too much).

### Keep Reading

You MUST read the extensive comments:

* Henk Smit [explaining the efforts](https://blog.ipspace.net/2020/11/ospf-not-using-tcp.html#246) to use [TCP transport with IS-IS](https://tools.ietf.org/html/draft-hsmit-lsr-isis-flooding-over-tcp-00)
* [Tony Przygienda](https://blog.ipspace.net/2018/03/data-center-routing-with-rift-on.html) describing [tons of things that could go wrong](https://blog.ipspace.net/2020/11/ospf-not-using-tcp.html#250) in a transport protocol used by a routing protocol
* Minh Ha [debunking the _TCP is a resource hog_ myth](https://blog.ipspace.net/2020/11/ospf-not-using-tcp.html#251)

I also received pointers to:

* [Experiments with IS-IS flooding](https://www.youtube.com/watch?v=TLa8puyZ_q4&feature=youtu.be&t=1629) by Sarah Chen and Tony Li ([PDF](https://datatracker.ietf.org/meeting/108/materials/slides-108-lsr-04-isisfloodingstudy-00)) from IETF108
* [More tests of IS-IS flooding](https://youtu.be/OmBSdjGkfuI?t=1000) from IETF109

Have I missed anything? Got it all wrong? Please write a comment or [send me an email](https://www.ipspace.net/Contact#Tech).