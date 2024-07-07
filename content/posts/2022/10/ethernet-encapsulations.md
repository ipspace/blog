---
title: "History of Ethernet Encapsulations"
date: 2022-10-26 07:43:00
tags: [ LAN ]
---
Henk Smit [conscientiously pointed out a major omission](/2022/09/from-bits-to-applications/#1356) I made when summarizing [Peter Paluch's excellent description](/2022/09/from-bits-to-applications/) of how bits get parsed in network headers:

> EtherType? What do you mean EtherType? There are/were 4 types of Ethernet encapsulation. Only one of them (ARPA encapsulation) has an EtherType. The other 3 encapsulations do not have an EtherType field.

What is he talking about? Time for another history lesson[^BYA].
<!--more-->
Ethernet started as a bit of a science project[^SP] at the center of "just good enough" mentality sometimes known as _Silicon Valley_. To keep things simple, it used:

[^BYA]: Before someone asks: I started working with Ethernet in late 1980s, so I was a bit late to the party, but nevertheless had the "privilege" of working with thick yellow cable and vampire taps and lived through the nightmares of thin coax cables being charred by under-the-desk heaters.

[^SP]: [According to Wikipedia](https://en.wikipedia.org/wiki/Ethernet), Robert Metcalfe _named it after the luminiferous aether once postulated to exist as an "omnipresent, completely-passive medium for the propagation of electromagnetic waves."_

* A preamble (to synchronize sender's and receivers' clocks)
* A start frame delimiter (to tell everyone to really start listening)
* Source and destination MAC addresses
* 2-byte field identifying higher-layer[^HL] protocol
* Payload
* Frame Check Sequence

The 2-byte field I mentioned above is called EtherType. ARPA encapsulation is a Cisco-speak for original Ethernet encapsulation, which could also be called DIX[^DIX] Ethernet, or (probably most correctly) Ethernet II framing because the latest version of DIX Ethernet specification was Version 2, published in November 1982. After that, [IEEE finally got their act together](https://en.wikipedia.org/wiki/Ethernet#History) -- it took them almost four years to "standardize" a shipping technology.

Anyway, you might have noticed there's something missing in the above list of Ethernet frame parts -- there's no end-of-frame delimiter. How do we know we got a valid frame? Remember the "just good enough" approach? Here's how it works:

* Original shared-medium Ethernet ([10BASE5](https://en.wikipedia.org/wiki/10BASE5) and [10BASE2](https://en.wikipedia.org/wiki/10BASE2)) uses [Manchester coding](https://en.wikipedia.org/wiki/Manchester_code) with a transition at the middle of each bit. If there's no transition, the sender obviously stopped sending.
* As the receiver is collecting bits into an incoming frame, it's continuously calculating the [Frame Check Sequence](https://en.wikipedia.org/wiki/Ethernet_frame#Frame_check_sequence).
* If the receiver perceives the sender stopping at a byte boundary, and the calculated FCS matches the "verify value", the receiver believes it got a valid frame.

That was obviously not good enough for IEEE purists[^TR], but it's hard to argue with shipping products when a [competing standards body starts to standardize](https://en.wikipedia.org/wiki/Ethernet#Standardization) what you've been pondering for years, so they reached a "compromise"[^ATM]:

* Ethernet will retain it's good-enough physical layer
* IEEE version of the Ethernet will have a belt-and-braces *length* field after the MAC addresses to verify that the frame truly has the right length.
* EtherTypes will use values above 1500, so it will be evident whether we're dealing with IEEE encapsulation or Ethernet II encapsulation[^JF].

[^HL]: A 7-layer purist would say _oh, you mean a layer-3 protocol_. Unfortunately we've seen applications riding directly on top of Ethernet, many of them coming from Digital (DEC), the infamous inventor of transparent bridge -- the [kludge needed to support them](/2010/07/bridges-kludge-that-shouldnt-exist/).

[^DIX]: DIX = Digital, Intel, Xerox -- the initials of the three major companies pushing early Ethernet in alphabetical order. Even though Ethernet was invented within [Xerox PARC](https://en.wikipedia.org/wiki/PARC_(company)), they still got the last place in the acronym.

[^TR]: A hint: [Token Ring frames](https://en.wikipedia.org/wiki/Token_Ring#Data) have *ending delimiter*, as do [FDDI frames](https://en.wikipedia.org/wiki/Fiber_Distributed_Data_Interface#Frame_format).

[^ATM]: See also: a [diplomatic explanation](https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode#Protocol_architecture) of what made ATM cells 53 bytes long

[^JF]: Don't even think about asking what happens when jumbo frames use IEEE encapsulation.

To be fair, there's a better reason for the *length* field. Ethernet frames have a minimum length of 64 bytes[^RUNT]. Not a big deal -- add padding to your protocol. Well, IBM didn't like that argument; they wanted to [keep sending SDLC/HDLC frames over LAN networks](https://en.wikipedia.org/wiki/IEEE_802.2#Control_Field)[^SDLC].

[^RUNT]: We need a minimum frame length to make sure the sender detects a collision (and starts sending gobbledygook that will bork the FCS value) before it finishes sending the frame. The frame length is thus a function of transmission speed and collision domain size, which depended on cable lengths and the number of repeaters in an Ethernet segment.

[^SDLC]: What could be better than taking a protocol that was designed for 1200-baud noisy modem connections and put it onto a 4 Mbps pretty reliable Token Ring LAN? Chalk it up to _doing more with less_ mentality aka _it costs too much to redesign our broken stuff_.

Anyway, at that point we still had a simple decision to make:

* Is the 16-bit value after MAC addresses higher than 1536[^600]? Must be an EtherType.
* Otherwise, it's an IEEE 802.2 packet.

[^600]: Where did they get such a weird number? 1536 = 0x600, a value reserved for an old Xerox protocol

OK, but what's riding on top of an IEEE 802.2 packet? IEEE's first idea was to take the OSI stack and [put it on top of LAN networks](https://en.wikipedia.org/wiki/IEEE_802.2#LSAP_values) -- every packet would have a Source Service Access Point (SSAP) and Destination Service Access Point (DSAP). Why would you need two? Would IP stack ever send a packet to OSI stack? Of course not, but that's what you get with an academic layered approach.

There was just a bit of a hurdle: tons of companies were interested in Ethernet connectivity in those days, and all of them had proprietary protocols (just look at the reservation ranges for [IANA IEEE 802 numbers](https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml)), but there were only 128 available SAP numbers[^SAP8]. In a wonderful application of RFC 1925 Rule 6a, IEEE reserved SAP value 0xAA to mean *SNAP Extension* which really means _we just wasted 6 bytes to tell you to look at the EtherType that follows._[^W6]

[^SAP8]: That's what you get when you're approaching a megabit transport technology with a 1200-baud design mindset and try to squeeze everything into one byte where you could easily have two. Oh, and of course every header field must have at least one reserved bit ;)

[^W6]: In case you haven't noticed: they wasted six bytes (plus the length field) because they tried to save two. Good job.

So far we have three different Ethernet encapsulation. Hank mentioned four. Welcome to Novell IPX Raw Encapsulation SNAFU. They believed in the magic powers of IEEE (or needed a length field) but couldn't be bothered waiting for IEEE to agree on LLC2 frame format -- IPX payload directly follows the *length* field without any indication of what higher-layer protocol is riding in the Ethernet packet[^NE].

[^NE]: Who would want to run anything else but Novell Netware on a LAN anyway?

Fortunately (for everyone else who had to parse their stupidity) IPX packet header format included a checksum as the first two bytes of the packet, and Novell never implemented a proper checksum for IPX, so every IPX packet always started with 0xFFFF[^IOTW], which would be understood as _global broadcast_ by anyone complying with 802.2 standards, but who's counting.

[^IOTW]: Which is how everyone else identified the idiots on the wire

Does all of this matter? Not really unless you're an Ethernet history addict, but it resulted in a nice consulting project for my company in 1990s[^RSC].

[^RSC]: I also had to run through this explanation way too many times while delivering Router Software Configuration (and later ICND) course.

Local experts in IBM connectivity couldn't make an IBM AIX server talk to a Cisco router. They were also too thrifty to invest in a [protocol analyzer](https://en.wikipedia.org/wiki/Sniffer_(protocol_analyzer)) (that thing could cost around $10K in those days) and wanted to borrow ours. In the end we agreed we'd charge them a day of consulting services, come over with the Sniffer and figure out what's going on. It took me a few moments to realize AIX used SNAP encapsulation, and a few minutes to figure out how to configure that on Cisco routers[^IOSH]. Problem solved.

Just in case you'll ever have to work with a 30-year-old IBM Unix server: the command to use is **arp snap**. Cisco IOS constructs layer-2 headers for individual IP next-hops from ARP entries, and the encapsulation used toward a next hop depends on the what encapsulation that next hop used in ARP request/reply. You cannot specify what encapsulation you want to use for IP, but you can specify which encapsulation(s) ARP requests will use. For some other gory details, see [RFC 1042](https://datatracker.ietf.org/doc/html/rfc1042).

[^IOSH]: Cisco software had no ?-triggered help until Terry Slattery got a contract to rewrite its CLI parsers, so I had to go through the documentation.