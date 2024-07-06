---
title: "Is X.25 Still Alive?"
date: 2022-04-27 07:04:00
tags: [ WAN ]
---
Enrique Vallejo [asked an interesting question](/2022/04/do-you-care-about-mpls.html#1137) a while ago:

> When was X.25 official declared dead? Note that the wikipedia claims that it is still in use in parts of the world.

[Wikipedia is probably right](https://en.wikipedia.org/wiki/X.25), and had several encounters with X.25 that would corroborate that claim. If you happen to have more up-to-date information, please leave a comment.
<!--more-->
More than two decades ago (IIRC before MPLS/VPN was on the drawing board), I was doing some consulting for a service provider specialized in building global IP-based VPN networks for aviation industry[^BOOK]. They ran a well-designed IP-only network but mentioned that they still support X.25 over TCP (XOT). I thought X.25 was dead by that time, but it turned out a large percentage of check-in terminals still used it. 

[^BOOK]: A similar design is described in the *Dedicated-Router Approach to Peer-to-Peer Model* in Chapter 7 of the original *MPLS and VPN Architectures book*.

Aside: X.25 was an ideal connectivity solution for check-in terminals:

* You were billed by the usage and usually didn't have to pay a fixed recurring fee for expensive circuits going to airfields out in the boondocks.
* Bandwidth requirements were minimal. In those days people didn't have a problem with memorizing three-letter CLI commands[^AMADEUS].
* X.25 was so reliable that you could run it over a barbed wire with severe error rate or packet loss that would make TCP stall in a second.

[^AMADEUS]: Looking for some fun reading full of cryptic 3-7 letter commands? [Check out The Complete Amadeus Manual](https://air.flyingway.com/books/amadeus/Amadeus_Guide.pdf).

Fast forward at least 15 years. During an intro chat in one of my Expert Express engagements the networking engineer I was working with mentioned that they still supported X.25 (again, using XOT). My immediate reaction was "_do you work for an airline?_" to which he replied "_no, at an airport, but how did you know?_" They were still using check-in terminals with X.25 uplinks, and I'm positive some of those terminals are still in use today.

Finally, a bizarre fact: France Telecom shut down [Minitel](https://en.wikipedia.org/wiki/Minitel) in 2012, at which time the service still had 800.000 terminals, and some POS credit card terminals used underlying X.25 network which was also discontinued (see [comment by Pierre](#1186)).

Let me just mention that [Tim Berners-Lee had a working WWW implementation in late 1990](https://en.wikipedia.org/wiki/History_of_the_World_Wide_Web#1989%E2%80%931993:_Origins_and_development) -- it took Minitel service over 20 years to be taken over by The Internet.

### Speaking of Barbed Wire

Parts of the X.25 protocol stack are used in environment with error rate resembling what you would expect from a barbed wire connection (VHF/UHF radio links):

* [AX25](https://en.wikipedia.org/wiki/AX.25) is used by amateur radio operators to run [packet radio](https://en.wikipedia.org/wiki/Packet_radio) networks (HT: [ICT4F Marcus](https://twitter.com/Ict4F/status/1519227508096393216)).
* X.25 is part of the [VHF Data Link](https://en.wikipedia.org/wiki/VHF_Data_Link) (aircraft-to-ground data links) protocol stack (see [comment by Bela Varkony](#1185)).

### Revision History

2022-04-28
: Added further X.25 use cases based on readers' comments
