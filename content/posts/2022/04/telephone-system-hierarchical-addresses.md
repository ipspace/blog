---
date: 2022-04-14 06:24:00+00:00
multihoming_tag: session
series:
- multihoming
tags:
- Internet
title: Telephone System Is a Bad Example of Hierarchical Addresses
---
Networking engineers proposing strict hierarchical addressing scheme as a solution to global BGP table explosion often cite the international telephone system numbering plan ([E.164](https://en.wikipedia.org/wiki/E.164)) as a perfect example of an addressing plan that uses hierarchy to minimize routing table sizes. Even more, widespread mobile roaming and [local number portability](https://en.wikipedia.org/wiki/Local_number_portability) indicate that we could solve IP mobility and multihoming if only _insert-your-favorite-opinion-here_.
<!--more-->
I don't know enough about the [telephony signaling](https://en.wikipedia.org/wiki/Signalling_System_No._7) to write a lengthy in-depth blog post on the topic, but from what little I glanced from public information, it seems to me that there's huge difference between IP mobility/multihoming and telephony signaling.

**Telephony signaling is a control-plane activity**. You don't have to go beyond the high level overview [Wikipedia article on Local Number Portability](https://en.wikipedia.org/wiki/Local_number_portability) to figure out that the hard work is done in the call setup phase through a number of directory lookups. Telephone numbers are thus an equivalent of DNS names, not IP addresses.

**Traditional telephony used virtual circuits**. After the control-plane call setup phase was completed, an end-to-end circuit was set up and the data plane was no more complex than a simple label (or circuit) switching. Telephone calls were thus similar to MPLS RSVP/TE tunnels, not to packet forwarding in IP networks.

**Traditional telephony was bloody expensive**. While it's still cheaper to do simple label lookups than TCAM/trie lookups at very high speeds (see also: [Juniper PTX-series](https://www.juniper.net/us/en/products/routers/ptx-series.html)), having a lookup table that contains *every single phone call that takes 64 kbps* becomes ridiculously expensive at terabit speeds. There's a reason voice service providers use VoIP transport inside their networks.

**VoIP just offloads the problem to IP networks**. VoIP is just an application on top of IP. In a modern voice network, a directory service is used during the call setup phase to find the IP address(es) of the call participant(s), and the transport problem is offloaded to underlying IP infrastructure. Claiming how telephony numbering works better than IP addressing is like claiming how [SD-WAN is better than traditional IP networks](https://blog.ipspace.net/2015/07/routing-protocols-and-sd-wan-apples-and.html)... conveniently ignoring the unpleasant fact that both technologies rely on traditional IP networks to work (see also: [there are no wires](https://dilbert.com/strip/2010-04-24)).

**Long story short**: Using E.164 as an example of hierarchical *addressing* plan is misguided. Telephone numbers stopped being *location identifiers* a long time ago, they became *names* much like DNS names.
