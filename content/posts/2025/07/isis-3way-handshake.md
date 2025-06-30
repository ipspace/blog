---
title: "IS-IS 3-Way Handshake and the Power of SHOULD"
date: 2025-07-01 08:17:00+0200
tags: [ IS-IS ]
---
Yesterday, I [mentioned](/2025/06/netlab-start-tools/) that a Cisco router running pre-standard IS-IS 3-way handshake ([this is why you need it](https://isis.bgplabs.net/basic/3-p2p/#three-way-handshake)) interoperates with multiple implementations of [RFC 5303](https://datatracker.ietf.org/doc/html/rfc5303). How's that possible, and does it matter whether you configure the ancient Cisco routers (release 15.x) to use IETF 3-way handshake instead of the "proprietary" one?

{{<long-quote>}}
**TL&DR:** It SHOULD NOT matter, but the more I explore the RFCs, the more I'm amazed anything works at all. 
{{</long-quote>}}

I took a [trip to the Wireshark land](/2025/06/netlab-start-tools/) to figure out the details (you can [download the capture file](/2025/07/capture-isis-hello.pcapng)):
<!--more-->
Here's a pre-standard (cisco) IS-IS P2P hello sent by a Cisco router running IOSv release 15.9:

{{<figure src="/2025/07/ws-isis-p2p-hello-cisco.png">}}

And here's a standard (RFC 5303) IS-IS P2P hello sent by FRRouting release 10.3:

{{<figure src="/2025/07/ws-isis-p2p-hello-ietf.png">}}

The only difference between the two is the extra values in TLV 240, starting with Extended Local Circuit ID. It's nice of Cisco IOS to ignore the fields it does not understand, but why do other implementations accept the shorter version of TLV 240? Welcome the magic powers of [SHOULD](https://datatracker.ietf.org/doc/html/rfc2119) (and a judicious application of the [Robustness Principle](https://en.wikipedia.org/wiki/Robustness_principle) that [some vendors sometimes forget about](/2025/06/evpn-route-attributes-matter/)). Straight from [RFC 5303](https://datatracker.ietf.org/doc/html/rfc5303#section-3.1):

> Any system that supports this mechanism MUST include the Adjacency Three-Way State field in this option.  The other fields in this option SHOULD be included as explained below in section 3.2.

Section 3.2 contains even more weasely language:

> If the option with a valid Adjacency Three-Way State is present, the Neighbor System ID and Neighbor Extended Local Circuit ID fields, if present, SHALL be examined.

Let me rephrase:

* It's OK if those fields are missing
* It's also acceptable that you ignore those fields.

But wait, there's more:

> If they are present, and the Neighbor System ID contained therein does not match the local system's ID, or the Neighbor Extended Local Circuit ID does not match the local system's extended circuit ID, the PDU SHALL be discarded and no further action is taken.

Rephrased into plain English: Even if you find a mismatch in circuit IDs (the only reason we have them in TLV 240), it's acceptable that you ignore it.

Isn't that a great way to write standards? Everyone can claim compliance, regardless of the details of what they do. On a more realistic front, I [experienced](https://blog.ipspace.net/2015/02/rfc-7454-bgp-operations-and-security/) how the RFC sausage is made and decided to avoid that particular experience in the future (hint: [obstinate vendors](https://blog.ipspace.net/2021/10/ipv6-multiple-addresses-per-interface/) don't help).
