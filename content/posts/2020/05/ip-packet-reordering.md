---
title: "Musings on IP Packet Reordering"
date: 2020-05-19 06:36:00
tags: [ IP routing, bridging ]
---
During the [Comparing Transparent Bridging and IP Routing](https://my.ipspace.net/bin/list?id=Net101#SWITCH) part of [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar I said something along the lines of:

> While packets should never be reordered in transit in transparent bridging, there's no such guarantee in IP networks, and IP applications should tolerate out-of-order packets.

One of my regular readers who designs and builds networks supporting VoIP applications disagreed with that citing numerous real-life examples.

Of course he was right, but let's get the facts straight first:
<!--more-->
* Transparent bridging emulates the original Ethernet cable, and some applications designed to run in that environment expected strict ordering of packets. Some of them (example: IBM SNA) would even reset the session when receiving an out-of-order packet, so we had to take great precautions when implementing various source-route-bridging-over-IP stupidities (RSRB, FST, DLSW, DLSW+...) to preserve the packet ordering.
* IP routing never made such guarantees. It was always understood that packets could arrive out-of-order and that the transport protocol (TCP) or the applications would have to deal with that. Stateless applications (DNS) have no problem whatsoever, and streaming applications could either buffer the packets or ignore out-of-order packets resulting in lower voice- or video quality.

Nobody ever claimed packet reordering is NOT harmful, although (IIRC) people who know better told me it's no longer a big problem with decent TCP stack, and I encountered a not-insignificant amount of reordered packets when I had to troubleshoot traffic traversing the Internet. 

{{<note info>}}What's your experience? How often do you see reordered packets? Write a comment!{{</note>}}

However, reality and laws of physics (and networking) have never stopped application developers from assuming that [real life behaves in exactly the same way as their loopback interface](https://my.ipspace.net/bin/list?id=Net101#FALLACIES), and I blame their managers for not exposing them to that fact during testing- and acceptance procedures. After all, you could easily simulate a real-life network behavior with **tc** or use a CLI wrapper around **tc** like [Comcast](https://github.com/tylertreat/Comcast) if you can't be bothered to figure out its arcane options.

I also know that a lot of networking engineers get [pushed into designing or implementing networks that support such delusions](/2013/04/this-is-what-makes-networking-so-complex/), but if that's the case, please don't claim that IP has to work the way you made it work, it's just that you are unfortunate enough to have to support something with broken expectations that deviate from how IP was always supposed to work.

On the other hand, it might turn out that there's a good use case behind the weird requirements, and that you need something different from vanilla IP routing. No problem, fork IP, and go your own way. For example, there's TCP-over-lossless-transport (apparently [not such a good idea](https://blogs.cisco.com/datacenter/the-napkin-dialogues-lossless-iscsi)), then there's [Deterministic Networking](https://datatracker.ietf.org/wg/detnet/about/) (DETNET), and I'm sure there are other similar examples... but should we still call them IP routing? I don't know.