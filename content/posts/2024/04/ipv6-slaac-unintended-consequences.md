---
title: "Unintended Consequences of IPv6 SLAAC"
date: 2024-04-16 08:45:00+0200
tags: [ IPv6 ]
---
One of my friends is running a large IPv6 network and has already experienced a shortage of IPv6 neighbor cache on some of his switches. Digging deeper into the root causes, he discovered:

> In my larger environments, I see significant neighbor table cache entries, especially on network segments with hosts that make many long-term connections. These hosts have 10 to 20 addresses that maintain state over days or weeks to accomplish their processes.

What's going on? A perfect storm of numerous unrelated annoyances:
<!--more-->
* **Stateless Autoconfiguration**. IPv6 was designed before IPv4 got DHCP and wanted to mimic the ease-of-deployment of AppleTalk and Novell IPX, resulting in SLAAC. SLAAC was supposed to generate a single (global) IPv6 address per node.
* **SLAAC Privacy Extensions**. SLAAC used the interface MAC address to generate an IPv6 address. That could be used to track users across network segments; IETF solved that with SLAAC Privacy Extensions (RFC 4941 and [RFC 8981](https://datatracker.ietf.org/doc/html/rfc8981)).
* **Long-running TCP sessions.** According to RFC 8981, a host should periodically generate a new IPv6 address and deprecate its old addresses (the default rotation period is 24 hours). Deleting an IPv6 address kills any TCP session using it (unless you're running MP-TCP), so the deprecated addresses stay active as long as TCP sessions are using them.
* **Reconnecting to the Network.** I was told (years ago) that some mobile devices generate a new IPv6 address every time they wake up. I have no idea what modern iOS/Android implementations do; feedback would be highly appreciated.

Why is that a problem? In two words: cache trashing. When a hardware packet forwarding device runs out of the IPv6 ND cache, it punts transit packets to the CPU (increasing the CPU load) to trigger IPv6 neighbor discovery. Some devices might drop the "offending" IPv6 packets, resulting in increased packet drops and reduced performance, eventually making IPv6 perform worse than IPv4.

Can we fix it? As is always the case in network design, you have to choose what tradeoffs you want to make:

* **Limiting the number of ND entries** per interface will protect the scarce hardware resources but result in suboptimal performance for everyone using IPv6 on an affected segment.
* **Using Semantically Opaque Interface Identifiers** ([RFC 7217](https://datatracker.ietf.org/doc/html/rfc7217)) would solve the problem but enable user tracking *within a segment* (but not across segments).
* **DHCPv6 IA_NA address allocation** could limit the number of addresses assigned to a single IPv6 host. Contrary to popular lore spread by DHCPv6 haters, [a host can request multiple IPv6 addresses via DHCPv6](/2021/10/ipv6-multiple-addresses-per-interface/) (address rotation is thus not a big deal), and a DHCPv6 server can deny a request for a new address (forcing the host to choose between privacy and broken TCP sessions).

OK, it looks like environments facing hardware resource shortages could use DHCPv6 to fix that, right? Well, no. Look at the [overview of IPv6 support in various operating systems](https://en.wikipedia.org/wiki/Comparison_of_IPv6_support_in_operating_systems) and tell me if you can spot popular end-user operating systems that do not support DHCPv6.

As of March 2024, two modern end-user operating systems did not support DHCPv6[^NT], both from the company that graced us with a generative AI model that [refused to draw a picture of a white male pope for diversity reasons](https://en.wikipedia.org/wiki/Gemini_(chatbot)#Image_generation_controversy). Even worse, the [controversy goes back more than a decade](https://issuetracker.google.com/issues/36949085), and we're still forced to deal with the consequences of the stubbornness of highly opinionated engineers who _think they know better_ than us how to run our networks. No wonder we're experiencing low enterprise adoption of a protocol that could buy a beer even in the US for quite a few years.

[^NT]: We can probably agree to ignore OpenVMS and Windows NT, right?

On a completely unrelated topic, did you know that the only way to [get a VM IPv6 address in Google Cloud](https://cloud.google.com/compute/docs/ip-addresses/configure-ipv6-address) is to use DHCPv6?