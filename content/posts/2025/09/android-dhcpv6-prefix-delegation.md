---
title: "Android Phones Might Ask for /64 Delegated Prefix"
date: 2025-09-29 07:43:00+0200
tags: [ netlab ]
netlab_tag: graphs
---
Here's the latest episode of the hilarious[^WFAD] "DHCPv6 on Android" [soap opera](/2021/10/dhcpv6-matters/): in a 720-degree turnaround, Android will support DHCPv6, but only for *prefix delegation purposes*. Yes, you got it right, in a year or two, every phone might want to have a dedicated /64 prefix assigned to it *on WiFi segments*[^MPFX].

[^WFAD]: If you're privileged enough to watch it from a distance.

[^MPFX]: Every mobile device was traditionally assigned a /64 prefix on mobile networks because the networks treated every network-to-device connection as a point-to-point link (yes, it's tunnels all the way down). I have no idea whether 5G still uses that model, and I have no willpower to start figuring that out. A helpful comment would be much appreciated.

Want more details? Well, there's a [high-level overview](https://android-developers.googleblog.com/2025/09/simplifying-advanced-networking-with.html) published on the Android Developers blog and a corresponding message sent to the [v6ops mailing list](https://mailarchive.ietf.org/arch/msg/v6ops/Sq5TadeSsMQ-0uEWrdem3A1wDh0/). Let's see how much sense that makes.
<!--more-->
{{<note warn>}}
Before moving on, I can't resist pointing out that this announcement came from the same person who was for decades opposed to ever having the DHCPv6 client on Android and made [all sorts of ridiculous excuses](/2021/10/ipv6-multiple-addresses-per-interface/) to justify his position.
{{</note>}}

So, here's the gist of that blog post:

* IPv4 is bad (OK, we know that)
* IPv4 is bad for batteries because phones need to keep NAT sessions alive. To me, this makes as much sense as my usual quip that *copy-paste makes rockets explode*, but maybe I'm missing something.
* We couldn't solve that problem with IPv6 because the existing address assignment policies have limitations.

While I know that networks have already experienced the [ND cache exhaustion](/2024/04/ipv6-slaac-unintended-consequences/), the root cause is usually a crappy implementation that grabs too many addresses and holds onto them due to long-lived TCP sessions, not the *limitations of address assignment mechanisms*. However, I think anyone with any operational experience in replacing IPv4 with IPv6 knows that ND cache exhaustion is not the leading cause of IPv4 persistence.

And then there's this gem:

> Additionally, we’ve heard feedback from some users and network operators that they desire more control over the IPv6 addresses used by Android devices. Until now, Android only supported SLAAC, which does not allow networks to assign predictable IPv6 addresses, and makes it more difficult to track the mapping between IPv6 addresses and the devices using them. This has limited the availability of IPv6 on Android devices on some networks.

Imagine the audacity of the lead crusader against DHCPv6 clients repeating the claims he's been hearing from frustrated network operators for decades as an argument for *why IPv6 hasn't solved the problem yet*. If the Android IPv6 team cared, they could have solved the problem ages ago. If this isn't the pinnacle of hypocrisy, I don't know what is.

So, what's the solution to all these insurmountable problems? It's a DHCPv6 client on Android (SURPRISE !!!), but not to get controlled IPv6 addresses, but to request a whole /64 prefix *for every Android device*. WTAF? Why would anyone need that?

Here are the arguments from the blog post:

* In some future release, that **delegated prefix would be shared with wearable devices** or a hypothetical **tablet tethered to an Android phone connected to WiFi**[^MAI]. Let me point out that you don't need a delegated prefix for that. Mobile phones have supported tethering on IPv6 for ages; they simply extended the "outside" /64 prefix to the tethered network. There's no need for a different mechanism from WiFi to Bluetooth/USB. Also, my Apple Watch connects to WiFi directly (just saying).
* This **realizes the potential of IPv6... without requiring NAT**. Meh. Allocating another "outside" IPv6 address with DHCPv6 IA_NA mechanisms gets you to the same goal. But even if you were using NAT in the Android device to hide tethered devices behind the same IPv6 address, there would be no need for keepalives because Android would have control over the expiration of the NAT sessions. The Android device would have to be active whenever that NAT session is used because it needs to forward packets anyway.
* Because the prefix is assigned by the network, network operators can use existing DHCPv6 logging infrastructure to **track which device is using which prefix**. Gee, thanks for the roses, but you don't need IA_PD for that. Get off your crusade horse, implement a DHCPv6 client doing IA_NA like any other IPv6 implementation, and stop gaslighting us.

[^MAI]: Can you, please, try to find an example that isn't so obviously mocking your audience's intelligence?

Without going into too many details, instead of using a reasonable number of IPv6 addresses on a WiFi network, the "solution"[^ISOFAP] offered by the Android IPv6 team expects the network to allocate a /64 prefix to every Android device.

[^ISOFAP]: ... in search of a problem

{{<note>}}
Just in case you're wondering why the Android team wants to get a /64 prefix for every node: they want to be able to run virtual machines that would get their IPv6 addresses with SLAAC. You don't have to believe me, it's all [documented in RFC 9663](https://datatracker.ietf.org/doc/html/rfc9663#name-prefix-length-consideration).
{{</note>}}

But the "new" approach reduces the ND cache, right? Isn't that a good thing? Not so fast. Delegating a prefix to a device uses an ND entry and a routing table entry. Low-cost edge switches have always had fewer routing table entries (that use more expensive TCAM or similar hardware) than ND entries (that use simple hash tables). Depending on the hardware you use, going from multiple on-link addresses to prefix-per-host might exhaust the forwarding resources even sooner.

Even worse, the "delegated prefix" approach requires the edge switches to keep track of DHCPv6 prefix delegation state, synchronize it between multiple switches connected to the same segment, and fetch it from the DHCPv6 server on reloads (the [gory details](https://datatracker.ietf.org/doc/html/rfc9663#section-6.2) are in RFC 9663). None of that is needed if the network is using DHCPv6 IA_NA address delegation -- the state is kept in the DHCPv6 server(s), and the edge switches build the ND cache in the same way as if the attached devices were using SLAAC (unless you deployed [Source Address Validation](https://datatracker.ietf.org/doc/html/rfc6959)).

**To recap:** 

* The Android IPv6 team has yet again chosen to make their lives as simple as possible[^AWSP] while offloading all the hard work onto everyone else.
* They implemented the DHCPv6 client on Android in the most useless way for people who just want to run their networks in a bit more controlled way. However, I'm pretty sure they will claim "*they listened to the network operators and implemented DHCPv6 to help them track network devices*"
* When this gets rolled out and the developers start using it, expect complaints if your network won't support it.
* To implement this, you'll likely have to request more IPv6 address space and rework your IPv6 addressing.

[^AWSP]: There are alternate ways of solving the problem, but they require actual work, not writing RFCs and forcing your way through IETF working groups.

Finally, as a cherry on a cake, the Google blog post concludes with:

> We hope this change encourages more networks to adopt IPv6, leading to improved battery life, reliability, and code simplicity in these complex networking scenarios.

One cannot make this stuff up.
