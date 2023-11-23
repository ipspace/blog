---
title: "Worth Reading: DNS over IPv6"
date: 2023-12-03 07:44:00
tags: [ worth reading, IPv6 ]
---
What happens when you let a bunch of people work on different aspects of a solution without them ever talking to each other? You get DNS over IPv6. As [nicely explained by Geoff Huston](https://www.potaroo.net/ispcol/2023-11/dns-ipv6.html), this is just one of the bad things that could happen:
<!--more-->
* DNS reply grows over the MTU size because of DNSSEC (not to mention that the MTU size in IPv6 could be variable due to extension headers)
* The DNS reply gets dropped because the "*fragmentation is bad*" dogma is strictly enforced in IPv6
* In the not-so-awful case, the DNS server gets an ICMPv6 report and adjusts the maximum MTU in a forwarding cache entry.
* However, DNS runs over UDP, and the server doesn't care about retransmissions. It's up to the client to retry. That takes time.
* Worst case, someone decided based on their ancient experience with *[ping of death](https://en.wikipedia.org/wiki/Ping_of_death)*[^BP] that ICMP is bad, resulting in firewall filters dropping ICMPv6 packets. The server thus has no way of knowing someone dropped its reply, and the client only gets its answer once it gives up and retries using DNS-over-TCP.

[^BP]: Or myths-and-legends commonly known as *best practices*

To make matters worse, the Happy Eyeballs algorithm happily papers over the cracks, and the problems are not discovered until IPv4 breaks.

On a totally unrelated note, you might appreciate Geoff's sarcasm ;)

> I must admit that I'm very uncomfortable with this level of advice in the context of using the DNS over IPv6 transport in such strongly worded terms. This recommendation obviously plays well to the set of highly vocal IPv6 zealots out there, but aside from such unthinking zealotry and unfounded opining, there is some room for doubt here. 

Have fun [reading the whole article](https://www.potaroo.net/ispcol/2023-11/dns-ipv6.html)