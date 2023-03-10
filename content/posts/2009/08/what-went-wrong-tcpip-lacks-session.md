---
date: 2009-08-17 07:02:00+02:00
multihoming_tag: session
series:
- multihoming
tags:
- IPv6
- Internet
- networking fundamentals
title: 'What Went Wrong: TCP/IP Lacks a Session Layer'
url: /2009/08/what-went-wrong-tcpip-lacks-session.html
---
One of the biggest challenges facing the Internet core today is the [explosion of the IP routing and forwarding tables](https://blog.ipspace.net/2009/06/internet-anarchy-ill-advertise-whatever.html), which is caused primarily by traffic engineering and multihoming requirements. Things were supposed to get better when IPv6 introduced strict hierarchical addressing (similar to the phone number addressing, where the first few digits always denote the country code).

Unfortunately, the hierarchical IPv6 addressing idea relied on incredible belief that the world will shape itself according to the wills of the IETF working group members. Not surprisingly, that didn't happen and [the hierarchical IPv6 addressing idea was quietly scrapped](https://blog.ipspace.net/2009/05/lack-of-ipv6-multihoming-elephant-in.html), giving us plenty more prefixes to play with when trying to pollute the global IPv6 routing tables.
<!--more-->
If we take a step back and ask ourselves: "why do we need IP multihoming in the first place?" the answer is simple: because the client *application* (layer-7 entity) connects to the *IP address* (layer-3 entity) of the server. If we want to have persistent sessions, the server IP address must remain reachable -- the headaches are caused by tight coupling across numerous protocol layers.

The session persistence, session restarts, checkpoints and the ability to connect to multiple L3 addresses to reach the same service are the jobs of the OSI session layer ... only there is none in the TCP/IP protocol stack. In 1990s, the IP zealots were quick to point out that "_if you know what you're doing, four layers are enough, if you don't, even seven layers won't help you_" when making fun of the OSI protocol stack. Guess who's laughing now (although the laugh is somewhat bitter and utterly irrelevant).

The worst part of the story is that the IETF community had the chance to fix their design problems when they realized that IPv4 will have to be replaced by something else. Unfortunately, the only thing they could agree upon was to replace IPv4 addresses with longer IPv6 addresses while retaining the rest of the (then) 15-year old design. Some people realized years later that the whole approach is broken and tried to fix it with [SHIM6](http://en.wikipedia.org/wiki/Site_Multihoming_by_IPv6_Intermediation), but it was too little done way too late. The SHIM6 protocols are still in drafts, there are no commercial implementations and in the meantime we already ran out of IPv4 addresses.
