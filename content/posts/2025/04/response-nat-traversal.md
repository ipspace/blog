---
title: "Response: NAT Traversal Mess"
date: 2025-04-03 08:00:00+0200
tags: [ NAT ]
---
Let's look at another part of the [lengthy comment Bob left](https://blog.ipspace.net/2025/03/rise-of-nat/#2571) after listening to the [Rise of NAT podcast](/2025/03/rise-of-nat/). This one is focused on the NAT traversal mess:

> You mentioned that only video-conferencing and BitTorrent use client-to-client connectivity (and they are indeed the main use cases), but hell, do they need to engineer complex systems to circumvent these NATs and firewalls: STUN, TURN, ICE, DHT...

Cleaning up the acronym list first: DHT is unlike the others and [has nothing to do with NAT](https://en.wikipedia.org/wiki/Distributed_hash_table).
<!--more-->
Now that we're left with three acronyms let's try to figure out what they do:

* [STUN](https://en.wikipedia.org/wiki/STUN) detects NAT devices in the forwarding path and uses clever tricks to create port mappings in them that can ultimately be used to reach a peer node behind another NAT device.
* STUN does not work with all [types of NAT](https://en.wikipedia.org/wiki/Network_address_translation#Methods_of_translation). [TURN](https://en.wikipedia.org/wiki/Traversal_Using_Relays_around_NAT) fixes that.
* [ICE](https://en.wikipedia.org/wiki/Interactive_Connectivity_Establishment) seems to be an [umbrella solution on top of the other two](https://datatracker.ietf.org/doc/html/rfc8445) (please write a comment if I got it wrong)

Wouldn't it be better if, instead of the above mess, the host could tell the NAT device it needs a public port? Of course, we have at least three protocols to do that, proving yet again the [infinite wisdom of xkcd](https://xkcd.com/927/):

* [Internet Gateway Device Protocol](https://en.wikipedia.org/wiki/Internet_Gateway_Device_Protocol) part of [Universal Plug and ~~Pray~~ Play](https://en.wikipedia.org/wiki/Universal_Plug_and_Play)
* [Port Control Protocol](https://en.wikipedia.org/wiki/Port_Control_Protocol)
* [NAT Port Mapping Protocol](https://en.wikipedia.org/wiki/NAT_Port_Mapping_Protocol)

Why do we need STUN/TURN/ICE if we have a (supposedly) working solution? It often comes down to *I don't want to deal with those uncouth people from the IT basement* (aka "networking engineers"), a [well-known strategy used by the likes of Novell and VMware](https://blog.ipspace.net/2019/10/the-cost-of-disruptiveness-and/), or to *I want to make this work even though some stupid security people think it should be blocked* (see also: [using Signal to plan bomb strikes](https://en.wikipedia.org/wiki/United_States_government_group_chat_leak)).

I never said NAT is a great solution (it's not), but it's still a [necessary evil](/2025/03/response-end-to-end-connectivity/) (even in the [IPv6 world](/2011/12/we-just-might-need-nat66/)) that has to be dealt with. There are standard ways to do it, and in a sane world, we'd have a single library that everyone uses (like OpenSSL and OpenSSH) to get the job done[^NAGA].

After all, people stopped reinventing operating systems and databases ages ago. I haven't heard anyone (apart from a small circle of [database developers](https://brooker.co.za/blog/2024/12/03/aurora-dsql.html)) talking about the complexities of distributed databases that arise because they have to deal with [byzantine faults](https://en.wikipedia.org/wiki/Byzantine_fault) and the consequences of the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem). Why should NAT traversal be any different?

[^NAGA]: In other news, that's [not always a good idea](https://en.wikipedia.org/wiki/OpenSSL#Notable_vulnerabilities).

On a more positive front, a quick search for "Python [STUN|TURN|ICE] NAT" resulted in a half-dozen GitHub/PyPi projects, so it's not like you couldn't take a library and run with it if you need NAT traversal in your software.

Back to Bob:

> So, in my opinion, NATs and firewalls heavily hinged client-to-client connectivity and are the reason why the (mass market) internet is so unbalanced (and you could argue that this allowed the cloud to happen, then state surveillance, etc., but that's yet another topic).

I have to disagree. NAT traversal is a solved problem, and tons of working video conferencing solutions prove it can be solved reliably. We're back to [square one](/2025/03/response-end-to-end-connectivity/): mass-market Internet is so heavily unbalanced because it's easier for everyone to use servers-as-a-service (aka "websites" or "cloud") than to deploy their bespoke infrastructure. Just look at all the great networking engineers publishing their hard work on LinkedIn or Medium instead of spending an hour or two (= one or two orders of magnitude less than what they invested in the content) to set up their blog using free (and often open-source) solutions.

Fortunately, I can point you to several engineers who took the jump into the unknown, emerged unscathed, and documented their experience (comments with further pointers are most welcome):

* [Scott Lowe](https://blog.scottlowe.org/2015/01/05/blog-migration-complete/)
* [Bruno Wollmann](https://brunowollmann.com/2022/11/this-site-now-cooked-by-hugo/)
* [Ole Troan](https://blog.ipspace.net/2025/02/worth-reading-ipv6-failures/)
* [Gian Paolo Boarina](https://www.ifconfig.it/hugo/2016/08/18/welcome-hugo/)
* [David Peñaloza Seijas](https://recurseit.com/post/2025/03/migrating-from-wordpress-to-hugo---part-1/)
* [Mat Jovanovic](https://www.matscloud.com/blog/2020/04/24/hugo-with-docsy-and-aws-amplify/)
* [Abhi Mukherjee](https://networkingwithabhi.github.io/post/how-i-developed-this-site/)