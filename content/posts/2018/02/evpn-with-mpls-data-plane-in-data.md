---
date: 2018-02-23 10:00:00+01:00
evpn_tag: mpls
tags:
- MPLS
- data center
- EVPN
title: EVPN With MPLS Data Plane in Data Centers
url: /2018/02/evpn-with-mpls-data-plane-in-data.html
---
Mr. Anonymous (my most loyal reader and commentator) sent me this question as a comment to one of my blog posts:

> Is there any use case of running EVPN (or PBB EVPN) in DC with MPLS Data Plane, most vendors seems to be only implementing NVO to my understanding.

Sure there is: you already have MPLS control plane and want to leverage the investment.
<!--more-->
You might also want to persuade your customers that this is a must-have feature because your competitors don't have it in their products.

Sarcasm aside:

-   EVPN uses BGP Tunnel Encapsulation Attribute ([RFC 5512](https://tools.ietf.org/html/rfc5512), new version in [draft-ietf-idr-tunnel-encaps](https://tools.ietf.org/html/draft-ietf-idr-tunnel-encaps)) to indicate the encapsulation to use to reach the egress PE device (we shouldn't call them routers anymore, right)?
-   The values of this attribute can be found in [IANA registry](https://www.iana.org/assignments/bgp-parameters/bgp-parameters.xhtml#tunnel-types).
-   Almost all of them rely on something-over-IP tunneling.

Maybe the real question should be "*why is that the case?*" In a word: decoupling.

{{<note>}}Unrelated question: why do we need so many encapsulations? Because [standards](https://xkcd.com/927/).{{</note>}}

### The Benefits of Decoupling

When using whatever-over-IP encapsulation technology with EVPN, the transport fabric remains simple and clean. It's a pure IP fabric using a single encapsulation (IP) and running a single routing protocol.

MPLS encapsulation used with EVPN control plane requires end-to-end LSPs between PE devices. You'll have to deal with two encapsulations (IP and MPLS), two sets of forwarding tables (FIB and LFIB), and additional control-plane protocols -- LDP, MPLS-TE, BGP IPv4+labels or segment routing.

Each LSP has to exist in the forwarding table of every node it traverses. That introduces extra state in the transport fabric - not relevant if you have 10 switches, highly relevant if you have thousands of switches (example: WAN deployment) and the core switches use [high-speed merchant silicon](https://www.juniper.net/documentation/en_US/junos/topics/reference/general/mpls-scaling-values-qfx-series.html).

Admittedly, the MPLS encapsulation introduces lower overhead than whatever-over-IP encapsulation. That overhead becomes relevant when the bandwidth becomes expensive: in WAN networks, not in data centers.

To summarize: there's no free lunch. You have to accept higher encapsulation overhead or more complex transport fabric. I know what I would do when designing data center infrastructure.
