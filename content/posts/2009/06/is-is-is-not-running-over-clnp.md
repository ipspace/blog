---
date: 2009-06-23 07:06:00.001000+02:00
tags:
- IS-IS
- CLNP
title: IS-IS Is Not Running over CLNP
url: /2009/06/is-is-is-not-running-over-clnp/
lastmod: 2020-12-26 09:06:00
---
Numerous sources on the Internet claim that IS-IS runs on top of OSI’s Connectionless Network Protocol (CLNP). This is not the case; although IS-IS and CLNP share the same layer-2 Service Access Point (SAP), OSI provides an additional field (Network Layer Protocol Identifier; NLPID) in the first byte of the layer-3 header. 

Contrary to the IP world where the identification of layer-3 protocol is based on Ethertype or [PPP protocol ID](https://www.iana.org/assignments/ppp-numbers/ppp-numbers.xml#ppp-numbers-2), the identification of a layer-3 OSI protocol is performed based on layer-2 Service Access Point (DSAP = 0xFE) and the first byte of the layer-3 header, which has the following values:
<!--more-->
0x81
:	CLNP (Connectionless Network Protocol)

0x82
:	ES-IS: End system (host) to Intermediate System (router) protocol - used by CLNP hosts to announce themselves to the routers

0x83
:	IS-IS: Intermediate System to Intermediate System protocol -- used by routers running IS-IS to advertise themselves, establish adjacency, and exchange routing information.

IS-IS is therefore a separate network-layer protocol and does not rely on CLNP for datagram transport while IP routing protocols encapsulate their packets into IP or UDP datagrams.

{{<note info>}}For more details regarding End-System Hellos and Intermediate System Hellos watch the [*Network Addressing*](https://my.ipspace.net/bin/list?id=Net101#ADDR) part of *[How Networks Really Work](http://ipspace.net/Net101)* webinar.{{</note>}}

The relationship between various OSI protocols and their comparison with the IP protocol stack, where the layer-3 protocol demultiplexing relies exclusively on the values in the layer-2 header, is shown in the following diagram:

{{<figure src="/2009/06/OSI-ISIS-IP-stacks.png">}}

**Notes**
* IS-IS uses [LLC Type 1 encapsulation](https://en.wikipedia.org/wiki/IEEE_802.2) while IP commonly uses Ethertype encapsulation
* You [could run IP over LLC/SNAP encapsulation](https://tools.ietf.org/html/rfc1042) if you desperately want to do it... like IBM did 30 years ago.
* You could also run TCP over CLNS (see [TUBA IETF working group](https://datatracker.ietf.org/wg/tuba/documents/) for more details). Telnet-over-CLNS has been supported in Cisco IOS for years but seems to be missing in recent releases.

{{<note>}}You might be confused by the mixture of CLNS and CLNP acronyms. From the OSI perspective, a protocol (CLNP) is providing a service (CLNS) to upper layers. When a router is configured with **clns routing** it forwards CLNP datagrams -- the IOS configuration syntax is potentially misleading.{{</note>}}
