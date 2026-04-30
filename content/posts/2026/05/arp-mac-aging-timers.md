---
title: "On ARP and MAC Aging Timers"
date: 2026-05-07 08:14:00+0200
tags: [ ARP, bridging ]
---
[Naveen Kumar Devaraj](https://www.linkedin.com/in/naveenkumard/) mentioned an interesting fact in his [EVPN-related comment](https://blog.ipspace.net/2026/04/evpn-generating-macip-routes/#2947):

> The EOS default ARP timeout is 4 hours, and MAC aging is 5 minutes.

Arista is not the only platform using these default values; did you ever wonder where they came from?
<!--more-->
[ARP](https://datatracker.ietf.org/doc/html/rfc826) was created in the days when we could support 30 interactive users on a shared computer with 2 MB of memory and a CPU frequency in low MHz. Every bit counted, and it would be a cardinal sin to needlessly send broadcasts that would burn the CPU cycles on every computer attached to the same [thick coax cable](https://blog.ipspace.net/2015/04/what-is-layer-2-and-why-do-we-need-it/). The communication patterns were also widely different from what we see today; most workstations communicated only with a few servers.

{{<long-quote>}}
It's worth noting that ARP uses the request/reply mechanism because its designer considered the alternative (hosts advertising themselves with periodic HELLO messages as in CLNP End System Hellos) too wasteful.
{{</long-quote>}}

Setting the ARP timeout to a high value thus made perfect sense -- ARP creates a *mapping* between layers, not a packet-forwarding infrastructure. As IP and MAC addresses are usually somewhat stable[^PGC], you can safely use the ARP entry for a long time, and the Gratuitous ARP solves the challenge of occasional changes in MAC or IP addresses. ARP timeouts are more of a garbage collection mechanism.

[^PGC]: At least until people get overly creative

{{<note info>}}
Changing the MAC address of an IP host or assigning the IP address to another host are equivalent from the ARP cache perspective. The proof is left as an exercise for the reader.
{{</note>}}

Interestingly, the Host Requirements RFC (RFC 1122) mentions four mechanisms for [ARP cache validation](https://datatracker.ietf.org/doc/html/rfc1122#page-22), from the familiar timeout to *unicast poll*. The RFC was written in 1989, but I don't remember seeing a unicast ARP until well into the 2000s (or maybe I just wasn't looking hard enough; in that case, I'd appreciate a comment or two).

MAC aging solves a completely different problem: it keeps the packet-forwarding infrastructure (the MAC address table) reasonably clean. Until EVPN, transparent bridging never had a control plane that could authoritatively tell the ~~switches~~ bridges where a MAC address is. It's also crucial not to have stale entries in the MAC address table; it's based on guesswork (dynamic MAC learning), and it's better to flood a unicast frame than to send it in the wrong direction. On the other hand, a low MAC aging timer increases the amount of flooded unicast traffic, which is clearly undesirable if your bridge connects two 10 Mbps segments[^FB].

[^FB]: The first bridges had two 10-Base-T connections.

The 5-minute MAC aging timer is probably a compromise, and based on when the first bridges appeared[^FBD], one could reasonably guess that they chose a value lower than the time it takes to disconnect a workstation, move it to another room, and reconnect it 😜

[^FBD]: According to [this article](https://spectrum.ieee.org/how-dec-engineers-saved-ethernet), we got the transparent bridge idea in "*one evening in 1983*" with the product (LANBridge 100) shipping in 1986. I also found [an IEEE article from 1988](https://ieeexplore.ieee.org/document/3231). Sadly, the DEBET product code for the LANBridge looks familiar, as do DEMPR and DESPR. I must be getting a bit old. Finally, if you're into ancient history, I found the [MicroVAX 2000 Networking Guide](https://manx-docs.org/collections/antonio/dec/netacug3.pdf) from 1988.
