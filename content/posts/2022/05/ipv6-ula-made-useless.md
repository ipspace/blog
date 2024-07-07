---
title: "IPv6 Unique Local Addresses (ULA) Made Useless"
date: 2022-05-10 06:30:00
tags: [ IPv6 ]
---
Recent news from the *Department of Unintended Consequences*: [RFC 6724](https://datatracker.ietf.org/doc/html/rfc6724) changed the IPv4/IPv6 source/destination address selection rules a decade ago, and it seems that the common interpretation of those rules makes IPv6 Unique Local Addresses (ULA) *less preferred* than the IPv4 addresses, at least according to the recent *[Unintended Operational Issues With ULA](https://datatracker.ietf.org/doc/html/draft-buraglio-v6ops-ula-05)* draft by [Nick Buraglio](https://www.ipspace.net/Expert:Nick_Buraglio), Chris Cummings and [Russ White](https://www.ipspace.net/Author:Russ_White).

**End result**: If you use only ULA addresses in your dual-stack network[^NOULA], IPv6 won't be used **at all**. Even worse, if you use ULA addresses together with global IPv6 addresses (GUA) as a fallback mechanism, there might be hidden gotchas that you won't discover until you turn off IPv4. Looks like someone did a Truly Great Job, and ULA stands for Useless Local Addresses.
<!--more-->
[^NOULA]: Which you [REALLY SHOULD NOT](https://datatracker.ietf.org/doc/html/rfc6919#section-3).

For more details:

* Listen to [The Foibles and Frailties of IPv6 ULA](https://www.modem.show/post/s02e03/) episode of the Modem Podcast
* Read the [IETF draft](https://datatracker.ietf.org/doc/html/draft-buraglio-v6ops-ula-05)
* Enjoy the [recent discussion on v6ops mailing list](https://mailarchive.ietf.org/arch/msg/v6ops/7-SuigPyP0R-C6ZChm4-EOERBIQ/). I ran out of popcorn and patience and dropped out.

Do you care? Maybe. 

Someone asked a question along the lines "_does anyone know of a good ULA use case_" at the end of the Modem Podcast episode I mentioned above, and there happens to be one that might be relevant to a few mid-sized enterprise networks: site-to-site VPN with local Internet exit. I wrote about it in 2013 and as far as I know nothing changed in the meantime (apart from ULA addresses becoming useless). Here are the links to the (somewhat) relevant blog posts:

* [To ULA or not to ULA, That’s the Question](/2013/09/to-ula-or-not-to-ula-thats-question/) (September 2013)
* [PA, PI or ULA IPv6 Address Space? It depends](/2014/01/pa-pi-or-ula-ipv6-address-space-it/) (January 2014)
* [IPv6 Legends and Myths: More Opinions than Data Points](/2012/04/ipv6-legends-and-myths-more-opinions/) (April 2012)
* [Why Can’t We All Use Provider-Independent IPv6 Addresses?](/2018/04/why-cant-we-all-use-provider/) (April 2018)

Finally, let me conclude with an [awesome quote from Randy Bush](https://mailarchive.ietf.org/arch/msg/v6ops/7AUm63uxoa6opso7DTqnwgIB9b0/) (made in October 2012):

> It is cheering to see that the IPv6 ivory tower still stands despite
years of attack by reality.
