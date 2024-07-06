---
title: "Why Does DHCPv6 Matter?"
date: 2021-10-13 06:35:00
tags: [ IPv6, security, DHCP ]
---
In case you missed it, there's a new season of _[Lack of DHCPv6 on Android](https://mailarchive.ietf.org/arch/msg/v6ops/LsWLNn7jBuNkjKlLzeZOTCrnPN8/)_ soap opera on [v6ops mailing list](https://mailarchive.ietf.org/arch/browse/v6ops/). Before going into the juicy details, I wanted to look at the big picture: why would anyone care about lack of DHCPv6 on Android?

{{<note info>}}Please note that I'm not a DHCPv6 fan. DHCPv6 is just a tool not unlike sink plunger -- nobody loves it (I hope), but when you need it, you better have it handy.{{</note>}}

The requirements for DHCPv6-based address allocation come primarily from enterprise environments facing legal/compliance/other [layer 8-10](https://en.wikipedia.org/wiki/Layer_8) reasons to implement policy (*are you allowed to use the network*), control (*we want to decide who uses the network*) and attribution (*if something bad happens, we want to know who did it*).
<!--more-->

### But It Works in Service Provider Networks

You might wonder why the lack of DHCPv6 is not a big deal in mobile networks. As it happens, IPv6 hosts get used in two types of (logical) environments:

**Numbered point-to-point links** connecting a host to a router. 
A prefix is assigned to the (physical or virtual[^1]) point-to-point link after the user has been authenticated. The prefix assigned to the link thus uniquely identifies the user, and it doesn't matter if the user uses SLAAC afterwards to auto-generate a usable IPv6 address on the link (or a dozen of them). Mobile networks use this approach; see [section 5.2](https://datatracker.ietf.org/doc/html/rfc6459#section-5.2) of *IPv6 in 3rd Generation Partnership Project (3GPP) Evolved Packet System (EPS)* (RFC 6459) for details.

**Multi-access segments** (including Ethernet and WiFi) where all hosts share the same IPv6 prefix. IPv6 address is thus the only way to identify users once they are connected to the network. Allowing users to generate IPv6 addresses on the fly might clash with the legal/compliance requirements. There are only two ways out of this morass[^2]:

* Connect all Android users to an untrusted segment. That works well for mobile phones and tablets, but might not work for IoT devices using Android[^3].
* Remain on IPv4.

WiFi hotspots might not care. Most of them don't bother identifying the users anyway[^7]. Guess what most enterprises will do.

### Now what?

People trying to keep everyone happy[^8] and reach some sort of compromise are always pointing out workarounds. For example, you could periodically scrape ND tables from all edge devices to discover SLAAC-generated addresses and associated MAC addresses. 

There's a fundamental problem with this approach[^4]: it would give you attribution, but not control or policy mechanisms. You could figure out **who** caused a security incident, but you could not stop someone from getting connectivity once they manage to get attached to the network. One could argue that you should use other mechanisms to lock down the network edge, but I've often heard security engineers talk about something called *[belt and braces](https://wiki.c2.com/?BeltAndBraces)* and it's never fun if someone yanks the belt out of your pants.

Finally, the lack of controlled IPv6 address allocation wrecks many of the first-hop IPv6 security features available on modern campus gear[^9]. Trying to reconstruct valid IPv6-to-MAC mappings in environments using SLAAC is like chasing the horse that has bolted from the barn because someone removed the lock from the door[^5] -- you MUST have an **authoritative** source of allowed IPv6-to-MAC mappings for first-hop security to work well.

Here's another workaround: [use targeted Router Advertisement messages to give each user a different IPv6 /64 prefix](/2017/12/unique-ipv6-prefix-per-host-how-complex.html). WTF, really? All that just to work around an obstinate person who happens to control a feature of a protocol stack in a mobile platform? How did we ever manage to get to such a wrecked place?

### More to Explore

You know there are tons of [IPv6 blog posts](/tag/ipv6.html) and [webinars](https://www.ipspace.net/IPv6) on ipSpace.net. This time I want to point out the _[Layer-2 Security Challenges](https://my.ipspace.net/bin/get/IPv6Sec/E5.1%20-%20Layer-2%20IPv6%20Security%20Challenges.mp4?doccode=IPv6Sec)_ video by [Christopher Werny](https://www.ipspace.net/Author:Christopher_Werny). You'll find it in the [IPv6 Enterprise Security](https://my.ipspace.net/bin/list?id=IPv6Sec#ENTERPRISE) part of [IPv6 security webinar](https://www.ipspace.net/IPv6_security). 

You might also watch the slightly older *[Source Address Validation Improvement](https://my.ipspace.net/bin/get/IPv6Sec/D4%20-%20Source%20Address%20Validation%20Improvement.mp4?doccode=IPv6Sec)* video by [Eric Vyncke](https://www.ipspace.net/Author:Eric_Vyncke). Both videos are available with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).

[^1]: PPPoE session or [PDP context](https://en.wikipedia.org/wiki/GPRS_core_network#PDP_context)

[^2]: ... because it's unrealistic to expect Android to get DHCPv6 support anytime soon, and even then it might take a decade for the change to percolate to the gazillion low-end gizmos using Android.

[^3]: ... looks like existing security challenges of Internet-of-Trash are not enough.

[^4]: ... ignoring for the moment the headache of trying to do that on a dozen platforms from a half-dozen vendors, each of them using a different broken mechanism to fetch those addresses (because you probably don't want to do it with SNMP).

[^5]: ... because he might be religiously opposed to locks and believes in the freedom of spirit.

[^7]: ... as long as you buy a cup of coffee every now and then. I've heard sometimes they also call cops to remove you.

[^8]: How you can keep everyone happy if one of the participants refuses to listen to what others are saying is beyond my comprehension, but people are still trying.

[^9]: That makes me infinitely sad. It took over a decade of yelling, naming and shaming to get the vendors to implement those features correctly, and now we can't use them properly. Maybe it's time for another round of naming and shaming.
