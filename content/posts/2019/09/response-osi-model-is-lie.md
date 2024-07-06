---
date: 2019-09-10 09:23:00+02:00
tags:
- Internet
- CLNP
title: 'Response: The OSI Model Is a Lie'
url: /2019/09/response-osi-model-is-lie.html
---
Every now and then I stumble upon a blog post saying "*OSI 7-layer model sucks*" or "*OSI 7-layer model is a lie*", [most recent one coming from Robert Graham](https://blog.erratasec.com/2019/08/thread-on-osi-model-is-lie.html).

Before going into the details, let's agree on the fundamentals.

Most everyone who ever tried to build a network spanning more than one transmission technology and including intermediate nodes came to the conclusion that **[layered approach to networking](https://my.ipspace.net/bin/get/Net101/L2.1%20-%20The%20Need%20for%20Network%20Layers.mp4?doccode=Net101) makes sense**.

Whether you have three, four, five, or seven layers in your model doesn't matter. What really matters is that **your model contains [all the functionality](https://my.ipspace.net/bin/get/Net101/L1.3%20-%20Beyond%20Two%20Nodes.mp4?doccode=Net101) you need to implement host-to-host networking in target environment**.
<!--more-->
While the conceptual split of functionality in the OSI 7-layer model makes perfect sense to me, there were few implementations of transport layer or above at the time when it mattered (when it was still unclear whether IP or CLNP would prevail).

Lower layers were well specified and worked well enough that they were considered as a [replacement for IP](/2010/09/ipv6-experts-strike-again.html) when everyone realized IPv4 was running out of address space. Unfortunately, a clash between IAB and rest of IETF (that nobody wants to talk about) resulted in "*let's start from scratch and build our own stuff*". We're still dealing with the results of that decision (see also: [second system effect](https://en.wikipedia.org/wiki/Second-system_effect)).

Finally, reading the [The Elements of Networking Style](https://www.amazon.com/Elements-Networking-Style-Animadversions-Intercomputer/dp/0595088791) book will give you an idea of the battles between engineers building ARPANET and religious zealots promoting One True Religion (OSI model). I was lucky enough to be a bit too young to be involved in them, and remote enough to have a "*let's use the bits that make sense*" perspective, but unfortunately it looks like some people still have battle scars.

However, regardless of what your position might be, PLEASE do not spread the alternative facts. Here are the ones from Robert's post that triggered this rant:

> OSI model never worked and never came to pass

False. There were working implementations of the full stack, and at least the lower three layers were used extensively in DECnet Phase V, SDH management, TUBA trials...

> OSI wanted a "connection-oriented network layer", one that worked like the telephone system, where every switch in between the ends knows about the connection.

While that might have been the message passed around by the religious zealots of both persuasions (see above), OSI model had both connection-oriented and connectionless service at layer-2 (LAN or WAN) and layer-3 (CLNS versus CONS). CONS was based on X.25 and CLNS was similar enough to IP that you could run TCP on it (and there was code in Cisco IOS doing that).

> The big standards bodies wanted a slightly different way of how Ethernet should work, with an LLC layer on top of Ethernet. That never came to pass.

The "*what is the whole LLC mess*" topic deserves a blog post of its own, so I'll just mention a few facts:

-   The standard bodies wanted to have a common top-sublayer of LAN technologies (Ethernet, Token Ring, Token Bus, FDDI) so you could (in theory, with great pains) make them interoperate. LLC was supposed to be that layer;
-   Even today Ethernet supports three encapsulation formats: Ethernet-II (Ethertype), LLC, and SNAP (Ethertype in LLC). At least IBM used SNAP encapsulation on Ethernet (to interoperate with Token Ring) and Cisco IOS supported SNAP encapsulation for IP as early as mid-1990s.

Admittedly, with Ethernet being the only remaining LAN technology, LLC makes little sense... but like junk DNA some headers never go away. PPP frame is still mirroring the SDLC frame format with destination address (useless on P2P media) and control byte just in case you'd want to run connection-oriented PPP... which is described in [RFC 1663](https://tools.ietf.org/html/rfc1663) and was implemented in Cisco IOS (and came really handy in high-[BER](https://en.wikipedia.org/wiki/Bit_error_rate) environments).

> There's no Session or Presentation Layer in modern networks.

What about MP-TCP, HTTP, QUIC, or MIME? They provide some of the functionality that Session or Presentation layers were supposed to implement.

Unfortunately someone in the early ARPANET days decided they don't need them even though it was evident (as Mike Padlipsky explained in his book) that you need a common presentation format in something as simple as virtual terminals. We're still paying the price dealing with add-on kludges. At least they managed to reuse the MIME registry in HTTP.

How about ASN.1, XML and JSON? They are all standard ways of encoding data structures (see also [this wikipedia article](https://en.wikipedia.org/wiki/Presentation_layer)). So don't tell me there's no presentation layer in today's networks.

And finally a personal note to Robert (in case he ever comes across this rant): I love your writing, and I rely on it being technically correct, so please keep it that way.

### More Information

In case I got you interested, I would highly recommend the [The Elements of Networking Style](https://www.amazon.com/Elements-Networking-Style-Animadversions-Intercomputer/dp/0595088791) book for its historical perspective, the awesome [History of Networking](https://rule11.tech/history-of-networking/) series of podcasts, as well as my [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar.
