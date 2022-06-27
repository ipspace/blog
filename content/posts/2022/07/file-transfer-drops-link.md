---
title: "Twilight Zone: File Transfer Causes Link Drop"
date: 2022-07-13 07:48:00
tags: [ history, WAN ]
---
Long long time ago, we built a multi-protocol WAN network for a large organization. Everything worked great, until we got the weirdest bug report I've seen thus far:

> When trying to transfer a particular file with DECnet to the central location, the WAN link drops. That does not happen with any other file, or when transferring the same file with TCP/IP. The only way to recover is to power cycle the modem.

Try to figure out what was going on before reading any further ;)
<!--more-->
I got onsite, the customer started the file transfer, and (as claimed) the link dropped... but when the customer reached for the power-off button on the modem, I noticed something weird: the "_remote loopback_" LED was on.

We power cycled the modem, the link went up, routing protocols did their job, we restarted the file transfer... and the _remote loopback_ LED turned on. The link went down a few seconds after that.

### WTF?

Testing WAN links was a big deal in those days[^AMS], and one of the tests was the _loopback_ test: put a modem into a state where it would transmit every bit it received. You could do a _local loopback_ test (loop 3 in V.54 recommendation), where the modem would create a loop as close to the physical line as possible, allowing you to test the DTE-DCE connection[^DTE] and the local modem. In a  _remote loopback_ (loop 2 in V.54 recommendation), the modem would create a loop on the WAN link, so you'd be able to test all the components of a WAN link apart from the remote CPE.

A remote loopback could be triggered with a button on the modem front panel, but that obviously required an on-site person able to follow instructions. The remote loopback could also be triggered remotely: a modem would send a weird sequence of bits to the remote modem which would enter the remote loopback state until it would receive another weird sequence of bits.

CCITT[^ITU] [designed the _weird sequence of bits_](https://www.itu.int/rec/T-REC-V.54-198811-I/en) to be something that was almost impossible to occur in a real-life network. The V.54 recommendation includes a further protection for HDLC links[^HDLC]: 

> In order to provide protection against false recognition caused by user HDLC frames, the bit sequence consisting of seven consecutive binary 1s, which is at present in the preparatory pattern, must be included in the recognition criteria.

I don't know whether it was the _almost_ part, or the modem designers not following the V.54 recommendation to the letter[^BB] (or they got it wrong). In any case, that particular file contained the precise sequence of bits needed to throw a modem into remote loopback, and DECnet sliced application data into packets in a slightly different way than TCP/IP, so the loopback was triggered only when transferring files with DECnet.

Once we go that far, it was trivial to solve the problem: open the modem, and flip the _enable remote loopback_ [DIP switch](https://en.wikipedia.org/wiki/DIP_switch) to off.

### More to Explore

Why don't you check out _[How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work)_ webinar -- you can watch [numerous videos](https://my.ipspace.net/bin/list?id=Net101) in that webinar with [Free ipSpace.net Subscription](https://www.ipspace.net/Subscription/Free).

[^AMS]: When we ordered our first international leased line, one of the final steps in the provisioning process involved a 24-hour test of the circuit. We even got a test report proving they did their job.

[^DTE]: Data Terminal Equipment, oftentimes called a router by the uninitiated. It's usually connected to Data Circuit-terminating Equipment (DCE), colloquially called a modem.

[^HDLC]: Seven consecutive ones is a signal to abort the current frame, and is almost never used.

[^ITU]: The entity now known as ITU.

[^BB]: I don't remember the modem manufacturer, but it was one of those "creative" baseband modems that managed to push 1 Mbps over a telephone circuit that was supposed to be able to carry 28 kbps... obviously only when the stars were properly aligned. Considering that, I wouldn't be surprised if there were further mismatches between what the modem did and CCITT recommendations.
