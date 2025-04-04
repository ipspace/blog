---
title: "Response: NAT Traversal Mess"
date: 2025-04-10 08:00:00+0200
tags: [ NAT ]
---
Let's look at another part of the [lengthy comment Bob left](https://blog.ipspace.net/2025/03/rise-of-nat/#2571) after listening to the [Rise of NAT podcast](/2025/03/rise-of-nat/). This one is focused on the NAT traversal mess:

> You mentioned that only video-conferencing and BitTorrent use client-to-client connectivity (and they are indeed the main use cases), but hell, do they need to engineer complex systems to circumvent these NATs and firewalls: STUN, TURN, ICE, DHT...

Cleaning up the acronym list first: DHT is unlike the others and [has nothing to do with NAT](https://en.wikipedia.org/wiki/Distributed_hash_table).
<!--more-->
Now that we're left with three acronyms, let's try to figure out what they do:

* [STUN](https://en.wikipedia.org/wiki/STUN) detects NAT devices in the forwarding path and uses clever tricks to create the NAT translations that can ultimately be used to reach a peer node behind another NAT device.
* STUN does not work with all [types of NAT](https://en.wikipedia.org/wiki/Network_address_translation#Methods_of_translation). In particular, it does not work with symmetric NAT (NAT using 5-tuple NAT translations -- what you'd see on Cisco IOS). [TURN](https://en.wikipedia.org/wiki/Traversal_Using_Relays_around_NAT) tries to fix that.
* [ICE](https://en.wikipedia.org/wiki/Interactive_Connectivity_Establishment) seems to be an [umbrella solution on top of the other two](https://datatracker.ietf.org/doc/html/rfc8445) (please write a comment if I got it wrong)

Wouldn't it be better if, instead of the above mess, the host could tell the NAT device it needs a public port? Of course, we have at least three protocols to do that, proving yet again the [infinite wisdom of xkcd](https://xkcd.com/927/):

* [Internet Gateway Device Protocol](https://en.wikipedia.org/wiki/Internet_Gateway_Device_Protocol) part of [Universal Plug and ~~Pray~~ Play](https://en.wikipedia.org/wiki/Universal_Plug_and_Play)
* [Port Control Protocol](https://en.wikipedia.org/wiki/Port_Control_Protocol)
* [NAT Port Mapping Protocol](https://en.wikipedia.org/wiki/NAT_Port_Mapping_Protocol)

Why do we need STUN/TURN/ICE if we have a (supposedly) working solution? It often comes down to *I don't want to deal with those uncouth people from the IT basement* (aka "networking engineers"), a [well-known strategy used by the likes of Novell and VMware](https://blog.ipspace.net/2019/10/the-cost-of-disruptiveness-and/), or to *I want to make this work even though some stupid security people think it should be blocked* (see also: [using Signal to plan bomb strikes](https://en.wikipedia.org/wiki/United_States_government_group_chat_leak)).

I never said NAT is a great solution (it's not), but it's still a [necessary evil](/2025/03/response-end-to-end-connectivity/) (even in the [IPv6 world](/2011/12/we-just-might-need-nat66/)) that has to be dealt with. There are standard ways to do it, and fortunately, we have tons of libraries you can use to get the job done without going into the details. A quick search for "Python [STUN|TURN|ICE] NAT" resulted in a half-dozen GitHub/PyPi projects. Ideally, we'd have a single library that everyone uses to get the job done (like OpenSSL[^NAGA] and OpenSSH), but maybe we're not at that stage yet.

[^NAGA]: In other news, that's [not always a good idea](https://en.wikipedia.org/wiki/OpenSSL#Notable_vulnerabilities).

Last but not least, networking engineers love to think that [networking's complexities are unique](https://blog.ipspace.net/2014/02/is-cli-in-my-way-or-is-it-just-symptom/). Well, I can point you to numerous other IT disciplines full of complexities, but they managed to build layers of abstraction around them. For example, people stopped reinventing compilers, operating systems, and databases ages ago. I haven't heard anyone (apart from a small circle of [database developers](https://brooker.co.za/blog/2024/12/03/aurora-dsql.html)) talking about the complexities of distributed databases that arise because they have to deal with [byzantine faults](https://en.wikipedia.org/wiki/Byzantine_fault) and the consequences of the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem). Why should NAT traversal be any different?

### But It Would Be Better in IPv6 World

Here's the most common counter-argument to my "_NAT is a necessary evil_" rants, [this time made by Daryll Swer](https://blog.ipspace.net/2025/03/response-end-to-end-connectivity/#2585):

> All these problems don't exist on native routed (and static) IPv6.

**TL&DR:** Bollocks.

Most hosts connected to the public IPv6 Internet over a LAN or WiFi sit behind a stateful firewall[^SFW6] (for various reasons[^SFR]). Punching holes through that firewall is equivalent to establishing NAT translations.

[^SFW6]: As one would expect, there's an [RFC describing the details](https://datatracker.ietf.org/doc/html/rfc6092).

[^SFR]: Copiously described in the [Local Network Protection for IPv6](https://datatracker.ietf.org/doc/html/rfc4864) RFC with the added "_you don't need NAT for that_" slant.

Oh, but dealing with firewalls is so much simpler in the IPv6 world:

> Firewall hole punching only involves STUN, and that's it. We move on with our lives.

Sort of[^LCF]. Decent stateful firewalls match on the full 5-tuple, which is functionally equivalent to symmetric NAT, but don't change the UDP port numbers when packets traverse them (making them equivalent to *‌port-restricted cone NAT*), so it's easier to discover what hole your peer punched in their firewall.

On a more practical note, even the Cisco router[^IOS] between me and the global Internet seems to be using *port-restricted cone NAT* (another term for the same behavior seems to be *Endpoint-Independent Mapping* -- EIM), and I don't remember when a VoIP call or a video conferencing app would not work. Yes, things are unnecessarily complex (from the perspective of IPv6 fans), but they work. It seems the NAT-induced complexity is still not expensive enough to make migration to IPv6 cost-effective.

[^IOS]: EIM-NAT seems to be the default on Cisco IOS XE and [requires a nerd knob on Cisco IOS Classic](https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/217599-understand-nat-to-enable-peer-to-peer-co.html).

[^LCF]: As always, leave a comment with enough technical details, and I'll fix the blog post.

However, to be fair, CG-NAT in the IPv4 world does introduce a whole new level of evilness not present in the IPv6 world. For example, if two devices in the same CG-NAT cone[^INS] want to communicate but happen to use a server outside of the NAT cone[^OUT] to find their respective IP addresses, the traffic has to go through the NAT device (hairpinning).

[^INS]: A fancy name for the *inside* NAT interface(s)

[^OUT]: A fancy name for the *outside* NAT interface(s)
