---
date: 2015-04-02 08:57:00+02:00
tags:
- bridging
- IP routing
title: What Is Layer-2 and Why Do We Need It?
url: /2015/04/what-is-layer-2-and-why-do-we-need-it.html
---
I'm constantly [ranting against large layer-2 domains](http://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html); recently going as far as saying "[*we don't really need all that stuff.*](http://blog.ipspace.net/2015/02/lets-get-rid-of-thick-yellow-cable.html)" Unfortunately, the IP+Ethernet mentality is so deeply ingrained in every networking engineer's mind that we rarely ever stop to question its validity.

Let's fix that and start with the fundamental question: **What is Layer-2**?
<!--more-->
I don't know whether they still teach OSI model in baseline networking courses (they should), but if you're lucky enough to have heard about it, this is probably the picture you've seen:

{{<figure src="/2015/04/s550-OSI.png" caption="Bottom layers of the OSI stack">}}

**Layer-1** (physical layer) is easy to explain: it defines the connectors, voltages and encoding scheme needed to pass a bunch of zeroes and ones between adjacent devices.

Networking devices working at layer-1 convert zeroes and ones between different voltages or transmission media. A few examples: modems (the traditional ones, not the thing that connects your WiFi to cable network, that one is at least a bridge if not a router), media converters (fiber-to-copper converters are still reasonably popular), hubs (you have to be pretty old to have real-life experience with them) and Media Access Units (Token Ring anyone?).

**Layer-2** is where things get complex. It was initially defined as the layer that allows *adjacent network devices* to exchange frames. Every layer-2 technology has to define at least these components:

-   How do you group zeroes and ones provided by layer-1 into frames (proper layer-2 terminology for packets);
-   Start-of-frame indication (the receiver has to know a new frame is coming), sometimes also know as [frame synchronization](http://en.wikipedia.org/wiki/Frame_synchronization);
-   End-of-frame indication, which can be either a special bit sequence or frame length encoded somewhere else in the frame;
-   Error correction mechanism in case the physical layer cannot guarantee error-free transmission of zeroes and ones (they usually don't);

Have you noticed that I haven't mentioned *layer-2 addresses* (known as *MAC addresses* in Ethernet)? There's a simple reason for that: sometimes you don't need them. You only need layer-2 addresses when you have more than two devices attached to the same physical network, like we used to have in the old cable-based Ethernet networks:

{{<figure src="/2015/04/s550-00+-+Thick+Coax+Cable.png" caption="Emulating coax cable with Ethernet gear">}}

{{<note info>}}Use of point-to-point links is the [primary reason for lack of layer-2 addresses in Fibre Channel networks](http://blog.ipspace.net/2011/07/is-fibre-channel-switching-bridging-or.html) (regardless of the violent disagreement I get every time I mention this).{{</note>}}

The first time you truly need unique addresses is layer-3, which should provide end-to-end packet delivery across the network.

Now let's answer some interesting questions:

**Why do we have MAC addresses in Ethernet frames**? Because the original Ethernet used a coax cable with numerous devices attached to the same physical medium.

**Why do we still use MAC addresses in Ethernet frames**? Because IEEE always wanted to keep everything backward compatible with the original Ethernet. 100 Mbps Ethernet still supported hubs (think of them as cable extenders), and 10GE is the first Ethernet technology that doesn't have half-duplex support.

{{<note info>}}Only a single sender can transmit over a shared medium (cable, WiFi frequency) at the same time -- we call that half-duplex transmission. Both end nodes can transmit at the same time on a bidirectional point-to-point link with two unidirectional paths -- a full-duplex transmission.{{</note>}}

**Do we still need layer-2**? In many cases, the answer is **no**. Every device that uses software-based forwarding can act as a layer-3 forwarding device (properly known as *router* but called *layer-3 switch* by almost everyone). Hardware in many high-speed forwarding devices (particularly switches deployed in data centers) already supports layer-3 forwarding.

**Why are we still using layer-2**? Because every vendor (apart from Amazon and [initial heroic attempts by Hyper-V Network Virtualization team](http://blog.ipspace.net/2013/12/hyper-v-network-virtualization-packet.html)) thinks they need to support really bad practices that originated from the thick yellow coax cable environment, like [protocols without layer-3](http://blog.ipspace.net/2010/07/bridges-kludge-that-shouldnt-exist.html) (and thus no usable end-to-end addresses) or [solutions that misuse the properties of shared medium](http://blog.ipspace.net/2012/02/microsoft-network-load-balancing-behind.html) in ways nobody ever envisioned.

Finally, **why is everyone using frame format from 40 year old technology**? Because nobody wants to change the device drivers in every host deployed in a data center (or in the global Internet).

### Want to Know More?

Read these blog posts and watch the [How Networks Really Work](https://www.ipspace.net/How_Networks_Really_Work) webinar

-   [Bridging and routing -- is there a difference?](http://blog.ipspace.net/2010/07/bridging-and-routing-is-there.html)
-   [Bridging and routing -- part II](http://blog.ipspace.net/2010/07/bridging-and-routing-part-ii.html)
-   [Transparent bridging scalability issues](http://blog.ipspace.net/2012/05/transparent-bridging-aka-l2-switching.html)
-   [Layer-2 network is a single failure domain](http://blog.ipspace.net/2012/05/layer-2-network-is-single-failure.html)
-   [Why is TRILL not routing at layer-2?](http://blog.ipspace.net/2010/07/why-is-trill-not-routing-at-layer-2.html)
-   [Is layer-3 switch more than a router?](http://blog.ipspace.net/2012/08/is-layer-3-switch-more-than-router.html)
-   [Is Fibre Channel switching bridging or routing?](http://blog.ipspace.net/2011/07/is-fibre-channel-switching-bridging-or.html)
