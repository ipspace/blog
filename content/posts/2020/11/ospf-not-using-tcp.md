---
title: "Why Is OSPF not Using TCP?"
date: 2020-11-18 07:53:00
tags: [ OSPF, IP routing, networking fundamentals ]
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

Then there might have been other considerations, including:

**TCP was considered an overkill**. After all, TCP provided decent reliable end-to-end transport under a variety of conditions while all we need in OSPF is a single-hop quick fix.

**TCP was considered to be a resource hog** by people writing networking code. I never understood this one, as it persisted long after WWW took off for real.

**CPU cycles were precious in early routers**, as they used the same CPU for control-plane activities and packet forwarding. Networking vendors cutting costs and using the cheapest CPU they could get away with didn't help either. Keep in mind that running an [O(|E| + |V|.log(|V|)) algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) on a graph with hundred nodes was considered to be a big deal in those days.

**Networking is special**. We couldn't simply reuse a protocol that works. We have to invent something _more optimal_ (leading to tons of protocols with unique binary encodings instead of everyone using the same markup language). [Lack of understanding of what _presentation layer_ should provide](https://blog.ipspace.net/2019/09/response-osi-model-is-lie.html) didn't help either (considering the alternative could be ASN.1 maybe I shouldn't complain too much).

Have I missed anything? Got it all wrong? Please write a comment or [send me an email](https://www.ipspace.net/Contact#Tech).