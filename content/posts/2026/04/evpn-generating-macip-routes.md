---
title: "On Generating EVPN MAC/IP Routes"
date: 2026-04-29 07:38:00+0200
tags: [ EVPN ]
evpn_tag: details
---
[Naveen Kumar Devaraj](https://www.linkedin.com/in/naveenkumard/) was reading my [Integrated Routing and Bridging (IRB) with EVPN MAC-VRF Instances](https://evpn.bgplabs.net/evpn/3-irb/) lab exercise and spotted this detail:

> Arista EOS originates MAC-IP routes with and without IP addresses, effectively doubling the size of the EVPN BGP table

He kindly wrote a [LinkedIn comment](https://www.linkedin.com/feed/update/urn:li:activity:7450795115603750912?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7450795115603750912%2C7450965921457831936%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287450965921457831936%2Curn%3Ali%3Aactivity%3A7450795115603750912%29) explaining that behavior:
<!--more-->
> This is by design since the triggers for these two types of routes are fundamentally different. A MAC table update triggers and aligns with a MAC-Only route, while an ARP table update triggers and aligns with a MAC+IP route. They are kept separate in EVPN for the exact same reason ARP and MAC tables are separate, as we know traditionally.

You know I had to check that against the [RFC 7432](https://datatracker.ietf.org/doc/html/rfc7432), right? Here's what it says in [Section 9.2.1](https://datatracker.ietf.org/doc/html/rfc7432#section-10) (ARP and ND):

{{<long-quote>}}
Note that a MAC-only route can be advertised along with, but
independent from, a MAC/IP route for scenarios where the MAC learning over an access network/node is done in the data plane, and independent from ARP snooping that generates a MAC/IP route. In such scenarios, when the ARP entry times out and causes the MAC/IP to be withdrawn, then the MAC information will not be lost.
{{</long-quote>}}

Thanks a million, Naveen (I also fixed the exercise description)!