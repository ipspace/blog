---
title: "Stop the Network-Based Application Recognition Nonsense"
date: 2024-04-24 08:35:00+0200
tags: [ QoS ]
original_URL: https://www.linkedin.com/messaging/thread/2-MGIzYTc4ZmEtMDhmNy00ZGIwLWI1MWMtYjU0NTZkMmE3MWI3XzAxMg==
---
One of my readers sent me an interesting update on the post-QUIC round of NBAR whack-a-mole (**TL&DR:** everything is better with ~~Bluetooth~~ AI):

{{<long-quote>}}
Cloudflare (and the other hyperscalers) are full into QUIC, as it gives them lots of E2E control, taking a lot of choice away from the service providers on how they handle traffic and congestion. It is quite well [outlined by Geoff Huston in an APNIC podcast](https://blog.apnic.net/2024/02/08/podcast-dns-is-the-new-bgp-how-we-really-route-things-in-the-modern-internet/).
{{</long-quote>}}

So far, so good. However, whenever there's a change, there's an opportunity for marketing FUD, coming from the usual direction.
<!--more-->
{{<long-quote>}}
At the same time, we don't live in a world with infinite bandwidth, and Cisco is looking for ways for ISPs to regain some of that control with the Cisco Ultra Traffic Optimization AI. It is quite well documented in a [Cisco Live talk](https://www.ciscolive.com/c/dam/r/ciscolive/emea/docs/2023/pdf/BRKSPM-2024.pdf).
 
I can see both sides of the challenge here, but I would love to hear your opinion about it in one of your blogs.
{{</long-quote>}}

I always believed that a Service Provider network should be as simple as possible (see also: plumbing)[^ENT]. It should provide each client with its fair share of resources and ignore the rest. Obviously, that's not too hard to implement (apart from the "*What exactly is a client?*" bit and a few other details). 

[^ENT]: Enterprise networks are a completely different story, as the various enterprise policies dictate how the network should behave. Hint: enforcing application visibility is easier if you manage to make it a compliance issue ;)

The *as simple as possible* idea doesn't work well with "premium" vendors, who try to keep their fat margins by persuading everyone how special their networks should be. Service Provider business development folks who dream of increasing ARPU[^ARPU] love those fairy tales. The next thing you know, everyone keeps repeating the "*OMG, we need traffic engineering or bandwidth management[^BM] based on application recognition to fix broken apps*" mantra.

[^ARPU]: Average Revenue Per User

[^BM]: A fancier way of saying "QoS", potentially safe to use even in environments that have realized how much hard work goes into deploying and operating QoS policies.

Ignoring the marketing gimmicks, why might we care about recognizing applications? Back to my reader...

{{<long-quote>}}
The problem is that we can't identify individual applications anymore with QUIC. It all looks the same. Being fair to apps goes out of the window. QUIC is a firehose that takes all the bandwidth that it can. The TCP backoff mechanism took care of fairness, and that's gone now.
{{</long-quote>}}

Nobody (sane) ever promised that we'd be *fair to apps*. We have to be fair to *everyone paying for our service* in the sense that *everyone paying the same amount should get an equal share of a congested resource*.

With that in mind, how about an alternate idea: instead of deploying Ultra Traffic Optimization AI, yell at your vendor to implement a congestion management mechanism that monitors link utilization by individual users. For example, it could increase the drop probability of a packet if the same user[^WU] already has multiple packets in the same output queue[^CODEL], or it could keep some sort of longer-term statistics. I'm positive someone already worked on something along these lines and got ignored because the solution is not complex enough.

[^WU]: Where a *user* could be identified by an IPv4 address, an IPv6 prefix, or any other relevant sequence of bits in the packet header (flow label comes to mind).

[^CODEL]: Good congestion management mechanisms could be surprisingly simple. See [CoDel](https://en.wikipedia.org/wiki/CoDel) for more details.

As for *QUIC is a firehose*, that could be true, but that would be nothing new; we experienced the same drama at least a half dozen times, starting with "UDP will kill TCP!" Remember the days of "[BitTorrent will bring down our networks](/2010/07/p2p-traffic-is-bad-for-network/)"? How about the days of "Video will kill our networks"? Either the QUIC-based applications behave politely enough not to be noticed, or we'll experience another round of countermeasures along the lines of [RFC 6057](https://www.rfc-editor.org/rfc/rfc6057.html)[^NAR]. In the meantime, can we please keep monitoring and running our networks without the unnecessary drama?

[^NAR]: RFC 6057 is worth reading. It has "*protocol agnostic*" in the title for a good reason and needs no application recognition to work.


